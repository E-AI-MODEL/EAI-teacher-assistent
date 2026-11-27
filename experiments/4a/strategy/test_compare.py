import unittest
from compare import Controller, Trial, entropy, load, metrics, run

PARAMS = load()[0]["parameters"]


class StrategyTests(unittest.TestCase):
    def test_entropy(self):
        self.assertEqual(entropy(["A", "A"], [1, 2], 2), 0.0)
        self.assertAlmostEqual(entropy(["A", "B"], [1, 1], 2), 1.0)
        self.assertLess(entropy(["A", "B"], [1, 3], 2), 1.0)
        with self.assertRaises(ValueError):
            entropy([], [], 2)
        with self.assertRaises(ValueError):
            entropy(["A"], [0], 2)

    def test_separate_tracks_and_vector(self):
        m = metrics(["AXL", "AYL", "AXL", "AYL"], PARAMS)
        self.assertEqual(m["signal"], 0.0)
        self.assertGreater(m["cue"], 0.75)
        self.assertGreater(m["vector"], 0.0)
        self.assertEqual(m["window"], 1)
        self.assertEqual(m["anchor_stability"], 1.0)

    def test_constellation_and_hysteresis(self):
        c = Controller("hysteresis", PARAMS)
        first = c.choose("SA", "AXL")
        held = c.choose("SA", "BYL")
        self.assertFalse(held["review"])
        self.assertEqual(held["constellation"], first["constellation"])
        new = c.choose("SA", "BXL")
        self.assertTrue(new["review"])
        self.assertEqual(new["choice"], "B")
        self.assertEqual(new["reason"], "persistent_conflict")

    def test_anchor_change_is_hard_review_and_measured(self):
        c = Controller("adaptive", PARAMS)
        c.choose("SA", "AXL")
        changed = c.choose("SA", "AXR")
        self.assertTrue(changed["review"])
        self.assertEqual(changed["reason"], "anchor_change")
        self.assertAlmostEqual(changed["metrics"]["anchor_stability"], 2 / 3)

    def test_expiry_and_adaptive_no_extension(self):
        c = Controller("adaptive", PARAMS)
        for _ in range(5):
            r = c.choose("SA", "AXL")
        self.assertEqual(r["age"], 5)
        self.assertTrue(c.choose("SA", "AXL")["review"])
        changed = c.choose("SA", "AYL")
        self.assertLessEqual(changed["limit"], 3)
        # Any later increase applies only after an explicit review.
        while True:
            old_limit = c.states["SA"]["limit"]
            r = c.choose("SA", "AYL")
            if r["review"]:
                break
            self.assertLessEqual(r["limit"], old_limit)

    def test_authorization_aba_and_forged_scope(self):
        trial = Trial("adaptive", PARAMS)
        trial.step("AXL")
        trial.step("SB>SA:BXL")
        self.assertEqual(trial.rows[-1]["status"], "#")
        trial.step("AXL")
        self.assertFalse(trial.rows[-1]["review"])
        trial.step("AXL/p2,p3")
        self.assertEqual(trial.rows[-1]["status"], "~")
        self.assertEqual(trial.rows[-1]["executed"], "R1")
        self.assertIsNone(trial.rows[-1]["delivered"])
        trial.step("AXL")
        self.assertTrue(trial.rows[-1]["review"])

    def test_frozen_comparison(self):
        result = run()
        self.assertEqual(result["hard_cases_passed"], 48)
        for totals in result["totals"].values():
            self.assertEqual(totals["requests"], 120)
            self.assertEqual(totals["executed"] - totals["delivered"], 3)
            self.assertEqual(totals["reviews"] + totals["reuse"], totals["executed"])


if __name__ == "__main__":
    unittest.main()
