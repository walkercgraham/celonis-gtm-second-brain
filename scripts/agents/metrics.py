#!/usr/bin/env python3
"""Vault health metrics for the agent team. Standard library only.

    metrics.py              markdown table to stdout
    metrics.py --json       JSON to stdout
    metrics.py --out PATH   also write a markdown note (with frontmatter) to PATH
    metrics.py --open-loops PATH   measure another open-loops file (loop-keeper shadow output)

Used for the baseline snapshot, the critic's loop-keeper reconciliation, and the day-20 review.
"""
import argparse
import datetime as dt
import glob
import json
import os
import re

VAULT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TODAY = dt.date.today()
DUE = re.compile(r"#due/(\d{4}-\d{2}-\d{2})")


def read(rel):
    p = os.path.join(VAULT, rel)
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    out = {}
    if m:
        for line in m.group(1).splitlines():
            k, _, v = line.partition(":")
            if v.strip():
                out[k.strip()] = v.strip().strip('"')
    return out


def open_loops(path="_current/open-loops.md"):
    text = read(path)
    dv = text.find("```dataview")
    body = text[:dv] if dv >= 0 else text
    open_items = re.findall(r"^\s*- \[ \] .*$", body, re.M)
    done_items = re.findall(r"^\s*- \[x\] .*$", body, re.M | re.I)
    overdue = [l for l in open_items
               if (m := DUE.search(l)) and dt.date.fromisoformat(m.group(1)) < TODAY]
    sections = {}
    current = None
    for line in body.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections.setdefault(current, 0)
        elif current and re.match(r"^\s*- \[ \] ", line):
            sections[current] += 1
    return {
        "open": len(open_items),
        "done_in_file": len(done_items),
        "overdue": len(overdue),
        "overdue_30d": sum(1 for l in overdue
                           if (TODAY - dt.date.fromisoformat(DUE.search(l).group(1))).days > 30),
        "added_sections": len(re.findall(r"^## Added", body, re.M)),
        "inbox_unsorted": sections.get("Inbox (unsorted)", 0),
        "stale_section": sections.get("Stale: confirm or drop", 0),
        "action_required_tags": sum("#action-required" in l for l in open_items),
        "dataview_block_sha": __import__("hashlib").sha256(text[dv:].encode()).hexdigest()[:12]
        if dv >= 0 else None,
    }


def file_age_days(rel):
    fm = frontmatter(read(rel))
    try:
        return (TODAY - dt.date.fromisoformat(fm.get("modified", "")[:10])).days
    except ValueError:
        return None


def inbox_verdicts():
    files = ["_current/agent-inbox.md"] + sorted(
        os.path.relpath(p, VAULT) for p in glob.glob(os.path.join(VAULT, "_agents/inbox-archive/*.md")))
    yes = no = pending = 0
    for f in files:
        for line in read(f).splitlines():
            if "**You:**" in line:
                if "[x] ✅" in line:
                    yes += 1
                elif "[x] ❌" in line:
                    no += 1
                else:
                    pending += 1
    decided = yes + no
    return {"approved": yes, "rejected": no, "pending": pending,
            "approval_rate": round(yes / decided, 2) if decided else None}


def meetings(days=30):
    since = TODAY - dt.timedelta(days=days)
    auto = manual = with_wispr = 0
    for p in glob.glob(os.path.join(VAULT, "02-areas/celonis/**/meetings/*.md"), recursive=True):
        fm = frontmatter(open(p, encoding="utf-8").read(4000))
        try:
            created = dt.date.fromisoformat(fm.get("created", "")[:10])
        except ValueError:
            continue
        if created < since:
            continue
        if fm.get("created_by") == "ingestor":
            auto += 1
        else:
            manual += 1
        with_wispr += bool(fm.get("wispr_id"))
    return {"window_days": days, "auto": auto, "manual": manual, "with_wispr_id": with_wispr}


def daily_streak():
    have = {os.path.basename(p)[:10] for p in glob.glob(os.path.join(VAULT, "01-daily/*/*.md"))}
    weekdays = [TODAY - dt.timedelta(days=i) for i in range(1, 15)]
    weekdays = [d for d in weekdays if d.weekday() < 5]
    return {"weekday_daily_notes_last_14d": sum(d.isoformat() in have for d in weekdays),
            "weekdays_last_14d": len(weekdays)}


def collect(open_loops_path="_current/open-loops.md"):
    inbox_dir = os.path.join(VAULT, "00-inbox")
    return {
        "date": TODAY.isoformat(),
        "open_loops": open_loops(open_loops_path),
        "this_week_age_days": file_age_days("_current/this-week.md"),
        "active_clients_age_days": file_age_days("_current/active-clients.md"),
        "inbox_files": len([f for f in os.listdir(inbox_dir) if not f.startswith(".")])
        if os.path.isdir(inbox_dir) else 0,
        "agent_inbox": inbox_verdicts(),
        "meetings": meetings(),
        "daily_notes": daily_streak(),
    }


def to_markdown(m):
    ol = m["open_loops"]
    rows = [
        ("Open-loops open items", ol["open"]),
        ("Open-loops overdue", ol["overdue"]),
        ("Open-loops overdue > 30d", ol["overdue_30d"]),
        ("`## Added` sections", ol["added_sections"]),
        ("`## Inbox (unsorted)` items", ol["inbox_unsorted"]),
        ("`## Stale` items", ol["stale_section"]),
        ("`#action-required` on open items", ol["action_required_tags"]),
        ("Dataview block sha", ol["dataview_block_sha"]),
        ("this-week.md age (days)", m["this_week_age_days"]),
        ("active-clients.md age (days)", m["active_clients_age_days"]),
        ("00-inbox files", m["inbox_files"]),
        ("Agent inbox approved / rejected / pending",
         f"{m['agent_inbox']['approved']} / {m['agent_inbox']['rejected']} / {m['agent_inbox']['pending']}"),
        ("Agent inbox approval rate", m["agent_inbox"]["approval_rate"]),
        (f"Meeting notes last {m['meetings']['window_days']}d auto / manual",
         f"{m['meetings']['auto']} / {m['meetings']['manual']}"),
        ("Meeting notes with wispr_id", m["meetings"]["with_wispr_id"]),
        ("Weekday daily notes, last 14d",
         f"{m['daily_notes']['weekday_daily_notes_last_14d']} / {m['daily_notes']['weekdays_last_14d']}"),
    ]
    return "| Metric | Value |\n|---|---|\n" + "\n".join(f"| {k} | {v} |" for k, v in rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--open-loops", default="_current/open-loops.md",
                    help="vault-relative path, e.g. a loop-keeper shadow file")
    a = ap.parse_args()
    m = collect(a.open_loops)
    md = to_markdown(m)
    print(json.dumps(m, indent=1) if a.json else md)
    if a.out:
        path = os.path.join(VAULT, a.out)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(f"---\ntype: resource\ntags: [agents, metrics]\ncreated: {m['date']}\n"
                     f"modified: {m['date']}\nstatus: active\nrelated:\n  - \"[[AGENTS]]\"\n"
                     f"  - \"[[open-loops]]\"\n---\n\n# Vault metrics — {m['date']}\n\n{md}\n\n"
                     f"```json\n{json.dumps(m, indent=1)}\n```\n")


if __name__ == "__main__":
    main()
