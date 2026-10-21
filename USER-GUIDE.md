# User Guide — Celonis GTM Second Brain

## What This Is

This is an Obsidian vault + Claude Code system designed for Celonis GTM professionals. It acts as your second brain — storing everything you know about clients, stakeholders, meetings, and your own career progression in a structured, searchable, AI-augmented knowledge graph. It has two layers:

1. **22 skills** you invoke manually (`/prep`, `/meeting`, `/morning`, etc.)
2. **14 autonomous agents** that run in the background on schedules — monitoring accounts, surfacing risks, curating research, and keeping your vault in order while you focus on client work

**Who it's for:** AEs, AVEs, VEs, SEs, CSMs, BDRs — anyone in the Celonis GTM motion who manages client relationships and needs to carry context across dozens of accounts and hundreds of meetings.

**What it replaces:** Scattered notes in OneNote/Google Docs, lost Slack context, pre-call scrambles asking "what did we discuss last time?", forgotten action items, and the recurring feeling that you know things but can't find them when you need them. The agents also replace the manual monitoring you never have time for — checking public filings, tracking silent stakeholders, spotting cross-account patterns.

---

## Setup (15 Minutes)

### 1. Install the Tools
- **Obsidian** — [obsidian.md](https://obsidian.md) (free, local-first markdown editor)
- **Claude Code** — Anthropic's CLI tool, pointed at this vault directory
- **Optional:** Granola or Otter (meeting transcript capture)

### 2. Configure the Vault
1. Clone/copy this template to your local machine
2. Open the folder in Obsidian (File → Open Vault → select this folder)
3. Install recommended plugins: Periodic Notes, Templater, QuickAdd, Dataview, Calendar
4. Edit `CLAUDE.md` — fill in the `[Your Name]`, `[Your Role]`, `[Your City]`, `[Your Timezone]` placeholders

### 3. Configure Claude Code
1. Install Claude Code CLI or desktop app
2. Point it at this vault directory
3. Connect any MCP integrations you have access to (Google Calendar, Gmail, Slack, Granola, Knowledge Lake)
4. Test with: `/daily` — it should create today's daily note

### 4. Create Your First Client
Run `/new-client [client-name]` in Claude Code. This creates the folder structure and hub file. Populate the hub with what you already know — including the agent-required fields (`email_domains`, `slack_channels`, `region`, `involvement`).

### 5. Enable Agents (When Ready)
Once you're comfortable with the vault and skills (typically 1–2 weeks):
1. Copy the config: `cp _agents/config-template.yaml _agents/config.yaml`
2. Fill in your Slack IDs, timezone, and vault path
3. Copy region packs: `cp _agents/account-watch/regions-template.yaml _agents/account-watch/regions.yaml`
4. Register scheduled tasks (see `_agents/scheduled-tasks.md` for the full list)
5. All agents start in **shadow mode** — they write to `_agents/<agent>/shadow/` only
6. Review shadow output for 1–2 weeks, then switch agents to live tier by tier

Full agent setup guide: `_agents/README.md`

---

## Daily Workflow

### Morning (5 min) — Get Oriented

| Action | How | What It Does |
|--------|-----|-------------|
| Full morning briefing | **chief-of-staff agent** (auto) | Creates daily note, pulls calendar, runs per-meeting prep, posts briefing to Slack |
| Manual morning briefing | `/morning` (manual) | Same thing, invoked on demand |
| Just the daily note | `/daily` (manual) | Creates today's note from template with your 3 focus items |
| Check agent proposals | Open `_current/agent-inbox.md` | Review overnight ✅/❌ decisions — chief-of-staff carries them out |

**With agents enabled**, your morning is mostly done before you open the laptop. The chief-of-staff agent creates the daily note at 06:30, runs `/prep` for each meeting on your calendar, and posts a briefing to your agent Slack channel. You check the inbox, mark your verdicts, and you're ready.

**Without agents**, the `/morning` command is your single entry point. It chains together: daily note creation → calendar scan → per-meeting vault context → Gmail flags → open-loops due today.

### Before Every Client Call (2 min) — Get Briefed

| Action | Command | What It Does |
|--------|---------|-------------|
| Quick prep | `/prep [client]` | One-page briefing: status, stakeholders, recent activity, open loops, talking points |
| Deep discovery prep | `/research [client]` | Full 5-layer intelligence: vault + Knowledge Lake + Slack + web + stakeholders |
| Workshop prep | `/discover [client]` | Discovery-specific: questions, objections, reference materials |

**`/prep` is your most-used skill.** Run it before every external call. It reads the client hub, last 3-5 meetings, stakeholder notes, and open loops — then synthesizes a briefing. You walk into every call knowing exactly what was promised, what's outstanding, and what each person in the room cares about.

### During the Day — Capture Everything

- Quick thoughts → drop in your **capture Slack channel** (capture-keeper files them into the vault hourly) or type directly into today's daily note
- Meeting transcripts → paste into Claude Code and run `/meeting`
- Random captures → drop into `00-inbox/`
- Client updates → update the client hub file directly, or use `/client-status [client]`

**The capture-keeper agent** is the lowest-friction capture path. Send a voice memo or typed thought to your dedicated Slack channel — the agent files it into today's daily note with wikilinks to the right clients and people, and adds any to-dos to open-loops. No laptop needed.

**The `/meeting` skill is transformative.** Paste a transcript (or let it pull from Granola) and it:
- Creates a structured meeting note in the correct folder
- Resolves all attendees to wikilinked stakeholder pages
- Creates stub pages for anyone new
- Updates stakeholder histories
- Updates the client hub timeline
- Adds your action items to open-loops

One paste → five files updated → zero manual filing.

### End of Day (5 min) — Close the Loop

| Action | How | What It Does |
|--------|-----|-------------|
| Process captures | `/process-inbox` (manual) | Triages inbox, moves files to correct locations, extracts actions |
| Sync action items | **loop-keeper agent** (auto, nightly) or `/sync-actions` (manual) | Scans recent notes for tasks, updates open-loops dashboard |
| Reflect | `/eod` (manual) | Honest analysis: completion rate, meeting load, context switches, carryover |

**With agents**, the loop-keeper runs at 22:00 and handles open-loops maintenance automatically — extracting tasks, deduplicating, flagging overdue items. You still run `/eod` for the reflection (agents don't replace your thinking), and `/process-inbox` for any inbox files.

**`/eod` is your accountability partner.** It reads your daily note, calculates what actually happened vs. what you planned, flags drift from weekly priorities, and commits everything to git. It's brutally honest — "2/3 focus items done, but 4.5h in meetings across 6 contexts is why the proposal didn't happen."

---

## Weekly Workflow

### Weekly Review (20-30 min) — Patterns & Planning

| Action | How | When |
|--------|-----|------|
| Weekly review | **chief-of-staff** (auto, Fri 17:00) or `/weekly-review` (manual) | Friday afternoon |
| Weekly prep | **chief-of-staff** (auto, Sun 17:00) | Sunday evening |
| Account health sweep | **account-sentinel** (auto, Fri 16:00) or `/portfolio` (manual) | Friday |
| Opportunity scan | **opportunity-scout** (auto, Fri 15:00) | Friday |
| Research curation | **field-brief** (auto, Sun 20:00) | Sunday |
| Triage open-loops | `/triage` (manual) | During or after weekly review |
| Refresh client data | `/refresh light` (manual) | When hubs feel stale |
| Vault hygiene | `/clean-up` (manual) | Monthly, or when vault feels messy |

**With agents**, your Friday afternoon is packed with automated intelligence. At 15:00 the opportunity-scout finds reusable assets and cross-account patterns. At 16:00 the account-sentinel runs a RAG health check across every active account. At 17:00 the chief-of-staff writes your weekly review. On Sunday, the weekly prep drafts next week's focus and the field-brief surfaces 3 enterprise AI articles with ready-to-promote vault notes. All of this lands in `_current/agent-inbox.md` for your review.

**Without agents**, `/weekly-review` scans all 5 daily notes from the week, generates a summary (accomplishments, patterns, open items by client), and creates a review note. `/portfolio` gives you the RAG-rated dashboard manually.

**`/triage`** is interactive — it walks through open-loops and asks: keep, defer, drop, or delegate? This prevents the list from becoming a graveyard of stale items.

---

## Monthly & Quarterly

| Action | Command | When |
|--------|---------|------|
| Monthly review | `/monthly-review [month]` | Last day of month or first of next |
| Quarterly review | `/quarterly-review [quarter]` | End of quarter |
| Surface wins | `/wins [period]` | Before reviews, promotion cases, or morale boosts |
| Client retro | `/retro [client]` | After engagement completes or stalls |

**`/wins`** is underrated. It searches your entire vault for evidence of impact — deal progression, stakeholder feedback, delivered value, internal recognition. Before any performance conversation, run this and you'll have concrete evidence rather than fuzzy memories.

---

## Research & Intelligence

| Action | Command | When |
|--------|---------|------|
| Full client intelligence | `/research [client]` | Before new engagements, major milestones |
| Company research (web) | `/external-research` | When populating account briefs |
| Stakeholder deep-dive | `/stakeholder-research` | Before meeting a new executive |
| Cross-account patterns | `/pattern [use-case]` | "Where else have we done this?" |
| Refresh stale hubs | `/refresh full [client]` | Monthly, or for Red-rated clients |

**`/pattern`** is uniquely powerful. Ask "spare parts lookup" and it searches your vault, Knowledge Lake, and Slack to find every account where this use case has been discussed, delivered, or is active. You instantly know who to reference in your next positioning conversation.

**`/stakeholder-research`** builds a profile from public sources before you meet someone new — their career history, likely priorities, communication preferences. Walk into that first meeting already knowing what they care about.

---

## Manager Prep

| Action | Command | When |
|--------|---------|------|
| 1:1 prep | `/1-1` | Before your weekly 1:1 |

**`/1-1`** builds a complete briefing: portfolio status with momentum signals, workload data from your EOD reviews, open items from last 1:1, what your manager's been discussing in Slack, and career/initiative updates. Your 1:1 goes from "anything to discuss?" to a data-backed strategic conversation.

---

## How This Benefits Your Daily Role

### For AEs
- **Before calls:** `/prep` gives you full context without re-reading 20 emails
- **Deal strategy:** Hub files track hypotheses, stakeholder maps, and engagement timelines in one place
- **Forecasting:** `/portfolio` shows you which deals are accelerating vs. stalling
- **QBRs:** `/quarterly-review` generates your narrative from actual data

### For VEs / AVEs
- **Demo prep:** `/prep` + `/research` = walk in knowing the company, the people, and what's worked before
- **Cross-account leverage:** `/pattern` finds reference implementations across your portfolio
- **Hypothesis tracking:** Hub files capture what you're testing and what evidence you've gathered
- **PoV management:** Sub-project folders keep complex multi-track engagements organized

### For SEs
- **Technical context:** Meeting notes capture architectural decisions and integration requirements
- **Handoff quality:** The hub file IS the handoff — everything is already documented
- **Reference customers:** `/pattern` finds who's done what you're proposing

### For CSMs
- **Renewal prep:** Full engagement history in one file — no archaeology needed
- **Health monitoring:** `/portfolio` with staleness detection catches disengaging clients
- **Expansion signals:** Meeting notes and stakeholder pages surface new opportunities
- **Value documentation:** `/wins` pulls evidence of delivered outcomes

### For BDRs
- **Research efficiency:** `/external-research` + `/stakeholder-research` builds prospecting context in minutes
- **Pattern matching:** `/pattern` tells you which accounts match successful deal profiles
- **Handoff documentation:** Everything you learn goes into the hub — AE gets full context from day one

---

## The Compound Effect

| Week | What Changes |
|------|-------------|
| 1 | Feels like overhead. You're creating notes nobody reads yet. |
| 2 | You find something from last week faster than searching Slack. |
| 4 | Pre-call prep takes 2 minutes instead of 15. You never ask "what did we discuss?" |
| 8 | Cross-account patterns emerge. You start referencing one client's win at another. |
| 12 | Weekly reviews surface themes invisible in the daily grind. Agents running in shadow. |
| 16 | Agents go live. Morning briefing, account monitoring, and research happen without you. |
| 20 | Account-watch catches a profit warning before the AE sees it. Opportunity-scout drafts a reusable asset. |
| 26 | Genuine knowledge graph + autonomous monitoring. Months of context in seconds, nothing slips. |

The system compounds in two ways. First, every note makes every future query richer — the 100th meeting processed makes the 101st prep briefing better. Second, the agents get smarter as the vault grows — more context means better signals, fewer false positives, more relevant opportunities surfaced.

---

## The Agent System

The agent system is the second layer of the Second Brain. While skills are manual (you invoke them), agents run autonomously on schedules and surface their findings through the agent inbox.

### How It Works

1. Agents run on cron schedules via Claude Code scheduled tasks
2. Every run follows a safety protocol: `guard.py start` → work → critic QA → `guard.py finish` → Slack post
3. The **critic** subagent runs 7 independent checks on every agent's output before it can commit
4. **Shadow mode** means agents write only to their own folder — nothing touches the vault until you switch to live
5. Agents propose actions through `_current/agent-inbox.md` — you ✅ or ❌ each one
6. **Chief-of-staff** carries out your ✅'d decisions each morning

### The Three Tiers

Enable progressively. Each tier adds MCP integrations and new capabilities.

**Tier 1 — Foundation** (vault + Google Calendar)

| Agent | Schedule | What It Does |
|-------|----------|--------------|
| **chief-of-staff** | Daily 06:30, Fri 17:00, Sun 17:00 | Morning briefing with per-meeting prep, inbox management, weekly review and planning |
| **loop-keeper** | Nightly 22:00 | Open-loops maintenance: extracts tasks from recent notes, dedupes, flags overdue |
| **prep** | _(subagent)_ | Per-meeting briefing from vault + Knowledge Lake context |
| **critic** | _(subagent)_ | 7-check QA on every agent run |

**Tier 2 — Signal Intelligence** (+ Gmail, Slack, Knowledge Lake)

| Agent | Schedule | What It Does |
|-------|----------|--------------|
| **ingestor** | Twice daily | Scans Gmail + Slack per account, writes one signal line per account per day to your daily note |
| **account-sentinel** | Friday 16:00 | RAG early-warning across all active accounts: quiet accounts, hub drift, overdue clusters, stakeholder silence |
| **opportunity-scout** | Friday 15:00 | Finds reusable assets, cross-account patterns, repeated objections, career evidence gaps — with first drafts |
| **capture-keeper** | Hourly 08–20 | Files your Slack captures (voice memos, quick thoughts) into the vault with links and actions |

**Tier 3 — External Research** (+ WebSearch, WebFetch)

| Agent | Schedule | What It Does |
|-------|----------|--------------|
| **field-brief** | Sunday 20:00 | Curates 3 enterprise AI articles per week with draft vault notes ready to promote |
| **account-watch** | Mon/Wed/Fri 05:45 | Monitors public sources (filings, press, vendors, jobs) for every active account across your regions |

### The Agent Inbox

`_current/agent-inbox.md` is your cockpit. Each entry tells you:
- What the agent did or found
- Why it matters (linked to your current priorities)
- Risk and how to undo
- Options with exactly what happens on ✅
- Your verdict: ✅ or ❌ with a reason

Chief-of-staff enforces a 5-item cap in `## Today`. Excess items fold to `## Below the fold`. Check it each morning — it takes 2 minutes.

### Skills vs. Agents

Skills and agents coexist. The agent automates what the skill does manually. Keep the skill for ad-hoc use.

| Skill | Agent | Relationship |
|-------|-------|-------------|
| `/morning` | chief-of-staff (daily) | Agent runs it automatically at 06:30. Skill stays for manual "run it now". |
| `/prep [client]` | prep (subagent) | Agent runs prep per meeting. Skill stays for ad-hoc prep. |
| `/weekly-review` | chief-of-staff (Fri/Sun) | Agent automates the review. Skill stays for manual runs. |
| `/sync-actions` | loop-keeper | Loop-keeper is a superset. Skill stays for quick manual syncs. |
| `/portfolio` | account-sentinel | Sentinel adds Gmail/Slack data. Skill stays for quick manual checks. |
| `/external-research` | account-watch | Skill is one-shot deep research. Agent is continuous monitoring. Complementary. |
| `/pattern` | opportunity-scout | Scout finds patterns autonomously. Skill stays for manual matching. |

### Getting Started with Agents

See `_agents/README.md` for the full setup guide. The short version:

1. Use skills only for 1–2 weeks to build the vault habit
2. Copy `_agents/config-template.yaml` → `_agents/config.yaml`, fill in your details
3. Start Tier 1 agents in shadow mode — review their shadow output
4. When shadow output looks good, switch to live — one tier at a time
5. Enable Tier 2 when you have Gmail + Slack + Knowledge Lake MCP
6. Enable Tier 3 when you have WebSearch + WebFetch MCP

---

## Quick Reference — All Skills

| Skill | Command | Arguments | When to Use |
|-------|---------|-----------|-------------|
| Morning Kickstart | `/morning` | `[YYYY-MM-DD]` | Opening laptop, start of day |
| Daily Note | `/daily` | `[YYYY-MM-DD]` | Each morning (auto-called by /morning) |
| Client Prep | `/prep` | `[client-name]` | Before every client call |
| Meeting Process | `/meeting` | `[client or date]` | After every meeting (paste transcript) |
| End of Day | `/eod` | — | Before closing laptop |
| Process Inbox | `/process-inbox` | — | End of day, or when inbox accumulates |
| Sync Actions | `/sync-actions` | — | End of day |
| Weekly Review | `/weekly-review` | — | Friday/Sunday |
| Monthly Review | `/monthly-review` | `[month year]` | End of month |
| Quarterly Review | `/quarterly-review` | `[Q#-YYYY]` | End of quarter |
| Portfolio Health | `/portfolio` | — | Weekly, before manager meetings |
| Triage | `/triage` | — | Weekly, when open-loops is cluttered |
| Refresh | `/refresh` | `[light\|full] [client]` | Weekly (light), monthly (full) |
| Clean-up | `/clean-up` | — | Monthly vault hygiene |
| Full Research | `/research` | `[client-name]` | Before new engagements |
| External Research | `/external-research` | — | Populating account briefs |
| Stakeholder Research | `/stakeholder-research` | — | Before meeting new stakeholders |
| Pattern Match | `/pattern` | `[use-case or client]` | "Where else have we done this?" |
| 1:1 Prep | `/1-1` | — | Before manager 1:1 |
| Wins | `/wins` | `[time period]` | Before reviews, promotion cases |
| Retro | `/retro` | `[client-name]` | After engagements complete |
| Skill Creator | `/skill-creator` | — | When creating new skills |

---

## Tips for Success

1. **Start with just `/daily` and `/meeting`.** These two skills alone transform your workflow. Add others as you build the habit. Agents come later.

2. **Don't organise at point of capture.** Dump everything into `00-inbox/`, your daily note, or your Slack capture channel. Let `/process-inbox` and the capture-keeper handle the filing. Your job is to capture, not categorise.

3. **The hub file is sacred.** After every client interaction, the hub should reflect reality. This is what makes `/prep` magic and what makes the agents accurate — they all read from a single source of truth.

4. **Run `/eod` honestly.** It only works if your daily note reflects what actually happened. 2/3 focus items is more useful data than a polished lie.

5. **Weekly review is non-negotiable.** Skip daily notes occasionally — fine. Skip the weekly review and the system dies within a month. With agents, the chief-of-staff drafts it for you — but you still need to read it and think.

6. **Use `/pattern` aggressively.** The cross-account intelligence is the biggest unlock vs. working in isolation. "We did this at [Company A]" is the most powerful sentence in enterprise sales. The opportunity-scout automates this weekly.

7. **Commit to git daily.** The `/eod` skill does this automatically. Agents also commit through `guard.py` on every run.

8. **Trust shadow mode.** When enabling agents, run them in shadow for at least a week. Review the shadow output, ❌ anything wrong with a reason — the agent reads your reasons and adjusts. This is how you calibrate the system to your portfolio.

9. **Check the agent inbox each morning.** It takes 2 minutes. Your ✅/❌ decisions are carried out by chief-of-staff. Ignoring it defeats the purpose — agents propose, you decide.

10. **Fill in the hub frontmatter.** `email_domains`, `slack_channels`, `region`, `involvement` — these fields are what make agents work. Without them, agents can't find your clients' emails, Slack activity, or public filings.
