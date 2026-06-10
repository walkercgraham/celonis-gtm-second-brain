---
name: morning
description: Calendar-aware morning kickstart. Chains daily note creation, per-meeting context, and Gmail flags into one oriented start. Run when opening laptop.
argument-hint: "[optional: YYYY-MM-DD to override date]"
---

# Morning Kickstart

Get fully oriented in one command. Creates the daily note, surfaces today's schedule with per-meeting vault context, and flags any emails needing attention.

## Steps

### 1. Create (or open) today's daily note

Run the `/daily` skill logic for today (or `$ARGUMENTS` date if provided):
- Create `01-daily/YYYY-MM-DD.md` from template if it doesn't exist
- Pre-populate meetings into `## Log` section from Calendar using format `**HH:MM–HH:MM** — [Event Title]`
- Skip if note already exists — open it and continue

### 2. Build per-meeting context

For each meeting found on calendar today (from step 1):

a. **Identify the client or project** from the event title/description
   - Match against known client folders in `02-areas/celonis/`
   - Flag as "Internal" if no match (e.g. team syncs, 1:1s)

b. **For client meetings**: pull quick context from vault
   - Read client hub `[client].md`: status one-liner + active hypotheses
   - Check `_current/open-loops.md` for items tagged `#client/[client]`
   - Note the most recent meeting date

c. **Check for unprocessed meeting transcripts** (if a transcript tool like Granola is configured): call `query_granola_meetings` with the client/event name
   - Flag any recent meetings not yet in vault
   - If no transcript tool is available, skip this step

### 3. Scan Gmail for flags

Call `search_threads` with query: `"is:unread (is:starred OR is:important) newer_than:2d"`
- For each thread (max 10): extract sender, subject, brief snippet
- Classify as: **Action needed** / **FYI** / **Can wait**
- Action needed = reply requested, deadline mentioned, from a client/manager
- Ignore automated notifications, newsletters, calendar invites

### 4. Check open-loops for today

Read `_current/open-loops.md`:
- Extract tasks with `#due/[today's date]`
- Extract any tasks marked `#action-required` (regardless of due date)

### 5. Output morning briefing to screen

Format:

```
# Morning — [Day], [Date]

## Today's Schedule
[HH:MM]–[HH:MM] — [Event Title]
[HH:MM]–[HH:MM] — [Event Title]
...

---

## Per-Meeting Context

### [HH:MM] [Event Title]
**Client:** [[client-name]] | **Status:** [one-liner]
**Open loops:** [count] items — [top 1-2]
**⚠ Unprocessed Granola:** [meeting title if any]

[repeat for each client meeting]

---

## Email Flags ([N] items)
- **[Subject]** from [Sender] — [one-line ask] → [Action needed / FYI]
[...]

---

## Due Today
- [ ] [task] #client/x #due/today
[...]
```

Omit any section where there's nothing to report (no emails, no due items, etc.).

Do **not** save this output to a file. Screen only.

## Notes

- Internal meetings (team syncs, 1:1s) get no vault context block — just listed in schedule
- If Calendar returns no events, still proceed with email + open-loops sections
- Gmail search may return threads from previous days if still unread — that's intentional
- Keep per-meeting context tight: 3 lines max per client. This is orientation, not a full `/prep`
- For a full pre-call briefing, run `/prep [client]` separately
