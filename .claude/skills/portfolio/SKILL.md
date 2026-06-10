---
name: portfolio
description: Client health dashboard. Scans all client hubs, assigns RAG ratings, distinguishes active engagements from context holders. Updates active-clients.md. Run weekly or before manager meetings.
---

# Portfolio Health Dashboard

Generate a portfolio-wide view distinguishing active engagements from context-holder accounts. Updates `_current/active-clients.md` with current data.

## Steps

### Step 1: Scan All Client Folders

1. List all folders in `02-areas/celonis/` (excluding `_internal/`)
2. For each client folder, read the hub file (`[client]/[client].md`)
3. Extract from frontmatter and content:
   - `status` field (active, paused, complete, archived)
   - `stage` field (discovery, pov, delivery, expansion)
   - Current status narrative (first paragraph or "Status" section)
   - Last modified date of the hub file
   - Count of meeting notes in `meetings/` folder
   - Date of most recent meeting note

### Step 2: Classify Accounts

**Active Engagement** — meets ANY of:
- Hub `status: active` AND meeting note within last 21 days
- Mentioned in `_current/this-week.md`
- Has items in `_current/open-loops.md` with due dates this month

**Context Holder** — ALL of:
- No meeting notes in last 30 days (or zero meeting notes ever)
- Not mentioned in `this-week.md`
- No active open-loop items with near-term due dates
- Hub contains useful context (hypotheses, stakeholders, pain points from AE handoff)

**Inactive / Stub** — ALL of:
- Hub has minimal content (<500 chars body text)
- No stakeholder pages
- No meeting notes
- No open-loop items

### Step 3: Assess Active Engagements

For each active engagement:

1. **Last touch:** Date of most recent meeting note or hub modification
2. **Open items:**
   - Count from `open-loops.md` tagged `#client/[name]`
   - Split: ours (unchecked) vs. waiting-on (tagged `#waiting-on`)
   - Any overdue? (due date < today)
3. **Momentum signal:**
   - **Accelerating:** Meeting within 3 days + deliverables progressing + stakeholder engagement increasing
   - **Steady:** Regular cadence (7-14 day meeting rhythm), no blockers
   - **Stalled:** 14+ days since last meeting OR overdue items piling up (3+)
   - **Risk:** Explicit blocker in hub, competitive threat noted, or stakeholder disengagement
4. **Stage progression:** Has stage changed recently? (e.g., discovery → pov)

### Step 4: Assess Context Holders

For each context holder:

1. **Use case opportunities:** Extract hypotheses or pain points from hub
2. **Readiness signal:**
   - **Warm:** Has stakeholder pages + specific pain points documented + AE actively working
   - **Cold:** Minimal content, no recent AE activity, placeholder only
3. **Pattern match potential:** What use cases from `_moc-ai-use-cases.md` apply?

### Step 5: Update active-clients.md

Rewrite `_current/active-clients.md` with current data:

```markdown
---
type: area
tags: [dashboard, celonis]
modified: YYYY-MM-DD
---

# Active Clients

Last updated: YYYY-MM-DD (via /portfolio)

## Active Engagements

| Client | Stage | Last Touch | Momentum | Open Items | Notes |
|--------|-------|-----------|----------|------------|-------|
| [[client]] | [stage] | [date] | [signal] | [X ours / Y waiting] | [1-line status] |

## Context Holders (Pre-Engagement Intelligence)

| Client | Industry | Key Opportunities | Readiness | Pattern Match |
|--------|----------|-------------------|-----------|---------------|
| [[client]] | [industry] | [top use case opportunities] | [warm/cold] | [related MOC categories] |

## Recently Completed / Archived
| Client | Outcome | Archived |
|--------|---------|----------|
| [if any] | [result] | [date] |

## Portfolio Summary
- **Active engagements:** [count]
- **Context holders:** [count]
- **Stalled/Risk:** [list names]
- **Recently touched (this week):** [list names]
```

### Step 6: Present Summary to Screen

```markdown
## Portfolio Health — [Date]

### Active ([count])
| Client | Stage | Momentum | Action Needed? |
|--------|-------|----------|---------------|
| ... | ... | [GREEN/AMBER/RED] | [Y/N — what] |

### Attention Required
- **[Client]** — [reason: stalled 14d, 5 overdue items, competitive threat, etc.]

### Context Holders with Opportunity ([count])
| Client | Top Use Case | Readiness |
|--------|-------------|-----------|
| ... | ... | warm/cold |

### Suggested Actions
1. [Most urgent intervention — e.g. "Schedule catch-up with [client] AE — 14 days since last touch"]
2. [Second]
3. [Third]
```

## Quality Rules

1. **Never flag context holders as problems** — they're intelligence assets, not neglected accounts
2. **Momentum must be evidence-based** — "Stalled" means actual data (no meetings + overdue items), not vibes
3. **Update the file, don't just present** — this skill MUST write to `_current/active-clients.md`
4. **Preserve wikilinks** — all client names should be `[[client-name]]` format
5. **Be honest about gaps** — if a hub file is stale or minimal, say so rather than inventing a status
