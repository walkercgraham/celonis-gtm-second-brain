---
name: eod
description: End-of-day reflection. Captures what happened, spots patterns, updates open-loops. Run before closing laptop
---

# End of Day Review

Brutally honest daily reflection. No sugar-coating.

## Steps

1. **Read today's daily note** at `01-daily/YYYY-MM-DD.md`
   - What was planned (Focus section)
   - What actually happened (Log section)
   - Raw captures and thoughts

2. **Analyze the day:**

   **Completion Rate**
   - How many of the 3 focus items got done?
   - If <2/3, why? Be specific — was it meetings, context switches, poor scoping, or avoidance?

   **Time Allocation**
   - Count meetings from the log (look for time patterns like "10-10:30am")
   - Calculate: meeting hours vs. available hours
   - Flag if >60% of day was meetings — that's not sustainable for deep work

   **Context Switches**
   - How many different clients/projects touched today?
   - If >4, note the cost — scattered attention means shallow progress everywhere

   **Energy Drains**
   - Look for frustration signals in captures ("frustrating", "too many", "didn't get to")
   - What patterns are repeating from previous days?

3. **Check for drift:**
   - Read `_current/this-week.md` — are today's activities aligned with weekly priorities?
   - If not, call it out directly

4. **Run sync-actions logic:**
   - Extract any new action items from today's note
   - Update `_current/open-loops.md` with new items
   - Mark completed items as done

5. **Update active-clients.md (Recently Touched):**
   - Identify all clients mentioned in today's daily note Log section
   - For each, update their "Recently Touched" entry in `_current/active-clients.md` with today's date and a one-liner of what happened (e.g., "May 7 — demo delivered, feedback positive")
   - If the file has no "Recently Touched" format, add the date next to the client's status line

6. **Save EOD review:**
   - Create `02-areas/celonis/_internal/reviews/YYYY-MM-DD-eod.md` with:
     - Completion: X/3 focus items
     - Meeting load: X hours (X%)
     - Context switches: X clients/projects
     - Full analysis and recommendations
   - Add a brief `## EOD Reflection` section to the daily note linking to the full review

7. **Commit and push to GitHub:**
   - Run: `git add -A`
   - Run: `git commit -m "eod: YYYY-MM-DD — X/3 focus items, X meetings"` (use actual date and stats from step 2)
   - Run: `git push`
   - Report success or any errors to the user

## Output

Be direct. Example tone:

> "2/3 focus items done. But you spent 4.5 hours in meetings across 6 different contexts — that's why the [Client A] build didn't happen. Tomorrow: block 2 hours for deep work or it won't get done. The 30-minute gaps between calls aren't enough."

End with:
- **Tomorrow's carryover:** What must happen tomorrow
- **Pattern to watch:** If this is a recurring issue, name it
