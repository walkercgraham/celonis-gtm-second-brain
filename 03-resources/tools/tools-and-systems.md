---
type: area
tags: [tools, obsidian, claude-code, systems]
created: 2026-01-01
modified: 2026-01-01
status: active
related: []
---

# Tools & Systems

## Recommended Tech Stack
| Tool | Purpose |
|---|---|
| **Obsidian** | Knowledge and context (this vault) |
| **Claude Code** | Reasoning layer; reads/writes vault directly |
| **Granola** (or equivalent) | Meeting transcripts (feeds into Obsidian) |
| **Google Calendar** | Scheduling |
| **Slack / Email** | Transient communication (feeds into Obsidian, not a system of record) |

## Obsidian Setup
- **Vault approach:** Local markdown files. Claude Code reads/writes directly.
- **Sync options:** Git, iCloud, or Dropbox (for cross-device)
- **Methodology:** PARA-adjacent (Projects, Areas, Resources, Archive) + Maps of Content
- **Key principle:** Start with blank daily notes and inbox. Let Claude Code add structure retroactively in batches. Don't enforce templates at point of creation — that's overhead for a beginner.
- **Recommended plugins:** Periodic Notes, Templater, QuickAdd, Dataview, Calendar, Omnisearch, Kanban
- **Daily note = keystone habit.** Everything else is optional scaffolding. Create every morning with 3 priorities, fill in reflection every evening. Miss a day → don't stress. Miss a week → system is dead.

## Claude Code Setup
- Install Claude Code CLI or use the desktop app
- Point it at this vault directory
- The CLAUDE.md file provides all routing instructions
- Skills in `.claude/skills/` provide specialized workflows

## Sharing Knowledge with Colleagues
- Strongest option: Git-backed shared vault per account
- Pragmatic middle ground: Claude Code generates shareable outputs (docs, slides) for AEs unwilling to adopt new tools
- Shared knowledge base via MCP connections for collaborative accounts

## Other Useful Tools
- **Jarvis** — Celonis internal tool for building custom demos
- **Make (Integromat)** — Useful for parsing agent output in automation workflows
- **Supabase MCP connector** — Conversational schema design, data exploration
