#!/usr/bin/env python3
"""Tests for capture.py against a throwaway fixture vault. Run: python3 -m unittest scripts/agents/tests/test_capture.py"""
import datetime as dt
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import capture  # noqa: E402

TZ = ZoneInfo("America/New_York")
DAY = dt.datetime(2026, 10, 2, 9, 0, tzinfo=TZ)

DAILY = """---
type: daily
tags: [daily]
created: 2026-10-02
modified: 2026-10-02
status: active
related:
  - "[[this-week]]"
---

# 2026-10-02 — Friday

## Log

**09:00** — something

## Captures

## Actions Discovered
"""

OPEN_LOOPS = """---
type: area
---

# Open loops

## Inbox (unsorted)

## This Week (due within 7 days)
- [ ] existing item
"""


def write(v, path, text):
    full = os.path.join(v, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    capture._write(full, text)


def read(v, path):
    return capture._read(os.path.join(v, path))


def ts_at(hour, minute):
    return f"{DAY.replace(hour=hour, minute=minute).timestamp():.6f}"


class CaptureTest(unittest.TestCase):
    def setUp(self):
        self.v = tempfile.mkdtemp()
        os.environ["CAPTURE_VAULT"] = self.v
        write(self.v, "01-daily/2026-10/2026-10-02.md", DAILY)
        write(self.v, "_current/open-loops.md", OPEN_LOOPS)
        write(self.v, "02-areas/celonis/example-client/example-client.md",
              "---\nclient: Example Client\nstatus: active\n---\n# Example Client\n")
        write(self.v, "02-areas/celonis/example-client/stakeholders/jane-doe.md",
              "---\nrole: AE\n---\n# Jane Doe\n")
        write(self.v, "03-resources/concepts/Discovery Template.md", "# Discovery Template\n")
        write(self.v, "_agents/capture-keeper/state.json", "")
        write(self.v, "_agents/config.yaml", f"timezone: America/New_York\nslack_capture_channel_id: CTEST01\nslack_self_user_id: UTEST01\n")
        capture.save_state(self.v, "live", {"last_ts": f"{DAY.replace(hour=8).timestamp():.6f}"})

    def tearDown(self):
        shutil.rmtree(self.v)
        os.environ.pop("CAPTURE_VAULT", None)

    def apply(self, captures, mode="live", today=dt.date(2026, 10, 6)):
        f = os.path.join(self.v, "captures.json")
        capture._write(f, json.dumps({"captures": captures}))
        buf = io.StringIO()
        with redirect_stdout(buf):
            capture.cmd_apply(self.v, mode, f, today=today)
        return json.loads(buf.getvalue())

    def short(self, **kw):
        c = {"ts": ts_at(10, 15), "raw": "ask jane whether demo for example-client can go to LT next week",
             "text": "Ask Jane whether demo for Example Client can go to LT next week",
             "permalink": "https://example.enterprise.slack.com/archives/CTEST01/p1790856631879979",
             "links": ["example-client", "jane-doe"], "client": "example-client",
             "action": "Ask Jane whether demo for Example Client can go to LT", "structured": False}
        c.update(kw)
        return c

    def test_short_capture_line_and_action(self):
        s = self.apply([self.short()])
        daily = read(self.v, "01-daily/2026-10/2026-10-02.md")
        self.assertIn("- 💭 10:15 Ask Jane whether demo for Example Client can go to LT next week → [[example-client]], "
                      "[[jane-doe]]", daily)
        self.assertIn(f"%%cap:{ts_at(10, 15)}%%", daily)
        cap = daily.index("## Captures")
        self.assertLess(cap, daily.index("💭"))
        self.assertLess(daily.index("💭"), daily.index("## Actions Discovered"))
        self.assertIn("%%\n\n## Actions Discovered", daily)
        ol = read(self.v, "_current/open-loops.md")
        inbox = ol[ol.index("## Inbox (unsorted)"):ol.index("## This Week")]
        self.assertIn("- [ ] Ask Jane whether demo for Example Client can go to LT #client/example-client (from [[2026-10-02]])", inbox)
        self.assertEqual(s["processed_ts"], [ts_at(10, 15)])
        self.assertEqual(capture.load_state(self.v, "live")["last_ts"], ts_at(10, 15))

    def test_rerun_is_idempotent(self):
        c = self.short()
        self.apply([c])
        capture.save_state(self.v, "live", {"last_ts": f"{DAY.replace(hour=8).timestamp():.6f}"})
        s = self.apply([c])
        daily = read(self.v, "01-daily/2026-10/2026-10-02.md")
        self.assertEqual(daily.count("%%cap:"), 1)
        self.assertEqual(read(self.v, "_current/open-loops.md").count("%%cap:"), 1)
        self.assertEqual(s["skipped"][0]["why"], "already captured")

    def test_old_ts_skipped(self):
        s = self.apply([self.short(ts=ts_at(7, 0))])
        self.assertEqual(s["processed_ts"], [])
        self.assertNotIn("💭", read(self.v, "01-daily/2026-10/2026-10-02.md"))

    def test_agent_post_filtered(self):
        s = self.apply([self.short(raw="📥 Ingestor 13:07 — 4 account updates", text="📥 Ingestor 13:07 — 4 account updates",
                                   action=None)])
        self.assertEqual(s["skipped"][0]["why"], "agent post")
        self.assertNotIn("💭", read(self.v, "01-daily/2026-10/2026-10-02.md"))

    def test_unresolved_link_dropped(self):
        s = self.apply([self.short(links=["example-client", "no-such-note"], action=None)])
        daily = read(self.v, "01-daily/2026-10/2026-10-02.md")
        self.assertNotIn("no-such-note", daily)
        self.assertTrue(any("no-such-note" in w for w in s["warnings"]))

    def test_long_capture_stays_in_daily_note(self):
        long_text = ("Reusable discovery template idea: " + "we keep rebuilding the same Mural board for each account. " * 6)
        s = self.apply([self.short(ts=ts_at(11, 5), raw=long_text, text=long_text, links=["Discovery Template"],
                                   client=None, action=None, title="Reusable discovery template")])
        self.assertEqual(s["inbox_notes"], [])
        self.assertFalse(os.path.isdir(os.path.join(self.v, "00-inbox")))
        daily = read(self.v, "01-daily/2026-10/2026-10-02.md")
        self.assertIn("- 💭 11:05 Reusable discovery template → [[Discovery Template]]", daily)
        self.assertIn("%%\n  > Reusable discovery template idea: we keep rebuilding", daily)
        self.assertLess(daily.index("  > Reusable"), daily.index("## Actions Discovered"))

    def test_note_prefix_creates_inbox_note(self):
        s = self.apply([self.short(ts=ts_at(11, 5), raw="note: pitch angle for Example Client demo",
                                   text="Note: pitch angle for Example Client demo",
                                   links=["example-client"], action=None, title="Example Client demo pitch angle")])
        self.assertEqual(len(s["inbox_notes"]), 1)
        note = s["inbox_notes"][0]
        self.assertTrue(note.startswith("00-inbox/2026-10-02-1105-example-client-demo-pitch-angle"))
        body = read(self.v, note)
        self.assertTrue(body.startswith("---\ntype: resource\ntags: [capture, celonis, client/example-client]\n"))
        self.assertIn('  - "[[2026-10-02]]"\n  - "[[example-client]]"', body)
        self.assertIn("\npitch angle for Example Client demo\n", body)
        daily = read(self.v, "01-daily/2026-10/2026-10-02.md")
        self.assertIn("- 💭 11:05 Example Client demo pitch angle → [[2026-10-02-1105-example-client-demo-pitch-angle]], [[example-client]]", daily)

    def test_no_daily_note_yet_is_held(self):
        sat = f"{dt.datetime(2026, 10, 3, 10, 0, tzinfo=TZ).timestamp():.6f}"
        later = f"{dt.datetime(2026, 10, 3, 11, 0, tzinfo=TZ).timestamp():.6f}"
        s = self.apply([self.short(ts=sat), self.short(ts=later, action=None)], today=dt.date(2026, 10, 3))
        self.assertEqual(s["processed_ts"], [])
        self.assertEqual(len(s["held"]), 2)
        self.assertFalse(os.path.isdir(os.path.join(self.v, "00-inbox")))
        self.assertNotIn("%%cap:", read(self.v, "_current/open-loops.md"))
        self.assertLess(float(capture.load_state(self.v, "live")["last_ts"]), float(sat))
        write(self.v, "01-daily/2026-10/2026-10-05.md", DAILY.replace("2026-10-02", "2026-10-05"))
        s = self.apply([self.short(ts=sat), self.short(ts=later, action=None)], today=dt.date(2026, 10, 5))
        self.assertEqual(s["processed_ts"], [sat, later])
        self.assertEqual(read(self.v, "01-daily/2026-10/2026-10-05.md").count("%%cap:"), 2)
        self.assertEqual(capture.load_state(self.v, "live")["last_ts"], later)

    def test_weekend_capture_lands_on_next_daily_note(self):
        write(self.v, "01-daily/2026-10/2026-10-05.md", DAILY.replace("2026-10-02", "2026-10-05"))
        sat = dt.datetime(2026, 10, 3, 10, 0, tzinfo=TZ).timestamp()
        s = self.apply([self.short(ts=f"{sat:.6f}")])
        self.assertNotIn("💭", read(self.v, "01-daily/2026-10/2026-10-02.md"))
        mon = read(self.v, "01-daily/2026-10/2026-10-05.md")
        self.assertIn("- 💭 Sat 03 Oct 10:00 Ask Jane", mon)
        self.assertIn("(from [[2026-10-05]])", read(self.v, "_current/open-loops.md"))
        self.assertEqual(s["held"], [])

    def test_held_message_does_not_block_later_ones_twice(self):
        write(self.v, "01-daily/2026-10/2026-10-05.md", DAILY.replace("2026-10-02", "2026-10-05"))
        capture.save_state(self.v, "live", {"last_ts": f"{DAY.replace(hour=8).timestamp():.6f}"})
        a = self.short(ts=ts_at(10, 15), action=None)
        self.apply([a])
        s = self.apply([a])
        self.assertEqual(read(self.v, "01-daily/2026-10/2026-10-02.md").count("%%cap:"), 1)
        self.assertEqual(s["processed_ts"], [])

    def test_shadow_writes_nothing_outside_agent_folder(self):
        before_daily = read(self.v, "01-daily/2026-10/2026-10-02.md")
        before_ol = read(self.v, "_current/open-loops.md")
        s = self.apply([self.short()], mode="shadow")
        self.assertEqual(read(self.v, "01-daily/2026-10/2026-10-02.md"), before_daily)
        self.assertEqual(read(self.v, "_current/open-loops.md"), before_ol)
        self.assertTrue(s["report"].startswith("_agents/capture-keeper/shadow/"))
        self.assertEqual(capture.load_state(self.v, "live")["last_ts"], f"{DAY.replace(hour=8).timestamp():.6f}")

    def test_client_hub_allowed_despite_duplicate_stem(self):
        write(self.v, "02-areas/celonis/_internal/initiatives/x/nominations/example-client.md", "# nomination\n")
        self.apply([self.short(action=None)])
        self.assertIn("→ [[example-client]]", read(self.v, "01-daily/2026-10/2026-10-02.md"))

    def test_index_has_clients_people_concepts(self):
        idx = capture.build_index(self.v)
        links = {(i["kind"], i["link"]) for i in idx}
        self.assertIn(("client", "example-client"), links)
        self.assertIn(("person", "jane-doe"), links)
        self.assertIn(("concept", "Discovery Template"), links)

    def test_section_insert_creates_missing_section(self):
        out = capture.section_insert("# Day\n\n## Log\n\nx\n\n## Shipped\n", "Captures", "- line",
                                     before_headings=("Shipped",))
        self.assertIn("## Captures\n\n- line\n\n## Shipped", out)


if __name__ == "__main__":
    unittest.main()
