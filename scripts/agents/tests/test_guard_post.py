#!/usr/bin/env python3
"""Tests for guard.py channel posts (outbox → workflow webhook). Run: python3 -m unittest discover scripts/agents"""
import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile
import time
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import guard  # noqa: E402

CFG = {"slack_self_user_id": "UEXAMPLE01", "slack_agent_channel_id": "CEXAMPLE01"}
PICK = "Why AI projects fail (Automotive Logistics, 2026-09-30) — start with the decision\nhttps://example.com/a"


class RenderTest(unittest.TestCase):
    def test_every_agent_template_has_action_and_mention(self):
        for agent, tpl in guard.SLACK_TEMPLATES.items():
            self.assertTrue(tpl.startswith("{notify_user} "), agent)
            self.assertIn("{action}", tpl, agent)

    def test_missing_fields_become_dash_and_user_is_added(self):
        payload, text = guard.render_post("opportunity-scout", {"headline": "2 ideas"}, CFG)
        self.assertEqual(payload, {"headline": "2 ideas", "ideas": "—", "action": "—", "notify_user": "UEXAMPLE01"})
        self.assertTrue(text.startswith("*Opportunity Scout* — 2 ideas"))
        self.assertNotIn("UEXAMPLE01", text)  # fallback posts as user: a self-mention is useless

    def test_unknown_field_rejected(self):
        with self.assertRaisesRegex(ValueError, "unknown field"):
            guard.render_post("loop-keeper", {"message": "hi"}, CFG)

    def test_mentions_in_fields_rejected(self):
        for bad in ("<@U123> look", "ping @here", "<!channel>", "see <#C123>"):
            with self.assertRaisesRegex(ValueError, "mention"):
                guard.render_post("ingestor", {"headline": bad}, CFG)

    def test_field_brief_picks_need_links(self):
        with self.assertRaisesRegex(ValueError, "pick_2 has no https"):
            guard.render_post("field-brief", {"pick_1": PICK, "pick_2": "No link here"}, CFG)
        payload, _ = guard.render_post("field-brief", {"pick_1": PICK, "pick_2": PICK, "pick_3": ""}, CFG)
        self.assertEqual(payload["pick_3"], "—")

    def test_account_watch_signals_need_links(self):
        line = "Client-A · ORG-WORKFORCE · HIGH — claims job cuts https://example.com/a"
        with self.assertRaisesRegex(ValueError, "signals line has no https"):
            guard.render_post("account-watch", {"signals": line + "\nClient-B · TECH-VENDOR · MED — no link"}, CFG)
        guard.render_post("account-watch", {"signals": line + "\n" + line}, CFG)
        guard.render_post("account-watch", {"signals": "none this run"}, CFG)
        payload, _ = guard.render_post("account-watch", {"headline": "quiet"}, CFG)
        self.assertEqual(payload["signals"], "—")

    def test_too_long_rejected(self):
        with self.assertRaisesRegex(ValueError, "chars"):
            guard.render_post("ingestor", {"accounts": "x" * 2000}, CFG)
        with self.assertRaisesRegex(ValueError, "lines"):
            guard.render_post("ingestor", {"accounts": "\n".join(["a"] * 30)}, CFG)

    def test_bad_user_id_rejected(self):
        with self.assertRaisesRegex(ValueError, "slack_self_user_id"):
            guard.render_post("ingestor", {}, {})


class OutboxTest(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.patches = [mock.patch.object(guard, "AGENTS_DIR", self.d),
                        mock.patch.object(guard, "OUTBOX", os.path.join(self.d, ".outbox")),
                        mock.patch.object(guard, "SECRETS", os.path.join(self.d, ".secrets"))]
        for p in self.patches:
            p.start()
        os.makedirs(os.path.join(self.d, ".outbox"))
        os.makedirs(os.path.join(self.d, ".secrets"))
        os.makedirs(os.path.join(self.d, "critic", "verdicts"))
        self.snap = {"started": (dt.datetime.now().astimezone() - dt.timedelta(minutes=5)).isoformat()}

    def tearDown(self):
        for p in self.patches:
            p.stop()
        shutil.rmtree(self.d)

    def draft(self, agent="loop-keeper", fields=None):
        with open(guard.outbox_path(agent), "w") as fh:
            json.dump(fields or {"headline": "closed 1", "action": "Nothing"}, fh)

    def verdict(self, first_line, agent="loop-keeper", age_minutes=0):
        f = os.path.join(self.d, "critic", "verdicts", f"{dt.date.today()}-{agent}.md")
        with open(f, "w") as fh:
            fh.write(first_line + "\n")
        t = time.time() - age_minutes * 60
        os.utime(f, (t, t))

    def secret(self, agent="loop-keeper", url="https://hooks.slack.com/triggers/E/1/x"):
        with open(os.path.join(self.d, ".secrets", f"slack_webhook_url.{agent}"), "w") as fh:
            fh.write(url + "\n")

    def test_pass_promotes_to_ready(self):
        self.draft()
        self.verdict("VERDICT: PASS")
        self.assertEqual(guard.settle_outbox("loop-keeper", self.snap, ok=True), "ready")
        self.assertTrue(os.path.exists(guard.outbox_path("loop-keeper", ready=True)))

    def test_fail_verdict_discards(self):
        self.draft()
        self.verdict("VERDICT: FAIL")
        self.assertIn("discarded", guard.settle_outbox("loop-keeper", self.snap, ok=True))
        self.assertFalse(os.path.exists(guard.outbox_path("loop-keeper", ready=True)))
        self.assertFalse(os.path.exists(guard.outbox_path("loop-keeper")))

    def test_old_pass_verdict_from_earlier_run_does_not_count(self):
        self.draft()
        self.verdict("VERDICT: PASS", age_minutes=60)
        self.assertIn("no verdict this run", guard.settle_outbox("loop-keeper", self.snap, ok=True))

    def test_revert_or_shadow_discards_even_on_pass(self):
        self.draft()
        self.verdict("VERDICT: PASS")
        self.assertIn("discarded", guard.settle_outbox("loop-keeper", self.snap, ok=False))

    def test_post_sends_once_via_workflow(self):
        self.draft()
        self.verdict("VERDICT: PASS")
        guard.settle_outbox("loop-keeper", self.snap, ok=True)
        self.secret()
        with mock.patch.object(guard, "send_webhook", return_value=None) as send:
            self.assertEqual(guard.cmd_post("loop-keeper", CFG), 0)
        url, payload = send.call_args[0]
        self.assertEqual(url, "https://hooks.slack.com/triggers/E/1/x")
        self.assertEqual(payload["notify_user"], "UEXAMPLE01")
        self.assertEqual(guard.cmd_post("loop-keeper", CFG), 2)  # nothing left to send

    def test_webhook_failure_prints_fallback(self):
        self.draft()
        self.verdict("VERDICT: PASS")
        guard.settle_outbox("loop-keeper", self.snap, ok=True)
        self.secret()
        with mock.patch.object(guard, "send_webhook", return_value="HTTP 500: boom"), \
                mock.patch("builtins.print") as out:
            self.assertEqual(guard.cmd_post("loop-keeper", CFG), 4)
        printed = "\n".join(str(c.args[0]) for c in out.call_args_list)
        self.assertIn("FALLBACK", printed)
        self.assertIn("*Loop Keeper* — closed 1", printed)

    def test_missing_secret_falls_back(self):
        self.draft()
        self.verdict("VERDICT: PASS")
        guard.settle_outbox("loop-keeper", self.snap, ok=True)
        with mock.patch("builtins.print"):
            self.assertEqual(guard.cmd_post("loop-keeper", CFG), 4)

    def test_non_slack_url_ignored(self):
        self.secret(url="https://evil.example.com/hook")
        self.assertIsNone(guard.webhook_url("loop-keeper"))

    def test_invalid_post_rejected_and_removed(self):
        self.draft(fields={"bogus": "x"})
        self.verdict("VERDICT: PASS")
        guard.settle_outbox("loop-keeper", self.snap, ok=True)
        with mock.patch("builtins.print"):
            self.assertEqual(guard.cmd_post("loop-keeper", CFG), 2)
        self.assertFalse(os.path.exists(guard.outbox_path("loop-keeper", ready=True)))


class DocsInStepTest(unittest.TestCase):
    """Every field an agent file tells the agent to write must exist in that agent's Slack template."""

    def test_agent_files_match_templates(self):
        for agent, tpl in guard.SLACK_TEMPLATES.items():
            fields = set(re.findall(r"{(\w+)}", tpl)) - {"notify_user"}
            agent_file = os.path.join(guard.VAULT, ".claude", "agents", f"{agent}.md")
            if not os.path.exists(agent_file):
                continue  # agent files may not be ported yet during development
            with open(agent_file, encoding="utf-8") as fh:
                body = fh.read()
            self.assertIn(f"_agents/.outbox/{agent}.json", body, agent)
            for f in fields:
                self.assertRegex(body, rf'"{f}"|`{f}`', f"{agent}.md never mentions field {f}")


if __name__ == "__main__":
    unittest.main()
