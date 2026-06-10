---
name: prep
description: Prepare briefing for a client call. Gathers context, stakeholders, recent activity, open items
argument-hint: "[client-name]"
---

# Client Prep Briefing

Gather context for **$ARGUMENTS** and synthesize a call prep briefing.

## Steps

1. Find the client folder at `02-areas/celonis/$ARGUMENTS/`
   - If not found, try common variations (lowercase, hyphenated)
   - If still not found, report error and suggest running `/new-client`

2. Read the client hub file `$ARGUMENTS/$ARGUMENTS.md`:
   - Current status
   - Stakeholders table
   - Active hypotheses
   - Key wins & learnings
   - Open action items (ours and theirs)

3. Read stakeholder notes from `$ARGUMENTS/stakeholders/`:
   - For each stakeholder, note their role and what they care about

4. Read the last 3-5 meeting notes from `$ARGUMENTS/meetings/`:
   - Sort by date (most recent first)
   - Extract key decisions, outcomes, and patterns

5. Check `_current/open-loops.md` for items tagged `#client/$ARGUMENTS`:
   - What we owe them
   - What they owe us
   - Any overdue items

6. Check `_current/this-week.md` for any mentions of this client

7. **Calendar enrichment** — call `list_events` to find the next upcoming meeting with this client:
   - `startTime`: now (current datetime, [your-timezone-region])
   - `endTime`: 7 days from now
   - `fullText`: client name
   - `timeZone`: "[your-timezone-region]"
   - If found: extract call time, duration, attendees (accepted vs. pending)
   - If not found: note "No upcoming calendar event found for this client"

8. **Meeting transcript gap check** — if a meeting transcript tool (e.g. Granola) is configured, call `query_granola_meetings` with query: "recent meetings about [client name]":
   - Cross-reference results against vault meetings folder
   - Flag any meetings from the last 14 days that have **no matching note** in `02-areas/celonis/[client]/meetings/`
   - List unprocessed meetings as: "⚠ Unprocessed: [Title] ([Date]) — run /meeting to capture"
   - If no transcript tool is available, skip this step

9. **Slack signal** — search for recent internal discussions about this client:
   ```
   slack_search_public_and_private(
     query: "[client name]",
     sort: "timestamp",
     sort_dir: "desc",
     limit: 5
   )
   ```
   - Surface any threads from the last 14 days: AE updates, deal strategy, internal flags
   - Note who's discussing and what the context is
   - If nothing found, omit this section

10. **Knowledge Lake reference** — if you're positioning a specific use case for this client, query for proof points:
    ```
    search_knowledge(
      query: "[client's industry] [active use case from hub hypotheses]",
      topics: ["cortex_external"],
      top_n: 3
    )
    ```
    - Surface 1-2 reference customers to mention on the call (same industry or same use case)
    - If nothing relevant, omit this section

## Output

Synthesize a briefing with these sections:

### Status
One-liner on where we are in the engagement

### Key People
Who's likely on the call and what each person cares about (from stakeholder notes)

### Recent Activity
Summary of last 2-3 interactions and what was decided

### Slack Signal
Internal threads about this client in the last 14 days (AE updates, strategy discussions, flags). Omit if nothing found.

### Open Loops
- **Ours:** What we owe them
- **Theirs:** What they owe us
- **Overdue:** Flag anything past due

### What's Worked
Approaches or framings that have landed well with this client

### Reference Customers
1-2 proof points from Knowledge Lake to mention if relevant. Omit if nothing useful found.

### Next Call
- **When:** [date/time from Calendar, or "not found"]
- **Attendees:** [names + accepted/pending status]
- **Duration:** [X min]

### Unprocessed Meetings
List any Granola meetings not yet in vault (from step 8). If none, omit this section.

### Suggested Talking Points
Based on context, what should be on the agenda

---

Output as formatted markdown to screen (do not save to file unless asked).
