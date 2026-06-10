---
name: weekly-review
description: Weekly review and planning. Analyzes past week, spots patterns, plans next week. Run Sunday or Monday morning
---

# Weekly Review

Brutally honest week-level analysis. This is where patterns become visible.

## Steps

### Part 1: Gather Data

1. **Read all daily notes from the past 7 days** (`01-daily/`)
   - Compile: focus items planned vs completed
   - Compile: all meetings by client
   - Compile: captures and frustrations

2. **Read `_current/open-loops.md`**
   - What's overdue?
   - What's been sitting untouched for 2+ weeks?
   - What got completed this week?

3. **Read `_current/active-clients.md`**
   - Which clients got attention this week?
   - Which clients got zero touchpoints?

4. **Scan meeting notes created this week** (`02-areas/celonis/*/meetings/`)
   - What decisions were made?
   - What commitments were created?

### Part 2: Analyze Patterns

**Productivity Analysis:**
- Total focus items planned vs completed (percentage)
- **Total working hours for the week** — calculate from each day's start/finish time in the log
- **Total meeting hours for the week** — sum all meeting durations from the log (look for time patterns like "10-10:30am")
- Average meetings per day
- Days with >60% meeting time (flag these)
- Context switches per day average

**Client Health Dashboard:**
| Client | Touchpoints | Momentum | Risk |
|--------|-------------|----------|------|
For each active client:
- Touchpoints: meetings, updates, work done
- Momentum: advancing / stalled / slipping
- Risk: on track / needs attention / going cold

**Attention Allocation:**
- Where did time actually go vs. where it should go?
- Which clients are over-indexed? Under-indexed?
- Which high-value clients are being neglected?

**Pattern Detection:**
- What frustrated you multiple times this week?
- What got repeatedly pushed to "tomorrow"?
- What meetings could have been async?

### Part 3: Honest Assessment

Rate the week (be harsh):
- **Execution:** Did you do what you said you'd do?
- **Progress:** Did needle-moving work happen, or just activity?
- **Sustainability:** Could you maintain this pace? Energy level?

Call out:
- The thing you're avoiding (there's always one)
- The client/project that's drifting without you noticing
- The pattern that will hurt you if it continues

### Part 4: Plan Next Week

1. **Update `_current/this-week.md`:**
   - Set 3 focus areas (not 5, not 7 — three)
   - Key dates and deadlines
   - Carry forward any critical unfinished items

2. **Triage open-loops:**
   - What's actually urgent vs. feels urgent?
   - What can be dropped or delegated?
   - What's blocking multiple other things?

3. **Identify one habit to change:**
   - Based on patterns, what's one concrete change for next week?
   - Make it specific and measurable

## Output

Generate a weekly review note at `02-areas/celonis/_internal/reviews/YYYY-WXX-weekly.md` with:
- Week number and date range
- Completion stats including **total working hours** and **total meeting hours**
- Client health table
- Patterns spotted
- Honest assessment
- Next week's focus

Also output a summary to screen with the most important insights.

**Tone example:**

> "You touched 6 clients but made real progress on 2. [Client A] and [Client B] moved forward. [Client C] demo build got zero hours despite being due in 9 days. [Client D] has gone cold — no touchpoint since [date]. 
>
> Pattern: You're saying yes to every meeting and then wondering why builds don't happen. The working session you skipped Monday? That was the right call. Do more of that.
>
> Next week: [Client C] demo is the only thing that matters. Everything else is maintenance mode until [deadline]."
