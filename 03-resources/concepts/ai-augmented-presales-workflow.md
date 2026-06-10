---
type: concept
tags: [celonis, presales, ai, workflow, framework]
created: 2026-01-01
modified: 2026-01-01
status: active
related:
  - "[[knowledge-management-philosophy]]"
---

# AI-Augmented Presales Workflow

A framework for using Claude as a presales co-pilot across client engagements.

## The Core Idea

Treat presales deliverables as **reproducible outputs** generated from structured source data (Account Briefs), not as one-off documents crafted from scratch each time. A single Account Brief feeds multiple generators that produce 7+ deliverables per engagement.

## The Deliverable Pipeline

```
Account Brief (source of truth)
    ├── Hypothesis Generator → 3-5 scored pain hypotheses
    ├── Storyline Creator → 6-part narrative arc
    ├── Pitch Deck Creator → JSON slide manifest → PPTX
    ├── Demo Storyline → View-by-view demo sequence
    ├── Enablement Pack → Interactive HTML for AE prep
    ├── One-Pagers → Company + stakeholder summaries
    └── Demo Script → Talk track with [Tell]/[Show] annotations
```

## Key Principles

**Hypotheses drive everything.** The hook and demo anchor are selected from scored hypotheses, not invented independently. Use the customer's own words about their priorities — anchoring the narrative in their stated goals, not yours.

**Storyline is capability-agnostic.** The 6-part story (hook → problem → impact → vision → proof → CTA) doesn't mention Celonis features. It frames the problem in terms the customer already cares about. Features appear only when demonstrating proof.

**Pre-filling signals competence.** Walk into discovery with pre-drawn process maps, pre-seeded pain point lists, and pre-filled technical data matrices. This accelerates collaboration and earns trust — the customer sees you've done homework, not that you're fishing.

**Two-phase discovery is now standard:**
1. **Strategic discovery** (executive audience) — Frame the problem, align on business impact, validate hypotheses
2. **Operational discovery** (engineer audience) — Map end-to-end processes, pinpoint pain, collect technical data

Strategic outputs feed into operational discovery as pre-seeded materials. Operational findings feed into a director readback package for upward translation.

## The Engagement Sequence

```
Research → Hypotheses → Strategic Demo → Operational Discovery → Director Readback → Executive Sponsorship
```

Each step produces artifacts that feed the next. The director readback is the critical gate to VP access — every output must be packaged for upward translation.

## Demo Scripting Lessons

**Presenter notes bridge reality gaps.** The demo environment rarely matches the customer's exact situation. Use `[Presenter note]` annotations to connect visible KPIs to customer-specific impact stories.

**Clickpath precision matters.** Every click instruction must match the actual demo environment. One wrong reference and credibility evaporates. When the script says "click Emergency Rate" but the dashboard shows "On-Time Completion," fix the script — don't hope no one notices.

**Persona-to-capability mapping** makes architecture human-centered. Tie each process step to a real job role, grounding abstract platform capabilities in recognizable daily workflows.

## What This Isn't

This workflow generates high-quality starting material for experienced AEs and VEs. It doesn't replace judgment about which hypotheses to lead with, how to read a room, or when to deviate from the script. The automation creates drafts; the human creates the relationship.
