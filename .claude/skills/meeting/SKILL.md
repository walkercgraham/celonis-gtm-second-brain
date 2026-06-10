# Process Meeting Transcript

Turn a raw meeting transcript into a fully linked, structured meeting note — with stub stakeholder pages for anyone new.

## Input

Two modes — try Granola first, fall back to inline paste:

### Mode A: Granola auto-fetch (preferred)
If `$ARGUMENTS` is provided (meeting name, client, or date like "smurfit", "today", "2026-04-30"):
1. Call `query_granola_meetings` with the argument as the query
2. If a clear match is found, use its transcript and metadata — proceed to Step 1
3. If multiple matches, list them and ask the user to confirm which one

If `$ARGUMENTS` is empty:
1. Call `list_meetings` with `time_range: "this_week"` to find recent meetings
2. Cross-reference against vault meetings folder — identify the most recent meeting **not yet processed** (no matching file in any `meetings/` folder)
3. Confirm the meeting with the user ("Found: [Title] on [Date] — process this one?")
4. Call `get_meetings` with the confirmed ID to fetch full transcript and attendees

### Mode B: Inline paste (fallback)
If Granola fetch fails or user explicitly pastes a transcript, process the pasted content directly.

---

User pastes transcript inline. Transcript may include meeting metadata (title, date, participants) at the top, or these must be inferred from content.

## Steps

### 1. Parse the transcript

Extract:
- **Date** — from metadata header or infer from conversation context (today's date if unclear)
- **Title** — from metadata or synthesize from content (e.g. "Invoice Automation Review", "Weekly Team Sync")
- **Attendees** — all named participants. Distinguish yourself (always "Me:") from others ("Them:")
- **Client / account** — which client or project this meeting is about
- **Type** — client-facing or internal Celonis
- **Key content** — decisions, discussion points, action items, open questions

### 2. Determine file location

| Meeting type | Location |
|---|---|
| Client-facing | `02-areas/celonis/[client]/meetings/YYYY-MM-DD - Meeting - [Title].md` |
| Internal Celonis only | `02-areas/celonis/_internal/meetings/YYYY-MM-DD - Meeting - [Title].md` |
| Sub-project | `02-areas/celonis/[client]/[sub-project]/meetings/YYYY-MM-DD - Meeting - [Title].md` |

Filename: `YYYY-MM-DD - Meeting - [Short Title].md` — title should be descriptive but concise.

### 3. Resolve stakeholder wikilinks

For every named attendee (excluding yourself):

1. **Search for existing page** in this order:
   - `02-areas/celonis/[client]/stakeholders/` — client-side people
   - `02-areas/celonis/_internal/team/stakeholders/direct-team/` — direct Celonis team
   - `02-areas/celonis/_internal/team/stakeholders/wider-network/` — wider Celonis network
   - Any other client stakeholders folders if person works across clients

2. **Match on name** — fuzzy match (e.g. "John" → `john-smith.md`, "Jane" → `jane-doe.md`)

3. **If found** → use `[[filename-without-extension]]` as the wikilink

4. **If NOT found** → create a stub stakeholder page (see Step 4), then link to it

### 4. Create stub stakeholder pages

For anyone without an existing page, create a file using this structure:

```markdown
---
type: stakeholder
tags: [celonis, client/[client-tag]]
client: "[Client Name]"
role: "[Role if known from transcript, else leave blank]"
created: YYYY-MM-DD
modified: YYYY-MM-DD
status: active
related:
  - "[[client-hub-file]]"
---

# [Full Name]

## Profile
- **Company:** [Client or Celonis]
- **Role:** [If mentioned in transcript]
- **Reports to:** 
- **Tenure:** 

## What They Care About
<!-- To be filled from meeting notes -->

## Communication Style
- Preferred channel: 
- Best times: 
- Detail level: 

## History with Us
- [YYYY-MM-DD] — Met in [[YYYY-MM-DD - Meeting - Title]]

## Notes
```

**File naming:** `firstname-lastname.md` (lowercase-hyphenated)

**Save location:**
- Client-side person → `02-areas/celonis/[client]/stakeholders/`
- Celonis colleague (recognisable as internal) → `02-areas/celonis/_internal/team/stakeholders/wider-network/`

**Internal vs client signal:** If they appear in attendee list alongside client stakeholders and their name/context suggests Celonis, save internally. If they're clearly from the client organisation, save in client folder. When ambiguous, default to client folder.

### 5. Write the meeting note

Use this structure:

```markdown
---
type: meeting
tags:
  - celonis
  - client/[client-tag]
  - meeting
  - [domain tags e.g. ai-agent, process-mining]
created: YYYY-MM-DD
modified: YYYY-MM-DD
status: active
client: "[Client Name]"
attendees:
  - "[Your Name]"
  - "[[firstname-lastname|Display Name]]"
  - "[[firstname-lastname|Display Name]]"
action-items:
  - "Person: Action item description"
  - "Person: Another action item"
related:
  - "[[client-hub-file]]"
  - "[[previous-meeting-in-series]]"
---

# YYYY-MM-DD — Meeting — [Title]

## Context
[1-2 sentences: why this meeting happened, what it was trying to achieve]

---

## Notes
[Structured by topic. Use H3 subheadings for major discussion areas. Be specific — include numbers, decisions, quotes where relevant. Don't just summarise; capture the detail that would be useful in a future /prep briefing.]

---

## Decisions Made
- [Concrete decisions only — things that were agreed and won't be relitigated]

---

## Action Items
- [ ] [Person]: [Action] [#client/x] [#due/YYYY-MM-DD] [#action-required OR #waiting-on]

---

## Next Steps
- [What happens next, even if not a specific action item]
```

**Linking rules (strictly enforced):**
- Tags: NO `#` prefix in frontmatter YAML
- `attendees:` always a YAML list, never inline array
- `attendees:` every attendee (except yourself) MUST be a quoted wikilink to their stakeholder page: `"[[firstname-lastname|Display Name]]"`. Your own name stays as plain text (no stakeholder page).
- `action-items:` every item MUST be quoted (strings containing `:` are interpreted as YAML key-value pairs if unquoted, breaking rendering): `"Person: Action description"`
- `related:` always a list with quoted wikilinks
- Client hub (`[[client-name]]`) always in `related:`
- If this is part of a series (e.g. Discovery Workshop 4), link to the previous meeting

### 6. Update stakeholder pages

For every named attendee with an existing stakeholder page, review the transcript for signal worth capturing on their page. Update if any of the following are present:

- A concern, priority, or opinion they expressed
- A change in their position, stance, or level of engagement
- A new role detail, reporting line, or area of ownership
- A win, blocker, or friction point involving them
- How they responded to Celonis / the demo / a proposal
- Anything that would be useful context in a future `/prep`

**What NOT to update:** Generic attendance, small talk, or anything already captured on their page.

**How to update:**
- Add a dated entry under `## History with Us` (or `## Interaction History` if that's the existing heading): `- [YYYY-MM-DD] — [What was learned] — [[meeting-note-link]]`
- Update `## What They Care About` if new priorities emerged
- Update `## Notes` for anything that doesn't fit elsewhere
- Update `modified:` frontmatter date

Only update pages where there is genuine new signal. Skip if the person was present but nothing substantive about them emerged from the transcript.

### 7. Update client hub files

For every client or project mentioned in the meeting (not just the primary client), check if the content warrants updating their `[client].md` hub file. Update if any of the following are present:

- A status change (progressing, blocked, stalled, won)
- A new use case, hypothesis, or scope development
- A stakeholder movement (champion gained, contact lost, new person involved)
- A concrete decision or commercial signal
- A win or blocker worth tracking at the account level

**How to update:**
- Add a dated entry to `## Engagement Timeline` summarising what was learned: `### YYYY-MM-DD — [Brief title]\n[What happened, sourced from this meeting]`
- Update `## Current Status` if the one-liner is now stale
- Update `## Open Action Items` if new items emerged
- Update `modified:` frontmatter date

Only update hubs where something substantive changed. Skip if the client was mentioned in passing with no new signal.

### 8. Update open-loops.md

Append your action items to `_current/open-loops.md` under a section:

```markdown
## Added [Month Day] ([meeting title])
- [ ] [Your Name]: [Action] #client/[x] #due/YYYY-MM-DD #action-required
```

**Only add:**
- Items explicitly assigned to you
- Items where you are co-owner (e.g. "You + [colleague]")

**Tag as `#waiting-on`** (not `#action-required`) for items assigned to others that you need to track.

Do NOT add items that are purely other people's responsibility with no dependency on you.

### 8. Report to user

```
Meeting note saved: [path]

Stakeholder pages created:
- [Name] → [path]

Stakeholder pages updated:
- [Name] → [what was added]

Client hubs updated:
- [client].md → [what was added]

Action items added to open-loops: [N]

Review needed:
- [Any ambiguities — unclear names, missing roles, uncertain client assignment]
```

---

## Quality Checks

Before finishing, verify:
- [ ] Every named attendee (except yourself) is a quoted wikilink: `"[[slug|Name]]"`
- [ ] Every `action-items` entry is quoted: `"Person: Description"`
- [ ] Existing stakeholder pages updated where transcript contains new signal
- [ ] Client hub files updated where status, use cases, or stakeholders changed
- [ ] Client hub is in `related:`
- [ ] No `#` prefix on frontmatter tags
- [ ] `attendees:` is a YAML list (not inline)
- [ ] Action items include owner, due date, and correct tag
- [ ] If series meeting, previous meeting is linked in `related:`
- [ ] File saved to correct folder for meeting type

## Notes

- The vault owner is always "Me:" in the transcript
- Meeting metadata (title, date, participants) sometimes appears before the transcript body — parse it first
- Transcript quality varies — apply judgement on what's signal vs noise
- Internal Celonis colleagues who appear frequently should have pages in `_internal/team/stakeholders/` — check there before creating a new file
