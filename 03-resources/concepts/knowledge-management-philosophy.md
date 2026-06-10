---
type: concept
tags: [knowledge-management, obsidian, framework, meta]
created: 2026-01-01
modified: 2026-01-01
status: active
related:
  - "[[personal-productivity-system]]"
---

# Knowledge Management Philosophy

The design principles behind this Obsidian vault, crystallized through building and iterating.

## Core Insight: Structure Serves Two Audiences

The vault isn't just your second brain — it's structured so that Claude can navigate it too. Every organizational decision serves dual purposes: human readability and agent discoverability. The CLAUDE.md routing table, the cockpit (`_current/`), the standardized frontmatter — all reduce ambiguity for both audiences.

## The Three-Layer Model

Three distinct persistence layers serve different purposes:

1. **Procedural Skills** — How-to guides that encode best practices (e.g., demo-script-generator, research skill). These are reusable methods, not data.
2. **Automated Tasks** — Recurring execution on schedule or trigger (e.g., morning briefing, transcript sync). These do work, not store knowledge.
3. **Persistent Memory** — Working knowledge that contextualizes all sessions (CLAUDE.md, memory/ folder, vault notes). This is the institutional knowledge layer.

The distinction matters because conflating them creates bloat. A procedure doesn't need to remember when it last ran. A memory doesn't need to know how to execute. A task doesn't need to be a reusable template.

## Design Principles

**Organize by purpose, not content type.** A file's location should answer "what is this for?" not "what format is it?" The folder structure reflects workflow stages, not file extensions.

**Discoverability through structure.** The first question — "where does this file live?" — should have an unambiguous answer. A routing table in CLAUDE.md ("if doing X, read Y, then edit Z") eliminates guessing. This matters most for agent sessions where there's no implicit knowledge of where things are.

**The cockpit is the entry point.** `_current/` contains the working memory: this week's focus, active clients, open loops. It's the first thing to check, the last thing to update. Everything else supports the cockpit.

**Client indexes are the source of truth.** Each client's hub file (`[client].md`) is the canonical reference. Meeting notes, stakeholder profiles, and deliverables are supporting documents. If the index contradicts a meeting note, the index wins (and should be updated).

**Evergreen over ephemeral.** The memory system stores context that will be useful in future conversations, not task details for the current one. "Client's $2B operational excellence target" is a memory. "Need to finish slide 5 today" is a task.

## The Vault as Onboarding Document

The most useful mental model: treat the vault like onboarding materials for a smart colleague who just joined. They need to know who the key people are, what the active projects are, what's been tried before, and what the local vocabulary means. They don't need to know the implementation details of last Tuesday's commit.

This framing guides what to write and what to skip:
- **Write:** decisions and their reasoning, stakeholder preferences, project context, terminology
- **Skip:** step-by-step execution logs, code diffs, things derivable from the repo

## Folder Philosophy

```
_current/     → What's happening now (cockpit)
00-inbox/     → Unsorted captures (temporary)
01-daily/     → Chronological spine (daily notes)
02-areas/     → Ongoing responsibilities (by domain)
03-resources/ → Reference material (evergreen)
04-archive/   → Completed work (searchable past)
05-outputs/   → Generated deliverables (shareable)
```

The separation of `02-areas/` (active, evolving) from `04-archive/` (complete, frozen) prevents folder bloat and keeps the active workspace focused. The rule "never delete, always archive" preserves searchability while maintaining clarity.

## Open Questions

- How to prevent the vault from becoming a write-only system? The weekly review helps, but linking passes and orphan detection need to be more systematic.
- Should concept notes (like this one) live in the vault or in the memory system? Currently they're vault-native, which means Claude has to read them rather than having them auto-loaded.
- The dual-audience problem: optimizing for Claude's navigation sometimes creates structure that feels over-engineered for human browsing. Where's the balance?
