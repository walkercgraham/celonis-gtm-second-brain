#!/usr/bin/env python3
"""Tests for guard.py `require_verdict`: a run with no PASS verdict written this run never commits its work.
Run: python3 -m unittest discover scripts/agents"""
import datetime as dt
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import guard  # noqa: E402

AGENT = "account-watch"


class RequireVerdictTest(unittest.TestCase):
    def setUp(self):
        self.v = tempfile.mkdtemp()
        env = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
        self.env = mock.patch.dict(os.environ, env)
        self.env.start()
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=self.v, check=True)
        agents = os.path.join(self.v, "_agents")
        for d in (f"{AGENT}/shadow", "critic/verdicts"):
            os.makedirs(os.path.join(agents, d))
        self.write(f"_agents/{AGENT}/log.md", "# log\n")
        self.write("_current/agent-inbox.md", "## Today\n")
        self.write(f"_agents/{AGENT}/allowed-paths.txt", "shadow: _current/agent-inbox.md\n")
        subprocess.run(["git", "add", "-A"], cwd=self.v, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=self.v, check=True)
        self.patches = [mock.patch.object(guard, "VAULT", self.v),
                        mock.patch.object(guard, "AGENTS_DIR", agents),
                        mock.patch.object(guard, "LOCK", os.path.join(agents, ".lock")),
                        mock.patch.object(guard, "OUTBOX", os.path.join(agents, ".outbox")),
                        mock.patch.object(guard, "push", lambda *a, **k: None),
                        mock.patch("builtins.print")]
        for p in self.patches:
            p.start()
        self.cfg = {"allow_main": "true", "agents": {AGENT: {"mode": "shadow", "require_verdict": "true"}}}

    def tearDown(self):
        for p in reversed(self.patches):
            p.stop()
        self.env.stop()
        shutil.rmtree(self.v)

    def write(self, rel, text):
        full = os.path.join(self.v, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as fh:
            fh.write(text)

    def read(self, rel):
        with open(os.path.join(self.v, rel)) as fh:
            return fh.read()

    def run_agent(self, verdict=None):
        self.assertEqual(guard.cmd_start(AGENT, self.cfg), 0)
        self.write(f"_agents/{AGENT}/shadow/2026-10-21.md", "# shadow\n")
        self.write("_current/agent-inbox.md", "## Today\n### [account-watch] Shadow review\n")
        self.write(f"_agents/{AGENT}/log.md", "# log\n- run\n")
        if verdict:
            self.write(f"_agents/critic/verdicts/{dt.date.today()}-{AGENT}.md", verdict + "\n")
        return guard.cmd_finish(AGENT, self.cfg, revert=False, message=None)

    def last_commit(self):
        return subprocess.run(["git", "log", "-1", "--format=%s", "--name-only"], cwd=self.v,
                              capture_output=True, text=True).stdout

    def test_no_verdict_blocks_commit_of_work(self):
        self.assertEqual(self.run_agent(), 5)
        self.assertEqual(self.read("_current/agent-inbox.md"), "## Today\n")  # inbox entry reverted
        out = self.last_commit()
        self.assertIn("blocked: no verdict file this run", out)
        self.assertIn(f"_agents/{AGENT}/log.md", out)  # log and shadow kept for diagnosis
        self.assertNotIn("\n_current/agent-inbox.md", out)  # only its quarantine copy is committed

    def test_fail_verdict_blocks(self):
        self.assertEqual(self.run_agent("VERDICT: FAIL"), 5)
        self.assertIn("blocked: VERDICT: FAIL", self.last_commit())

    def test_pass_verdict_commits_everything(self):
        self.assertEqual(self.run_agent("VERDICT: PASS"), 0)
        out = self.last_commit()
        self.assertIn("— run", out)
        self.assertIn("_current/agent-inbox.md", out)
        self.assertIn(f"_agents/critic/verdicts/{dt.date.today()}-{AGENT}.md", out)

    def test_old_verdict_from_earlier_run_does_not_count(self):
        f = os.path.join(self.v, "_agents", "critic", "verdicts", f"{dt.date.today()}-{AGENT}.md")
        with open(f, "w") as fh:
            fh.write("VERDICT: PASS\n")
        old = (dt.datetime.now() - dt.timedelta(hours=1)).timestamp()
        os.utime(f, (old, old))
        subprocess.run(["git", "add", "-A"], cwd=self.v, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "old verdict"], cwd=self.v, check=True)
        self.assertEqual(self.run_agent(), 5)

    def test_agents_without_the_flag_are_unchanged(self):
        self.cfg["agents"][AGENT].pop("require_verdict")
        self.assertEqual(self.run_agent(), 0)
        self.assertIn("_current/agent-inbox.md", self.last_commit())


if __name__ == "__main__":
    unittest.main()
