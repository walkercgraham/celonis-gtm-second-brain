#!/usr/bin/env python3
"""Run guard for the vault agents. Standard library only.

    guard.py start  <agent>                      lock + snapshot of already-dirty files
    guard.py diff   <agent>                      show what this run changed (for the critic)
    guard.py finish <agent> [--revert] [-m MSG]  path-guard, commit agent paths, push, unlock
                                                 (agents with require_verdict: true need a PASS verdict written this
                                                 run, else finish acts as --revert and exits 5)
    guard.py pause                                hold the lock for an interactive session (no snapshot/judge/commit)
    guard.py resume                                release a lock held by `pause`
    guard.py status                               show lock + current run state
    guard.py release                              force-release a stuck lock
    guard.py post   <agent>                      send the critic-approved outbox post to the agent's Slack workflow

Design rules (see AGENTS.md):
- The user edits in Obsidian all day, so a dirty tree is normal. Only paths that changed *during
  the run* are judged or committed; pre-existing dirty files are never committed or reverted
  unless the agent also changed them.
- Never delete. Violating or reverted content is copied to _agents/<agent>/quarantine/ first.
- Never commit/push on main unless config `allow_main: true`.
- Interactive edits (Claude Code sessions writing to the vault live, e.g. /meeting) race scheduled
  agents the same way: a run's start→finish window has no way to tell "the agent drifted out of its
  lane" from "the user/Claude Code wrote something else at the same time" — both look like a path that
  changed during the run, and get reverted/quarantined. `pause`/`resume` hold the same lock scheduled
  runs already wait on in `cmd_start`, so they cleanly wait (up to `guard.lock_wait_minutes`) or back
  off instead of racing. Hold it for the duration of a batch of interactive vault writes.
- Channel posts go through one Slack Workflow Builder webhook per agent, so they post as the workflow (not
  as the user) and the `notify_user` mention actually notifies them. The agent drafts named fields in
  `_agents/.outbox/<agent>.json`; the critic may edit them; `finish` marks the file ready only on a live
  run whose newest verdict is PASS; `post` sends it. Webhook URLs live in `_agents/.secrets/` (git-ignored).
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request

VAULT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AGENTS_DIR = os.path.join(VAULT, "_agents")
LOCK = os.path.join(AGENTS_DIR, ".lock")
OUTBOX = os.path.join(AGENTS_DIR, ".outbox")
SECRETS = os.path.join(AGENTS_DIR, ".secrets")
STALE_LOCK_SECONDS = 2 * 60 * 60

# Never judged, committed or reverted by the guard.
IGNORED = [".obsidian/**", "_agents/.lock", "_agents/.guard.log", "_agents/*/.run/**", ".DS_Store", "**/.DS_Store",
           ".trash/**", "_agents/.outbox/**", "_agents/.secrets/**"]

# One Slack workflow per agent. Each template mirrors that workflow's message step exactly; its {fields} are the
# webhook variables (all Text, plus notify_user = Slack user ID, which the guard fills from config). The template
# is also the fallback text when the webhook fails and the agent posts directly via MCP.
SLACK_TEMPLATES = {
    "chief-of-staff": "{notify_user} *{run}* — {headline}\n{details}\n*Focus:* {focus}\n*👉 Your move:* {action}",
    "field-brief": "{notify_user} *Field Brief* — {headline}\n*1.* {pick_1}\n*2.* {pick_2}\n*3.* {pick_3}\n"
                   "*👉 Your move:* {action}",
    "ingestor": "{notify_user} *Ingestor* — {headline}\n{accounts}\n*Issues:* {issues}\n*👉 Your move:* {action}",
    "loop-keeper": "{notify_user} *Loop Keeper* — {headline}\n{changes}\n*Needs attention:* {attention}\n"
                   "*👉 Your move:* {action}",
    "account-sentinel": "{notify_user} *Account Sentinel* — {rag}\n🔴 {red}\n🟠 {amber}\n🟢 {green}\n"
                        "*Report:* {report}\n*👉 Your move:* {action}",
    "opportunity-scout": "{notify_user} *Opportunity Scout* — {headline}\n{ideas}\n*👉 Your move:* {action}",
    "account-watch": "{notify_user} *Account Watch* — {headline}\n{signals}\n*👉 Your move:* {action}",
}
POST_MAX_LINES = 20         # whole rendered post
FIELD_MAX_CHARS = 1500
MENTION_RE = re.compile(r"<[@!#]|@channel|@here|@everyone", re.I)


# ---------- helpers ----------

def now():
    return dt.datetime.now().astimezone()


def git(*args, check=True):
    r = subprocess.run(["git", *args], cwd=VAULT, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {r.stderr.strip()}")
    return r


def load_config():
    """Minimal parser for _agents/config.yaml (two-level `key: value` only)."""
    cfg, section, sub = {}, None, None
    path = os.path.join(AGENTS_DIR, "config.yaml")
    if not os.path.exists(path):
        return cfg
    for raw in open(path, encoding="utf-8"):
        line = raw.split(" #", 1)[0].rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        key, _, val = line.strip().partition(":")
        val = val.strip().strip('"')
        if indent == 0:
            section, sub = key, None
            cfg[key] = val if val else {}
        elif indent == 2 and isinstance(cfg.get(section), dict):
            sub = key
            cfg[section][key] = val if val else {}
        elif indent == 4 and sub and isinstance(cfg[section].get(sub), dict):
            cfg[section][sub][key] = val
    return cfg


def agent_cfg(cfg, agent):
    a = cfg.get("agents", {}).get(agent, {})
    return a if isinstance(a, dict) else {}


def agent_mode(cfg, agent):
    a = cfg.get("agents", {}).get(agent, {})
    return (a.get("mode") if isinstance(a, dict) else None) or cfg.get("mode") or "shadow"


def glob_to_regex(pat):
    out, i = "", 0
    while i < len(pat):
        if pat.startswith("**/", i):
            out += "(?:.*/)?"
            i += 3
        elif pat.startswith("**", i):
            out += ".*"
            i += 2
        elif pat[i] == "*":
            out += "[^/]*"
            i += 1
        elif pat[i] == "?":
            out += "[^/]"
            i += 1
        else:
            out += re.escape(pat[i])
            i += 1
    return re.compile("^" + out + "$")


HUB_RE = re.compile(r"^02-areas/celonis/([^/]+)/\1\.md$")


def matches(path, patterns):
    for p in patterns:
        if p == "HUB":
            if HUB_RE.match(path):
                return True
        elif glob_to_regex(p).match(path):
            return True
    return False


def allowed_patterns(agent, mode):
    """Always: own folder + critic verdicts. Live: + allowed-paths.txt. Shadow: + `shadow:` lines."""
    pats = [f"_agents/{agent}/**", "_agents/critic/verdicts/**", "_agents/critic/log.md"]
    f = os.path.join(AGENTS_DIR, agent, "allowed-paths.txt")
    if os.path.exists(f):
        for raw in open(f, encoding="utf-8"):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("shadow:"):
                pats.append(line[len("shadow:"):].strip())
            elif mode == "live":
                pats.append(line)
    return pats


def file_hash(path):
    full = os.path.join(VAULT, path)
    if not os.path.exists(full):
        return "DELETED"
    if os.path.isdir(full):
        return "DIR"
    h = hashlib.sha256()
    with open(full, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def dirty_paths():
    """{path: 'tracked'|'untracked'} for everything differing from HEAD (incl. untracked files)."""
    r = git("status", "--porcelain=v1", "-z", "--untracked-files=all")
    parts = r.stdout.split("\0")
    out, i = {}, 0
    while i < len(parts):
        entry = parts[i]
        i += 1
        if not entry:
            continue
        code, path = entry[:2], entry[3:]
        if code[0] in "RC":  # rename/copy: next field is the old path
            old = parts[i]
            i += 1
            out[old] = "tracked"
        out[path] = "untracked" if code == "??" else "tracked"
    return {p: k for p, k in out.items() if not matches(p, IGNORED)}


def run_dir(agent):
    return os.path.join(AGENTS_DIR, agent, ".run")


def snapshot_file(agent):
    return os.path.join(run_dir(agent), "snapshot.json")


def log_line(agent, msg):
    with open(os.path.join(AGENTS_DIR, ".guard.log"), "a", encoding="utf-8") as fh:
        fh.write(f"{now():%Y-%m-%d %H:%M:%S} {agent}: {msg}\n")


# ---------- lock ----------

def acquire_lock(agent, wait_minutes):
    deadline = time.time() + wait_minutes * 60
    while True:
        try:
            fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, json.dumps({"agent": agent, "pid": os.getpid(),
                                     "started": now().isoformat()}).encode())
            os.close(fd)
            return True
        except FileExistsError:
            age = time.time() - os.path.getmtime(LOCK)
            if age > STALE_LOCK_SECONDS:
                print(f"guard: taking over stale lock ({int(age/60)} min old): {open(LOCK).read()}")
                os.remove(LOCK)
                continue
            if time.time() > deadline:
                return False
            time.sleep(15)


def release_lock():
    if os.path.exists(LOCK):
        os.remove(LOCK)


# ---------- changes ----------

def run_changes(agent):
    """Paths changed during this run: new dirty paths, or pre-dirty paths whose content changed."""
    snap = json.load(open(snapshot_file(agent)))
    before = snap["dirty"]
    current = dirty_paths()
    changed = {}
    for p, kind in current.items():
        if p not in before or before[p]["hash"] != file_hash(p):
            changed[p] = kind
    for p in before:  # was dirty before, now matches HEAD → the run reverted it
        if p not in current:
            changed[p] = before[p]["kind"]
    return snap, changed


def quarantine(agent, path, stamp):
    src = os.path.join(VAULT, path)
    if not os.path.isfile(src):
        return None
    dst = os.path.join(AGENTS_DIR, agent, "quarantine", stamp, path)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
    return os.path.relpath(dst, VAULT)


def restore(agent, path, snap, kind):
    """Return path to its pre-run state. Content is quarantined by the caller first."""
    before = snap["dirty"].get(path)
    full = os.path.join(VAULT, path)
    if before:  # was already dirty before the run → restore from backup
        backup = os.path.join(run_dir(agent), "backup", path)
        if before["hash"] == "DELETED":
            if os.path.exists(full):
                os.remove(full)  # content already quarantined; pre-run state was "absent"
        elif os.path.exists(backup):
            os.makedirs(os.path.dirname(full), exist_ok=True)
            shutil.copy2(backup, full)
    elif kind == "untracked":
        if os.path.exists(full):
            os.remove(full)  # new file created by the run; copy kept in quarantine
    else:
        git("checkout", "HEAD", "--", path)


# ---------- commands ----------

def cmd_start(agent, cfg):
    wait = int(cfg.get("guard", {}).get("lock_wait_minutes", 10) or 10)
    if not acquire_lock(agent, wait):
        print(f"guard: lock held by {open(LOCK).read()} — gave up after {wait} min")
        log_line(agent, "start: lock timeout")
        return 2
    try:
        if os.path.isdir(run_dir(agent)):
            shutil.rmtree(run_dir(agent))
        os.makedirs(os.path.join(run_dir(agent), "backup"))
        for f in (outbox_path(agent), outbox_path(agent, ready=True)):  # a crashed run's post never carries over
            if os.path.exists(f):
                os.remove(f)
        os.makedirs(OUTBOX, exist_ok=True)
        dirty = {}
        for p, kind in dirty_paths().items():
            h = file_hash(p)
            dirty[p] = {"kind": kind, "hash": h}
            if h not in ("DELETED", "DIR"):
                dst = os.path.join(run_dir(agent), "backup", p)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(os.path.join(VAULT, p), dst)
        branch = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
        snap = {"agent": agent, "mode": agent_mode(cfg, agent), "branch": branch,
                "head": git("rev-parse", "HEAD").stdout.strip(),
                "started": now().isoformat(), "dirty": dirty}
        json.dump(snap, open(snapshot_file(agent), "w"), indent=1)
    except Exception:
        release_lock()
        raise
    log_line(agent, f"start mode={snap['mode']} branch={branch} pre_dirty={len(dirty)}")
    print(f"guard: started {agent} | mode={snap['mode']} | branch={branch} | "
          f"pre-existing dirty files={len(dirty)}")
    if branch == "main" and cfg.get("allow_main") != "true":
        print("guard: WARNING on main with allow_main=false — changes will be left uncommitted")
    return 0


def cmd_diff(agent, cfg):
    snap, changed = run_changes(agent)
    mode = snap["mode"]
    pats = allowed_patterns(agent, mode)
    print(f"# Run diff: {agent} (mode={mode}, branch={snap['branch']})\n")
    for p in sorted(changed):
        flag = "ok" if matches(p, pats) else "VIOLATION"
        print(f"- [{flag}] {p} ({changed[p]})")
    print()
    for p in sorted(changed):
        if p.endswith("/.run") or "/.run/" in p:
            continue
        print(f"\n===== {p} =====")
        if changed[p] == "untracked":
            full = os.path.join(VAULT, p)
            try:
                lines = open(full, encoding="utf-8").read().splitlines()
            except (UnicodeDecodeError, FileNotFoundError, IsADirectoryError):
                print("(binary or missing)")
                continue
            print("\n".join(lines[:300]))
            if len(lines) > 300:
                print(f"... ({len(lines) - 300} more lines)")
        else:
            out = git("diff", "HEAD", "--", p, check=False).stdout.splitlines()
            print("\n".join(out[:400]))
            if len(out) > 400:
                print(f"... ({len(out) - 400} more diff lines)")
    return 0


def cmd_finish(agent, cfg, revert, message):
    if not os.path.exists(snapshot_file(agent)):
        print("guard: no snapshot — was `start` run?")
        return 2
    rc = 0
    try:
        snap, changed = run_changes(agent)
        mode = snap["mode"]
        pats = allowed_patterns(agent, mode)
        stamp = now().strftime("%Y-%m-%d-%H%M")
        keep_on_revert = [f"_agents/{agent}/log.md", "_agents/critic/verdicts/**", "_agents/critic/log.md",
                          f"_agents/{agent}/shadow/**"]

        violations = [p for p in changed if not matches(p, pats)]
        to_restore = set(violations)
        unverified = None
        if not revert and agent_cfg(cfg, agent).get("require_verdict") == "true":
            started = dt.datetime.fromisoformat(snap["started"]).timestamp()
            verdict = newest_verdict(agent, started)
            if verdict != "VERDICT: PASS":
                unverified = verdict or "no verdict file this run"
                revert = True
                rc = 5
                print(f"guard: require_verdict — {unverified}; treating as --revert (log, shadow and verdict kept)")
        if revert:
            to_restore |= {p for p in changed if not matches(p, keep_on_revert)}

        vlog = []
        for p in sorted(to_restore):
            q = quarantine(agent, p, stamp)
            restore(agent, p, snap, changed[p])
            reason = "violation" if p in violations else "critic-revert"
            vlog.append(f"{stamp} {reason} {p} -> {q or '(no content: deletion restored)'}")
        if vlog:
            qdir = os.path.join(AGENTS_DIR, agent, "quarantine")
            os.makedirs(qdir, exist_ok=True)
            with open(os.path.join(qdir, "violations.log"), "a", encoding="utf-8") as fh:
                fh.write("\n".join(vlog) + "\n")
            print("guard: restored/quarantined:\n  " + "\n  ".join(vlog))
            if violations:
                rc = 1

        # Re-scan after restores; commit only this run's surviving, allowed paths.
        _, changed = run_changes(agent)
        commit_paths = sorted(p for p in changed if matches(p, pats))
        qlog = f"_agents/{agent}/quarantine/violations.log"
        if vlog and os.path.exists(os.path.join(VAULT, qlog)):
            commit_paths.append(qlog)
        commit_paths = sorted(set(commit_paths))

        branch = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
        if not commit_paths:
            print("guard: nothing to commit")
        elif branch == "main" and cfg.get("allow_main") != "true":
            print(f"guard: on main with allow_main=false — left {len(commit_paths)} path(s) "
                  "uncommitted")
            rc = rc or 3
        else:
            msg = message or (f"blocked: {unverified}" if unverified else "vetoed by critic" if revert else "run")
            # Stage only our paths (including new files/deletions) and commit only them.
            git("add", "-A", "--", *commit_paths)
            git("commit", "-q", "-m",
                f"agent({agent}): {now():%Y-%m-%d} {mode} — {msg}\n\n"
                f"Automated by scripts/agents/guard.py",
                "--", *commit_paths)
            print(f"guard: committed {len(commit_paths)} path(s) on {branch}")
            push(branch, int(cfg.get("guard", {}).get("push_retries", 4) or 4))
        outbox = settle_outbox(agent, snap, ok=(rc == 0 and not revert and mode == "live"))
        log_line(agent, f"finish rc={rc} revert={revert} committed={len(commit_paths)} "
                        f"restored={len(vlog)} outbox={outbox}")
    finally:
        if os.path.isdir(run_dir(agent)):
            shutil.rmtree(run_dir(agent))
        release_lock()
    return rc


def push(branch, retries):
    if not git("remote", check=False).stdout.strip():
        print("guard: no remote configured — commit kept local")
        return
    delay = 2
    for attempt in range(1, retries + 1):
        r = git("push", "origin", branch, check=False)
        if r.returncode == 0:
            print(f"guard: pushed {branch}")
            return
        if "rejected" in r.stderr or "fetch first" in r.stderr:
            git("pull", "--rebase", "--autostash", "origin", branch, check=False)
        time.sleep(delay)
        delay *= 2
    print(f"guard: push failed after {retries} attempts — commit kept local:\n{r.stderr.strip()}")


# ---------- channel post ----------

def outbox_path(agent, ready=False):
    return os.path.join(OUTBOX, f"{agent}.ready.json" if ready else f"{agent}.json")


def newest_verdict(agent, since):
    """First line of the newest critic verdict for `agent` written at or after `since` (epoch), else None."""
    vdir = os.path.join(AGENTS_DIR, "critic", "verdicts")
    if not os.path.isdir(vdir):
        return None
    rx = re.compile(rf"^\d{{4}}-\d{{2}}-\d{{2}}-{re.escape(agent)}(-\d{{4}})?\.md$")
    found = [os.path.join(vdir, f) for f in os.listdir(vdir) if rx.match(f)]
    found = [f for f in found if os.path.getmtime(f) >= since - 1]
    if not found:
        return None
    with open(max(found, key=os.path.getmtime), encoding="utf-8") as fh:
        return fh.readline().strip()


def settle_outbox(agent, snap, ok):
    """At finish: promote the draft to ready only for a clean live run with a PASS verdict; otherwise discard."""
    draft, ready = outbox_path(agent), outbox_path(agent, ready=True)
    if os.path.exists(ready):
        os.remove(ready)  # never send a previous run's post
    if not os.path.exists(draft):
        return "none"
    started = dt.datetime.fromisoformat(snap["started"]).timestamp()
    verdict = newest_verdict(agent, started)
    if ok and verdict == "VERDICT: PASS":
        os.replace(draft, ready)
        return "ready"
    os.remove(draft)
    return f"discarded ({verdict or 'no verdict this run'})"


def render_post(agent, fields, cfg):
    """Validate the drafted fields and return (payload for the workflow, fallback text). Raises ValueError."""
    tpl = SLACK_TEMPLATES.get(agent)
    if not tpl:
        raise ValueError(f"no Slack template for {agent}")
    names = [n for n in re.findall(r"{(\w+)}", tpl) if n != "notify_user"]
    if not isinstance(fields, dict):
        raise ValueError("outbox must be a JSON object of field -> text")
    unknown = sorted(set(fields) - set(names))
    if unknown:
        raise ValueError(f"unknown field(s) {unknown}; {agent} takes {names}")
    payload = {}
    for n in names:
        v = fields.get(n, "")
        if not isinstance(v, str):
            raise ValueError(f"field {n} must be text")
        v = v.strip() or "—"
        if len(v) > FIELD_MAX_CHARS:
            raise ValueError(f"field {n} is {len(v)} chars (max {FIELD_MAX_CHARS})")
        if MENTION_RE.search(v):
            raise ValueError(f"field {n} contains a mention or channel/user reference; only the guard adds the mention")
        payload[n] = v
    if agent == "field-brief":
        for n in ("pick_1", "pick_2", "pick_3"):
            if payload[n] != "—" and "https://" not in payload[n]:
                raise ValueError(f"{n} has no https:// article link")
    if agent == "account-watch" and payload["signals"] != "—" and not payload["signals"].lower().startswith("none"):
        for line in payload["signals"].splitlines():
            if line.strip() and "https://" not in line:
                raise ValueError(f"signals line has no https:// source link: {line[:60]!r}")
    user = cfg.get("slack_self_user_id", "")
    if not re.match(r"^U[A-Z0-9]+$", user):
        raise ValueError("slack_self_user_id missing or invalid in config")
    fallback = tpl.replace("{notify_user} ", "").format(**payload)
    if len(fallback.splitlines()) > POST_MAX_LINES:
        raise ValueError(f"post is {len(fallback.splitlines())} lines (max {POST_MAX_LINES})")
    payload["notify_user"] = user
    return payload, fallback


def webhook_url(agent):
    f = os.path.join(SECRETS, f"slack_webhook_url.{agent}")
    if not os.path.exists(f):
        return None
    with open(f, encoding="utf-8") as fh:
        url = fh.read().strip()
    return url if url.startswith("https://hooks.slack.com/") else None


def send_webhook(url, payload, attempts=2):
    """POST JSON to a Slack workflow trigger. Returns None on success, else the last error string."""
    err = None
    for i in range(attempts):
        req = urllib.request.Request(url, data=json.dumps(payload).encode(), method="POST",
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                body = r.read().decode(errors="replace")
            if r.status == 200 and '"ok":true' in body.replace(" ", ""):
                return None
            err = f"HTTP {r.status}: {body[:200]}"
        except urllib.error.HTTPError as e:
            err = f"HTTP {e.code}: {e.read().decode(errors='replace')[:200]}"
        except (urllib.error.URLError, OSError) as e:
            err = f"{type(e).__name__}: {e}"
        if i + 1 < attempts:
            time.sleep(3)
    return err


def cmd_post(agent, cfg):
    """0 = posted via workflow. 4 = webhook failed: fallback text printed for the agent to send via MCP.
    2 = nothing to send (no ready post) or the post is invalid."""
    ready = outbox_path(agent, ready=True)
    if not os.path.exists(ready):
        print("guard: no ready post (shadow mode, critic FAIL, revert, or nothing drafted) — not posting")
        return 2
    try:
        with open(ready, encoding="utf-8") as fh:
            payload, fallback = render_post(agent, json.load(fh), cfg)
    except (ValueError, json.JSONDecodeError) as e:
        os.remove(ready)
        print(f"guard: post rejected — {e}")
        log_line(agent, f"post rejected: {e}")
        return 2
    os.remove(ready)  # one send per run, success or not
    url = webhook_url(agent)
    err = send_webhook(url, payload) if url else f"no webhook URL in _agents/.secrets/slack_webhook_url.{agent}"
    if err is None:
        log_line(agent, "post sent via workflow")
        print("guard: posted via workflow")
        return 0
    log_line(agent, f"post webhook failed: {err}")
    print(f"guard: webhook failed — {err}\nFALLBACK: send exactly the text below with mcp__slack__slack_send_message "
          f"(channel_id: {cfg.get('slack_agent_channel_id', '?')}):\n----\n{fallback}")
    return 4


def cmd_pause(cfg):
    wait = int(cfg.get("guard", {}).get("lock_wait_minutes", 10) or 10)
    if not acquire_lock("interactive", wait):
        print(f"guard: lock held by {open(LOCK).read()} — gave up after {wait} min")
        return 2
    print("guard: paused — scheduled agents will wait on this lock or back off. "
          "Run `guard.py resume` when done.")
    return 0


def cmd_resume():
    if not os.path.exists(LOCK):
        print("guard: no lock held")
        return 0
    held_by = json.load(open(LOCK))
    if held_by.get("agent") != "interactive":
        print(f"guard: lock is held by {held_by} (not an interactive pause) — not releasing. "
              f"Use `guard.py release` to force it.")
        return 2
    release_lock()
    print("guard: resumed — lock released")
    return 0


def cmd_status():
    if os.path.exists(LOCK):
        print(f"lock: HELD {open(LOCK).read()} "
              f"({int((time.time() - os.path.getmtime(LOCK)) / 60)} min)")
    else:
        print("lock: free")
    for name in sorted(os.listdir(AGENTS_DIR)) if os.path.isdir(AGENTS_DIR) else []:
        if os.path.exists(snapshot_file(name)):
            print(f"run in progress: {name}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("command", choices=["start", "diff", "finish", "pause", "resume", "status", "release", "post"])
    ap.add_argument("agent", nargs="?")
    ap.add_argument("--revert", action="store_true", help="critic FAIL: restore pre-run state")
    ap.add_argument("-m", "--message", default="", help="one-line commit summary")
    a = ap.parse_args()
    cfg = load_config()
    if a.command == "status":
        return cmd_status()
    if a.command == "release":
        release_lock()
        print("guard: lock released")
        return 0
    if a.command == "pause":
        return cmd_pause(cfg)
    if a.command == "resume":
        return cmd_resume()
    if not a.agent or not re.match(r"^[a-z0-9-]+$", a.agent):
        ap.error("agent name required (lowercase, hyphenated)")
    if a.command == "start":
        return cmd_start(a.agent, cfg)
    if a.command == "diff":
        return cmd_diff(a.agent, cfg)
    if a.command == "post":
        return cmd_post(a.agent, cfg)
    return cmd_finish(a.agent, cfg, a.revert, a.message)


if __name__ == "__main__":
    sys.exit(main())
