---
name: refresh
description: Systematic hub content refresh across all active clients. Detects staleness, ingests new signals (Slack, Knowledge Lake, web), and updates or flags hub sections. Light mode (vault + Slack + KL) for weekly use; full mode (adds web research) for monthly. Run after /portfolio, during weekly review, or when multiple hubs feel outdated.
argument-hint: "[light|full] [optional: client-name]"
---

# Portfolio Content Refresh

Scan all active client hubs for staleness, ingest new signals from Slack / Knowledge Lake / web, and either auto-update safe fields or flag issues for review.

## Modes

| Mode | Scope | Data Sources | When |
|------|-------|-------------|------|
| `light` (default) | Vault + Slack + KL | File reads, Slack search, Knowledge Lake | Weekly |
| `full` | Light + web research | Adds DuckDuckGo searches per stale client | Monthly |

Single-client override: `/refresh full [client-name]` runs full pipeline for one client only.

## Phase 0: Scope Resolution

1. Parse `$ARGUMENTS`:
   - First word: `light` or `full` (default: `light`)
   - Remaining words: optional client name filter
2. Read `_current/active-clients.md` — extract client names from the table
3. If single-client specified, filter to that client only
4. Set today's date for staleness calculations

## Phase 1: Staleness Audit

For each active client (parallelizable — all file reads):

### 1.1 Read Hub File

Read `02-areas/celonis/[client]/[client].md`. Extract:
- `modified` date from frontmatter
- Most recent date mentioned in `## Engagement Timeline` (or equivalent chronological section)
- All unchecked action items (`- [ ]`) with `#due/` dates
- Split actions into "Ours" vs "Theirs" based on section headers
- Active hypotheses and their last-mentioned dates

### 1.2 Read Latest Meeting Note

List files in `02-areas/celonis/[client]/meetings/` (and any sub-project `meetings/` folders). Find most recent by filename date prefix.

### 1.3 Calculate Staleness

```
days_since_last_meeting = today - most_recent_meeting_date
days_since_hub_modified = today - frontmatter_modified_date
overdue_actions = count of items where #due/date < today
status_narrative_age = days since most recent date referenced in Current Status section
```

### 1.4 Assign Rating

Read thresholds from `references/staleness-thresholds.md`. Default:

| Rating | Criteria (ANY triggers) |
|--------|------------------------|
| **Fresh** (Green) | Meeting ≤7d AND hub modified ≤7d AND <2 overdue |
| **Aging** (Amber) | Meeting 8-14d, OR 3-5 overdue, OR hub modified 14-21d |
| **Stale** (Red) | Meeting 15+d, OR 6+ overdue, OR status narrative 21+d old |

## Phase 2: Signal Ingestion

**Only for Amber/Red clients** (skip Fresh clients to save API calls).  
Exception: single-client mode always proceeds regardless of rating.

### 2A: Slack Signal Scan (Both Modes)

For each qualifying client:

```
slack_search_public_and_private(
  query: "[client name]",
  sort: "timestamp",
  sort_dir: "desc",
  limit: 10
)
```

Also search common aliases (e.g., "AZ" for [Company A], "[Company B]" for [Company B]).

**Filter results:**
- Only keep messages NEWER than hub's last timeline entry
- Discard pure logistics ("can you join?", "running 5 min late")
- Keep: deal updates, meeting confirmations, deliverable progress, escalations, new stakeholder mentions

**Per result, determine:** Is this signal already reflected in the hub?

### 2B: Knowledge Lake Scan (Both Modes)

For each qualifying client, run 2 searches:

```
search_knowledge(
  query: "[client name] [industry]",
  topics: ["cortex_internal", "cortex_external"],
  top_n: 5
)
```

```
search_knowledge(
  query: "[active hypothesis keywords] [process area]",
  topics: ["ve", "cs"],
  top_n: 3
)
```

**Extract:**
- New reference customers in same industry (not already in hub)
- New assets/demos relevant to active hypotheses
- Prior engagement data missing from hub

### 2C: External Web Research (FULL MODE ONLY)

For each qualifying client, run 3 targeted DuckDuckGo searches:

```
WebFetch:
  url: "https://html.duckduckgo.com/html/?q=[Company]+news+[current year]"
  prompt: "Extract news headlines, dates, and summaries. Focus on: leadership changes, M&A, partnerships, restructuring, earnings."
```

```
WebFetch:
  url: "https://html.duckduckgo.com/html/?q=[Company]+earnings+OR+results+[recent quarter]"
  prompt: "Extract financial headlines, revenue figures, growth metrics, strategic commentary."
```

```
WebFetch:
  url: "https://html.duckduckgo.com/html/?q=[Company]+digital+transformation+OR+AI+[current year]"
  prompt: "Extract technology initiatives, platform announcements, AI strategy signals."
```

**Cap:** 5 web fetches per client maximum. Follow top 1-2 links only if snippets are insufficient.

**Extract:**
- Trigger events with dates (M&A, earnings, leadership, regulatory)
- Technology signal changes (new platform, cloud migration)
- Stakeholder movements (new roles, departures)

## Phase 3: Gap Analysis

For each client with signals found, compare against hub content:

| Gap Type | Detection | Classification |
|----------|-----------|----------------|
| Timeline gap | Slack activity with no corresponding hub timeline entry | Auto-update |
| New stakeholder | Person mentioned in Slack/meetings not in stakeholder table | Auto-update |
| Action complete | Item confirmed done in meeting/Slack | Auto-update |
| Overdue flagging | Action item past due date, no `#overdue` tag | Auto-update |
| Status drift | Current Status references dates 21+d old, newer signals exist | Flag |
| Hypothesis stale | No evidence/activity for 30+ days | Flag |
| Contradiction | Slack says "paused" but hub says "active" (or similar) | Flag (prominent) |
| Stage change | Evidence suggests stage has progressed (discovery → pov) | Flag |
| Research stale | Trigger events in last 60d not in Research & Context | Flag (light) / Append (full) |

## Phase 4: Output

### 4A: Auto-Updates (Apply Directly)

Rules for safe auto-updates:
- **Timeline entries:** Append new dated entry below most recent. Format: `- **[Date]** — [Summary] *(Source: Slack #channel, [date])*`
- **Stakeholder rows:** Append to table with name + role (leave Notes sparse for [user] to fill)
- **Action completion:** Change `- [ ]` to `- [x]` with `*(confirmed [date], Source: [channel/meeting])*`
- **Overdue tags:** Append `#overdue` to items past due date
- **Modified date:** Update frontmatter `modified:` to today

**NEVER auto-update:**
- Current Status narrative
- Hypothesis status fields
- Stage or status frontmatter
- Research & Context prose
- Any removal of existing content

### 4B: Screen Report

Present to [user]:

```markdown
## Portfolio Refresh — [Date] ([Light/Full] Mode)

### Staleness Overview
| Client | Rating | Last Meeting | Overdue | Signals Found |
|--------|--------|-------------|---------|---------------|
| [[client]] | Green/Amber/Red | [date] | [count] | [count] |

### Auto-Applied Updates
- **[[client]]:** [what was updated] *(Source: [source])*

### Flags for Review
#### [[client]] — [flag type]
**Current hub says:** [excerpt]  
**New signal suggests:** [what changed]  
**Recommendation:** [specific action]

### Hypothesis Health
| Client | Hypothesis | Last Evidence | Days Silent | Recommendation |
|--------|-----------|---------------|-------------|----------------|

### New Intelligence (Not Yet in Hubs)
#### [[client]]
- **[Source type] ([date]):** [signal summary]

### Suggested Next Steps
1. [Most urgent — e.g., "Update [[edf]] status: no activity 25 days, consider pausing"]
2. [Second]
3. [Third]
```

### 4C: Footer Update

Append to `_current/active-clients.md`:
```
Last refreshed: [date] ([light/full])
```

## Quality Rules

1. **Append-only safety.** Never overwrite existing prose. New data is appended; existing content is preserved.
2. **Source everything.** Every auto-appended entry includes `(Source: [type] #[channel/URL], [date])`.
3. **Data-driven staleness.** Ratings come from measurable signals (days, counts), never vibes.
4. **Signal over noise.** Discard Slack logistics, irrelevant KL results, web results that confirm what hub already says. Only surface signals that ADD information.
5. **Preserve wikilinks.** All client names as `[[client]]`, all stakeholders as `[[stakeholder-name]]`.
6. **No hallucinated updates.** If sources return nothing new, say so. "No new signals" is valid output.
7. **Contradiction priority.** If any signal contradicts the hub, flag it PROMINENTLY at top of report.
8. **Progressive depth.** Fresh = skip Phase 2. Amber = Slack + KL. Red = Slack + KL + web (in full mode).
9. **Frontmatter hygiene.** Always update `modified:` when changing hub content.
10. **Escalation path.** If a Red client has zero signals even after full mode, recommend running `/research [client]` for deep investigation.

## Integration

| Direction | Skill | How |
|-----------|-------|-----|
| Reads from | `/portfolio` | Client list from `active-clients.md` |
| Reads from | `/external-research` | Web search methodology (DuckDuckGo patterns) |
| Feeds into | `/prep` | Freshened hubs make prep more accurate |
| Feeds into | `/weekly-review` | Staleness data informs weekly priorities |
| Escalates to | `/research [client]` | When Red + zero signals = needs deep discovery |
