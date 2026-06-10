---
type: resource
tags: [obsidian, workflow, guide]
created: 2026-04-10
modified: 2026-04-10
status: active
---

# Obsidian Daily Workflow Guide

## The 15-Minute Daily System

Your Obsidian habit lives or dies on consistency, not volume. Here's a system designed around your actual workday as a Celonis GTM professional.

---

## Morning Routine (5 minutes — with your coffee)

### 1. Create Today's Daily Note
Open Obsidian → `Cmd/Ctrl + P` → "Daily Note" (or use the Periodic Notes plugin to auto-create on open).

### 2. Set Your Top 3
Write the three things that would make today a success. Be specific:
- ❌ "Work on [client]"
- ✅ "Finish discovery question set for Thursday's workshop"

### 3. Pull Forward Open Items
Scan yesterday's daily note. Any unchecked `- [ ]` items get copied to today. If something has carried forward 3+ days, either do it, delegate it, or delete it.

### 4. Check Your Calendar
Glance at your schedule. Add any meetings to the daily note with time slots. This becomes your anchor for the day.

**Time:** ~5 minutes. Do this before opening Slack or email.

---

## During the Day (Capture, Don't Organise)

### The Inbox Rule
Everything goes into `00-inbox/`. Don't think about where it belongs. Don't add tags. Don't create links. Just capture.

**What to capture:**
- Quick thoughts → new note in inbox, even if it's one sentence
- Meeting notes → use the meeting template, drop in inbox
- Interesting links/articles → paste URL + one line on why it matters
- Call summaries → bullet points, names, outcomes
- Ideas for initiatives → even half-formed ones

**Keyboard shortcut:** Set up QuickAdd plugin so you can create an inbox note with one hotkey (`Ctrl+Shift+N`).

### Meeting Notes During Calls
Keep Obsidian open during calls. Use the meeting template. Focus on:
- **Decisions** (not discussion) — what was actually agreed?
- **Action items** — who does what by when?
- **Signals** — anything surprising or politically important?
- **Exact quotes** — when someone says something that matters, capture it verbatim

Don't try to transcribe everything. A transcript tool (Granola, Otter, etc.) handles that. Your meeting note is the *processed* version — what mattered.

### The Two-Minute Rule
If a thought takes less than two minutes to capture properly (with a link or tag), do it now. If it takes longer, inbox it and move on.

---

## End of Day (5 minutes — before closing laptop)

### 1. Process the Inbox
Run through `00-inbox/`. For each item:
- Add frontmatter (type, tags, status)
- Move to the right folder
- Add at least one `[[wikilink]]` to a related note
- If it's an action item, add it to tomorrow's daily note

**With Claude Code:** Run `/process-inbox` and let it handle the mechanical parts. Review what it did, adjust any links or tags.

### 2. Fill in the Work Log
Go back to your daily note. Under "Work Log," jot down what actually happened. This doesn't need to be detailed — 3-5 bullet points. This becomes invaluable when you need to write a weekly update or remember what happened on a specific day.

### 3. One-Sentence Reflection
Under "End of Day," write one sentence. What did you learn? What surprised you? What would you do differently? This is the highest-ROI journaling habit — tiny effort, huge compounding value.

---

## Weekly Review (30 minutes — Friday afternoon or Sunday evening)

This is where the vault transforms from notes into a knowledge graph.

### 1. Review Daily Notes
Skim all 5 daily notes from the week. Look for:
- Patterns (what kept coming up?)
- Wins (what went well?)
- Recurring blockers
- Ideas that appeared more than once

### 2. Run the Linking Pass
Open Graph View. Look for isolated clusters or orphaned notes. Ask yourself: "Does this note connect to anything else?" Add links.

**With Claude Code:** Run `/link` to auto-detect potential connections, then review and approve them.

### 3. Update Project Notes
For each active project, add a weekly log entry:
- Current status
- What happened this week
- What's next
- Any blockers or risks

### 4. Archive Completed Items
Anything that's done → move to `04-archive/`. Update status to `complete`. Don't let dead projects clutter your active workspace.

### 5. Generate Weekly Review Note
Create `01-daily/YYYY-WXX-review.md` summarising the week. This note links to the daily notes and any significant project updates.

**With Claude Code:** Run `/weekly-review` for an auto-generated draft, then edit it.

---

## Essential Obsidian Plugins

Install these from Settings → Community Plugins:

| Plugin             | Why You Need It                                                                     |
| ------------------ | ----------------------------------------------------------------------------------- |
| **Periodic Notes** | Auto-creates daily/weekly notes from templates                                      |
| **Templater**      | Dynamic templates with dates, cursor placement                                      |
| **QuickAdd**       | One-hotkey capture to inbox                                                         |
| **Dataview**       | Query your vault like a database — surface all action items, filter by client, etc. |
| **Calendar**       | Visual calendar sidebar linked to daily notes                                       |
| **Graph Analysis** | Better graph view with clustering                                                   |
| **Kanban**         | Turn any note into a board — good for project tracking                              |
| **Omnisearch**     | Better full-text search across the vault                                            |

### Dataview Queries to Set Up

Embed these in your daily note template or a dashboard note:

**All open action items:**
```dataview
TASK FROM "02-areas"
WHERE !completed
SORT file.mtime DESC
```

**Recent meeting notes:**
```dataview
TABLE client, attendees
FROM #meeting
SORT created DESC
LIMIT 10
```

**Active projects by priority:**
```dataview
TABLE priority, deadline, status
FROM "02-areas"
WHERE status = "active"
SORT priority ASC
```

---

## Optimisation Tips for Your Specific Workflow

### For Client Engagements
Create a subfolder per client under `02-areas/celonis/`. Each client folder gets:
- `[client-name].md` — engagement hub: stakeholders, deal stage, hypotheses, timeline
- Meeting notes
- Hypothesis notes
- Deliverables (or links to them in `05-outputs/`)

Before any client call, run `/prep [client-name]` with Claude Code. It scans the vault and produces a one-page brief of everything you know, what you promised, and what's outstanding.

### For Learning and Concepts
When you learn something new — a framework, a technique, a mental model — create a concept note in `03-resources/concepts/`. Write it in your own words. Link it to where you first encountered it and where you've applied it. These notes compound more than anything else in the vault.

---

## The Compound Effect

Week 1: This feels like overhead. You're creating notes no one reads.
Week 4: You start finding things faster than you could in Slack or email.
Week 8: Before a client call, you pull up everything from past meetings in seconds.
Week 12: Your weekly reviews surface patterns you'd never have noticed.
Week 26: You have a genuine knowledge graph. Claude Code can traverse it and generate deliverables directly from your accumulated context.

The key is to survive the first two weeks. After that, the search-and-find value alone justifies the effort. Everything after that is compounding returns.

---

## Quick Start Checklist

- [ ] Download Obsidian (https://obsidian.md)
- [ ] Create vault folder (e.g., `~/obsidian-vault/`)
- [ ] Copy the folder structure from CLAUDE.md into the vault
- [ ] Copy CLAUDE.md to the vault root
- [ ] Copy templates to `03-resources/templates/`
- [ ] Install plugins: Periodic Notes, Templater, QuickAdd, Dataview, Calendar
- [ ] Configure Periodic Notes to use the daily template
- [ ] Set up QuickAdd hotkey for inbox capture
- [ ] Create your first daily note
- [ ] Commit the vault to a private Git repo
- [ ] Start capturing — don't optimise yet, just build the habit
