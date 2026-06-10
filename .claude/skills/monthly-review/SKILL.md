---
name: monthly-review
description: Monthly review — client progression, patterns across weeks, wins for the promotion case. Run last day of the month or first of the next. Sits between weekly (tactical) and quarterly (trajectory).
argument-hint: "[month, e.g., April 2026]"
---

# Monthly Review

Synthesizes the 4-5 weekly reviews into month-level patterns, client progression, and wins for the promotion case. Does NOT re-read daily notes — weekly reviews already synthesized them.

## Context

Month: $ARGUMENTS (or current month if not specified)

---

## Steps

### Part 1: Gather Data

**Step 1 — Identify the weeks.**
Parse the month from `$ARGUMENTS`. Find all weekly review files that cover that month in `02-areas/celonis/_internal/reviews/YYYY-WXX-weekly.md`. Include a week if any of its days fall in the target month.

**Step 2 — Read all weekly reviews for the month.**
Primary data source — do not skip any. From each, extract:
- Total working hours and meeting hours (already calculated)
- Focus item completion rate
- Client health dashboard (per-client touchpoints, momentum, risk)
- Attention allocation section
- Patterns detected
- Honest assessment ratings (Execution / Progress / Sustainability letter grades)
- "The thing you're avoiding" — record the exact item
- Carry-forwards to next week

**Step 3 — Read active client hub files.**
For each client in `02-areas/celonis/[client]/[client].md`, read:
- `stage:` frontmatter or Current Status section (stage at end of month)
- `## Key Wins & Learnings` section (wins with dates — filter to target month)
- Current Status section

**Step 4 — Read `_current/open-loops.md`.**
Scan for:
- Total incomplete items (`- [ ]` count)
- Overdue items: `#due/YYYY-MM-DD` dates that have passed and are still `- [ ]`
- Oldest unresolved item still open (earliest past-due date on an open item)
- Estimate items completed this month from visible `- [x]` entries

**Step 5 — Read `_current/active-clients.md`** for current client table.

**Step 6 — Read `_current/this-week.md`** for current focus areas (baseline for next month priorities).

---

### Part 2: Analyze and Write

Work through each of the 9 sections below.

---

#### Section 1: The Month in Numbers

Aggregate from all weekly reviews:

| Metric | Month Total | Weekly Avg |
|--------|-------------|------------|
| Working hours | Xh | Xh/week |
| Meeting hours | Xh (X%) | Xh/week |
| Focus items completed | X/Y (X%) | X%/week |
| Nights past 8pm | X | — |

No editorializing — numbers speak. Save the verdict for Section 5.

---

#### Section 2: Client Progression

Full-month arc per active client. Sum touchpoints from all weekly client health dashboards. Use client hub files to determine stage start vs. end.

| Client | Stage Start | Stage End | Touchpoints | Momentum | Month Verdict |
|--------|------------|-----------|-------------|----------|---------------|

Momentum options: `Consistently advancing` / `Stalled` / `Volatile` / `Cold`

Below the table, write 2-3 sentences:
- Which clients genuinely advanced (stage moved or concrete outcome delivered)?
- Which had touchpoints but no real movement (activity ≠ progress)?
- Which are at risk of going cold if next month looks the same?

---

#### Section 3: Where the Time Actually Went

Aggregate attention allocation from all weekly reviews. Ranked list by estimated hours — highest to lowest. Include non-client time (internal initiatives, team meetings, enablement, certifications).

Flag: which areas were over-indexed vs. stated priorities? Which high-value clients got under-allocated?

---

#### Section 4: Month-Level Patterns

Read every "Patterns Detected" section and every "the thing you're avoiding" entry across all weekly reviews. Find what repeated 2+ times — these are structural, not situational.

Write 3-5 numbered observations as direct prose (3-5 sentences each, no sub-bullets). For each: name the pattern, cite the evidence across weeks, state what it means if it continues.

**Explicitly check for:**

1. **The same "thing you're avoiding" across weeks.** If the same item appeared in multiple consecutive weekly reviews, write: "The same item — [name it] — appeared as 'the thing you're avoiding' for X consecutive weeks."

2. **Carry-forward compounding.** Did the same items get pushed to next week repeatedly? Name them and count how many weeks they carried.

3. **Sustainability pattern.** If sustainability was rated below C every week, do not average — say: "Sustainability rated [grade] for X consecutive weeks. This is structural, not situational."

4. **Whether the "habit to change" from weekly reviews landed.** Compare the habit set in week 1 to the patterns visible by week 4.

5. **Meeting load vs. build time.** If meetings consistently crowded out deep work, name it with data (e.g., "Meeting hours averaged X% of working time — X weeks above 60%").

---

#### Section 5: Honest Assessment

Same 3-axis structure as weekly, evaluated over the full month.

- **Execution:** Did you do what you said? Use aggregate completion rates but adjust for hours required to achieve them.
- **Progress:** Did client engagements move, or just have activity? Use the Section 2 table as evidence.
- **Sustainability:** Aggregate weekly ratings. If consistently the same, the month gets that grade — do not average up.

```
Execution: [Grade] — [2-3 sentences]
Progress: [Grade] — [2-3 sentences]
Sustainability: [Grade] — [2-3 sentences]

The month in one sentence: [Blunt. No hedging.]
```

---

#### Section 6: Wins — Promotion Case Evidence

From client hub Key Wins sections and weekly review wins. Include only wins with a concrete output or customer confirmation. Standard: could you say this in a promotion conversation?

For each win:
- What it was (one line)
- Date or date range
- Evidence (a number, customer confirmation, or shipped artifact)

Target 5-10 wins. If fewer than 5 with real evidence, flag it: "Only X evidence-backed wins identified for [Month]. This is thin for a promotion case."

Activities are not wins. "Ran discovery session" is not a win. "Discovery confirmed $X opportunity" is.

---

#### Section 7: What Got Deprioritized

**Deliberately deferred** (conscious call made):
Item, reason given, whether the reason was defensible in hindsight.

**Drifted without decision** (never explicitly deferred, just kept not happening):
Item, how many days open or weeks carried forward. These are the real problem.

Max 5 items per category. End with a 2-sentence verdict on whether drift is accumulating.

---

#### Section 8: Action Item Velocity

From `_current/open-loops.md`:

```
Open-loops health (end of [Month]):
- Total open: X items
- Completed this month: ~X items
- Overdue: X items (X% of open)
- Oldest unresolved: [item] — X days overdue
- Trend: Growing / Shrinking / Stable
```

2 sentences: is the action system working? If the list is net growing every month, the system is capturing but not closing — say so.

---

#### Section 9: Next Month's Priorities (Celonis)

Generated from the analysis above — not copied from anywhere.

- **The one non-negotiable:** Single most consequential unresolved item or client at inflection. If this doesn't happen, the month failed.
- **Three focus areas:** Dimension-level, not task-level. "Bring [Client A] to confirmed next stage" not "do the [Client A] call." Three maximum.
- **One structural change:** Something about how work is organized, not just what gets done. Based on the dominant pattern from Section 4. Specific and behavioral.

Write as a direct directive:

> "In [Month], the three things that matter are X, Y, Z. Everything else is maintenance. The structural change is [specific behavior]."

---

### Part 3: Write Output

Create `02-areas/celonis/_internal/reviews/YYYY-MM-monthly.md` with this frontmatter:

```yaml
---
type: resource
created: YYYY-MM-DD
month: YYYY-MM
status: complete
tags: [celonis, review, monthly]
related:
  - "[[YYYY-WXX-weekly]]"
  - "[[this-week]]"
  - "[[open-loops]]"
---
```

Include all 9 sections. Then output a summary to screen:

```
Monthly Review — [Month] [Year]

[1-sentence blunt verdict on the month]

3 things that defined the month:
1. [Most important pattern/event — with a number]
2. [Second most important — with a number]
3. [Third most important]

Clients that moved: [list]
Clients needing attention in [next month]: [list]

[Next month's non-negotiable]

Full review: 02-areas/celonis/_internal/reviews/YYYY-MM-monthly.md
```

---

## Tone

Match the weekly/quarterly review voice: direct, honest, slightly confrontational with comfortable truths.

- Name the thing being avoided — don't gesture at it
- Use actual numbers ("61h" not "around 60h")
- "Four consecutive weeks" not "multiple weeks"
- Don't soften wins — promotion case material, state impact cleanly
- Don't soften misses — "untouched for 18 days" not "received limited attention"
- Activities are not wins; outcomes with evidence are wins
- If a client went cold, say "cold"

**Tone example:**

> "[Month] was a 6/10. You shipped real work on [Client A] and [Client B] — models, numbers, customer confirmation — but ran at 61h/week for four consecutive weeks and never had the capacity conversation that would have prevented it. The same item appeared as 'the thing you're avoiding' in every weekly review. That's not a bad week; that's a pattern.
>
> [Client C]'s track drifted the entire month while other work got done. [Client D] has the analysis but no demo built. [Client E] barely exists in your calendar.
>
> Next month needs one thing above everything else: bring two clients to a resolved state — either a confirmed next stage or an explicit decision to deprioritize. Carrying eight active threads is why sustainability is a D."
