---
name: daily
description: Create today's daily note from template. Use each morning when starting work
argument-hint: "[optional: YYYY-MM-DD to override date]"
---

# Create Daily Note

Create a daily note for today (or the date provided in $ARGUMENTS if specified).

## Steps

1. Determine the target date:
   - If `$ARGUMENTS` is provided and is a valid date (YYYY-MM-DD format), use that
   - Otherwise, use today's date

2. Check if the daily note already exists at `01-daily/YYYY-MM-DD.md`
   - If it exists, open and display it instead of creating a new one

3. Read the daily template from `03-resources/templates/daily-template.md`

4. Create the new daily note at `01-daily/YYYY-MM-DD.md`:
   - Replace `{{date}}` with the target date (YYYY-MM-DD)
   - Replace `{{day}}` with the day of week (e.g., "Monday")
   - Set `created` in frontmatter to the target date

5. Fetch today's calendar events using `list_events`:
   - `startTime`: target date at 00:00:00 ([your-timezone-region])
   - `endTime`: target date at 23:59:59 ([your-timezone-region])
   - `timeZone`: "[your-timezone-region]"
   - Filter out declined events and all-day non-meeting events (birthdays, OOO blocks)
   - **Exclude** any event whose title contains "lunch" (case-insensitive)
   - For each event: extract title, start time, end time
   - Pre-populate the `## Log` section with meetings in chronological order, inserted after the `<!-- Timestamped entries throughout day -->` comment:

```markdown
## Log
<!-- Timestamped entries throughout day -->
9:15–10:30am Weekly 1-1 with [Manager]
11:00–11:30am [Client A] Status Review
2:00–3:00pm [Client B] Working Session
```

   Use the format `H:MM–H:MMam/pm` (e.g. `9:15–10:30am`, `2:00–3:00pm`). Both start and end time must be shown. If no events found, leave the Log section with just the comment placeholder — do not add a `## Meetings` section.

6. Check `_current/open-loops.md` for items due today:
   - Look for tasks with `#due/YYYY-MM-DD` matching the target date
   - If any exist, mention them to the user

7. Confirm the file was created and is ready for use

## Output

Report what was created, meetings found on calendar, and any items due today from open-loops.
