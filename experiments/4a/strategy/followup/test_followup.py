import unittest
from compare_followup import RelevantController, execute, load, run

PARAMS = load()[0]["parameters"]


class FollowupTests(unittest.TestCase):
    def test_relevant_change_is_immediate(self):
        c = RelevantController("relevant_change", PARAMS)
        c.choose("SA", "AXL")
        self.assertFalse(c.choose("SA", "AYL")["review"])
        self.assertEqual(c.choose("SA", "BYL")["choice"], "B")
        self.assertEqual(c.choose("SA", "AXL")["choice"], "A")

    def test_entropy_ignores_cue(self):
        t = execute("signal_entropy", PARAMS, ["AXL", "AYL"] * 8)
        self.assertEqual(sum(r["review"] for r in t.rows), 4)
        self.assertEqual(sum(r["entropy_evaluations"] for r in t.rows), 16)
        self.assertTrue(all(r["metrics"]["signal"] == 0 for r in t.rows))

    def test_debounce_and_constellation(self):
        c = RelevantController("relevant_debounce", PARAMS)
        first = c.choose("SA", "AXL")
        held = c.choose("SA", "BYL")
        self.assertFalse(held["review"])
        self.assertEqual(held["constellation"], first["constellation"])
        self.assertEqual(c.choose("SA", "BXL")["choice"], "B")

    def test_window_does_not_extend(self):
        c = RelevantController("signal_entropy", PARAMS)
        c.choose("SA", "AXL")
        for obs in ["BXL", "AXL", "AXL", "AXL", "AXL", "AXL"]:
            old = c.states["SA"]["limit"]
            r = c.choose("SA", obs)
            if not r["review"]:
                self.assertLessEqual(r["limit"], old)

    def test_rights_and_aba(self):
        for arm in ("relevant_change", "signal_entropy", "relevant_debounce"):
            t = execute(arm, PARAMS, ["AXL", "SB>SA:BXL", "AXL/p2,p3", "AXL", "@p2", "AXL", "BXL"])
            self.assertEqual("".join(r["status"] for r in t.rows), "A#~A#B")
            self.assertIsNone(t.rows[2]["delivered"])
            self.assertTrue(t.rows[3]["review"])

    def test_full_frozen_comparison(self):
        report = run(write=False)
        self.assertEqual(report["hard_cases_passed"], 105)
        for totals in report["totals"].values():
            self.assertEqual(totals["requests"], 188)
            self.assertEqual(totals["executed"] - totals["delivered"], 3)
            self.assertEqual(totals["reviews"] + totals["reuse"], totals["executed"])
        self.assertLess(report["totals"]["relevant_change"]["reviews"], report["totals"]["per_turn"]["reviews"])


if __name__ == "__main__":
    unittest.main()
