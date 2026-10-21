# Agent System

An autonomous team of Claude Code agents that runs on schedules in the background, monitors your accounts, surfaces opportunities and risks, curates research, and keeps your vault in order — while you focus on client work.

## How It Works

1. Agents run on cron schedules via Claude Code scheduled tasks
2. Every run follows: `guard.py start` → work → critic QA → `guard.py finish` → `guard.py post`
3. The **critic** subagent runs 7 checks on every agent's output before it commits
4. **Shadow mode** writes only to `_agents/<agent>/shadow/` — review before going live
5. Agents propose actions to you through `_current/agent-inbox.md` (max 5 visible items)
6. Your checkmarks are carried out by chief-of-staff each morning

## The Agents

### Tier 1 — Foundation (vault + Google Calendar)

| Agent | Schedule | What it does |
|-------|----------|--------------|
| **chief-of-staff** | Daily 06:30 + Fri 17:00 + Sun 17:00 | Morning briefing, per-meeting prep, inbox management, weekly review/prep |
| **loop-keeper** | Daily 22:00 | Open-loops maintenance: extract tasks, dedup, flag overdue |
| **prep** | _(subagent of chief-of-staff)_ | Per-meeting briefing from vault + Knowledge Lake |
| **critic** | _(subagent of all agents)_ | 7-check QA on every run before commit |

### Tier 2 — Signal Intelligence (+ Gmail, Slack, Knowledge Lake)

| Agent | Schedule | What it does |
|-------|----------|--------------|
| **ingestor** | Daily 07:00 + 18:00 | Gmail/Slack signal pipeline → daily note timeline |
| **account-sentinel** | Fri 16:00 | RAG early-warning across all active accounts |
| **opportunity-scout** | Fri 15:00 | Finds reusable assets, cross-account patterns, career evidence gaps |
| **capture-keeper** | Hourly 08–20 weekdays | Files your Slack captures into vault |

### Tier 3 — External Research (+ WebSearch, WebFetch)

| Agent | Schedule | What it does |
|-------|----------|--------------|
| **field-brief** | Sun 20:00 | Enterprise AI research curation: 3 articles/week |
| **account-watch** | Mon/Wed/Fri 05:45 | Public-source monitoring: filings, press, vendors, jobs |

## Setup

### Prerequisites

- Claude Code with scheduled tasks support
- MCP servers configured (progressively):
  - **Tier 1:** Google Calendar (+ optionally Knowledge Lake for prep)
  - **Tier 2:** + Gmail, Slack, Knowledge Lake
  - **Tier 3:** + WebSearch, WebFetch

### Quick Start

1. **Copy the config template:**
   ```bash
   cp _agents/config-template.yaml _agents/config.yaml
   ```

2. **Fill in your details** in `_agents/config.yaml`:
   - `owner.name`, `owner.role`, `owner.timezone`
   - `slack_self_user_id` — your Slack member ID (profile → ⋯ → Copy member ID)
   - `slack_agent_channel_id` — create a private channel for agent output
   - `slack_capture_channel_id` — create a channel for quick captures (voice memos, thoughts)
   - `vault_path` — absolute path to this vault

3. **Copy the regions template** (for account-watch):
   ```bash
   cp _agents/account-watch/regions-template.yaml _agents/account-watch/regions.yaml
   ```
   Activate your regions by setting `mode: active` on the ones you need.

4. **Add agent fields to client hubs.** Every client hub (`02-areas/celonis/<client>/<client>.md`) needs:
   ```yaml
   email_domains: [example.com]     # Gmail domain(s)
   slack_channels: [C0123456789]    # Slack channel ID(s)
   slack_keywords: ["Client Name"]  # DM search terms
   region: uk                       # Region code from regions.yaml
   involvement: lead                # lead | consultative
   ```

5. **Register scheduled tasks** — see `_agents/scheduled-tasks.md` for the full list and cron expressions.

6. **Start in shadow mode.** All agents default to `mode: shadow` in the config. Shadow runs write to `_agents/<agent>/shadow/` only. Review shadow output for 1–2 weeks. When you're satisfied, switch agents to `mode: live` one tier at a time.

### Progressive Enablement

Start with Tier 1. Once those agents produce good shadow output for a week, enable Tier 2 (which requires Gmail + Slack + Knowledge Lake MCP). Then Tier 3 (WebSearch + WebFetch).

## Key Files

| File | What it is |
|------|------------|
| `AGENTS.md` | Charter read by every agent (decision rights, output contract, run protocol) |
| `_agents/config.yaml` | Your personal config (from `config-template.yaml`; gitignored) |
| `_current/agent-inbox.md` | Where agents write proposals; you ✅ or ❌ them |
| `.claude/agents/*.md` | Individual agent definitions |
| `_agents/<agent>/allowed-paths.txt` | Path enforcement per agent |
| `_agents/<agent>/log.md` | Each agent's run history |
| `scripts/agents/guard.py` | Safety infra: locking, git commits, path enforcement, Slack posting |
| `_agents/account-watch/regions.yaml` | Your region packs for account-watch (from template; gitignored) |
| `_agents/scheduled-tasks.md` | Schedule reference with cron expressions |

## Safety Model

- **Decision rights:** Level 5 = autonomous (write inside own folder), Level 4 = must propose (changes to vault files need your ✅)
- **Path enforcement:** Each agent has `allowed-paths.txt` listing exactly which files it may write
- **Guard system:** `guard.py` manages file locking, git commits, and rejects writes outside allowed paths
- **Critic QA:** Independent subagent checks every run for citations, decision rights, external leaks, proportionality
- **Shadow mode:** New agents/users start in shadow — output goes to `_agents/<agent>/shadow/`, nothing touches the vault
- **Inbox cap:** Max 5 items in `## Today` — excess is folded to `## Below the fold` by chief-of-staff

## The Agent Inbox

`_current/agent-inbox.md` is how agents communicate with you. Each entry has:
- What the agent did/found
- Why it matters
- Risk and how to undo
- Options with exactly what happens on ✅
- Your verdict: `✅` or `❌` with a reason

Check it each morning. Chief-of-staff processes your verdicts and carries out the ✅'d actions.

## Troubleshooting

- **Agent didn't run:** Check `_agents/<agent>/log.md` for errors. Common: MCP server not connected, another agent holds the lock.
- **Guard exit 2:** Another agent is running (lock held). The agent will retry next schedule.
- **Critic FAIL:** The run is reverted. Check `_agents/critic/verdicts/` for the reason. The agent learns from it on the next run.
- **No Slack posts:** Verify `slack_agent_channel_id` in config and that the Slack MCP server is connected.
- **Shadow output looks wrong:** That's the point of shadow mode. ❌ the shadow review entry with a reason — the agent reads your reasons and adjusts.
