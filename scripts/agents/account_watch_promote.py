#!/usr/bin/env python3
"""Promote an account-watch shadow run into the vault. Standard library only.

    account_watch_promote.py <shadow file> [--except 2,5] [--reason "…"] [--no-commit] [--dry-run]

Each `## → <research file>` section of the shadow file holds numbered entries (`### [n] YYYY-MM-DD · CODE · …`) exactly as
they would land. This script inserts every entry not listed in --except into its account's `<slug>-external-research.md`
(created from 03-resources/templates/external-research-template.md if missing), in date order under `## Signals (newest first)`,
skips any entry whose `<!-- key: … -->` is already in the file, and marks promoted keys `mode: live` in state.json. Excluded
entries are recorded under `## Rejected signals` in the agent log with the reason. Hubs that are no longer `status: active`
are refused. Running it twice changes nothing.

Run by chief-of-staff for `apply: promote-signals` (with --no-commit: the change rides in its own run commit), or by hand
(commits `agent(account-watch): promote shadow <date>` so `git revert` undoes it; pause the guard first).
"""
import argparse
import datetime as dt
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import guard  # noqa: E402  (reuse git)

AGENT = "account-watch"
SECTION_RE = re.compile(r"^## → (02-areas/celonis/([^/]+)/\2-external-research\.md)\s*$")
ENTRY_RE = re.compile(r"^### \[(\d+)\] (\d{4}-\d{2}-\d{2}) · (.+)$")
KEY_RE = re.compile(r"<!-- key: (.+?) -->")
SIGNALS_H = "## Signals (newest first)"


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def parse_shadow(text):
    """[{n, date, path, slug, body (entry as it lands, no [n]), key}] in file order."""
    entries, path, slug, cur = [], None, None, None
    for line in text.splitlines():
        sec = SECTION_RE.match(line)
        if sec or (line.startswith("## ") and not line.startswith("### ")):
            cur = None
            path, slug = (sec.group(1), sec.group(2)) if sec else (None, None)
            continue
        m = ENTRY_RE.match(line)
        if m and path:
            cur = {"n": int(m.group(1)), "date": m.group(2), "path": path, "slug": slug,
                   "lines": [f"### {m.group(2)} · {m.group(3)}"]}
            entries.append(cur)
            continue
        if cur is not None:
            cur["lines"].append(line)
    for e in entries:
        while e["lines"] and not e["lines"][-1].strip():
            e["lines"].pop()
        e["body"] = "\n".join(e["lines"])
        k = KEY_RE.search(e["body"])
        e["key"] = k.group(1).strip() if k else None
        del e["lines"]
    return entries


def hub_status(v, slug):
    hub = os.path.join(v, "02-areas", "celonis", slug, f"{slug}.md")
    if not os.path.exists(hub):
        return None
    m = re.search(r"^status:\s*(\S+)", _read(hub), re.M)
    return m.group(1) if m else None


def new_research_file(v, slug, today):
    tpl = _read(os.path.join(v, "03-resources", "templates", "external-research-template.md"))
    hub = _read(os.path.join(v, "02-areas", "celonis", slug, f"{slug}.md"))
    m = re.search(r'^client:\s*"?([^"\n]+)"?', hub, re.M)
    title = m.group(1).strip() if m else slug
    return tpl.replace("{{slug}}", slug).replace("{{date}}", today).replace("{{title}}", title)


def insert_entry(text, entry):
    """Insert entry under the Signals heading, keeping newest-first order by the entry date."""
    lines = text.split("\n")
    try:
        start = lines.index(SIGNALS_H) + 1
    except ValueError:
        raise ValueError(f"no '{SIGNALS_H}' heading")
    end = next((i for i in range(start, len(lines)) if lines[i].startswith("## ")), len(lines))
    pos = end
    for i in range(start, end):
        m = re.match(r"^### (\d{4}-\d{2}-\d{2}) · ", lines[i])
        if m and m.group(1) <= entry["date"]:
            pos = i
            break
    while pos > start and pos == end and not lines[pos - 1].strip():
        pos -= 1  # append after the last entry, not after trailing blanks
    block = entry["body"].split("\n") + [""]
    if pos > start and lines[pos - 1].strip():
        block = [""] + block
    lines[pos:pos] = block
    return "\n".join(lines)


def set_front(text, key, val):
    rx = re.compile(rf"^{key}:.*$", re.M)
    head, sep, rest = text.partition("\n---\n")
    if rx.search(head):
        head = rx.sub(f"{key}: {val}", head, count=1)
    return head + sep + rest


def quote_lines(entry):
    out = []
    for line in entry["body"].splitlines():
        if line.startswith("- **Quotes:**"):
            src = re.search(r"\]\((https?://[^)]+)\)", entry["body"])
            q = line[len("- **Quotes:**"):].strip()
            out.append(f"- {q}, {entry['date']}" + (f" ([source]({src.group(1)}))" if src else ""))
    return out


def promote(v, shadow_path, exclude=(), reason="", today=None, commit=True, dry=False):
    today = today or dt.date.today().isoformat()
    shadow_rel = os.path.relpath(os.path.abspath(shadow_path), v)
    entries = parse_shadow(_read(shadow_path))
    if not entries:
        raise SystemExit(f"no numbered entries found in {shadow_rel}")
    exclude = set(exclude)
    unknown = exclude - {e["n"] for e in entries}
    if unknown:
        raise SystemExit(f"--except numbers not in the shadow file: {sorted(unknown)}")

    state_p = os.path.join(v, "_agents", AGENT, "state.json")
    state = json.loads(_read(state_p)) if os.path.exists(state_p) else {"event_keys": {}}
    state.setdefault("event_keys", {})
    files, summary = {}, {"promoted": [], "skipped_existing": [], "excluded": [], "refused_inactive": []}

    for e in entries:
        if e["n"] in exclude:
            summary["excluded"].append(e["n"])
            continue
        if hub_status(v, e["slug"]) != "active":
            summary["refused_inactive"].append(f"[{e['n']}] {e['slug']}")
            continue
        full = os.path.join(v, e["path"])
        if e["path"] not in files:
            files[e["path"]] = _read(full) if os.path.exists(full) else new_research_file(v, e["slug"], today)
        text = files[e["path"]]
        if (e["key"] and f"<!-- key: {e['key']} -->" in text) or (not e["key"] and e["body"] in text):
            summary["skipped_existing"].append(e["n"])
            continue
        text = insert_entry(text, e)
        for q in quote_lines(e):
            if q not in text:
                text = text.rstrip("\n") + "\n" + q + "\n"
        files[e["path"]] = text
        summary["promoted"].append(e["n"])
        if e["key"]:
            state["event_keys"][e["key"]] = {"first_seen": e["date"], "mode": "live", "path": e["path"]}

    for p in files:
        files[p] = set_front(set_front(files[p], "modified", today), "last_checked", today)

    log_p = os.path.join(v, "_agents", AGENT, "log.md")
    log = _read(log_p) if os.path.exists(log_p) else ""
    rejected = []
    for e in entries:
        if e["n"] in exclude:
            line = f"- {e['key'] or e['body'].splitlines()[0]} — {today} — " \
                   f"{reason or 'excluded by user'} (shadow {os.path.basename(shadow_path)} [{e['n']}])"
            if line not in log:
                rejected.append(line)
    if rejected and "## Rejected signals" in log:
        log = re.sub(r"(## Rejected signals[^\n]*\n(?:<!--.*?-->\n)?)", lambda m: m.group(1) + "\n".join(rejected) + "\n",
                     log, count=1)

    changed = []
    if not dry:
        for p, text in files.items():
            full = os.path.join(v, p)
            if not os.path.exists(full) or _read(full) != text:
                _write(full, text)
                changed.append(p)
        if summary["promoted"]:
            _write(state_p, json.dumps(state, indent=1))
            changed.append(os.path.relpath(state_p, v))
        if rejected and os.path.exists(log_p):
            _write(log_p, log)
            changed.append(os.path.relpath(log_p, v))
        if commit and changed:
            date = re.search(r"\d{4}-\d{2}-\d{2}", os.path.basename(shadow_path))
            run_git(v, "add", "--", *changed)
            run_git(v, "commit", "-m", f"agent(account-watch): promote shadow {date.group(0) if date else shadow_rel}"
                                       f" — {len(summary['promoted'])} signals")
    summary["files"] = sorted(files)
    summary["changed"] = changed
    return summary


def run_git(v, *args):
    if os.path.abspath(v) == os.path.abspath(guard.VAULT):
        return guard.git(*args)
    import subprocess
    return subprocess.run(["git", *args], cwd=v, check=True, capture_output=True, text=True)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("shadow")
    ap.add_argument("--except", dest="exclude", default="", help="entry numbers to leave out, e.g. 2,5")
    ap.add_argument("--reason", default="", help="user's reason, recorded with the excluded entries")
    ap.add_argument("--no-commit", action="store_true", help="leave the change for the caller's commit (chief-of-staff)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--vault", default=guard.VAULT)
    a = ap.parse_args(argv)
    exclude = [int(x) for x in re.split(r"[,\s]+", a.exclude.strip()) if x]
    shadow = a.shadow if os.path.isabs(a.shadow) else os.path.join(a.vault, a.shadow)
    s = promote(a.vault, shadow, exclude, a.reason, commit=not a.no_commit, dry=a.dry_run)
    print(json.dumps(s, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
