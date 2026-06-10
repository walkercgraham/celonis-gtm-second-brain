---
type: concept
tags: [productivity, automation, workflow]
created: 2026-01-01
modified: 2026-01-01
status: active
related:
  - "[[knowledge-management-philosophy]]"
---

# Personal Productivity System

The automated productivity layer built on top of this vault. Integrates meeting transcripts, task management, calendar, and email into a unified daily workflow.

## The Automation Stack

| Automation | Schedule | Sources | Output |
|---|---|---|---|
| Morning Briefing | [Your timezone] daily | Calendar, Tasks, Meetings, Gmail | Draft email with day's priorities |
| Transcript → Tasks | 12:00 & 17:00 UTC | Meeting transcripts | New tasks (deduplicated) |
| Weekly Progress Summary | Friday morning | Tasks, Meetings, Calendar, Gmail | Draft email with weekly review |
| Weekly Memory Refresh | Weekly | All sources + memory files | REVIEW.md for manual approval |

## Design Principles

**Automation creates starting material, not finished goods.** Every automation outputs a draft for human review rather than auto-executing. The morning briefing is a draft email, not a sent one. The weekly memory refresh writes a REVIEW.md for approval, not direct memory updates. This inverts the typical automation pattern: the system proposes, the human disposes.

**Graceful degradation over hard failure.** When a source auth expires, the briefing pulls from alternative sources instead of failing entirely. Each source is additive, not required.

**Deduplication is a first-class concern.** The transcript-to-tasks automation checks existing tasks before creating new ones. Running twice produces the same result as running once. This matters when automations fire on schedule regardless of whether you've already processed things manually.

**Sub-2-minute scanning.** The morning briefing is structured for rapid consumption: schedule → priorities → meeting context → emails → first 3 actions. If it takes longer than 2 minutes to read, it's too long.

## Morning Briefing Structure

1. **Today's Schedule** — Chronological with RSVP flags and conflict detection
2. **Top Priorities** — P1-first grouping from task manager
3. **Key Context from Recent Meetings** — 3-5 action items/blockers
4. **Emails Needing Attention** — 2-3 high-priority messages
5. **First 3 Actions** — The most urgent things before anything else

The "First 3 Actions" concept is the most useful section. It forces prioritization into a concrete, actionable starting point for the day.

## Weekly Memory Refresh Logic

The memory refresh is the most nuanced automation. It scans a week of activity and generates suggestions, but applies a **high-confidence threshold**: fewer, higher-quality suggestions beat many low-quality ones.

Rules:
- New people must appear 2+ times or be key collaborators (skip one-off contacts, event organizers)
- Project updates must add genuinely new information (not just "still happening")
- Only flag stale items with no mentions in 4+ weeks
- System writes REVIEW.md; you approve changes before memory updates

## Open Tensions

- **Auth persistence** — recurring token expiry requires manual re-auth, breaking the automation chain
- **New session context loss** — each session starts fresh; persistent folder connection must be established before automations can access prior context
- **Notification mechanism** — email-as-interface works, but native notifications could reduce inbox noise
- **Twice-daily vs. continuous sync** — captures most meetings, but anything after EOD gets missed until next morning
