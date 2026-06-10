---
name: clean-up
description: Vault hygiene sweep. Finds orphan notes, stale items, missing frontmatter, contradictions, empty notes. Offers fixes.
---

# Clean-Up (Vault Linting)

Systematic sweep of the vault to find inconsistencies, stale data, and hygiene issues. Run weekly or before major planning sessions.

## Checks to Perform

### 1. Orphan Notes (No Incoming Links)

Scan all notes in:
- `02-areas/`
- `03-resources/`

For each note, check if any other note links to it via `[[wikilink]]`. Flag notes with zero incoming links.

**Exclude from orphan check:**
- Hub files (`[client].md`) — these are entry points
- Template files in `03-resources/templates/`
- Files in `_current/` — these are dashboards
- Daily notes in `01-daily/` — linked by date, not wikilink

**Report format:**
```
ORPHAN NOTES (no incoming links):
- 02-areas/celonis/[client]/some-random-note.md
- 03-resources/concepts/Half-Baked Idea.md
```

**Fix offer:** "Would you like me to find related notes and add links, or move these to archive?"

---

### 2. Stale #due/ Items (Past Due)

Read `_current/open-loops.md` and scan notes for uncompleted tasks (`- [ ]`) with `#due/YYYY-MM-DD` where the date is before today.

**Report format:**
```
OVERDUE ITEMS (X items):
- [ ] [Client]: Complete discovery summary #due/2026-04-10 (4 days overdue)
  Location: _current/open-loops.md
- [ ] Fix EUP1 data pull #due/2026-04-12 (2 days overdue)
  Location: 02-areas/celonis/[client]/[sub-project].md
```

**Fix offer:** "Would you like me to update due dates, mark items as complete, or remove them?"

---

### 3. Client Hub Files with Outdated Status

For each client folder in `02-areas/celonis/`:
1. Read the hub file (`[client].md`)
2. Check the `modified` date in frontmatter
3. Check the most recent meeting note in `[client]/meetings/`
4. Flag if:
   - Hub `status: active` but no meeting notes in 14+ days
   - Hub `modified` date is 14+ days old for active clients
   - Hub says "active" but `_current/active-clients.md` doesn't list them (or vice versa)

**Report format:**
```
STALE CLIENT HUBS:
- [client-a]/[client-a].md
  Status: active | Last meeting: 2026-03-28 (17 days ago)
  Hub last modified: 2026-03-30
  Recommendation: Update status or add recent activity

- [client-b]/[client-b].md
  Status: active | Last meeting: 2026-04-06 (8 days ago)
  Listed in active-clients.md: YES
  Note: Approaching stale threshold
```

**Fix offer:** "Would you like me to update hub statuses, or prompt you for current status on each?"

---

### 4. Notes Missing Required Frontmatter

Check all notes for required frontmatter fields based on type:

**All notes must have:**
- `type`
- `created`
- `status`

**Meeting notes must also have:**
- `client`
- `attendees`

**Venture notes must also have:**

- `priority`

**Report format:**
```
MISSING FRONTMATTER:
- 02-areas/celonis/[client]/meetings/YYYY-MM-DD - Meeting - Discovery.md
  Missing: attendees
  
- 02-areas/celonis/[client]/[sub-project]/notes.md
  Missing: type, priority, status
```

**Fix offer:** "Would you like me to add missing fields with placeholder values?"

---

### 5. Contradictory Information

This is the most complex check. Read related notes and flag inconsistencies:

**Stakeholder contradictions:**
- Read all stakeholder notes in `[client]/stakeholders/`
- Check if the same person is described differently across notes (role, title, sentiment)
- Check if meeting notes mention people not in stakeholders folder

**Status contradictions:**
- Compare hub file status with tone of recent meeting notes
- Flag if hub says "going well" but recent meetings show blockers

**Date/deadline contradictions:**
- Check if the same deadline appears with different dates across notes
- Check if `open-loops.md` dates conflict with dates in source notes

**Report format:**
```
POTENTIAL CONTRADICTIONS:

Stakeholder Mismatch:
- [stakeholder].md says "VP Operations"
- 2026-04-14 meeting notes say "Director of Operations"
  → Verify correct title

Status Mismatch:
- sasol.md hub status: "active, progressing well"
- Last 2 meeting notes mention: "blocked on data access", "waiting on [person]"
  → Hub may need status update

Date Conflict:
- open-loops.md: "[Client] demo #due/YYYY-MM-DD"
- 01-daily/2026-04-14.md: "[Client] demo presenting [date]"
  → Confirm correct deadline
```

**Fix offer:** "Would you like me to reconcile these? I'll show you the conflicting information side-by-side."

---

### 6. Empty or Near-Empty Notes

Find notes that have:
- No content beyond frontmatter
- Less than 50 characters of actual content
- Only headings with no content under them

**Exclude:**
- Template files
- Hub files (which may be sparse by design initially)

**Report format:**
```
EMPTY/SPARSE NOTES:
- 02-areas/celonis/[client]/stakeholders/[name].md
  Content: Only frontmatter, no body
  
- 03-resources/concepts/Process Mining ROI.md
  Content: 23 characters (just a heading)
```

**Fix offer:** "Would you like me to populate these with placeholder content, or move to archive?"

---

## Execution Flow

1. Run all 6 checks in sequence
2. Aggregate findings into a single report
3. Display report to screen with counts:
   ```
   VAULT CLEAN-UP REPORT (2026-04-14)
   ==================================
   
   Orphan notes:        3 found
   Overdue items:       7 found  
   Stale client hubs:   2 found
   Missing frontmatter: 4 notes
   Contradictions:      2 potential
   Empty notes:         1 found
   
   [Details below...]
   ```

4. After showing full report, ask:
   "Would you like me to fix any of these issues? I can:
   - Fix all automatically (where safe)
   - Go through each category and ask
   - Fix specific items you point out"

5. For fixes that require judgment (contradictions, status updates), show the conflicting information and ask [user] to confirm the correct version.

## Output

Report to screen only. Do not create a file unless [user] asks to save the report.

Tone: Direct and actionable. Don't soften findings — if something is stale, say it's stale.
