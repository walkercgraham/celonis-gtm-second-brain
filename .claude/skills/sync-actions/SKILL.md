---
name: sync-actions
description: Sync action items from recent notes to open-loops dashboard. Run at end of day
---

# Sync Action Items

Keep `_current/open-loops.md` current by scanning recent notes for tasks.

## Steps

1. Read the current `_current/open-loops.md` to understand existing items

2. Scan all notes modified in the last 7 days for uncompleted tasks:
   - Look for `- [ ]` checkbox items
   - Focus on items with `#due/YYYY-MM-DD` tags
   - Check `01-daily/` (daily notes)
   - Check `02-areas/celonis/*/meetings/` (meeting notes)
   - Check `02-areas/celonis/*/*.md` (client hub files)

3. For each task found:
   - If it has a `#due/` tag and is NOT already in open-loops, add it
   - If it's marked complete (`- [x]`) and IS in open-loops, mark it complete there too
   - Preserve the `#client/` tags for organization

4. Identify overdue items:
   - Any task with `#due/YYYY-MM-DD` where the date is in the past
   - Flag these in the report

5. Update `_current/open-loops.md`:
   - Add new items to appropriate sections (Pinned, Waiting On Others, etc.)
   - Update the `modified` date in frontmatter to today

## Output

Report:
- **Added:** New items synced to open-loops
- **Completed:** Items marked done
- **Overdue:** Items past their due date
- **Summary:** Total open items count
