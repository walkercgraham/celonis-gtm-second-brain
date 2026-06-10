---
type: resource
tags: [tools, claude-code, skills]
created: 2026-04-23
modified: 2026-04-23
status: active
related:
  - "[[skill-creator]]"
---

# Skill Ideas

## Build Queue (Priority Order)

### 1. Granola Ingestion `/granola` — HIGH ROI
Granola MCP already configured (`mcp__claude_ai_Granola__*`). Eliminates manual paste-and-clean workflow.
- Query today's meetings via `get_meetings`
- Pull transcripts via `get_meeting_transcript`
- Format into vault meeting notes with frontmatter, wikilinks, extracted action items
- Route to correct client folder automatically

**Build this first.**

---

### 2. Calendar → Daily Note Pre-population
Google Calendar MCP already available (`mcp__claude_ai_Google_Calendar__*`). Upgrade to existing `/daily` skill, not a separate skill.
- Pull today's events and pre-populate Log section with times + meeting names
- Create wikilinks to existing meeting notes or stubs for new ones
- Flag back-to-back blocks or conflicts
- Surface open-loops due today

---

### 3. Account & Stakeholder Research `/research [client|person]`
Goes outward where `/prep` stays vault-only. Uses WebSearch + WebFetch.
- Pull LinkedIn, company news, recent filings, trigger events
- Write structured output into `[client]/stakeholders/[person].md`
- Refresh stale stakeholder notes on demand before big meetings

---

### 4. `/before-call [client]` — 60-Second Pre-Call Flash
Distinct from `/prep` (which is deep, 10+ min output). This is a 30-second brief designed to run while walking to your desk.
- Who's on the call
- What they last said
- What you owe them
- One thing to say
- Vault-only, no research

---

### 5. Slack Context → `/prep` Enhancement
Slack MCP exists but needs auth. Don't build standalone — wire into `/prep [client]` as optional step.
- Pull last 7 days of messages in client's Slack channel
- Surface blockers, decisions, tone shifts not captured in meeting notes
- Situational value, high setup friction

---

## Other Ideas

### `/capture [text]` — Quick Capture
Append timestamped item to today's daily note, tagged for EOD processing. Reduces friction during back-to-back meetings.

### `/client-health` — Portfolio RAG Dashboard
One-screen red/amber/green table across all active clients. Scans hub files + last meeting note per client. Useful before weekly review or manager 1-1. No narrative — just signal.

---

## Already Built (Reference)

| Skill | Purpose |
|---|---|
| `/daily` | Create daily note from template |
| `/eod` | End-of-day reflection + action sync |
| `/prep [client]` | Pre-call briefing from vault |
| `/process-inbox` | Triage and route 00-inbox/ |
| `/sync-actions` | Sync tasks to open-loops |
| `/weekly-review` | 7-day analysis and planning |
| `/clean-up` | Vault hygiene sweep |
| `/wins` | Surface wins by time period |
| `/retro` | Post-engagement retrospective |
| `/quarterly-review` | Career trajectory zoom-out |
