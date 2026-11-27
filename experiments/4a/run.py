"""Replay frozen inputs; inspect actual trace and independent stub instrumentation."""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import sys
from runtime import Runtime, digest, encode

ROOT = Path(__file__).resolve().parent
FROZEN = "371e721518f17911fff2f9e73d96367535a246cf"
GIT_BLOBS = {"fixture.json": "d4993a49a6c4c66212fe58f97f34a1752ad9a8ee",
             "cases.jsonl": "c1fa7f3688b321f63c6a02589dfbc520fbd466a9",
             "expected.jsonl": "d5ddd199406cf3bc67c2e6e13f99bd142e5ad395"}


def verify_frozen():
    from hashlib import sha1
    for name, expected in GIT_BLOBS.items():
        data = (ROOT / name).read_bytes()
        actual = sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
        if actual != expected:
            raise ValueError(f"Frozen input changed: {name}")


def read_rows(name):
    return [json.loads(line) for line in (ROOT / name).read_text().splitlines()]


class Stub:
    def __init__(self, fixture, config, step, observe):
        self.kind = config.get("adapter", "local" if config["arm"] == "D" else "external")
        self.available = config.get("available", True)
        self.scenario = step.get("scenario", "success")
        self.proposal = step.get("proposal", {"kind": "GENERATE", "payload": "OK", "used_refs": []})
        self.usage = fixture["stub_usage"]
        self.observe = observe
        self.calls = []

    def invoke(self, task, trace_id):
        self.calls.append({"trace_id": trace_id, "task": deepcopy(task), "bytes": len(encode(task)), "adapter": self.kind})
        self.observe(task, len(self.calls) == 1)
        scenario = self.scenario if len(self.calls) == 1 else "success"
        if scenario in ("rejected", "uncertain"):
            return {"transport": scenario, "error": True}
        if scenario == "partial":
            return {"transport": "accepted", "error": True, "usage": {"input_total": 12}}
        return {"transport": "accepted", "proposal": deepcopy(self.proposal),
                "usage": {} if scenario == "missing" else deepcopy(self.usage)}


def match(expected, actual, path=""):
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            raise AssertionError(f"{path}: expected object, got {actual!r}")
        for key, value in expected.items():
            if key not in actual:
                raise AssertionError(f"{path}/{key}: missing")
            match(value, actual[key], f"{path}/{key}")
    elif isinstance(expected, list):
        if not isinstance(actual, list) or len(expected) != len(actual):
            raise AssertionError(f"{path}: expected {expected!r}, got {actual!r}")
        for i, (left, right) in enumerate(zip(expected, actual)):
            match(left, right, f"{path}/{i}")
    elif type(expected) is not type(actual) or expected != actual:
        raise AssertionError(f"{path}: expected {expected!r}, got {actual!r}")


def run_case(fixture, case, expected):
    rt = Runtime(fixture, case["config"])
    actual, calls, nested_total = [], [], 0
    for step in case["steps"]:
        if "event" in step:
            rt.event(step["event"])
            continue
        actor = step.get("actor", "SA")
        req = {"id": step["id"], "scope": step.get("scope", actor), "session": "S",
               "revision": rt.revision, "op": step["op"], "arg": step["arg"], **step.get("extra", {})}
        nested, violations, engine_calls = [], [], []
        def observe(task, first):
            # Independent observation of the actual stub payload at dispatch.
            if not set(task["records"]) <= set(rt.policy["scopes"][actor]):
                violations.append("outgoing scope violation")
            for event in step.get("during", []) if first else []:
                if event == "repeat":
                    nested.append(rt.handle(actor, req, stub, engine)["status"])
                else:
                    rt.event(event)
        stub = Stub(fixture, case["config"], step, observe)
        def engine(ref):
            engine_calls.append(ref)
            if step.get("scenario") == "engine_error":
                raise ValueError("injected engine failure")
            return {"kind": "SELECT", "ref": ref, "used_refs": [ref]}
        trace_index = len(rt.traces)
        outcome = rt.handle(actor, req, stub, engine, retry=step.get("retry", False))
        trace = rt.traces[trace_index]
        attempts = [a for a in rt.attempts if a["trace_id"] == trace["id"]]
        counts = {kind: sum(e["kind"] == kind for e in trace["events"]) for kind in
                  ("compile", "strategy_review", "authorize", "rule_execution")}
        row = {**outcome, "route": trace["route"], "attempts": len(attempts),
               "transport": [a["transport"] for a in attempts], "billing": [a["billing"] for a in attempts],
               "usage": [a["usage"] for a in attempts], "compiles": counts["compile"],
               "reviews": counts["strategy_review"], "auth_checks": counts["authorize"],
               "rules": counts["rule_execution"], "nested": nested,
               "external_calls": sum(c["adapter"] == "external" for c in stub.calls),
               "local_calls": sum(c["adapter"] == "local" for c in stub.calls),
               "context_bytes": sum(c["bytes"] for c in stub.calls)}
        if stub.calls:
            row.update(refs=list(stub.calls[-1]["task"]["records"]), required=stub.calls[-1]["task"]["required"])
        assert not violations, violations
        assert len(engine_calls) == counts["rule_execution"], "engine event mismatch"
        assert len(attempts) == len(stub.calls), "attempt ledger mismatch"
        assert all(a["context_bytes"] == c["bytes"] for a, c in zip(attempts, stub.calls)), "payload size mismatch"
        assert outcome["status"] == "OK" or "payload" not in outcome, "failed request delivered payload"
        calls.extend(stub.calls)
        nested_total += len(nested)
        actual.append(row)
    assert len(rt.traces) == len(actual) + nested_total, "missing trace"
    assert len({t["id"] for t in rt.traces}) == len(rt.traces)
    assert all(t["outcome"] is not None for t in rt.traces)
    assert len({a["id"] for a in rt.attempts}) == len(rt.attempts) == len(calls)
    assert all(a["mode"] == "simulated" for a in rt.attempts)
    assert case["config"]["arm"] != "D" or all(c["adapter"] == "local" for c in calls)
    match(expected, actual, case["id"])
    return {"id": case["id"], "config": case["config"], "config_digest": digest(case["config"]),
            "requests": actual, "traces": rt.traces, "attempts": rt.attempts, "observed_stub_calls": calls}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    if not __debug__:
        raise RuntimeError("Run without Python optimization; invariant assertions must remain active")
    verify_frozen()
    fixture = json.loads((ROOT / "fixture.json").read_text())
    cases = read_rows("cases.jsonl")
    expected = {r["id"]: r["requests"] for r in read_rows("expected.jsonl")}
    assert len(cases) == len(expected) == len({c["id"] for c in cases})
    assert {c["id"] for c in cases} == set(expected)
    # All contract cases before factor arms, regardless of physical fixture order.
    cases.sort(key=lambda c: c["id"].startswith("FACTOR-"))
    report = {"mode": "simulated", "fixture_commit": FROZEN, "fixture_blobs": GIT_BLOBS,
              "file_sha256": {n: sha256((ROOT / n).read_bytes()).hexdigest() for n in [*GIT_BLOBS, "runtime.py", "run.py"]},
              "python": sys.version.split()[0], "started_at": datetime.now(timezone.utc).isoformat(), "cases": []}
    failure = None
    checked_artifacts = False
    for case in cases:
        if case["id"].startswith("FACTOR-") and not checked_artifacts:
            compiled = [c for c in report["cases"] if c["id"].startswith("P02-D1-compile-")]
            used = [[e["digest"] for t in c["traces"] for e in t["events"] if e["kind"] == "artifact_used"] for c in compiled]
            if len(used) != 2 or used[0] != used[1]:
                failure = {"id": "P02-D1-artifact-equivalence", "error": "canonical artifact mismatch"}
                break
            checked_artifacts = True
        try:
            report["cases"].append(run_case(fixture, case, expected[case["id"]]))
        except Exception as exc:
            failure = {"id": case["id"], "error": str(exc)}
            break
    report["failure"] = failure
    report["passed_cases"] = len(report["cases"])
    report["offered_requests"] = sum(len(c["traces"]) for c in report["cases"])
    report["stub_attempts"] = sum(len(c["attempts"]) for c in report["cases"])
    executed = {c["id"] for c in report["cases"]}
    report["not_run"] = [c["id"] for c in cases if c["id"] not in executed and (not failure or c["id"] != failure["id"])]
    report["factor_summary"] = [{"id": c["id"], "compiles": sum(r["compiles"] for r in c["requests"]),
                                 "reviews": sum(r["reviews"] for r in c["requests"]),
                                 "stub_attempts": len(c["attempts"]), "context_bytes": sum(r["context_bytes"] for r in c["requests"]),
                                 "rules": sum(r["rules"] for r in c["requests"])} for c in report["cases"] if c["id"].startswith("FACTOR-")]
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ("passed_cases", "offered_requests", "stub_attempts", "failure", "not_run", "factor_summary")}, indent=2))
    return 1 if failure else 0


if __name__ == "__main__":
    sys.exit(main())
