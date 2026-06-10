# User Guide — Celonis GTM Second Brain

## What This Is

This is an Obsidian vault + Claude Code system designed for Celonis GTM professionals. It acts as your second brain — storing everything you know about clients, stakeholders, meetings, and your own career progression in a structured, searchable, AI-augmented knowledge graph.

**Who it's for:** AEs, AVEs, VEs, SEs, CSMs, BDRs — anyone in the Celonis GTM motion who manages client relationships and needs to carry context across dozens of accounts and hundreds of meetings.

**What it replaces:** Scattered notes in OneNote/Google Docs, lost Slack context, pre-call scrambles asking "what did we discuss last time?", forgotten action items, and the recurring feeling that you know things but can't find them when you need them.

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
Run `/new-client [client-name]` in Claude Code. This creates the folder structure and hub file. Populate the hub with what you already know.

---

## Daily Workflow

### Morning (5 min) — Get Oriented

| Action | Command | What It Does |
|--------|---------|-------------|
| Full morning briefing | `/morning` | Creates daily note, pulls calendar, surfaces per-meeting context, flags emails |
| Just the daily note | `/daily` | Creates today's note from template with your 3 focus items |

**The `/morning` command is your single entry point.** It chains together: daily note creation → calendar scan → per-meeting vault context → Gmail flags → open-loops due today. You open your laptop, run one command, and know exactly what your day looks like.

### Before Every Client Call (2 min) — Get Briefed

| Action | Command | What It Does |
|--------|---------|-------------|
| Quick prep | `/prep [client]` | One-page briefing: status, stakeholders, recent activity, open loops, talking points |
| Deep discovery prep | `/research [client]` | Full 5-layer intelligence: vault + Knowledge Lake + Slack + web + stakeholders |
| Workshop prep | `/discover [client]` | Discovery-specific: questions, objections, reference materials |

**`/prep` is your most-used skill.** Run it before every external call. It reads the client hub, last 3-5 meetings, stakeholder notes, and open loops — then synthesizes a briefing. You walk into every call knowing exactly what was promised, what's outstanding, and what each person in the room cares about.

### During the Day — Capture Everything

- Quick thoughts → type directly into today's daily note
- Meeting transcripts → paste into Claude Code and run `/meeting`
- Random captures → drop into `00-inbox/`
- Client updates → update the client hub file directly, or use `/client-status [client]`

**The `/meeting` skill is transformative.** Paste a transcript (or let it pull from Granola) and it:
- Creates a structured meeting note in the correct folder
- Resolves all attendees to wikilinked stakeholder pages
- Creates stub pages for anyone new
- Updates stakeholder histories
- Updates the client hub timeline
- Adds your action items to open-loops

One paste → five files updated → zero manual filing.

### End of Day (5 min) — Close the Loop

| Action | Command | What It Does |
|--------|---------|-------------|
| Process captures | `/process-inbox` | Triages inbox, moves files to correct locations, extracts actions |
| Sync action items | `/sync-actions` | Scans recent notes for tasks, updates open-loops dashboard |
| Reflect | `/eod` | Honest analysis: completion rate, meeting load, context switches, carryover |

**`/eod` is your accountability partner.** It reads your daily note, calculates what actually happened vs. what you planned, flags drift from weekly priorities, and commits everything to git. It's brutally honest — "2/3 focus items done, but 4.5h in meetings across 6 contexts is why the proposal didn't happen."

---

## Weekly Workflow

### Weekly Review (20-30 min) — Patterns & Planning

| Action | Command | When |
|--------|---------|------|
| Weekly review | `/weekly-review` | Friday afternoon or Sunday evening |
| Portfolio health | `/portfolio` | Before manager meetings or weekly planning |
| Triage open-loops | `/triage` | During or after weekly review |
| Refresh client data | `/refresh light` | During weekly review when hubs feel stale |
| Vault hygiene | `/clean-up` | Monthly, or when vault feels messy |

**`/weekly-review`** scans all 5 daily notes from the week, generates a summary (accomplishments, patterns, open items by client), and creates a review note. This is where you spot themes you'd otherwise miss.

**`/portfolio`** gives you a RAG-rated dashboard of every active client — momentum signal, overdue items, days since last touch. Perfect for preparing 1:1s or identifying accounts that are silently going cold.

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
| 12 | Weekly reviews surface themes invisible in the daily grind. Your 1:1s become strategic. |
| 26 | You have a genuine knowledge graph. Claude traverses months of context in seconds. |

The system compounds. Every meeting note, every stakeholder update, every daily reflection makes every future query richer. The 100th meeting you process makes the 101st prep briefing better than any system you've used before.

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

1. **Start with just `/daily` and `/meeting`.** These two skills alone transform your workflow. Add others as you build the habit.

2. **Don't organise at point of capture.** Dump everything into `00-inbox/` or your daily note. Let `/process-inbox` handle the filing. Your job is to capture, not categorise.

3. **The hub file is sacred.** After every client interaction, the hub should reflect reality. This is what makes `/prep` magic — it reads from a single source of truth.

4. **Run `/eod` honestly.** It only works if your daily note reflects what actually happened. 2/3 focus items is more useful data than a polished lie.

5. **Weekly review is non-negotiable.** Skip daily notes occasionally — fine. Skip the weekly review and the system dies within a month. It's where patterns become visible and priorities get reset.

6. **Use `/pattern` aggressively.** The cross-account intelligence is the biggest unlock vs. working in isolation. "We did this at [Company A]" is the most powerful sentence in enterprise sales.

7. **Commit to git daily.** The `/eod` skill does this automatically. Your vault is version-controlled, searchable, and backed up.
