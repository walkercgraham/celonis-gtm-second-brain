# Celonis GTM Second Brain

An Obsidian + Claude Code system that gives Celonis GTM professionals a persistent, AI-augmented memory across every client, meeting, and stakeholder interaction — plus an autonomous agent team that monitors your accounts, surfaces risks and opportunities, curates research, and keeps your vault in order while you focus on client work.

---

## The Problem

You manage multiple accounts. Dozens of meetings per week. Stakeholders with different priorities across every engagement. Your context lives in Slack threads you can't find, emails you half-remember, and notes scattered across three apps. Before every call you scramble to piece together "where were we?" — and you still miss things. Between calls, nothing monitors whether a client has gone quiet, a blocker has aged, or a public filing changes the deal.

## The Solution

One vault. One command before every call. Full context in seconds. And an agent team that works in the background so nothing falls through the cracks.

```
> /prep acme-corp

## Status: PoV in progress — awaiting data access confirmation
## Key People: Jane (VP Ops, cares about cost reduction), John (Dir IT, worried about governance)
## Open Loops: We owe them the ROI model (3 days overdue). They owe us SAP access.
## What's Worked: Leading with operational metrics, not IT transformation language.
## Talking Points: Follow up on data access, preview ROI model structure, confirm workshop date.
```

Meanwhile, your agents have already flagged that Acme Corp posted a profit warning yesterday, that Jane hasn't been mentioned in any channel for 14 days, and that the same objection you handled at one client came up at another — with a draft reusable answer waiting for your ✅.

---

## What You Get

### 22 AI-powered skills (manual — you invoke them)

| Category | Skills | What They Do |
|----------|--------|-------------|
| Daily ops | `/morning`, `/daily`, `/eod` | Orient, capture, reflect |
| Meetings | `/meeting`, `/prep` | Process transcripts, brief before calls |
| Portfolio | `/portfolio`, `/refresh`, `/triage` | Health dashboards, staleness detection, cleanup |
| Research | `/research`, `/external-research`, `/stakeholder-research`, `/pattern` | Deep intelligence from 5 sources |
| Reviews | `/weekly-review`, `/monthly-review`, `/quarterly-review`, `/wins` | Spot patterns, build promotion cases |
| Manager | `/1-1` | Data-backed 1:1 prep |
| Maintenance | `/process-inbox`, `/sync-actions`, `/clean-up` | Keep the system running |

### 14 autonomous agents (scheduled — they run in the background)

| Agent | Schedule | What It Does |
|-------|----------|--------------|
| **chief-of-staff** | Daily 06:30 + Fri/Sun | Morning briefing, per-meeting prep, inbox management, weekly review/prep |
| **ingestor** | Twice daily | Gmail + Slack signal pipeline — one line per account per day in your daily note |
| **loop-keeper** | Nightly | Open-loops maintenance: extract tasks, dedup, flag overdue |
| **account-sentinel** | Friday | RAG early-warning across all active accounts |
| **opportunity-scout** | Friday | Finds reusable assets, cross-account patterns, career evidence gaps |
| **capture-keeper** | Hourly (workdays) | Files your Slack voice memos and thoughts into the vault |
| **field-brief** | Sunday | Enterprise AI research curation: 3 articles/week with draft vault notes |
| **account-watch** | Mon/Wed/Fri | Public-source monitoring: filings, press, vendor announcements, jobs |
| **critic** | Every run | Independent QA — 7 checks on every agent's output before it commits |

Agents propose actions through `_current/agent-inbox.md`. You ✅ or ❌. Chief-of-staff carries out your decisions each morning. Everything starts in **shadow mode** — agents write to their own folder only until you're confident in their output.

### Structured vault

Folders, templates, and conventions that keep everything findable as it scales to hundreds of notes.

**Works for every GTM role** — AEs, VEs, AVEs, SEs, CSMs, BDRs. The structure adapts to your workflow.

---

## Quickstart (15 min)

### 1. Clone and open

```bash
git clone https://github.com/your-org/celonis-gtm-second-brain.git
cd celonis-gtm-second-brain
```

Open the folder as a vault in [Obsidian](https://obsidian.md).

### 2. Configure

Edit `CLAUDE.md` — replace the placeholders:
- `[Your Name]` — your name
- `[Your Role]` — your Celonis role
- `[Your City, Country]` — your location
- `[Your Timezone]` — e.g., CET, GMT, EST

### 3. Start using skills

Point [Claude Code](https://claude.ai/code) at the vault directory and run:

```
/daily          ← creates today's note
/new-client     ← sets up your first client
/meeting        ← paste a transcript, get a structured note
/prep [client]  ← briefing before your next call
```

That's it. Build from there.

### 4. Enable agents (when ready)

Once you're comfortable with the vault and skills (1–2 weeks), set up the agent system:

1. Copy the config: `cp _agents/config-template.yaml _agents/config.yaml`
2. Fill in your Slack IDs, timezone, and vault path
3. Register scheduled tasks (see `_agents/scheduled-tasks.md`)
4. All agents start in shadow mode — review their output before going live

Full setup guide: **[_agents/README.md](_agents/README.md)**

---

## The Compound Effect

| Week | What Changes |
|------|-------------|
| 1 | Feels like overhead |
| 4 | Pre-call prep takes 2 min instead of 15 |
| 8 | Cross-account patterns emerge — "we did this at Company A" |
| 12 | Weekly reviews surface invisible themes. Agents are running in shadow. |
| 16 | Agents go live. Morning briefing, account monitoring, and research curation run without you. |
| 26 | Genuine knowledge graph + autonomous monitoring — months of context in seconds, nothing slips |

---

## Documentation

- **[USER-GUIDE.md](USER-GUIDE.md)** — Full workflow guide, per-role benefits, all skill and agent details
- **[CLAUDE.md](CLAUDE.md)** — System instructions (Claude Code reads this automatically)
- **[AGENTS.md](AGENTS.md)** — Agent charter (decision rights, output contract, run protocol)
- **[_agents/README.md](_agents/README.md)** — Agent setup guide, progressive enablement, troubleshooting

---

## Requirements

- [Obsidian](https://obsidian.md) (free)
- [Claude Code](https://claude.ai/code) (CLI, desktop app, or IDE extension)

### For skills (optional MCP integrations)
- Google Calendar, Gmail, Slack — richer `/morning`, `/prep`, `/meeting` output
- Knowledge Lake — internal Celonis reference data
- Granola/Otter — meeting transcripts

### For agents (progressive — enable as you go)
- **Tier 1 (Foundation):** Google Calendar
- **Tier 2 (Signal Intelligence):** + Gmail, Slack, Knowledge Lake
- **Tier 3 (External Research):** + WebSearch, WebFetch

---

## Recommended Obsidian Plugins

Install from Settings → Community Plugins:

- **Periodic Notes** — auto-creates daily/weekly notes
- **Templater** — dynamic templates
- **QuickAdd** — one-hotkey inbox capture
- **Dataview** — query your vault like a database
- **Calendar** — visual calendar sidebar

---

## Contributing

This template was built from real daily use across a multi-account Celonis portfolio. If you find improvements, patterns, new skills or agent tweaks that work — PRs welcome.

---

*Built with Obsidian + Claude Code. 22 skills. 14 agents. Zero lost context.*
