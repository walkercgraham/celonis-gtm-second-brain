---
name: wins
description: Surface all wins from a time period. Use before promotion cases, annual reviews, or when you need a confidence boost
argument-hint: "[time period, e.g., Q1-2026, 2025, last-6-months]"
---

# Wins Extraction

Find all wins from **$ARGUMENTS** with evidence. No modesty allowed.

## Steps

1. **Parse the time period** from $ARGUMENTS:
   - "Q1-2026" → Jan 1 - Mar 31, 2026
   - "2025" → Full year
   - "last-6-months" → Calculate from today
   - If unclear, ask for clarification

2. **Scan all client hub files** (`02-areas/celonis/*/*.md`):
   - Look for "Key Wins" sections
   - Look for status changes (discovery → PoV → closed)
   - Look for confirmed hypotheses

3. **Scan all meeting notes** from the period:
   - Customer confirmations ("yes, that's exactly right")
   - Decisions made in your favor
   - Stakeholder praise or endorsement

4. **Scan engagement timelines** for:
   - Deals closed or advanced
   - Pipeline generated
   - Technical deliverables shipped

5. **Scan career/internal notes** (`02-areas/celonis/_internal/`):
   - Recognition received
   - Feedback from leadership
   - Cross-functional contributions

### Categorize Wins

**Revenue & Pipeline:**
- Deals closed (with amounts if known)
- Pipeline created or advanced
- Expansion opportunities opened

**Technical Delivery:**
- Demos built and delivered
- Solutions shipped
- Technical problems solved

**Customer Impact:**
- Customer-confirmed value (quotes if available)
- Problems solved for customers
- Relationships built

**Influence & Leadership:**
- People you helped or mentored
- Processes you improved
- Ideas that got adopted

**Personal Growth:**
- Skills developed
- Challenges overcome
- Stretch assignments completed

### Evidence Collection

For each win, capture:
- **What:** One-line description
- **When:** Date or date range
- **Evidence:** Specific proof (customer quote, metric, artifact)
- **Impact:** Why it mattered

## Output

Generate a wins document at `05-outputs/wins-$ARGUMENTS.md` with:
- Summary stats (X deals, $Y pipeline, Z deliverables)
- Categorized wins with evidence
- Highlight reel (top 5 most impressive)

Output to screen:
- Total wins count by category
- Top 5 wins with evidence
- Suggested framing for promotion/review conversations

**Tone:**

> "Q1 Wins: 12 total
>
> **Top 5:**
> 1. **[Client A] hypothesis confirmation** ([date]) — Customer validated core hypothesis in demo. Evidence: '[direct customer quote]' — [Stakeholder]. Impact: Unlocked [value] pipeline across [N] threads.
>
> 2. **[Client B] model accuracy milestone** ([date]) — Built solution in <1 day, validated by [stakeholder]. Evidence: '[customer quote]' — [Stakeholder]. Impact: Opened expansion opportunity.
>
> 3. **[Client C] solution handover** ([date]) — Transitioned ML solution to client team. Evidence: Successful UAT, clean handover. Impact: Proves delivery capability for enterprise accounts.
>
> **For your promotion case:** Lead with [Client A] (enterprise complexity, multi-thread strategy) and [Client B] (technical innovation, speed to value). Both have customer quotes as evidence."

## Promotion/Review Framing

Based on wins found, suggest:
- 3 talking points for manager conversations
- Evidence to reference for each point
- Gaps to acknowledge (what's missing for the next level?)
