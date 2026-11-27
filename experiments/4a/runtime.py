"""Single-threaded contract experiment. No real inference or network transport."""
from copy import deepcopy
from hashlib import sha256
import json
from time import perf_counter_ns


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def digest(value):
    return sha256(encode(value)).hexdigest()


def compile_artifact(bundle, policy):
    """Validate the neutral manifest and return immutable canonical bytes."""
    if set(bundle) != {"revision", "records", "rules", "operations"}:
        raise ValueError("bundle fields")
    if set(policy) != {"revision", "scopes"}:
        raise ValueError("policy fields")
    if any(type(x["revision"]) is not int or x["revision"] < 1 for x in (bundle, policy)):
        raise ValueError("revision")
    records, rules, scopes = bundle["records"], bundle["rules"], policy["scopes"]
    if set(records) != {"R1", "R2", "R3"} or not all(type(v) is str for v in records.values()):
        raise ValueError("records")
    if bundle["operations"] != ["LOOKUP", "RESOLVE"] or set(scopes) != {"SA", "SB"}:
        raise ValueError("operations or scopes")
    if not isinstance(rules, dict) or not all(type(k) is str for k in rules):
        raise ValueError("rules")
    for refs in [*rules.values(), *scopes.values()]:
        if type(refs) is not list or not all(type(r) is str and r in records for r in refs):
            raise ValueError("unknown reference")
        if len(set(refs)) != len(refs):
            raise ValueError("duplicate reference")
    return encode({"bundle": bundle, "policy": policy, "compiler_revision": "neutral-v1"})


class Runtime:
    def __init__(self, fixture, config):
        self.bundle = deepcopy(fixture["bundle"])
        self.policy = deepcopy(fixture["policy"])
        self.initial_policy = deepcopy(self.policy["scopes"])
        self.usage_fields = tuple(fixture["usage_fields"])
        self.arm = config["arm"]
        bits = config.get("factors", fixture["arms"][self.arm])
        if len(bits) != 4 or set(bits) - {"0", "1"}:
            raise ValueError("invalid factors")
        self.P, self.S, self.R, self.M = (x == "1" for x in bits)
        self.window = fixture["strategy_window"]
        self.budget = config.get("budget", 1)
        if type(self.budget) is not int or not 0 <= self.budget <= 2:
            raise ValueError("invalid attempt budget")
        self.revision = 1
        self.observation = "READY"
        self.observation_revision = 1
        self.artifact_cache = None
        self.strategy = {}
        self.ledger = {}
        self.traces = []
        self.attempts = []

    def event(self, name):
        """Trusted fixture controller only; not an operation exposed to requests."""
        if name in ("p2", "p3"):
            self.policy["revision"] += 1
            self.policy["scopes"] = deepcopy(self.initial_policy)
            if name == "p2":
                self.policy["scopes"]["SA"].remove("R1")
        elif name in ("source", "bad_manifest", "bad_ref"):
            self.bundle["revision"] += 1
            if name == "source":
                self.bundle["records"]["R1"] = "ALPHA2"
            elif name == "bad_manifest":
                self.bundle["operations"].append("EXEC")
            else:
                self.bundle["rules"]["EXACT1"] = ["R9"]
        elif name in ("critical", "unknown"):
            self.observation_revision += 1
            self.observation = "READY" if name == "critical" else None
        else:
            raise ValueError("unknown event")
        self.revision += 1

    def required_refs(self, scope, request):
        arg = request["arg"]
        if request["op"] == "LOOKUP":
            return [arg]
        return self.bundle["rules"].get(arg, ["R1" if scope == "SA" else "R3"])

    def authorize(self, trace, actor, request):
        trace["events"].append({"kind": "authorize", "revision": self.revision})
        if set(request) != {"id", "scope", "session", "revision", "op", "arg"}:
            return "INVALID"
        if not all(type(request[k]) is str and request[k] for k in ("id", "scope", "session", "op", "arg")):
            return "INVALID"
        scope = request["scope"]
        # The fixture harness supplies the trusted actor; the caller supplies only a claim.
        if actor not in ("SA", "SB") or actor != scope or scope not in self.policy["scopes"]:
            return "DENY"
        if request["op"] not in ("LOOKUP", "RESOLVE"):
            return "DENY"
        if type(request["revision"]) is not int or request["revision"] != self.revision:
            return "STALE"
        if not set(self.required_refs(scope, request)) <= set(self.policy["scopes"][scope]):
            return "DENY"
        return None

    def artifact(self, trace):
        key = (self.bundle["revision"], self.policy["revision"])
        if self.P and self.artifact_cache and self.artifact_cache[0] == key:
            data = self.artifact_cache[1]
            trace["events"].append({"kind": "artifact_used", "digest": sha256(data).hexdigest()})
            return json.loads(data)
        event = {"kind": "compile", "revision": key, "digest": None}
        trace["events"].append(event)
        data = compile_artifact(self.bundle, self.policy)
        event["digest"] = sha256(data).hexdigest()
        if self.P:
            self.artifact_cache = (key, data)
        trace["events"].append({"kind": "artifact_used", "digest": event["digest"]})
        return json.loads(data)

    def evaluate_strategy(self, trace, key):
        deps = (self.bundle["revision"], self.policy["revision"], self.observation_revision)
        old = self.strategy.get(key)
        if self.S and old and old[0] == deps and old[2] > 0 and self.observation is not None:
            self.strategy[key] = (deps, old[1], old[2] - 1)
            trace["events"].append({"kind": "strategy_reuse", "dependencies": deps})
            return old[1]
        value = "PROCEED" if self.observation == "READY" else "CLARIFY"
        trace["events"].append({"kind": "strategy_review", "dependencies": deps, "value": value})
        if self.S and value == "PROCEED":
            self.strategy[key] = (deps, value, self.window - 1)
        else:
            self.strategy.pop(key, None)
        return value

    def select_context(self, artifact, request):
        scope = request["scope"]
        allowed = artifact["policy"]["scopes"][scope]
        needed = self.required_refs(scope, request)
        refs = needed if self.M else allowed
        return {"operation": request["op"], "signal": request["arg"], "required": self.observation,
                "source_revision": artifact["bundle"]["revision"], "policy_revision": artifact["policy"]["revision"],
                "records": {r: artifact["bundle"]["records"][r] for r in refs}}

    def infer(self, trace, adapter, task, retry, actor, request):
        for index in range(self.budget):
            if index > 0:
                rejection = self.authorize(trace, actor, request)
                if rejection:
                    return None, rejection
            attempt = {"id": len(self.attempts) + 1, "trace_id": trace["id"], "adapter": adapter.kind,
                       "model_revision": "stub-v1", "task": task["operation"], "mode": "simulated",
                       "transport": "uncertain", "dispatched": None, "accepted": None, "billing": None,
                       "usage": dict.fromkeys(self.usage_fields), "context_bytes": len(encode(task))}
            self.attempts.append(attempt)
            start = perf_counter_ns()
            try:
                response = adapter.invoke(deepcopy(task), trace["id"])
                transport = response["transport"]
                if transport not in ("accepted", "rejected", "uncertain"):
                    raise ValueError("invalid transport")
                attempt.update(transport=transport, dispatched={"accepted": True, "rejected": False, "uncertain": None}[transport],
                               accepted={"accepted": True, "rejected": False, "uncertain": None}[transport],
                               billing=False if transport == "rejected" else None)
                reported = response.get("usage", {})
                for field in self.usage_fields:
                    v = reported.get(field)
                    if type(v) is int and v >= 0:
                        attempt["usage"][field] = v
                attempt["error"] = "transport_or_response_error" if response.get("error") else None
                if transport == "accepted" and not response.get("error"):
                    return response.get("proposal"), None
                if not (transport == "rejected" and retry and index == 0):
                    return None, "MODEL_ERROR"
            except Exception as exc:
                attempt["error"] = type(exc).__name__
                return None, "MODEL_ERROR"
            finally:
                attempt["duration_ns"] = perf_counter_ns() - start
                attempt["unknown_usage"] = {k: "not_reported_by_stub" for k, v in attempt["usage"].items() if v is None}
                attempt["billing_reason"] = "definitely_rejected" if attempt["billing"] is False else "no_real_provider_invoice"
        return None, "BUDGET"

    @staticmethod
    def proposal_result(proposal, context):
        if type(proposal) is not dict:
            return None
        kind = proposal.get("kind")
        if kind not in ("SELECT", "GENERATE", "CLARIFY", "HANDOFF"):
            return None
        field = "ref" if kind == "SELECT" else "payload"
        if set(proposal) != {"kind", field, "used_refs"}:
            return None
        refs, value = proposal["used_refs"], proposal[field]
        if type(refs) is not list or not all(type(r) is str and r in context["records"] for r in refs):
            return None
        if type(value) is not str or not value or len(value) > 128:
            return None
        if kind == "SELECT":
            if value not in context["records"] or value not in refs:
                return None
            value = context["records"][value]
        return {"status": "OK", "kind": kind, "payload": value, "used_refs": refs}

    def handle(self, actor, request, adapter, engine, *, retry=False):
        trace = {"id": len(self.traces) + 1, "request_id": request.get("id"), "arm": self.arm,
                 "revision": self.revision, "events": [], "route": None, "outcome": None}
        self.traces.append(trace)
        start = perf_counter_ns()
        def finish(outcome):
            trace["outcome"] = deepcopy(outcome)
            trace["duration_ns"] = perf_counter_ns() - start
            return deepcopy(outcome)
        rejection = self.authorize(trace, actor, request)
        if rejection:
            return finish({"status": rejection})
        key = (actor, request["scope"], request["session"], request["id"])
        fingerprint = digest(request)
        prior = self.ledger.get(key)
        if prior:
            if prior["fingerprint"] != fingerprint:
                return finish({"status": "CONFLICT"})
            if prior["outcome"] is None:
                return finish({"status": "IN_FLIGHT"})
            trace["route"] = prior["route"]
            return finish({**prior["outcome"], "replay": True})
        entry = {"fingerprint": fingerprint, "outcome": None, "route": None}
        self.ledger[key] = entry
        def execute():
            try:
                artifact = self.artifact(trace)
            except ValueError:
                return {"status": "INVALID_ARTIFACT"}
            if request["op"] == "LOOKUP":
                trace["route"] = "LOOKUP"
                ref = request["arg"]
                return {"status": "OK", "payload": artifact["bundle"]["records"][ref], "used_refs": [ref]}
            if self.evaluate_strategy(trace, key[:3]) != "PROCEED":
                return {"status": "CLARIFY"}
            context = self.select_context(artifact, request)
            matches = artifact["bundle"]["rules"].get(request["arg"], [])
            if self.R and len(matches) == 1:
                trace["route"] = "RULE"
                trace["events"].append({"kind": "rule_execution", "ref": matches[0]})
                try:
                    proposal = engine(matches[0])
                except Exception:
                    return {"status": "ENGINE_ERROR"}
            else:
                if self.arm == "D" and adapter.kind != "local":
                    return {"status": "DENY"}
                if not adapter.available:
                    return {"status": "UNAVAILABLE"}
                trace["route"] = "MODEL"
                proposal, error = self.infer(trace, adapter, context, retry, actor, request)
                if error:
                    return {"status": error}
            return self.proposal_result(proposal, context) or {"status": "INVALID_PROPOSAL"}
        try:
            outcome = execute()
            if outcome["status"] == "OK":
                # Re-check the trusted revision before delivery; ABA cannot restore an old request.
                rejection = self.authorize(trace, actor, request)
                if rejection or trace["revision"] != self.revision:
                    outcome = {"status": rejection or "STALE"}
                elif not set(outcome.get("used_refs", [])) <= set(self.policy["scopes"][request["scope"]]):
                    outcome = {"status": "DENY"}
        except Exception as exc:
            outcome = {"status": "INTERNAL_ERROR", "error": type(exc).__name__}
        entry.update(outcome=deepcopy(outcome), route=trace["route"])
        return finish(outcome)
