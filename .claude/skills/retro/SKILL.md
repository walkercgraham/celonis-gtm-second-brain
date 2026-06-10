---
name: retro
description: Post-engagement retrospective for a client. Captures what worked, what didn't, reusable patterns
argument-hint: "[client-name]"
---

# Client Retrospective

Extract learnings from the **$ARGUMENTS** engagement before it fades.

## Steps

1. **Read the client hub file** at `02-areas/celonis/$ARGUMENTS/$ARGUMENTS.md`
   - Full engagement timeline
   - Hypotheses (which proved true/false?)
   - Wins & learnings already captured

2. **Read all meeting notes** from `02-areas/celonis/$ARGUMENTS/meetings/`
   - Chronological story of the engagement
   - Key turning points
   - Decisions that mattered

3. **Read stakeholder notes** from `02-areas/celonis/$ARGUMENTS/stakeholders/`
   - Who was helpful vs blocking?
   - Relationships that worked

4. **Analyze the engagement:**

### What Worked

**Approaches that landed:**
- What framings resonated with stakeholders?
- What demos/artifacts got traction?
- What objections did you handle well?

**Relationship moves:**
- Which stakeholder relationships were key?
- How did you build trust?
- What access did you earn and how?

**Technical wins:**
- What builds/demos were most effective?
- What data or analysis was most compelling?

### What Didn't Work

**Mistakes made:**
- What would you do differently?
- What took too long to figure out?
- What did you miss early that cost you later?

**Approaches that failed:**
- What framings fell flat?
- What stakeholders did you misjudge?
- What assumptions were wrong?

**Time sinks:**
- What consumed time without proportional value?
- What meetings were unnecessary?
- What should have been escalated earlier?

### Reusable Patterns

**For similar engagements:**
- Industry-specific insights (if applicable)
- Process/use case patterns that transfer
- Stakeholder archetypes and how to handle them

**Artifacts to reuse:**
- Demos that can be templated
- Decks or framings that worked
- Data models or technical approaches

**Questions to ask earlier next time:**
- What would have accelerated this engagement?
- What qualifying questions were missing?

### Honest Assessment

- **Overall:** Was this a success? Partial? Failure?
- **Your contribution:** What specifically did you do that mattered?
- **Luck vs skill:** What outcomes were your doing vs circumstances?

## Output

1. **Update the client hub file** `$ARGUMENTS.md`:
   - Add retrospective findings to "Key Wins & Learnings" section
   - Update status to `archived` or `complete`
   - Add final timeline entry

2. **Create a retro note** at `04-archive/$ARGUMENTS-retro.md` with full analysis

3. **Update relevant MOCs** in `03-resources/concepts/`:
   - If industry-specific learnings, add to relevant MOC
   - If process patterns, add to `_moc-celonis-client-work.md`

4. **Pattern expansion** — identify where this solution applies elsewhere:
   - Extract the primary use case/solution delivered in this engagement
   - Suggest: "Run `/pattern [delivered solution]` to find expansion opportunities across your portfolio and Celonis globally"
   - If the user agrees, run the pattern skill inline

5. **Output summary to screen** with:
   - Top 3 things that worked (reusable)
   - Top 3 mistakes (don't repeat)
   - One key insight for future engagements
   - Pattern expansion opportunity (which accounts could benefit from this solution)

**Tone example:**

> "[Client A] retro: The hypothesis confirmation was the win — you got customer validation before building anything. That's the pattern: don't build until they confirm the pain in their words.
>
> Mistake: You spent 3 weeks on technical complexity before [team-member] said to simplify. Should have asked 'what's the minimum we need for director readback?' on day 1.
>
> Reusable: The multi-thread approach (ops + IT + finance + digital) prevented single-contact ceiling. Use this on any enterprise deal with >[deal-value] potential."
