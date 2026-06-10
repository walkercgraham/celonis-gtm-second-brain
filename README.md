# Celonis GTM Second Brain

An Obsidian + Claude Code system that gives Celonis GTM professionals a persistent, AI-augmented memory across every client, meeting, and stakeholder interaction. Stop re-reading Slack threads before calls. Stop forgetting what you promised. Start compounding context.

---

## The Problem

You manage multiple accounts. Dozens of meetings per week. Stakeholders with different priorities across every engagement. Your context lives in Slack threads you can't find, emails you half-remember, and notes scattered across three apps. Before every call you scramble to piece together "where were we?" — and you still miss things.

## The Solution

One vault. One command before every call. Full context in seconds.

```
> /prep acme-corp

## Status: PoV in progress — awaiting data access confirmation
## Key People: Jane (VP Ops, cares about cost reduction), John (Dir IT, worried about governance)
## Open Loops: We owe them the ROI model (3 days overdue). They owe us SAP access.
## What's Worked: Leading with operational metrics, not IT transformation language.
## Talking Points: Follow up on data access, preview ROI model structure, confirm workshop date.
```

---

## What You Get

**22 AI-powered skills** that automate the mechanical parts of knowledge work:

| Category | Skills | What They Do |
|----------|--------|-------------|
| Daily ops | `/morning`, `/daily`, `/eod` | Orient, capture, reflect |
| Meetings | `/meeting`, `/prep` | Process transcripts, brief before calls |
| Portfolio | `/portfolio`, `/refresh`, `/triage` | Health dashboards, staleness detection, cleanup |
| Research | `/research`, `/external-research`, `/stakeholder-research`, `/pattern` | Deep intelligence from 5 sources |
| Reviews | `/weekly-review`, `/monthly-review`, `/quarterly-review`, `/wins` | Spot patterns, build promotion cases |
| Manager | `/1-1` | Data-backed 1:1 prep |
| Maintenance | `/process-inbox`, `/sync-actions`, `/clean-up` | Keep the system running |

**Structured vault** with folders, templates, and conventions that keep everything findable as it scales to hundreds of notes.

**Works for every GTM role** — AEs, VEs, AVEs, SEs, CSMs, BDRs. The structure adapts to your workflow.

---

## Quickstart (15 min)

### 1. Clone and open

```bash
git clone https://github.com/walkercgraham/celonis-gtm-second-brain.git
cd celonis-gtm-second-brain
```

Open the folder as a vault in [Obsidian](https://obsidian.md).

### 2. Configure

Edit `CLAUDE.md` — replace the placeholders:
- `[Your Name]` — your name
- `[Your Role]` — your Celonis role
- `[Your City, Country]` — your location
- `[Your Timezone]` — e.g., CET, GMT, EST

### 3. Start using

Point [Claude Code](https://claude.ai/code) at the vault directory and run:

```
/daily          ← creates today's note
/new-client     ← sets up your first client
/meeting        ← paste a transcript, get a structured note
/prep [client]  ← briefing before your next call
```

That's it. Build from there.

---

## The Compound Effect

| Week | What Changes |
|------|-------------|
| 1 | Feels like overhead |
| 4 | Pre-call prep takes 2 min instead of 15 |
| 8 | Cross-account patterns emerge — "we did this at Company A" |
| 12 | Weekly reviews surface invisible themes |
| 26 | Genuine knowledge graph — months of context in seconds |

---

## Documentation

- **[USER-GUIDE.md](USER-GUIDE.md)** — Full workflow guide, per-role benefits, all skill details
- **[CLAUDE.md](CLAUDE.md)** — System instructions (Claude Code reads this automatically)

---

## Requirements

- [Obsidian](https://obsidian.md) (free)
- [Claude Code](https://claude.ai/code) (CLI, desktop app, or IDE extension)
- Optional: Granola/Otter (meeting transcripts), Google Calendar, Gmail, Slack (MCP integrations)

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

This template was built from real daily use across a multi-account Celonis portfolio. If you find improvements, patterns, or new skills that work — PRs welcome.

---

*Built with Obsidian + Claude Code. 22 skills. Zero lost context.*
