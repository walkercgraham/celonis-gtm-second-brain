---
name: pattern
description: Cross-account + cross-Celonis intelligence. Bidirectional pattern matching — "I solved X, where else?" (push) or "I'm prepping for Y, what's relevant?" (pull). Searches vault, Knowledge Lake, and Slack in parallel.
argument-hint: "[use-case description or client-name]"
---

# Pattern Intelligence

Find where a solution, use case, or capability applies across your portfolio AND the entire Celonis customer base. Works bidirectionally:

- **Push mode:** "spare parts copilot" → finds all accounts (yours + global) with this pain
- **Pull mode:** "anglo-american" → finds what you've solved elsewhere that's relevant to their known pain points

## Detect Mode from Input

**Push mode** (default): Input describes a use case, solution, or capability.
Examples: "spare parts copilot", "vendor inbox automation", "dunning AI", "Monte Carlo inventory"

**Pull mode**: Input is a client name (matches a folder in `02-areas/celonis/`).
Examples: "anglo-american", "barclays", "standard-bank"

If ambiguous, ask: "Are you looking for where [X] can be applied (push), or what's relevant for [X] (pull)?"

---

## Steps

### Step 0: Determine Mode and Build Search Context

**If push mode:**
- `search_terms` = the use case description provided
- `industry_terms` = infer relevant industries (manufacturing, mining, financial services, etc.)
- `process_terms` = infer process area (procurement, AP/AR, inventory, ITSM, O2C, P2P)

**If pull mode:**
1. Read the client hub file at `02-areas/celonis/$ARGUMENTS/$ARGUMENTS.md`
2. Extract: active hypotheses, pain points, use cases mentioned, industry, process areas
3. Build `search_terms` from their documented pain points and hypotheses
4. `industry_terms` = their industry
5. `process_terms` = their relevant process areas

---

### Step 1: Vault Search (Your Portfolio)

1. Read `03-resources/concepts/_moc-ai-use-cases.md`
   - Find matching use case categories
   - Extract the pattern table for each match (Account, Status, Specifics)
   - Note the "Pattern:" summary

2. Search client hub files across `02-areas/celonis/*/`:
   - Grep for `search_terms` keywords in hub files
   - For each match: read the hub's hypotheses section and status
   - Note which stakeholder cares about this (from stakeholder pages if available)

3. Check meeting notes for relevant discussions:
   - Grep across `02-areas/celonis/*/meetings/` for keywords
   - Extract any decisions or outcomes related to this use case

**Compile vault matches** with: Account, Status, Entry Point (specific angle), Stakeholder (who cares + why)

---

### Step 2: Knowledge Lake Search (All Celonis Globally)

Run these searches in parallel:

1. **Past engagements:**
   ```
   search_knowledge(
     query: "[search_terms] [industry_terms] implementation customer engagement",
     topics: ["cortex_internal"],
     top_n: 10
   )
   ```

2. **Available assets (demos, toolbox, talk tracks):**
   ```
   search_knowledge(
     query: "[search_terms] [process_terms] demo value toolbox",
     topics: ["ve"],
     top_n: 5
   )
   ```

3. **Success stories with metrics:**
   ```
   search_knowledge(
     query: "[search_terms] [industry_terms] success story results metrics",
     topics: ["cortex_external"],
     top_n: 5
   )
   ```

4. **Value benchmarks:**
   ```
   search_knowledge(
     query: "[process_terms] value opportunity inefficiency benchmark",
     topics: ["reasoning_external"],
     top_n: 5
   )
   ```

**From results, extract:**
- Customer name, region, what they did, outcome/metrics
- Best reference implementation (most detailed — approach, timeline, proof point)
- Available demos or toolbox assets
- Industry benchmarks (e.g. "15-30% maverick spend reduction typical in manufacturing procurement")

---

### Step 3: Slack Search (Real-Time Internal Signal)

1. **Use case discussions:**
   ```
   slack_search_public_and_private(
     query: "[search_terms] [process_terms]",
     sort: "timestamp",
     sort_dir: "desc",
     limit: 10
   )
   ```

2. **If pull mode, also search for client name:**
   ```
   slack_search_public_and_private(
     query: "[client-name]",
     sort: "timestamp",
     sort_dir: "desc",
     limit: 5
   )
   ```

**From results, extract:**
- Who posted (name, role if identifiable)
- Channel and date
- Context (1-line summary of what they discussed)
- Whether it's an active thread worth following

---

### Step 4: Synthesize Output

Structure the output as follows:

```markdown
## Pattern Match — [Use Case / Client Name]

### Your Portfolio
| Account | Status | Entry Point | Who to Talk To |
|---------|--------|-------------|----------------|
| [[account]] | [from MOC/hub] | [specific angle] | [[stakeholder]] — cares about [X] |

**Pattern:** [from MOC "Pattern:" field, or synthesized from hub matches]

### Celonis Global (Knowledge Lake)
| Customer | Region | What They Did | Outcome |
|----------|--------|---------------|---------|
| [name] | [region] | [brief description] | [metric if available] |

**Best reference:** [Most detailed result — describe the implementation approach, timeline, architecture if available. This is what you'd reference in a conversation.]

### Available Assets
- **Demo:** [name/description from VE topic, or "None found"]
- **Success story:** [from cortex_external — customer + metric]
- **Value benchmark:** [from reasoning_external — industry/process benchmark]
- **Playbook:** [from cs topic if relevant]

### Internal Experts (Slack)
- **[Name]** discussed this in #[channel] ([date]) — [1-line context]
- **Active thread:** [if found — channel + topic + whether worth joining]
- [or "No recent Slack activity found for this topic"]

### Positioning by Account
[For each account in "Your Portfolio" that isn't already delivered:]
- **[[Account]]:** Lead with [specific angle] because [[stakeholder]] cares about [X]. Reference [specific proof point from KL or your own delivery]. Use [specific asset if available].
```

---

## Quality Rules

1. **Vault matches must be specific** — don't just say "pain identified". Include which stakeholder cares and what the specific entry point is.
2. **KL results must add value beyond vault** — if Knowledge Lake only returns your own accounts, note "No additional global matches" rather than duplicating vault results.
3. **Slack results must be recent** — only include discussions from the last 60 days. Older threads are stale signal.
4. **Positioning must be actionable** — each account recommendation should name a specific person, a specific angle, and a specific proof point. Generic "position Celonis" statements are useless.
5. **If pull mode returns nothing** — say so clearly: "No pattern matches found for [client]'s pain points. Consider running /research [client] to gather external intelligence first."

---

## Integration

- After `/retro`: Run `/pattern` with the delivered solution to find expansion opportunities
- Before `/prep`: If preparing for a client where you're positioning a new use case, run `/pattern` first for proof points
- During `/1-1`: Reference pattern matches when discussing pipeline expansion with [manager-name]
