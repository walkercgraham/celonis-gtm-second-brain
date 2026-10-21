---
type: resource
tags: [agents]
created: 2026-10-21
modified: 2026-10-21
status: active
related:
  - "[[AGENTS]]"
---

# Agent Schedule Reference

All times are in your local timezone (set in `_agents/config.yaml`). Register these as Claude Code scheduled tasks.

## Daily

| Time | Agent | What it does |
|------|-------|--------------|
| 06:30 | **chief-of-staff** | Morning: creates daily note, runs per-meeting prep, applies ✅'d inbox entries, decays stale items, folds excess to "Below the fold", posts morning briefing |
| 13:00, 18:00 | **ingestor** | Gmail/Slack signal pipeline → daily note timeline (weekdays) |
| Hourly 08–20 | **capture-keeper** | Files your Slack captures into the vault (daily note + open-loops) |
| 22:00 | **loop-keeper** | Nightly open-loops maintenance: extracts tasks, dedupes, flags overdue |

## Weekly

| Day | Time | Agent | What it does |
|-----|------|-------|--------------|
| Mon | 05:45 | **account-watch** | Public-source monitoring: official sources (filings, results, regulators) |
| Wed | 05:45 | **account-watch** | Public-source monitoring: market sources (press, vendors, tenders) |
| Fri | 05:45 | **account-watch** | Public-source monitoring: intent + people (jobs, execs, catch-up) |
| Fri | 15:00 | **opportunity-scout** | Finds high-leverage tasks: reusable assets, cross-account patterns, career evidence gaps |
| Fri | 16:00 | **account-sentinel** | Early-warning RAG sweep across all active accounts |
| Fri | 17:00 | **chief-of-staff** | Weekly review: summarises the week, spots patterns, updates cockpit |
| Sun | 17:00 | **chief-of-staff** | Weekly prep: reads sentinel + scout, prepares next week's focus |
| Sun | 20:00 | **field-brief** | Enterprise AI research curation: 3 articles with draft vault notes |

## Subagents (spawned by parents, never scheduled directly)

| Agent | Parent | What it does |
|-------|--------|--------------|
| **prep** | chief-of-staff | Per-meeting briefing (Knowledge Lake + vault context) |
| **account-ingestor** | ingestor | Reads one account's Gmail + Slack activity, returns signal lines |
| **account-analyst** | account-sentinel | Reads one account's 30-day activity, returns RAG + signals |
| **account-researcher** | account-watch | Searches public sources for one account, returns classified entries |
| **critic** | all agents | 7-check QA on every agent run before commit |

## Registration

Register scheduled tasks in Claude Code:
```
claude task create --name "chief-of-staff-daily" --schedule "30 6 * * *" --agent chief-of-staff
claude task create --name "ingestor" --schedule "0 13,18 * * 1-5" --agent ingestor
claude task create --name "loop-keeper" --schedule "0 22 * * *" --agent loop-keeper
claude task create --name "capture-keeper" --schedule "0 8-20 * * 1-5" --agent capture-keeper
claude task create --name "account-watch-mwf" --schedule "45 5 * * 1,3,5" --agent account-watch
claude task create --name "opportunity-scout" --schedule "0 15 * * 5" --agent opportunity-scout
claude task create --name "account-sentinel" --schedule "0 16 * * 5" --agent account-sentinel
claude task create --name "chief-of-staff-weekly-review" --schedule "0 17 * * 5" --agent chief-of-staff
claude task create --name "chief-of-staff-weekly-prep" --schedule "0 17 * * 0" --agent chief-of-staff
claude task create --name "field-brief" --schedule "0 20 * * 0" --agent field-brief
```

All agents start in **shadow mode** (`mode: shadow` in `_agents/config.yaml`). Shadow runs write to `_agents/<agent>/shadow/` only — review shadow output for 1–2 weeks before switching any agent to `mode: live`.
