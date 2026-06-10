# CLAUDE.md — Celonis GTM Second Brain

## Vault Purpose
This is a personal knowledge management vault for Celonis GTM professionals. It serves as a second brain for:
- Client engagements (discovery, qualification, PoV, delivery, expansion)
- Professional development and learning
- Internal initiatives and enablement
- Career progression and visibility

## Owner Context
- **Name:** [Your Name]
- **Role:** [Your Role] at Celonis (e.g., Applied Value Engineer, Solution Engineer, Account Executive)
- **Location:** [Your City, Country]
- **Working hours:** [Your Timezone] (e.g., CET, GMT, EST)
- **Key tools:** Claude Code, Celonis EMS, [Your Additional Tools]

---

## Vault Structure

```
📁 _current/           → Daily cockpit (always open)
│   this-week.md       → Weekly focus areas
│   active-clients.md  → Client dashboard
│   open-loops.md      → All action items
📁 00-inbox/           → Raw captures. Everything lands here first.
📁 01-daily/           → Daily notes (YYYY-MM-DD.md)
📁 02-areas/           → Ongoing responsibilities & active work
│   📁 celonis/        → ALL Celonis work
│   │   📁 _internal/  → Enablement, career dev, team, non-client work
│   │   │   📁 meetings/ → Internal team meetings (weekly syncs, etc.)
│   │   📁 [client]/   → Client engagements (each has [client].md hub + stakeholders/ + meetings/)
📁 03-resources/       → Reference material, evergreen notes
│   📁 concepts/       → Ideas, mental models, frameworks, MOCs
│   📁 tools/          → Tool configs, workflows, cheat sheets
│   📁 templates/      → Note templates
│   📁 reading/        → Book notes, article highlights
📁 04-archive/         → Completed projects, past engagements
📁 05-outputs/         → Generated deliverables (briefings, scripts, exports)
```

---

## Naming Conventions

- **Daily notes:** `YYYY-MM-DD.md` (e.g., `2026-04-10.md`)
- **Meeting notes:** `YYYY-MM-DD - Meeting - [Company/Person].md`
- **Client folders:** lowercase, hyphenated (e.g., `acme-corp`, `global-industries`)
- **Client hub files:** Use folder name as filename (e.g., `acme-corp/acme-corp.md`, NOT `_index.md`)
- **Sub-project folders:** lowercase-hyphenated with hub file matching folder name (e.g., `inventory-pov/inventory-pov.md`)
- **Concept notes:** Title Case (e.g., `Monte Carlo Simulation.md`)
- **All other notes:** lowercase-hyphenated (e.g., `discovery-workshop-prep.md`)

---

## Frontmatter Standard

Every note MUST have YAML frontmatter:

```yaml
---
type: [daily | meeting | area | concept | resource | output]
tags: [tag-one, tag-two]
created: YYYY-MM-DD
modified: YYYY-MM-DD
status: [active | paused | complete | archived]
related:
  - "[[note-name]]"
---
```

> **YAML formatting rules — strictly enforced:**
>
> 1. **Tags: NO `#` prefix.** `#` is a YAML comment character and breaks rendering. Use plain strings only.
>    - Correct: `tags: [celonis, client/acme-corp, meeting]`
>    - Wrong: `tags: [#celonis, #client/acme-corp, #meeting]`
>    - The `#` prefix is only used in the **body** of a note (e.g. `#due/2026-04-21` in action items)
>
> 2. **`related`: always a list with quoted wikilinks, never inline.**
>    - Correct: `related:\n  - "[[note-name]]"`
>    - Wrong: `related: [[note-name]]`
>
> 3. **`attendees`: always a YAML list, never an inline array.**
>    - Correct: `attendees:\n  - [Person 1]\n  - [Person 2]`
>    - Wrong: `attendees: [[Person 1], [Person 2]]`

### Additional frontmatter by type:

**Meeting notes:**
```yaml
client: "Company Name"
attendees: []
action-items: []
```

---

## Tagging Taxonomy

### Context Tags
- `#celonis` — anything related to day job

### Client Tags
- `#client/[client-name]` — one tag per client (e.g., `#client/acme-corp`)

### Type Tags
- `#meeting`, `#demo`, `#workshop`, `#discovery`
- `#hypothesis`, `#decision`, `#blocker`, `#win`

### Status Tags
- `#action-required` — needs your attention
- `#waiting-on` — blocked on someone else
- `#review` — needs review before sharing

### Domain Tags
- `#process-mining`, `#ai-agent`, `#copilot-studio`, `#mcp`
- `#procurement`, `#inventory`, `#maintenance`, `#itsm`

---

## Claude Code Instructions

### Priority 1: Daily Operations

### Daily Note (`/daily`)
1. Create `01-daily/YYYY-MM-DD.md` from template at `03-resources/templates/daily-template.md`
2. Check `_current/open-loops.md` for items due today
3. Output: new daily note ready for use

### Processing Inbox (`/process-inbox`)
1. Read all files in `00-inbox/`
2. For each file:
   - Analyze content to determine type (meeting, research, capture, etc.)
   - Add proper frontmatter based on type
   - Identify client/project and move to correct folder:
     - Meeting notes → `02-areas/celonis/[client]/meetings/`
     - General captures → appropriate area or daily note
   - Add tags based on content analysis
   - Create `[[wikilinks]]` to any existing related notes
   - Extract action items with `#due/YYYY-MM-DD` format
3. Update `_current/open-loops.md` with any new action items found
4. Leave nothing in inbox when done
5. Report: files processed, where moved, actions extracted

### Sync Actions (`/sync-actions`)
1. Scan notes modified in last 7 days
2. Find all uncompleted tasks (`- [ ]`) with `#due` tags
3. Update `_current/open-loops.md`:
   - Add new items not already present
   - Remove completed items
   - Flag overdue items
4. Report: items added, items completed, items overdue

---

### Meeting Notes (`/meeting`)
1. User pastes meeting transcript inline
2. Parse date, title, attendees, client, action items from transcript
3. Resolve every attendee to a wikilink:
   - Search existing stakeholder pages (client folder + internal team)
   - Create stub pages for anyone new
4. Write structured meeting note to correct folder with full wikilinks
5. Update `_current/open-loops.md` with your action items
6. Report: file saved, stubs created, actions added, ambiguities flagged

---

### Priority 2: Client Work

### Client Prep (`/prep [client-name]`)
1. Find client folder in `02-areas/celonis/[client]/`
2. Read `[client].md` hub file for:
   - Current status
   - Stakeholders table
   - Active hypotheses
   - Key wins & learnings
3. Read last 3-5 meeting notes in the folder (by date)
4. Read all stakeholder notes in `stakeholders/` subfolder
5. Check `_current/open-loops.md` for items tagged `#client/[client]`
6. Synthesize into a briefing:
   - **Status**: One-liner on where we are
   - **Key People**: Who's on the call, what they care about
   - **Open Loops**: What we owe them, what they owe us
   - **What's Worked**: Approaches that landed well
   - **Talking Points**: Suggested agenda based on context
7. Output to screen (formatted markdown)

### Client Status Update (`/client-status [client-name]`)
1. Find client `[client].md` hub file
2. Ask:
   - What happened? (one-liner for status)
   - Any new action items?
   - Any wins or learnings to capture?
3. Update `[client].md` hub file:
   - Status line
   - Engagement timeline (add new entry)
   - Action items (if any)
   - Wins & learnings (if any)
4. Update `_current/active-clients.md` dashboard

### New Client (`/new-client [client-name]`)
1. Create folder: `02-areas/celonis/[client-name]/`
2. Create `[client-name].md` hub file from `03-resources/templates/client-index-template.md`
3. Create `stakeholders/` subfolder
4. Add client to `_current/active-clients.md` dashboard
5. Report: folder created, ready to populate

---

### Priority 3: Knowledge & Synthesis

### Discovery Prep (`/discover [client-name]`)
1. Run `/prep [client-name]` first to gather context
2. Search `03-resources/concepts/` for relevant MOCs
3. Search `04-archive/` for similar past engagements (same industry, use case)
4. Synthesize discovery workshop prep:
   - **Context**: What we know about this client
   - **Stakeholder-Specific Approaches**: Tailor to who's in the room
   - **Discovery Questions**: Based on what's worked before
   - **Risks & Objections**: Likely concerns and how to handle
   - **Content to Prepare**: Relevant decks, deliverables, reference materials
5. Output to screen or save to `05-outputs/`

### Weekly Review (`/weekly-review`)
1. Scan all daily notes from the past 7 days
2. Generate summary:
   - **Accomplishments**: What got done
   - **Open Items by Client**: Grouped action items
   - **Patterns**: What themes emerged
3. List all notes created/modified this week
4. Flag orphaned notes (no incoming links)
5. Output to `01-daily/YYYY-WXX-review.md`

### Ask (`/ask [question]`)
1. Search vault for relevant content based on question
2. Read matching notes
3. Synthesize answer using vault context
4. Cite sources with `[[wikilinks]]`
5. Output answer to screen

### Linking Pass (`/link`)
1. Scan notes modified in last 7 days
2. For each note, find potential connections:
   - Same client/project
   - Similar topics/tags
   - Mentioned people or concepts
3. Add `[[wikilinks]]` where relevant
4. Update `related:` frontmatter field
5. Report: connections made

### Archive (`/archive [project-name]`)
1. Move project folder to `04-archive/`
2. Update status frontmatter to `archived`
3. Add completion date
4. Generate project retrospective note with:
   - What worked
   - What didn't
   - Reusable patterns
5. Update `_current/active-clients.md` (remove from active)

---

## Templates

| Template | Location | Use For |
|----------|----------|---------|
| Daily Note | `03-resources/templates/daily-template.md` | Daily notes via `/daily` |
| Meeting Note | `03-resources/templates/meeting-template.md` | Meeting captures |
| Client Index | `03-resources/templates/client-index-template.md` | Client hub files (`[client].md`) |
| Stakeholder | `03-resources/templates/stakeholder-template.md` | People notes |
| Project | `03-resources/templates/project-template.md` | Sub-project hub files |

---

## Important Rules

1. **Never delete notes** — archive them instead
2. **Every note must link to at least one other note** — orphans are flagged in weekly review
3. **Action items use checkbox syntax:** `- [ ] Action item #client/name #due/YYYY-MM-DD`
4. **Timestamps in UTC** for frontmatter, local time in body text
5. **Client-sensitive content** should be tagged `#confidential` — never export these to shared locations
6. **Daily notes are sacred** — they're the spine of the vault, never skip them
7. **Client hub files are the source of truth** — always update `[client].md` after client interactions
8. **`_current/` is your cockpit** — keep it current, check it daily
9. **ALL Celonis content stays in `02-areas/celonis/`** — client work, internal initiatives, enablement, tools, career docs. Never put Celonis material in `03-resources/` or elsewhere. This includes:
   - Client engagements → `02-areas/celonis/[client]/`
   - Internal meetings → `02-areas/celonis/_internal/meetings/`
   - Enablement & tools → `02-areas/celonis/_internal/enablement/`
   - Career & reviews → `02-areas/celonis/_internal/career/`
   - Initiatives → `02-areas/celonis/_internal/initiatives/`

---

## Client Folder Structure

Each client in `02-areas/celonis/` follows this structure:

```
02-areas/celonis/[client-name]/
├── [client-name].md       ← Engagement hub (source of truth)
├── stakeholders/          ← People notes
│   ├── person-one.md
│   └── person-two.md
├── meetings/              ← All client meeting notes
│   └── YYYY-MM-DD - Meeting - [Topic].md
├── [sub-project]/         ← Sub-projects get their own folders
│   ├── [sub-project].md   ← Sub-project hub file
│   ├── technical/         ← Technical documentation
│   └── meetings/          ← Sub-project specific meetings
└── [other notes as needed]
```

## Internal Meetings Structure

Team meetings and internal syncs live in:

```
02-areas/celonis/_internal/meetings/
├── YYYY-MM-DD - Meeting - Weekly Team Sync.md
├── YYYY-MM-DD - Meeting - 1-1 with [Manager].md
└── [other internal meetings]
```

## Daily Workflow Summary

**Morning (5 min):**
1. Open `_current/this-week.md` — weekly focus
2. Scan `_current/open-loops.md` — what's due?
3. Create daily note (`/daily`)
4. Set 3 focus items

**During day:**
- `/prep [client]` before calls
- Captures go in daily note
- Meeting transcripts (from Granola, Otter, or manual paste) → `00-inbox/`

**End of day (5-10 min):**
1. `/process-inbox`
2. `/sync-actions`
3. Update touched client hub files

**Weekly (20-30 min):**
1. `/weekly-review`
2. Update `_current/this-week.md`
3. Clean `_current/open-loops.md`
