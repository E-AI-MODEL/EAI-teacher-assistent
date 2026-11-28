"""Second neutral strategy comparison; reuse the unchanged 4a.3 controller and trial."""
from hashlib import sha256
import json
from pathlib import Path
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))
import compare as prior

FROZEN = {"inputs.json": "eb39fd35a2333c866047deee9fe02ca2bba251a1",
          "expected.json": "3c73b8ac0714f65f7f10701ca406ddbe93252f76"}
PRIOR_BLOB = "a1153edeedaf20e4388c68adcf8a44125ebd6f2a"
NEW_ARMS = ("relevant_change", "signal_entropy", "relevant_debounce")


def load():
    if prior.blob((ROOT.parent / "compare.py").read_bytes()) != PRIOR_BLOB:
        raise ValueError("4a.3 implementation changed")
    result = []
    for name, expected in FROZEN.items():
        data = (ROOT / name).read_bytes()
        if prior.blob(data) != expected:
            raise ValueError(f"Frozen fixture changed: {name}")
        result.append(json.loads(data))
    return result


class RelevantController(prior.Controller):
    def choose(self, scope, obs):
        old = self.states.get(scope)
        changed_anchor = old is not None and old["constellation"][2] != obs[2]
        # Match the previous adaptive arm's history semantics on anchor changes.
        history = ((old["history"] if old else []) + [obs])[-self.params["history"]:] if self.arm == "signal_entropy" else []
        if changed_anchor:
            old = None
        limit = self.params["change_window"]
        measured = None
        if self.arm == "signal_entropy":
            weights = self.params["recency_weights"][:len(history)]
            score = prior.entropy([v[0] for v in history], weights, 2)
            low, mid, high = self.params["windows"]
            limit = low if score <= self.params["low_entropy"] else mid if score <= self.params["high_entropy"] else high
            measured = {"signal": score, "window": limit}
        contrary = (old["contrary"] + 1) if old and old["choice"] != obs[0] else 0
        active_limit = min(old["limit"], limit) if old else limit
        reason = "reuse"
        if not old:
            reason = "anchor_change" if changed_anchor else "new_state"
        elif old["age"] >= active_limit:
            reason = "expired"
        elif self.arm == "relevant_change" and old["choice"] != obs[0]:
            reason = "signal_change"
        elif self.arm in ("signal_entropy", "relevant_debounce") and contrary >= self.params["contrary_required"]:
            reason = "persistent_conflict"
        review = reason != "reuse"
        if review:
            state = {"choice": obs[0], "constellation": obs, "history": history,
                     "age": 1, "limit": limit, "contrary": 0}
        else:
            state = {**old, "history": history, "age": old["age"] + 1,
                     "limit": active_limit, "contrary": contrary}
        self.states[scope] = state
        return {"choice": state["choice"], "review": review, "reason": reason,
                "constellation": state["constellation"], "age": state["age"],
                "limit": state["limit"], "metrics": measured}


def execute(arm, params, stream):
    trial = prior.Trial(arm, params)
    if arm in NEW_ARMS:
        trial.controller = RelevantController(arm, params)
    with patch.object(prior, "entropy", wraps=prior.entropy) as counted:
        for token in stream:
            before = counted.call_count
            n = len(trial.rows)
            trial.step(token)
            if len(trial.rows) > n:
                trial.rows[-1]["entropy_evaluations"] = counted.call_count - before
        assert counted.call_count == sum(r["entropy_evaluations"] for r in trial.rows)
    return trial


def run(write=True):
    if not __debug__:
        raise RuntimeError("Run without Python optimization")
    inp, oracle = load()
    targets = {r[0]: r for r in oracle["streams"]}
    cases, traces = [], []
    for arm in inp["arms"]:
        for name, stream in inp["streams"]:
            trial = execute(arm, inp["parameters"], stream)
            row = prior.summarize(trial, targets[name])
            cases.append({"arm": arm, **row,
                          "entropy_evaluations": sum(r["entropy_evaluations"] for r in trial.rows),
                          "denied": sum(r["status"] == "#" for r in trial.rows),
                          "stale": sum(r["status"] == "~" for r in trial.rows)})
            traces.append({"arm": arm, "id": name, "rows": trial.rows,
                           "executions": trial.executions, "deliveries": trial.deliveries})
    indexed = {(r["arm"], r["id"]): r for r in cases}
    # Identical observations cannot yield two different decisions by oracle label.
    for arm in inp["arms"]:
        a = indexed[(arm, "ambiguous_burst_noise")]
        b = indexed[(arm, "ambiguous_burst_real")]
        assert all(a[k] == b[k] for k in a if k not in ("id", "wrong", "wrong_reuse", "wrong_review"))
        assert a["wrong"] + b["wrong"] >= 2
    for name, _ in inp["streams"]:
        assert indexed[("relevant_change", name)]["actual"] == indexed[("per_turn", name)]["actual"]
    keys = [k for k in cases[0] if k not in ("arm", "id", "actual")]
    totals = {arm: {k: sum(r[k] for r in cases if r["arm"] == arm) for k in keys} for arm in inp["arms"]}
    raw = json.dumps(traces, sort_keys=True, separators=(",", ":")).encode()
    report = {"fixture_blobs": FROZEN, "prior_controller_blob": PRIOR_BLOB,
              "hard_cases_passed": len(cases), "totals": totals,
              "cases": cases, "trace_sha256": sha256(raw).hexdigest()}
    if write:
        (ROOT / "traces.json").write_bytes(raw)
        (ROOT / "evidence.json").write_text(json.dumps(report, separators=(",", ":")) + "\n")
        print(json.dumps(totals, indent=2))
    return report


if __name__ == "__main__":
    run()
