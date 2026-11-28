"""Additional counterexamples found during candidate review; frozen cases unchanged."""
import json
import unittest
from copy import deepcopy
from run import ROOT, run_case, verify_frozen
from runtime import Runtime, compile_artifact

FIXTURE = json.loads((ROOT / "fixture.json").read_text())


class ReviewRegressions(unittest.TestCase):
    def test_frozen_inputs(self):
        verify_frozen()

    def test_retry_after_revocation_is_not_dispatched(self):
        case = {"id": "review-retry-revoked", "config": {"arm": "A", "budget": 2},
                "steps": [{"id": "1", "op": "RESOLVE", "arg": "OTHER",
                           "scenario": "rejected", "retry": True, "during": ["p2"]}]}
        result = run_case(FIXTURE, case, [{"status": "STALE", "route": "MODEL", "attempts": 1,
                                            "transport": ["rejected"], "external_calls": 1}])
        self.assertEqual(len(result["observed_stub_calls"]), 1)

    def test_stale_request_never_reaches_adapter(self):
        rt = Runtime(FIXTURE, {"arm": "D"})
        rt.event("source")
        result = rt.handle("SA", {"id": "1", "scope": "SA", "session": "S", "revision": 1,
                                  "op": "RESOLVE", "arg": "OTHER"}, None, None)
        self.assertEqual(result["status"], "STALE")
        self.assertFalse(rt.attempts)

    def test_compiler_rejects_unknown_operation_and_reference(self):
        for change in ("op", "ref", "extra"):
            with self.subTest(change=change):
                bundle = deepcopy(FIXTURE["bundle"])
                if change == "op":
                    bundle["operations"].append("EXEC")
                elif change == "ref":
                    bundle["rules"]["EXACT1"] = ["R9"]
                else:
                    bundle["glue_code"] = "EXEC"
                with self.assertRaises(ValueError):
                    compile_artifact(bundle, FIXTURE["policy"])

    def test_compilation_is_canonical(self):
        bundle = FIXTURE["bundle"]
        reversed_bundle = dict(reversed(list(bundle.items())))
        self.assertEqual(compile_artifact(bundle, FIXTURE["policy"]),
                         compile_artifact(reversed_bundle, FIXTURE["policy"]))


if __name__ == "__main__":
    unittest.main()
