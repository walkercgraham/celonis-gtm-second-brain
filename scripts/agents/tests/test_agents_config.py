#!/usr/bin/env python3
"""Tests for check_agents.py. Run: python3 -m unittest discover scripts/agents"""
import json
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import check_agents  # noqa: E402


def agent(name, tools, body):
    return f"---\nname: {name}\ndescription: x\ntools: {', '.join(tools)}\nmodel: sonnet\n---\n\n{body}\n"


class RealRepoTest(unittest.TestCase):
    def test_repo_is_clean(self):
        problems = check_agents.check()
        if not os.path.isdir(os.path.join(check_agents.VAULT, ".claude", "agents")):
            self.skipTest("no .claude/agents/ directory yet")
        self.assertEqual(problems, [], "\n".join(problems))


class FixtureTest(unittest.TestCase):
    GMAIL, SLACK = "mcp__gmail-v2__search_threads", "mcp__slack__slack_search_public_and_private"

    def setUp(self):
        self.v = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.v, ".claude", "agents"))
        self.allow = ["Read", "Glob", "Grep", "Agent", "Bash(python3 *)", self.GMAIL, self.SLACK,
                      "mcp__gmail-v2__get_thread"]
        self.write_settings()

    def tearDown(self):
        shutil.rmtree(self.v)

    def write_settings(self):
        with open(os.path.join(self.v, ".claude", "settings.local.json"), "w") as fh:
            json.dump({"permissions": {"allow": self.allow}}, fh)

    def put(self, name, tools, body):
        with open(os.path.join(self.v, ".claude", "agents", f"{name}.md"), "w") as fh:
            fh.write(agent(name, tools, body))

    def test_sentinel_bug_is_caught(self):
        self.put("account-sentinel", ["Read", "Agent"], "Spawn one `account-analyst` per client.")
        self.put("account-analyst", ["Read", "Glob", "Grep"], "Read the client folder.")
        problems = check_agents.check(self.v)
        self.assertTrue(any("account-analyst" in p and self.GMAIL in p for p in problems), problems)

    def test_body_tool_missing_from_tools_line(self):
        self.put("x", ["Read"], f"Call `{self.GMAIL}` for each client.")
        self.assertTrue(any("not in `tools:`" in p for p in check_agents.check(self.v)))

    def test_unknown_subagent(self):
        self.put("x", ["Read", "Agent"], "Spawn one `ghost-agent` per item.")
        self.assertTrue(any("ghost-agent" in p for p in check_agents.check(self.v)))

    def test_tool_not_preapproved(self):
        self.put("x", ["Read", "mcp__slack__slack_send_message"], "Post once.")
        self.assertTrue(any("not allowed" in p for p in check_agents.check(self.v)))

    def test_server_level_allow_counts(self):
        self.allow.append("mcp__wispr-flow")
        self.write_settings()
        self.put("x", ["Read", "mcp__wispr-flow__get_meeting"], "Fetch with `mcp__wispr-flow__get_meeting`.")
        self.assertEqual(check_agents.check(self.v), [])

    def test_spawning_without_agent_tool(self):
        self.put("child", ["Read"], "child")
        self.put("x", ["Read"], "Spawn one `child` per item.")
        self.assertTrue(any("`Agent` is not in" in p for p in check_agents.check(self.v)))

    def test_clean_fixture(self):
        self.put("account-analyst", ["Read", self.GMAIL, self.SLACK], f"Use `{self.GMAIL}` and `{self.SLACK}`.")
        self.put("account-sentinel", ["Read", "Agent"], "Spawn one `account-analyst` per client; then the `critic` subagent.")
        self.put("critic", ["Read"], "Judge.")
        self.assertEqual(check_agents.check(self.v), [])


if __name__ == "__main__":
    unittest.main()
