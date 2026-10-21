#!/usr/bin/env python3
"""Static checks for the agent team. Standard library only. Run after editing anything in .claude/agents/.

    python3 scripts/agents/check_agents.py          exit 0 = clean, 1 = problems (listed)

Checks
1. Every `mcp__…` tool named in an agent's body is in that agent's own `tools:` line
   (a subagent gets exactly its own tools; it inherits nothing from its parent).
2. Every subagent an agent spawns exists as an agent file (or is a built-in type).
3. Every tool in any `tools:` line is allowed in .claude/settings.local.json, so unattended runs never stop on a prompt.
4. Subagents that fetch their own connector data have the Gmail and Slack tools.
"""
import json
import os
import re
import sys

VAULT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BUILTIN_AGENTS = {"general-purpose", "Explore", "Plan", "claude"}
CONNECTOR_SUBAGENTS = {  # subagent -> tools it must have because it fetches its own client data
    "account-analyst": {"mcp__gmail-v2__search_threads", "mcp__slack__slack_search_public_and_private"},
    "account-ingestor": {"mcp__gmail-v2__search_threads", "mcp__gmail-v2__get_thread",
                         "mcp__slack__slack_search_public_and_private"},
    "prep": {"mcp__gmail-v2__search_threads", "mcp__slack__slack_search_public_and_private"},
}
MCP_RE = re.compile(r"\bmcp__[a-z0-9-]+__[a-z0-9_]+")
SPAWN_RES = [
    re.compile(r"subagent_type:\s*`?([A-Za-z0-9_-]+)`?"),
    re.compile(r"[Ss]pawn(?:s|ing)?\s+(?:the\s+|one\s+|ONE\s+|a\s+)?`([A-Za-z0-9_-]+)`"),
    re.compile(r"`([A-Za-z0-9_-]+)`\s+subagents?\b"),
]


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def parse_agent(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return None, [], text
    fm, body = m.group(1), m.group(2)
    name = re.search(r"^name:\s*(.+)$", fm, re.M)
    tools = re.search(r"^tools:\s*(.+)$", fm, re.M)
    tool_list = [t.strip() for t in tools.group(1).split(",")] if tools else []
    return (name.group(1).strip() if name else None), tool_list, body


def load_agents(vault):
    d = os.path.join(vault, ".claude", "agents")
    agents = {}
    for f in sorted(os.listdir(d)):
        if f.endswith(".md"):
            name, tools, body = parse_agent(_read(os.path.join(d, f)))
            agents[name or f[:-3]] = {"file": f".claude/agents/{f}", "tools": tools, "body": body}
    return agents


def allowed(tool, allow):
    if tool in allow:
        return True
    if tool.startswith("mcp__"):
        server = "__".join(tool.split("__")[:2])
        return server in allow
    if tool == "Bash":
        return any(a.startswith("Bash(") for a in allow)
    return False


def check(vault=VAULT):
    problems = []
    agents = load_agents(vault)
    settings_path = os.path.join(vault, ".claude", "settings.local.json")
    allow = set(json.loads(_read(settings_path)).get("permissions", {}).get("allow", [])) \
        if os.path.exists(settings_path) else set()
    for name, a in agents.items():
        tools = set(a["tools"])
        # 1. tools named in the body must be in the agent's own tools line
        for t in sorted(set(MCP_RE.findall(a["body"]))):
            if t not in tools:
                problems.append(f"{a['file']}: body uses {t} but it is not in `tools:` (the agent can't call it)")
        # 2. spawned subagents must exist
        spawned = set()
        for rx in SPAWN_RES:
            spawned |= set(rx.findall(a["body"]))
        for s in sorted(spawned):
            if s not in agents and s not in BUILTIN_AGENTS:
                problems.append(f"{a['file']}: spawns `{s}`, which is not an agent file in .claude/agents/")
        if spawned - BUILTIN_AGENTS - {"critic"} and "Agent" not in tools and name != "critic":
            problems.append(f"{a['file']}: spawns subagents but `Agent` is not in `tools:`")
        # 3. every tool must be pre-approved for unattended runs
        for t in a["tools"]:
            if not allowed(t, allow):
                problems.append(f"{a['file']}: tool {t} is not allowed in .claude/settings.local.json (runs would prompt)")
    # 4. connector-fetching subagents
    for sub, need in CONNECTOR_SUBAGENTS.items():
        if sub in agents:
            missing = need - set(agents[sub]["tools"])
            for t in sorted(missing):
                problems.append(f"{agents[sub]['file']}: fetches its own connector data but lacks {t}")
    return problems


def main():
    problems = check()
    if problems:
        print(f"check_agents: {len(problems)} problem(s)")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("check_agents: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
