---
name: research
description: Unified deep discovery combining all 5 intelligence layers — vault, Knowledge Lake, Slack, external web research, and stakeholder research. Use before new engagements, discovery workshops, or positioning conversations when you need the complete picture.
argument-hint: "[client-name]"
---

# Unified Research — All 5 Intelligence Layers

Orchestrates a complete research brief by combining internal Celonis intelligence (Knowledge Lake + Slack + vault) with external public research (company + stakeholder). Produces a single document that makes you the most prepared person in any room.

## When to Use

- Before a **new client engagement** (first meeting, discovery workshop)
- When **refreshing context** on a dormant account that's reactivating
- Before a **high-stakes meeting** where you need maximum preparation
- When an **AE asks for positioning help** and you need full context fast

## Reference Materials

This skill composes methodology from two existing skills:
- `.claude/skills/external-research/` — company research patterns, search templates, source quality guide, industry research guide
- `.claude/skills/stakeholder-research/` — stakeholder research patterns, role guide, search templates

Read the reference files in those skill folders when executing Phases 2-3 below.

---

## Steps

### Phase 1: Internal Intelligence (Fast — No Web)

Run these in parallel. This phase should complete in under 60 seconds.

#### 1.1 Vault Context

1. Check if client folder exists at `02-areas/celonis/$ARGUMENTS/`
2. If exists:
   - Read hub file (`$ARGUMENTS.md`) — extract status, hypotheses, pain points, stakeholder table, engagement timeline
   - Read all stakeholder pages in `stakeholders/` — extract "What They Care About"
   - Read last 3 meeting notes in `meetings/` — extract decisions, outcomes, open items
   - Check `_current/open-loops.md` for items tagged `#client/$ARGUMENTS`
3. If not exists: note "No vault context — new account. Internal intel only."

#### 1.2 Knowledge Lake — Prior Engagement

```
search_knowledge(
  query: "[Company Name] engagement implementation project",
  topics: ["cortex_internal"],
  top_n: 10
)
```
→ Has Celonis worked with this company before? What was done? Outcomes?

#### 1.3 Knowledge Lake — Industry Intelligence

```
search_knowledge(
  query: "[Industry] [process areas] value opportunity inefficiency",
  topics: ["reasoning_external"],
  top_n: 10
)
```
→ Industry benchmarks, typical inefficiencies, value potential

#### 1.4 Knowledge Lake — Reference Customers

```
search_knowledge(
  query: "[Industry] [relevant use cases] success story customer results",
  topics: ["cortex_external"],
  top_n: 5
)
```
→ Publishable proof points from industry peers

#### 1.5 Knowledge Lake — Available Assets

```
search_knowledge(
  query: "[Industry] [process areas] demo value toolbox talk track",
  topics: ["ve"],
  top_n: 5
)
```
→ Existing demos, positioning materials, talk tracks

#### 1.6 Knowledge Lake — Competitive Positioning

Only if competitive landscape is known from vault or AE context:
```
search_knowledge(
  query: "[known competitors — e.g. ServiceNow, Signavio, UiPath]",
  topics: ["competitive"],
  top_n: 5
)
```

#### 1.7 Knowledge Lake — Delivery Playbooks

```
search_knowledge(
  query: "[process areas] implementation playbook delivery",
  topics: ["cs"],
  top_n: 3
)
```
→ How have similar implementations been delivered?

#### 1.8 Slack — Internal Signal

```
slack_search_public_and_private(
  query: "[Company Name]",
  sort: "timestamp",
  sort_dir: "desc",
  limit: 10
)
```
→ Who's been discussing this company? AE updates? Deal context? Recent activity?

Also search for internal experts:
```
slack_search_public_and_private(
  query: "[Industry] [key use case] after:[30 days ago]",
  sort: "timestamp",
  sort_dir: "desc",
  limit: 5
)
```
→ Who internally has relevant experience right now?

---

### Phase 2: External Company Research

Follow the methodology in `.claude/skills/external-research/SKILL.md`:

1. Read the skill's reference materials:
   - `references/industry_research_guide.yaml` — for industry-specific search patterns
   - `references/non_us_company_guide.yaml` — if non-US company
   - `references/search_query_templates.yaml` — for query ideas

2. Execute the external-research workflow:
   - Phase 1: Initial Discovery (5-7 DuckDuckGo searches)
   - Phase 2: Deep Dive (8-12 searches — earnings, annual reports, tech, competitive)
   - Phase 3: Validation & Gap-Filling
   - Follow all source tracking requirements (URL, status, quality rating)

3. Key outputs to extract:
   - Strategic priorities with evidence
   - Trigger events with dates
   - Technology signals (ERP, cloud, AI platform partner)
   - Competitive landscape
   - Financial context

**Minimum: 10-15 distinct sources**

---

### Phase 3: Stakeholder Research

Follow the methodology in `.claude/skills/stakeholder-research/SKILL.md`:

1. Identify key stakeholders:
   - From vault hub file (if exists) — stakeholder table
   - From Knowledge Lake results (if prior engagement)
   - From calendar (if upcoming meeting has attendees)
   - Ask if none identified: "Who's the primary contact or meeting attendee?"

2. For each stakeholder (top 2-3 max):
   - Run Phase 0 vault-first check (from enhanced stakeholder-research skill)
   - Execute stakeholder research workflow (LinkedIn snippets, executive bios, statements)
   - Generate: career background, likely priorities, pain points, engagement approach

3. Read `references/role_research_guide.yaml` for role-specific context

---

### Phase 4: Synthesis

Cross-reference all findings and generate recommendations:

1. **Positioning:** Given their strategic priorities + competitive landscape + Celonis reference customers → how to frame Celonis
2. **Use cases to lead with:** Match their pain points to Knowledge Lake reference implementations
3. **Proof points:** Select most relevant success stories (same industry, same use case, or same scale)
4. **Entry points:** For each stakeholder, what resonates given their priorities + role
5. **Risks:** Competitive threats, governance concerns, technical blockers
6. **Internal resources:** Who to pull in, what assets to use, what playbook to follow

---

## Output Format

```markdown
## Research Brief — [Client Name]
**Generated:** [date] | **Sources:** [N external] + Knowledge Lake + Slack + Vault

---

### Internal Intelligence

#### Prior Celonis Engagement
[Summary from cortex_internal — or "No prior engagement found"]

#### Industry Pattern Matches (Knowledge Lake)
| Use Case | Reference Customer | Outcome | Asset |
|----------|-------------------|---------|-------|
| [use case] | [customer] | [metric] | [Demo/Playbook/Story] |

#### Value Benchmarks
- [Process area]: [benchmark metric from reasoning_external]
- [Process area]: [benchmark metric]

#### Internal Experts & Signal
- **[Name]** — [context from Slack, e.g. "discussed similar implementation in #channel"]
- **Slack threads:** [any active discussions about this company]
- [or "No internal signal found"]

---

### Company Profile

| Field | Value | Source |
|-------|-------|--------|
| Industry | [industry] | [source] |
| Revenue | [revenue] | [source] |
| Employees | [count] | [source] |
| ERP | [system + migration status] | [source] |
| Cloud | [platform] | [source] |
| AI Platform | [partner + maturity] | [source] |

#### Strategic Priorities
1. **[Priority]** — "[evidence/quote]" — [source ref]
2. **[Priority]** — "[evidence]" — [source ref]
3. **[Priority]** — "[evidence]" — [source ref]

#### Trigger Events
| Event | Date | Celonis Relevance |
|-------|------|-------------------|
| [event] | [date] | [why this matters for positioning] |

#### Technology & AI Strategy
- **Platform partner:** [Microsoft/AWS/Google/etc]
- **AI maturity:** [None/Piloting/Scaling/Embedded]
- **Celonis angle:** [specific positioning given their tech choices — from KL competitive topic + external-research methodology]

#### Competitive Landscape
- **Process intelligence:** [Greenfield/Competitor — which one]
- **Adjacent solutions:** [what else they have — ServiceNow, UiPath, etc.]
- **Positioning:** [how to frame Celonis given this landscape]

---

### Key Stakeholders

| Name | Title | Priorities | Engagement Approach |
|------|-------|-----------|-------------------|
| [name] | [title] | [top 2 priorities] | [tone + topics to emphasize] |

[For primary stakeholder, include fuller profile:]

#### [Primary Stakeholder Name] — [Title]
- **Background:** [career summary]
- **Likely priorities:** [3-4 items with rationale]
- **Pain points:** [2-3 role + company specific]
- **Approach:** [tone, topics to emphasize, topics to avoid]
- **Internal intel:** [what Slack/vault reveals about this person]

---

### Synthesis & Recommendations

#### Positioning
[2-3 sentences: how to frame Celonis given ALL evidence — their strategy, tech stack, competitive landscape, and what Celonis has solved for similar companies]

#### Use Cases to Lead With
1. **[Use case]** — because [their priority/pain] aligns with [KL reference customer outcome]
2. **[Use case]** — because [stakeholder] cares about [X] and [proof point]

#### Proof Points to Reference
- **[Customer]** ([industry]) — [metric/outcome] — [relevance to this account]
- **[Customer]** — [metric] — [relevance]

#### Co-sell Opportunity
[If strategic partnership identified — e.g. "Strong Microsoft alignment — explore co-sell via [partner team]"]

#### Risks & Objections
- [Risk 1 — e.g. "Signavio already deployed in X area — will face incumbent objection"]
- [Risk 2 — e.g. "IT governance is strong — will need compliance story"]

#### Recommended Next Steps
1. [Specific action — who to contact, what to prepare]
2. [Specific action]
3. [Specific action]

---

### Sources
| # | Type | URL | Status | Key Info Extracted |
|---|------|-----|--------|-------------------|
| 1 | [type] | [url] | [Accessible/Blocked/Snippet] | [what was found] |
| ... | ... | ... | ... | ... |
```

---

## Output Destination

**Default:** Present to screen (formatted markdown).

**If asked to save:** Write to `02-areas/celonis/[client]/[client]-research-brief.md` with proper frontmatter:
```yaml
---
type: output
tags: [celonis, client/[client], research]
created: YYYY-MM-DD
modified: YYYY-MM-DD
status: active
related:
  - "[[client-name]]"
---
```

---

## Quality Rules

1. **Internal before external** — Phase 1 results should inform Phase 2 searches (e.g., if KL reveals they're a SAP shop, search for SAP-specific triggers)
2. **Source everything** — follow external-research source tracking standard. Every claim needs a footnote.
3. **Synthesis must be specific** — "position Celonis" is useless. "Lead with vendor inbox automation because [stakeholder] mentioned AP pain and [Customer X] achieved 40% reduction" is useful.
4. **Don't duplicate vault** — if hub file already has detailed hypotheses, reference them rather than restating
5. **Flag confidence gaps** — if KL returns nothing and web sources are sparse, say so. "Low confidence — limited public information. Recommend AE provide additional context."
6. **Time-bound** — this skill should complete in 10-15 minutes. Don't rabbit-hole into 30+ searches. The 80/20 rule applies.
