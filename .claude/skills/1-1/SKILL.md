---
name: 1-1
description: Manager 1:1 prep. Builds portfolio status + workload data + career items into a layered briefing. Surfaces open items from last 1:1 and checks Slack for what's on your manager's radar.
---

# 1:1 Prep — Manager

Build a structured briefing for the weekly 1:1 covering three layers: portfolio status, workload health, and career progression. Ensures data-backed conversations and surfaces escalations that might otherwise be forgotten.

## Steps

### Step 1: Find Last 1:1 Note

1. Search `02-areas/celonis/_internal/meetings/` for the most recent file matching `*1-1*` or `*[manager-name]*`
2. Read it and extract:
   - Action items assigned to you (still open?)
   - Action items assigned to your manager (delivered?)
   - Decisions made that have time-bounds
   - Topics your manager raised (indicates what's on their mind)

### Step 2: Portfolio Status

1. Read `_current/active-clients.md` for the client list and current status
2. For each active client, read the hub file (`02-areas/celonis/[client]/[client].md`):
   - Extract: current status line, stage, last activity date
3. Read `_current/open-loops.md` and count items per client:
   - Items tagged `#action-required` (ours)
   - Items tagged `#waiting-on` (theirs)
   - Any items overdue by 7+ days
4. Determine momentum signal for each:
   - **Accelerating:** Recent meetings + progress on deliverables
   - **Steady:** Regular cadence, no blockers
   - **Stalled:** No meeting notes in 14+ days, or overdue items piling up
   - **Risk:** Explicit blockers, stakeholder disengagement, or competitive threat noted in hub

5. For each client, determine "Raise?" — yes if:
   - Risk or stalled momentum
   - Resource/capacity constraint blocking progress
   - Strategic decision needed from manager
   - Win worth sharing (visibility)

### Step 3: Workload Data

1. Read the last 5-7 EOD review files from `02-areas/celonis/_internal/reviews/`:
   - Files matching `YYYY-MM-DD-eod.md` or similar pattern, sorted by date desc
2. Extract from each:
   - Meeting hours
   - Focus item completion (X/Y)
   - Context switches
   - Any patterns or flags noted
3. Calculate averages:
   - Avg meeting hours per day
   - Avg completion rate
   - Trend: improving, stable, or declining
4. Read `_current/this-week.md` for:
   - Planned focus items vs. actual (if assessable)
   - Any explicit capacity concerns noted

5. Determine escalation:
   - **Yes** if: avg meeting hours >4h/day, completion rate <50%, or pattern of >12h days
   - Include specific data points to back up the escalation

### Step 4: Slack — What's on Manager's Radar

Search Slack for recent threads involving your manager that mention your clients or relevant topics:

```
slack_search_public_and_private(
  query: "from:[manager-name]",
  sort: "timestamp",
  sort_dir: "desc",
  limit: 10
)
```

Also search for threads mentioning your active clients in channels your manager frequents:

```
slack_search_public_and_private(
  query: "[top 3 client names] after:[7 days ago YYYY-MM-DD]",
  sort: "timestamp",
  sort_dir: "desc",
  limit: 10
)
```

Extract: topics your manager is discussing, clients they're asking about, any flags or escalations they've raised.

### Step 5: Career / Initiatives

1. Read career docs in `02-areas/celonis/_internal/career/`:
   - Current criteria gaps
   - Recent evidence added
2. Check initiative status:
   - Search `02-areas/celonis/_internal/initiatives/` for active initiatives
   - Read most recent meeting note in each
3. Read the most recent weekly or monthly review for:
   - Wins captured this period
   - Skills or visibility gaps noted

### Step 6: Build Output

```markdown
## 1:1 Prep — [Manager Name] | [Today's Date]

### Portfolio (sorted by urgency — risks first)
| Client | Stage | Momentum | Open Items | Raise? |
|--------|-------|----------|------------|--------|
| [name] | [stage] | [signal] | [X ours / Y waiting] | [Y/N + 1-line why] |

### Workload (last 7 days)
- **Meeting hours:** Xh avg/day (Yh total / Z days)
- **Focus completion:** X/Y items (Z%)
- **Context switches:** X avg/day
- **Trend:** [improving/stable/declining]
- **Escalation needed?** [Yes — data: ... / No — sustainable]

### From Last 1:1 ([date])
- **Open items (mine):** [list anything still pending]
- **Open items (manager):** [list anything they committed to]
- **Decisions to revisit:** [any time-bound decisions expiring]

### On Manager's Radar (Slack)
- [Thread/topic — context]
- [or "No relevant Slack activity found"]

### Career / Initiatives
- **[Initiative 1]:** [status + next milestone]
- **[Initiative 2]:** [status]
- **Promotion evidence this period:** [wins, if any]
- **Gap to address:** [from career docs]

### Suggested Agenda (5 items max, urgency-sorted)
1. [Most urgent — typically risk/escalation]
2. [Second]
3. [Third]
4. [Win to share — visibility]
5. [Career item — if space]
```

## Output

Present the briefing to screen. Do NOT save to a file unless asked.

## Quality Rules

1. Portfolio table must reflect CURRENT reality — if `active-clients.md` is stale, read individual hub files directly
2. Workload data must include specific numbers, not vibes — "4.2h avg meetings" not "lots of meetings"
3. Escalation recommendation must be backed by data — quote the specific numbers or patterns
4. Suggested agenda must be sorted by urgency, not alphabetically
5. If no EOD reviews found in the last 7 days, note the gap and use daily notes as fallback
