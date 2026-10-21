#!/usr/bin/env python3
"""Capture Keeper helper: Slack thoughts in the capture channel -> linked vault captures. Standard library only.

    capture.py plan                      write _agents/capture-keeper/.run/plan.json (exact Slack call + link index)
    capture.py apply <captures.json>     validate the LLM's decisions and do every vault write; print a JSON summary
    capture.py seed                      set state.json last_ts to now (so older channel history is never ingested)

The LLM only decides what each message is about (cleaned text, links, action, structured). Everything mechanical
(windows, dedup, placement, frontmatter, state) happens here. See .claude/agents/capture-keeper.md.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import guard  # noqa: E402  (reuse load_config / agent_mode)

AGENT = "capture-keeper"
LONG_CHARS = 280  # longer thoughts get a short title line with the full text quoted beneath it
NOTE_PREFIX = re.compile(r"^\s*(note|idea)\s*:\s*", re.I)
AGENT_PREFIXES = ("📥", "☀️", "☀", "🛰️", "🛰", "💡", "🔁")
SKIP_DIRS = {".obsidian", ".git", ".trash", "_agents", ".claude", "scripts", "node_modules"}


def _tz():
    """Resolve timezone from config, falling back to UTC."""
    tz_name = guard.load_config().get("timezone", "")
    if tz_name:
        try:
            return ZoneInfo(tz_name)
        except (KeyError, ValueError):
            pass
    return ZoneInfo("UTC")


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _write(path, text):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


# ---------- paths / state ----------

def vault():
    return os.environ.get("CAPTURE_VAULT", guard.VAULT)


def agent_dir(v):
    return os.path.join(v, "_agents", AGENT)


def run_dir(v):
    return os.path.join(agent_dir(v), ".run")


def state_path(v, mode):
    sub = "shadow" if mode == "shadow" else ""
    return os.path.join(agent_dir(v), sub, "state.json")


def load_state(v, mode):
    tz = _tz()
    p = state_path(v, mode)
    if not os.path.exists(p) and mode == "shadow":
        p = state_path(v, "live")  # shadow starts from the live watermark
    if os.path.exists(p):
        return json.loads(_read(p))
    return {"last_ts": f"{dt.datetime.now(tz).timestamp() - 86400:.6f}"}


def save_state(v, mode, state):
    p = state_path(v, mode)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    _write(p, json.dumps(state, indent=1))


def current_mode(v, override=None):
    if override:
        return override
    return guard.agent_mode(guard.load_config(), AGENT)


def config_value(key, default=""):
    return guard.load_config().get(key, default) or default


# ---------- markdown helpers ----------

def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    out = {}
    if not m:
        return out
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, _, val = line.partition(":")
            out[k.strip()] = val.strip().strip('"')
    return out


def h1(text):
    m = re.search(r"^# (.+)$", text, re.M)
    return m.group(1).strip() if m else ""


def stem_counts(v):
    """{stem: number of notes with that filename}. A wikilink to a stem with count > 1 is ambiguous in Obsidian."""
    counts = {}
    for root, dirs, files in os.walk(v):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith(".md"):
                counts[f[:-3]] = counts.get(f[:-3], 0) + 1
    return counts


def client_hubs(v):
    celonis = os.path.join(v, "02-areas", "celonis")
    if not os.path.isdir(celonis):
        return set()
    return {c for c in os.listdir(celonis)
            if not c.startswith("_") and os.path.exists(os.path.join(celonis, c, f"{c}.md"))}


def linkable(v):
    """Stems that resolve to exactly one note, plus client hub slugs (the vault-wide convention for [[client]])."""
    counts = stem_counts(v)
    return {s for s, n in counts.items() if n == 1} | (client_hubs(v) & set(counts))


def build_index(v):
    """Link targets the LLM should pick from. `link` is the exact wikilink target (file stem)."""
    idx = []
    celonis = os.path.join(v, "02-areas", "celonis")
    if os.path.isdir(celonis):
        for c in sorted(os.listdir(celonis)):
            hub = os.path.join(celonis, c, f"{c}.md")
            if c.startswith("_") or not os.path.exists(hub):
                continue
            fm = frontmatter(_read(hub))
            idx.append({"kind": "client", "link": c, "name": fm.get("client", c), "status": fm.get("status", ""),
                        "email_domains": fm.get("email_domains", "")})
        for root, _, files in os.walk(celonis):
            if "/stakeholders" not in root.replace(os.sep, "/"):
                continue
            rel = os.path.relpath(root, celonis).split(os.sep)[0]
            for f in sorted(files):
                if f.endswith(".md"):
                    t = _read(os.path.join(root, f))
                    fm = frontmatter(t)
                    idx.append({"kind": "person", "link": f[:-3], "name": h1(t) or f[:-3], "client": rel,
                                "role": fm.get("role", "")})
        ini = os.path.join(celonis, "_internal", "initiatives")
        if os.path.isdir(ini):
            for d in sorted(os.listdir(ini)):
                hub = os.path.join(ini, d, f"{d}.md")
                if os.path.exists(hub):
                    idx.append({"kind": "initiative", "link": d, "name": h1(_read(hub)) or d})
    con = os.path.join(v, "03-resources", "concepts")
    if os.path.isdir(con):
        for f in sorted(os.listdir(con)):
            if f.endswith(".md"):
                idx.append({"kind": "concept", "link": f[:-3], "name": f[:-3]})
    ok = linkable(v)
    return [i for i in idx if i["link"] in ok]  # never offer an ambiguous target


def section_insert(text, heading, line, before_headings=()):
    """Append `line` at the end of the `## heading` section. Create the section if missing."""
    lines = text.split("\n")
    try:
        start = next(i for i, l in enumerate(lines) if l.strip() == f"## {heading}")
    except StopIteration:
        insert_at = len(lines)
        for i, l in enumerate(lines):
            if any(l.strip() == f"## {h}" for h in before_headings):
                insert_at = i
                break
        block = [f"## {heading}", "", line, ""]
        if insert_at > 0 and lines[insert_at - 1].strip():
            block.insert(0, "")
        lines[insert_at:insert_at] = block
        return "\n".join(lines)
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    last = end
    while last - 1 > start and not lines[last - 1].strip():
        last -= 1
    new = [line]
    if last == start + 1:
        new = ["", line]  # keep a blank line under the heading
    if last == end and end < len(lines):
        new.append("")  # keep a blank line before the next heading
    lines[last:last] = new
    return "\n".join(lines)


def slugify(s, n=50):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:n].rstrip("-") or "capture"


# ---------- commands ----------

def cmd_plan(v, mode):
    tz = _tz()
    state = load_state(v, mode)
    last = dt.datetime.fromtimestamp(float(state["last_ts"]), tz)
    after = (last.date() - dt.timedelta(days=1)).isoformat()  # Slack after: is exclusive
    channel = config_value("slack_capture_channel_id")
    user = config_value("slack_self_user_id")
    if not channel or not user:
        print("capture: slack_capture_channel_id / slack_self_user_id missing in config", file=sys.stderr)
        return 2
    plan = {
        "mode": mode,
        "now": dt.datetime.now(tz).isoformat(timespec="seconds"),
        "last_ts": state["last_ts"],
        "slack_call": {
            "tool": "mcp__slack__slack_search_public_and_private",
            "filters": f"in:<#{channel}> from:<@{user}> after:{after}",
            "sort": "timestamp", "sort_dir": "asc", "limit": 20, "include_context": False,
            "response_format": "detailed", "natural_language_query": "",
        },
        "keep_only": f"messages with Message_ts > {state['last_ts']}",
        "index": build_index(v),
    }
    os.makedirs(run_dir(v), exist_ok=True)
    out = os.path.join(run_dir(v), "plan.json")
    _write(out, json.dumps(plan, indent=1, ensure_ascii=False))
    print(json.dumps({"plan": os.path.relpath(out, v), "slack_call": plan["slack_call"], "keep_only": plan["keep_only"],
                      "index_size": len(plan["index"])}, ensure_ascii=False, indent=1))
    return 0


def capture_line(hhmm, text, links, permalink, ts):
    arrow = (" → " + ", ".join(f"[[{l}]]" for l in links)) if links else ""
    return f"- 💭 {hhmm} {text}{arrow} [↗]({permalink}) %%cap:{ts}%%"


def inbox_note(date, hhmm, title, text, links, permalink, client, daily_link):
    related = ([f"[[{daily_link}]]"] if daily_link else []) + [f"[[{l}]]" for l in links]
    tags = ["capture"] + (["celonis", f"client/{client}"] if client else [])
    rel = "\n".join(f'  - "{r}"' for r in related) or '  - "[[open-loops]]"'
    return (f"---\ntype: resource\ntags: [{', '.join(tags)}]\ncreated: {date}\nmodified: {date}\nstatus: active\n"
            f"source: \"{permalink}\"\ncreated_by: {AGENT}\nrelated:\n{rel}\n---\n\n# {title}\n\n{text}\n\n"
            f"*Captured {hhmm} via Slack — [original]({permalink}).*\n")


def cmd_apply(v, mode, captures_file, dry=False, today=None):
    tz = _tz()
    data = json.loads(_read(captures_file))
    state = load_state(v, mode)
    last_ts = float(state["last_ts"])
    counts = stem_counts(v)
    ok = linkable(v)
    summary = {"mode": mode, "processed_ts": [], "written": [], "inbox_notes": [], "actions": [], "skipped": [],
               "held": [], "warnings": []}
    pending = {}  # path -> new text (applied at the end; shadow/dry: reported only)

    def read(path):
        if path in pending:
            return pending[path]
        full = os.path.join(v, path)
        return _read(full) if os.path.exists(full) else None

    max_ts = last_ts
    first_held = None  # ts of the first capture whose daily note doesn't exist yet; the watermark stops before it
    today = today or dt.datetime.now(tz).date()
    for c in sorted(data.get("captures", []), key=lambda c: float(c["ts"])):
        ts, raw = str(c["ts"]), (c.get("raw") or "").strip()
        text = " ".join((c.get("text") or raw).split())
        if float(ts) <= last_ts:
            summary["skipped"].append({"ts": ts, "why": "not newer than last_ts"})
            continue
        if raw.startswith(AGENT_PREFIXES) or text.startswith(AGENT_PREFIXES):
            summary["skipped"].append({"ts": ts, "why": "agent post"})
            max_ts = max(max_ts, float(ts))
            continue
        want_note = bool(NOTE_PREFIX.match(raw) or NOTE_PREFIX.match(text))
        text = NOTE_PREFIX.sub("", text, count=1).strip()
        if not text:
            summary["skipped"].append({"ts": ts, "why": "empty"})
            max_ts = max(max_ts, float(ts))
            continue
        permalink = c.get("permalink", "")
        if "slack.com/archives/" not in permalink:
            summary["warnings"].append(f"{ts}: missing/odd permalink")
        links = []
        for l in c.get("links", []):
            l = l.strip().strip("[]")
            if l in links:
                continue
            if l in ok:
                links.append(l)
            else:
                why = "ambiguous" if counts.get(l, 0) > 1 else "unresolved"
                summary["warnings"].append(f"{ts}: dropped {why} link [[{l}]]")
        client = c.get("client") if c.get("client") in client_hubs(v) else None
        when = dt.datetime.fromtimestamp(float(ts), tz)
        date, hhmm = when.date().isoformat(), when.strftime("%H:%M")
        anchor = f"%%cap:{ts}%%"

        # File into the capture day's note, or the first daily note after it (weekend/early thoughts land on the next
        # working day). No such note yet -> hold: nothing is written and the watermark stays before this message.
        target, target_text = None, None
        d = when.date()
        while d <= today:
            path = f"01-daily/{d:%Y-%m}/{d.isoformat()}.md"
            t = read(path)
            if t is not None:
                target, target_text = path, t
                break
            d += dt.timedelta(days=1)
        if target is None:
            summary["held"].append({"ts": ts, "why": f"no daily note on/after {date} yet"})
            first_held = first_held if first_held is not None else float(ts)
            continue
        if first_held is None:
            max_ts = max(max_ts, float(ts))
        target_date = target[-13:-3]
        label = hhmm if target_date == date else f"{when:%a %d %b} {hhmm}"

        if anchor in target_text:
            summary["skipped"].append({"ts": ts, "why": "already captured"})
            summary["processed_ts"].append(ts)
            continue

        line_links, quote = list(links), None
        title = (c.get("title") or text[:60]).strip().rstrip(".")
        if want_note:
            note = f"00-inbox/{date}-{when:%H%M}-{slugify(title)}.md"
            if read(note) is None:
                pending[note] = inbox_note(date, hhmm, title, text, links, permalink, client, target[-13:-3])
                summary["inbox_notes"].append(note)
            line_links = [note[len("00-inbox/"):-3]] + links
            line_text = title
        elif len(text) > LONG_CHARS:
            line_text, quote = title, text  # full text stays in the daily note, quoted under the line
        else:
            line_text = text
        line = capture_line(label, line_text, line_links, permalink, ts)
        if quote:
            line += "\n  > " + quote
        pending[target] = section_insert(target_text, "Captures", line,
                                         before_headings=("Actions Discovered", "Shipped", "Decided", "EOD Reflection"))
        summary["written"].append({"ts": ts, "file": target})
        if c.get("action"):
            ol = "_current/open-loops.md"
            ol_text = read(ol)
            if ol_text is None or "## Inbox (unsorted)" not in ol_text:
                summary["warnings"].append(f"{ts}: open-loops Inbox missing; action not added")
            elif anchor not in ol_text:
                tag = f" #client/{client}" if client else ""
                due = f" #due/{c['due']}" if re.match(r"^\d{4}-\d\d-\d\d$", str(c.get("due") or "")) else ""
                item = f"- [ ] {' '.join(c['action'].split())}{tag}{due} (from [[{target_date}]]) {anchor}"
                pending[ol] = section_insert(ol_text, "Inbox (unsorted)", item)
                summary["actions"].append(item)
        summary["processed_ts"].append(ts)
    if first_held is not None:
        max_ts = max(last_ts, min(max_ts, first_held - 0.000001))

    if mode == "shadow" or dry:
        if not dry:
            stamp = dt.datetime.now(tz).strftime("%Y-%m-%d-%H%M")
            rep = os.path.join(agent_dir(v), "shadow", f"{stamp}.md")
            os.makedirs(os.path.dirname(rep), exist_ok=True)
            body = [f"---\ntype: output\ntags: [agents, capture-keeper]\ncreated: {stamp[:10]}\nmodified: {stamp[:10]}\n"
                    f"status: active\nrelated:\n  - \"[[AGENTS]]\"\n---\n\n# Capture Keeper shadow run {stamp}\n",
                    "```json\n" + json.dumps(summary, ensure_ascii=False, indent=1) + "\n```\n"]
            for path, new in pending.items():
                body.append(f"\n## Would write `{path}`\n\n```markdown\n{new}\n```\n")
            _write(rep, "".join(body))
            summary["report"] = os.path.relpath(rep, v)
            save_state(v, "shadow", {"last_ts": f"{max_ts:.6f}"})
    else:
        for path, new in pending.items():
            full = os.path.join(v, path)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            _write(full, new)
        save_state(v, "live", {"last_ts": f"{max_ts:.6f}"})
    summary["last_ts"] = f"{max_ts:.6f}"
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return 0


def cmd_seed(v):
    tz = _tz()
    ts = f"{dt.datetime.now(tz).timestamp():.6f}"
    save_state(v, "live", {"last_ts": ts})
    print(f"capture: state seeded last_ts={ts}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("command", choices=["plan", "apply", "seed"])
    ap.add_argument("file", nargs="?")
    ap.add_argument("--mode", choices=["live", "shadow"], help="override config mode (tests)")
    ap.add_argument("--dry-run", action="store_true", help="apply: print what would happen, write nothing")
    a = ap.parse_args()
    v = vault()
    if a.command == "seed":
        return cmd_seed(v)
    mode = current_mode(v, a.mode)
    if a.command == "plan":
        return cmd_plan(v, mode)
    if not a.file:
        ap.error("apply needs the captures.json path")
    return cmd_apply(v, mode, a.file, dry=a.dry_run)


if __name__ == "__main__":
    sys.exit(main())
