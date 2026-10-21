#!/usr/bin/env python3
"""Tests for account_watch_promote.py. Run: python3 -m unittest discover scripts/agents"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import account_watch_promote as awp  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(os.path.dirname(os.path.dirname(HERE)), "03-resources", "templates",
                        "external-research-template.md")

SHADOW = """---
type: resource
tags: [agents, shadow, account-watch]
---

# account-watch shadow 2026-10-26

## → 02-areas/celonis/client-a/client-a-external-research.md
### [1] 2026-10-23 · ORG-WORKFORCE · RISK · HIGH
**Client A to cut claims roles**
- **Facts:** ~500 roles.
- **Source:** [Reuters, 2026-10-22](https://example.com/a) · S7 · tier 3 · region uk
- **What it means for Celonis:** Budget/timing — freeze risk.
- **Suggested action:** raise with the AE.
<!-- key: client-a|ORG-WORKFORCE|2026-10|claims roles -->

### [2] 2026-10-25 · STRAT-TARGET · OPP · MEDIUM
**Client A sets £250m cost-out target**
- **Facts:** £250m by 2027.
- **Source:** [Client A, 2026-10-25](https://example.com/b) · S2 · tier 1 · region uk
- **What it means for Celonis:** Value case — anchor the PoV on it.
- **Suggested action:** quote it in the blueprint.
- **Quotes:** "We will take out £250m" (CFO, Q3 trading update)
<!-- key: client-a|STRAT-TARGET|2026-10|250m cost-out -->

## → 02-areas/celonis/client-b/client-b-external-research.md
### [3] 2026-10-24 · LEADER · NEUTRAL · HIGH
**New CFO**
- **Source:** [X, 2026-10-24](https://example.com/c) · S3 · tier 1 · region gcc-sa
<!-- key: client-b|LEADER|2026-10|cfo -->

## Accounts checked
- client-a: 6 searches
"""


class PromoteTest(unittest.TestCase):
    def setUp(self):
        self.v = tempfile.mkdtemp()
        for slug, status in (("client-a", "active"), ("client-b", "context")):
            d = os.path.join(self.v, "02-areas", "celonis", slug)
            os.makedirs(d)
            with open(os.path.join(d, f"{slug}.md"), "w") as fh:
                fh.write(f'---\ntype: area\nclient: "{slug.replace("-", " ").title()}"\nstatus: {status}\n---\n\n# {slug}\n')
        os.makedirs(os.path.join(self.v, "03-resources", "templates"))
        if os.path.exists(TEMPLATE):
            shutil.copy(TEMPLATE, os.path.join(self.v, "03-resources", "templates"))
        else:
            with open(os.path.join(self.v, "03-resources", "templates", "external-research-template.md"), "w") as fh:
                fh.write("---\ntype: resource\ntags: [celonis, client/{{slug}}, external-research]\n"
                         "created: {{date}}\nmodified: {{date}}\nlast_checked: {{date}}\nstatus: active\n"
                         "related:\n  - \"[[{{slug}}]]\"\n---\n\n# {{title}}: external research\n\n"
                         "## Signals (newest first)\n\n## Quote bank\n")
        agent = os.path.join(self.v, "_agents", "account-watch", "shadow")
        os.makedirs(agent)
        self.shadow = os.path.join(agent, "2026-10-26.md")
        with open(self.shadow, "w") as fh:
            fh.write(SHADOW)
        with open(os.path.join(self.v, "_agents", "account-watch", "state.json"), "w") as fh:
            json.dump({"last_run": None, "accounts": {}, "event_keys": {
                "client-a|ORG-WORKFORCE|2026-10|claims roles": {"first_seen": "2026-10-23", "mode": "shadow"}}}, fh)
        with open(os.path.join(self.v, "_agents", "account-watch", "log.md"), "w") as fh:
            fh.write("# log\n\n## Rejected signals (do not re-raise)\n<!-- format -->\n\n## Runs\n")
        self.research = os.path.join(self.v, "02-areas", "celonis", "client-a", "client-a-external-research.md")

    def tearDown(self):
        shutil.rmtree(self.v)

    def run_promote(self, **kw):
        kw.setdefault("commit", False)
        return awp.promote(self.v, self.shadow, today="2026-10-27", **kw)

    def read(self, path):
        with open(path) as fh:
            return fh.read()

    def test_parse_numbers_paths_and_keys(self):
        es = awp.parse_shadow(SHADOW)
        self.assertEqual([e["n"] for e in es], [1, 2, 3])
        self.assertEqual(es[0]["slug"], "client-a")
        self.assertTrue(es[0]["body"].startswith("### 2026-10-23 · ORG-WORKFORCE"))
        self.assertNotIn("[1]", es[0]["body"])
        self.assertEqual(es[2]["key"], "client-b|LEADER|2026-10|cfo")
        self.assertNotIn("Accounts checked", es[2]["body"])

    def test_creates_from_template_newest_first_with_quotes(self):
        s = self.run_promote()
        self.assertEqual(s["promoted"], [1, 2])
        text = self.read(self.research)
        self.assertIn("tags: [celonis, client/client-a, external-research]", text)
        self.assertIn("# Client A: external research", text)
        self.assertIn("last_checked: 2026-10-27", text)
        self.assertLess(text.index("2026-10-25 · STRAT-TARGET"), text.index("2026-10-23 · ORG-WORKFORCE"))
        self.assertLess(text.index("## Signals"), text.index("2026-10-25 · STRAT-TARGET"))
        self.assertLess(text.index("2026-10-23 · ORG-WORKFORCE"), text.index("## Quote bank"))
        self.assertIn('- "We will take out £250m" (CFO, Q3 trading update), 2026-10-25 ([source](https://example.com/b))',
                      text.split("## Quote bank", 1)[1])

    def test_refuses_inactive_hub(self):
        s = self.run_promote()
        self.assertEqual(s["refused_inactive"], ["[3] client-b"])
        self.assertFalse(os.path.exists(os.path.join(self.v, "02-areas", "celonis", "client-b",
                                                     "client-b-external-research.md")))

    def test_except_skips_and_logs_reason(self):
        s = self.run_promote(exclude=[1], reason="wrong client")
        self.assertEqual(s["promoted"], [2])
        self.assertNotIn("ORG-WORKFORCE", self.read(self.research))
        log = self.read(os.path.join(self.v, "_agents", "account-watch", "log.md"))
        self.assertIn("- client-a|ORG-WORKFORCE|2026-10|claims roles — 2026-10-27 — wrong client", log)
        self.assertLess(log.index("wrong client"), log.index("## Runs"))

    def test_unknown_except_number_rejected(self):
        with self.assertRaises(SystemExit):
            self.run_promote(exclude=[9])

    def test_state_keys_flip_to_live(self):
        self.run_promote()
        st = json.loads(self.read(os.path.join(self.v, "_agents", "account-watch", "state.json")))
        k = st["event_keys"]["client-a|ORG-WORKFORCE|2026-10|claims roles"]
        self.assertEqual(k["mode"], "live")
        self.assertEqual(k["path"], "02-areas/celonis/client-a/client-a-external-research.md")
        self.assertNotIn("client-b|LEADER|2026-10|cfo", st["event_keys"])

    def test_idempotent(self):
        self.run_promote(exclude=[1], reason="x")
        before = self.read(self.research)
        log_before = self.read(os.path.join(self.v, "_agents", "account-watch", "log.md"))
        s = self.run_promote(exclude=[1], reason="x")
        self.assertEqual(s["promoted"], [])
        self.assertEqual(s["skipped_existing"], [2])
        self.assertEqual(s["changed"], [])
        self.assertEqual(self.read(self.research), before)
        self.assertEqual(self.read(os.path.join(self.v, "_agents", "account-watch", "log.md")), log_before)

    def test_existing_file_keeps_user_annotations_and_inserts_in_order(self):
        with open(self.research, "w") as fh:
            fh.write("---\ntype: resource\nmodified: 2026-10-01\nlast_checked: 2026-10-01\n---\n\n# Client A\n\n"
                     "## Signals (newest first)\n\n### 2026-10-24 · FIN-PERF · RISK · MEDIUM\n**Old**\n"
                     "> Note: worth a call\n<!-- key: client-a|FIN-PERF|2026-10|q3 -->\n\n"
                     "### 2026-10-01 · LEADER · NEUTRAL · LOW\n**Older**\n\n## Quote bank\n")
        self.run_promote()
        text = self.read(self.research)
        self.assertIn("> Note: worth a call", text)
        order = [text.index(h) for h in ("2026-10-25 · STRAT", "2026-10-24 · FIN-PERF", "2026-10-23 · ORG",
                                          "2026-10-01 · LEADER", "## Quote bank")]
        self.assertEqual(order, sorted(order))
        self.assertIn("modified: 2026-10-27", text)

    def test_dry_run_writes_nothing(self):
        s = self.run_promote(dry=True)
        self.assertEqual(s["promoted"], [1, 2])
        self.assertFalse(os.path.exists(self.research))

    def test_commit_mode_makes_one_commit(self):
        subprocess.run(["git", "init", "-q"], cwd=self.v, check=True)
        subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "--allow-empty", "-m", "init"],
                       cwd=self.v, check=True)
        env = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
        old = {k: os.environ.get(k) for k in env}
        os.environ.update(env)
        try:
            self.run_promote(commit=True)
        finally:
            for k, val in old.items():
                if val is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = val
        msg = subprocess.run(["git", "log", "-1", "--format=%s"], cwd=self.v, capture_output=True, text=True).stdout
        self.assertEqual(msg.strip(), "agent(account-watch): promote shadow 2026-10-26 — 2 signals")


if __name__ == "__main__":
    unittest.main()
