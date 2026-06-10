---
name: triage
description: Interactive open-loops cleanup. Removes completed items, flags overdue, asks keep/defer/drop/delegate. Run weekly to keep the file lean and scannable.
---

# Open-Loops Triage

Focused cleanup of `_current/open-loops.md`. Transforms a bloated dump into a lean active dashboard. Interactive — asks [user] for decisions on overdue items.

## When to Use

- Weekly (Monday morning or Friday EOD)
- When `open-loops.md` feels overwhelming
- After `/weekly-review` identifies accumulation

## Steps

### Step 1: Read and Parse

1. Read `_current/open-loops.md` in full
2. Parse every line that starts with `- [ ]` or `- [x]`:
   - Extract: item text, client tag, due date, status tags (#action-required, #waiting-on)
   - Categorise as: completed (`[x]`), active (`[ ]`), or malformed
3. Count totals:
   - Total items
   - Completed (already checked)
   - Active (unchecked)
   - Overdue (due date < today)
   - No due date (unchecked, no `#due/` tag)

### Step 2: Remove Completed Items

1. Identify all `- [x]` items (including any `(DONE ...)` annotations)
2. Move them to a separate archive file: `04-archive/open-loops-done-YYYY-WXX.md`
   - Group by client
   - Include the completion date if annotated
   - Add frontmatter: `type: archive, tags: [open-loops], created: [today]`
3. Remove these lines from `open-loops.md`

### Step 3: Flag Overdue Items

Present overdue items to [user] grouped by age:

```markdown
## Overdue Items ([count] total)

### Critical (14+ days overdue)
- [ ] [item text] — Due [date] ([X] days ago) #client/[name]
  → **Keep** (new date?) / **Drop** / **Delegate** (to who?)

### Aging (7-13 days overdue)
- [ ] [item text] — Due [date] ([X] days ago) #client/[name]
  → **Keep** / **Drop** / **Delegate**?

### Recently Overdue (1-6 days)
- [ ] [item text] — Due [date] ([X] days ago)
  → [These usually just need a new date]
```

**Ask [user]** for a decision on each Critical and Aging item. Apply decisions:
- **Keep:** Update due date to [user]'s specified date
- **Drop:** Remove the item entirely (it's no longer relevant)
- **Delegate:** Add `#waiting-on/[name]` and remove `#action-required`
- **Defer to someday:** Move to a `## Someday` section at bottom (no due date, low priority)

For Recently Overdue (1-6 days): batch-update due dates to this week unless [user] flags specific ones.

### Step 4: Restructure Remaining Items

Rewrite `open-loops.md` with clean structure:

```markdown
---
type: area
tags: [open-loops, dashboard]
modified: YYYY-MM-DD
---

# Open Loops

Last triaged: YYYY-MM-DD | Active items: [count]

## This Week (due within 7 days)
[Items sorted by due date, grouped by client]

## Next Week
[Items due 8-14 days out]

## Waiting On Others
[All #waiting-on items, grouped by who we're waiting on]

## No Due Date
[Items without #due/ tags — consider adding dates or dropping]

## Someday
[Low priority, no timeline — review monthly]
```

### Step 5: Report

```markdown
## Triage Complete

| Metric | Before | After |
|--------|--------|-------|
| Total items | [X] | [Y] |
| Completed (archived) | [X] | 0 |
| Overdue | [X] | [Y] |
| Active | [X] | [Y] |

**Archived to:** `04-archive/open-loops-done-YYYY-WXX.md`
**Decisions made:** [X] items dropped, [Y] deferred, [Z] delegated
**Next triage:** [suggest date — 7 days from now]
```

## Quality Rules

1. **Never delete without asking** — always confirm drops with [user]
2. **Preserve client tags** — every item must retain its `#client/` tag for filtering
3. **Batch similar decisions** — if [user] drops 3 items from the same dead initiative, offer to drop all related items
4. **Flag patterns** — if a client has 10+ overdue items, note "Consider running /prep or scheduling a catch-up call"
5. **Keep structure after triage** — the restructured format should be maintained by `/sync-actions` and `/eod` going forward
