---
name: process-inbox
description: Process all files in 00-inbox folder. Triage, tag, move to correct location, extract actions
---

# Process Inbox

Triage all files in `00-inbox/` and route them to the correct locations.

## Steps

1. List all files in `00-inbox/`
   - If empty, report "Inbox is clear" and exit

2. For each file, analyze the content to determine:
   - **Type:** meeting, research, capture, etc.
   - **Client/Project:** Which client or project does this relate to?
   - **Action items:** Any tasks that need tracking?

3. Add proper frontmatter based on type:

   **Meeting notes:**
   ```yaml
   type: meeting
   tags: [meeting, celonis, client/[name]]
   client: "[Client Name]"
   attendees: []
   action-items: []
   created: YYYY-MM-DD
   modified: YYYY-MM-DD
   status: active
   ```

   **General captures:**
   ```yaml
   type: resource
   tags: []
   created: YYYY-MM-DD
   modified: YYYY-MM-DD
   status: active
   ```

4. Move files to correct locations:
   - Meeting notes → `02-areas/celonis/[client]/meetings/`
   - Concepts/ideas → `03-resources/concepts/`
   - General captures → append to today's daily note or appropriate area

5. For each file:
   - Add relevant tags (`#celonis`, `#client/[name]`, `#meeting`, etc.)
   - Create `[[wikilinks]]` to related existing notes
   - Extract action items with `#due/YYYY-MM-DD` format

6. Update `_current/open-loops.md` with any new action items found

7. Ensure `00-inbox/` is empty when done (all files processed)

## Output

Report:
- **Processed:** List of files and where they were moved
- **Actions extracted:** New items added to open-loops
- **Links created:** Connections made to existing notes

## Naming Conventions

When moving/renaming files, follow vault conventions:
- Meeting notes: `YYYY-MM-DD - Meeting - [Company/Person].md`
- Client folders: lowercase, hyphenated (e.g., `saudi-aramco`)
- Concept notes: Title Case (e.g., `Monte Carlo Simulation.md`)
- All other notes: lowercase-hyphenated
