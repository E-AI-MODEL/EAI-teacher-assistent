"""Neutral strategy experiment. No provider, network or production runtime."""
from collections import Counter
from hashlib import sha1, sha256
import json
from math import log
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FROZEN = {"inputs.json": "0c513a9eac7472e663e455e3eeaa9179d146d2c3",
          "expected.json": "4136bb81575c4de0ac0ab13d09571282c209b8f9"}


def blob(data):
    return sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def load():
    result = []
    for name, expected in FROZEN.items():
        data = (ROOT / name).read_bytes()
        if blob(data) != expected:
            raise ValueError(f"Frozen fixture changed: {name}")
        result.append(json.loads(data))
    return result


def entropy(values, weights, cardinality):
    if not values or len(values) != len(weights) or any(w <= 0 for w in weights):
        raise ValueError("invalid entropy input")
    counts = Counter()
    for value, weight in zip(values, weights):
        counts[value] += weight
    if len(counts) > cardinality or cardinality < 2:
        raise ValueError("invalid cardinality")
    total = sum(weights)
    return max(0.0, -sum((n / total) * log(n / total) for n in counts.values()) / log(cardinality))


def metrics(history, params):
    weights = params["recency_weights"][:len(history)]
    h = [entropy([v[i] for v in history], weights, 2) for i in range(3)]
    vector = entropy(history, weights, 8)
    anchor = sum(w for v, w in zip(history, weights) if v[2] == history[-1][2]) / sum(weights)
    score = max(h[:2])
    low, mid, high = params["windows"]
    window = low if score <= params["low_entropy"] else mid if score <= params["high_entropy"] else high
    return {"signal": h[0], "cue": h[1], "anchor": h[2], "vector": vector,
            "anchor_stability": anchor, "window": window}


class Controller:
    def __init__(self, arm, params):
        self.arm, self.params, self.states = arm, params, {}

    def reset(self, scope=None):
        if scope is None:
            self.states.clear()
        else:
            self.states.pop(scope, None)

    def choose(self, scope, obs):
        old = self.states.get(scope)
        changed_anchor = old is not None and old["constellation"][2] != obs[2]
        history = ((old["history"] if old else []) + [obs])[-self.params["history"]:] if self.arm == "adaptive" else []
        if changed_anchor:
            old = None
        limit = self.params["fixed_window"]
        measured = metrics(history, self.params) if self.arm == "adaptive" else None
        if measured:
            limit = measured["window"]
        contrary = (old["contrary"] + 1) if old and old["choice"] != obs[0] else 0
        active_limit = min(old["limit"], limit) if old else limit
        reason = "reuse"
        if self.arm == "per_turn":
            reason = "per_turn"
        elif not old:
            reason = "anchor_change" if changed_anchor else "new_state"
        elif old["age"] >= active_limit:
            reason = "expired"
        elif self.arm in ("hysteresis", "adaptive") and contrary >= self.params["contrary_required"]:
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


class Trial:
    def __init__(self, arm, params):
        self.controller = Controller(arm, params)
        self.params = params
        self.revision = 1
        self.allowed = {"SA": {"R1", "R2"}, "SB": {"R3"}}
        self.executions, self.deliveries, self.rows = [], [], []

    def event(self, name):
        if name == "p2":
            self.allowed["SA"] = {"R2"}
        elif name == "p3":
            self.allowed["SA"] = {"R1", "R2"}
        elif name not in ("source", "critical"):
            raise ValueError("unknown event")
        self.revision += 1
        self.controller.reset()

    @staticmethod
    def ref(scope, choice):
        return ("R1" if scope == "SA" else "R3") if choice == "A" else "R2"

    def step(self, token):
        if token.startswith("@"):
            self.event(token[1:])
            return
        raw, _, after = token.partition("/")
        actor, claim = "SA", "SA"
        if ":" in raw:
            prefix, raw = raw.split(":")
            actor, _, claim = prefix.partition(">")
            claim = claim or actor
        row = {"input": token, "actor": actor, "scope": claim, "revision": self.revision,
               "auth": 0, "fields": 0, "review": False, "choice": None, "reason": None,
               "terminal_reason": None,
               "executed": None, "delivered": None, "metrics": None}
        self.rows.append(row)

        def authorized(ref=None):
            row["auth"] += 1
            return actor == claim and claim in self.allowed and (ref is None or ref in self.allowed[claim])

        def finish(status, reason=None):
            row["status"] = status
            if reason:
                row["terminal_reason"] = reason

        if not authorized():
            return finish("#", "scope_denied")
        row["fields"] = len(raw)
        domains = [self.params["categories"][name] for name in ("signal", "cue", "anchor")]
        if len(raw) != 3 or any(v not in domain and v != "?" for v, domain in zip(raw, domains)):
            self.controller.reset(claim)
            return finish("!", "invalid_observation")
        if "?" in raw:
            self.controller.reset(claim)
            return finish("?", "unknown_observation")
        if not authorized(self.ref(claim, raw[0])):
            self.controller.reset(claim)
            return finish("#", "candidate_denied")
        row.update(self.controller.choose(claim, raw))
        chosen_ref = self.ref(claim, row["choice"])
        if not authorized(chosen_ref):
            self.controller.reset(claim)
            return finish("#", "chosen_denied")
        # Independent neutral executor records the reference it actually received.
        self.executions.append((len(self.rows), chosen_ref, self.revision))
        row["executed"] = chosen_ref
        for event in after.split(",") if after else []:
            self.event(event)
        allowed_now = authorized(chosen_ref)
        if self.revision != row["revision"]:
            return finish("~", "stale_delivery")
        if not allowed_now:
            return finish("#", "delivery_denied")
        self.deliveries.append((len(self.rows), chosen_ref, self.revision))
        row["delivered"] = chosen_ref
        finish("A" if chosen_ref == self.ref(claim, "A") else "B")


def summarize(trial, oracle):
    name, truth, reviews, exact, *counts = oracle
    rows = trial.rows
    if len(rows) != len(truth):
        raise AssertionError(f"{name}: request count")
    actual = "".join(r["status"] for r in rows)
    for i, (r, expected) in enumerate(zip(rows, truth), 1):
        if i in exact or expected not in "AB":
            if r["status"] != expected:
                raise AssertionError(f"{name}/{i}: hard outcome {r['status']} != {expected}")
        if i in reviews and not r["review"]:
            raise AssertionError(f"{name}/{i}: missing forced review")
        if (r["delivered"] is not None) != (r["status"] in "AB"):
            raise AssertionError(f"{name}/{i}: delivery mismatch")
    nreviews = sum(r["review"] for r in rows)
    assert nreviews + sum(r["reason"] == "reuse" for r in rows) == sum(r["choice"] is not None for r in rows)
    assert all(r["executed"] == r["delivered"] for r in rows if r["delivered"] is not None)
    assert len(trial.executions) == sum(r["executed"] is not None for r in rows)
    assert len(trial.deliveries) == sum(r["delivered"] is not None for r in rows)
    if counts and nreviews != counts[0][trial.controller.arm]:
        raise AssertionError(f"{name}: incorrect stable review count")
    wrong = [r for r, expected in zip(rows, truth) if expected in "AB" and r["status"] != expected]
    previous, switches = {}, 0
    for r in rows:
        if r["delivered"] is not None:
            key = r["scope"]
            switches += key in previous and previous[key] != r["status"]
            previous[key] = r["status"]
    return {"id": name, "actual": actual, "requests": len(rows), "reviews": nreviews,
            "reuse": sum(r["reason"] == "reuse" for r in rows), "switches": switches,
            "wrong": len(wrong), "wrong_reuse": sum(not r["review"] for r in wrong),
            "wrong_review": sum(r["review"] for r in wrong), "auth": sum(r["auth"] for r in rows),
            "fields": sum(r["fields"] for r in rows), "entropy_batches": sum(r["metrics"] is not None for r in rows),
            "executed": len(trial.executions), "delivered": len(trial.deliveries)}


def run():
    if not __debug__:
        raise RuntimeError("Run without Python optimization")
    inp, oracle = load()
    targets = {r[0]: r for r in oracle["streams"]}
    cases, traces = [], []
    for arm in inp["arms"]:
        for name, stream in inp["streams"]:
            trial = Trial(arm, inp["parameters"])
            for token in stream:
                trial.step(token)
            result = summarize(trial, targets[name])
            cases.append({"arm": arm, **result})
            traces.append({"arm": arm, "id": name, "rows": trial.rows,
                           "executions": trial.executions, "deliveries": trial.deliveries})
    keys = [k for k in cases[0] if k not in ("arm", "id", "actual")]
    totals = {arm: {k: sum(r[k] for r in cases if r["arm"] == arm) for k in keys} for arm in inp["arms"]}
    raw = json.dumps(traces, sort_keys=True, separators=(",", ":")).encode()
    report = {"fixture_blobs": FROZEN, "hard_cases_passed": len(cases), "totals": totals,
              "cases": cases, "trace_sha256": sha256(raw).hexdigest()}
    (ROOT / "traces.json").write_bytes(raw)
    (ROOT / "evidence.json").write_text(json.dumps(report, separators=(",", ":")) + "\n")
    print(json.dumps(totals, indent=2))
    return report


if __name__ == "__main__":
    run()
