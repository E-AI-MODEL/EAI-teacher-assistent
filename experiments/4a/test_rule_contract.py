"""Frozen additional contract tests for unique deterministic rules, no live adapters."""
import json
import unittest
from copy import deepcopy
from itertools import product
from pathlib import Path
from runtime import Runtime

FIXTURE = json.loads(Path(__file__).with_name("fixture.json").read_text())
# All eight P/S/M combinations with R=1, plus the local adapter arm.
ARMS = [("A", p+s+"1"+m) for p,s,m in product("01", repeat=3)] + [("D", "0011")]

def select(ref, refs=None):
    return {"kind": "SELECT", "ref": ref, "used_refs": [ref] if refs is None else refs}

def other(kind, refs=None):
    return {"kind": kind, "payload": "NEUTRAL", "used_refs": [] if refs is None else refs}

class Adapter:
    def __init__(self, kind, proposal):
        self.kind, self.available = kind, True
        self.proposal, self.calls = proposal, []
    def invoke(self, task, trace_id):
        self.calls.append((deepcopy(task), trace_id))
        return {"transport":"accepted", "proposal":deepcopy(self.proposal), "usage":{}}

class RuleContract(unittest.TestCase):
    def setup_case(self, arm, bits, signal="EXACT1", actor="SA", proposal=None, model=None):
        rt = Runtime(FIXTURE, {"arm":arm, "factors":bits})
        adapter = Adapter("local" if arm=="D" else "external", model)
        request = {"id":"1", "scope":actor, "session":"S", "revision":rt.revision,
                   "op":"RESOLVE", "arg":signal}
        calls = []
        def engine(ref):
            calls.append(ref)
            return deepcopy(proposal)
        return rt, adapter, request, calls, engine

    def test_exact_matches_and_replay(self):
        for arm,bits in ARMS:
            for signal,ref,value,actor in [("EXACT1","R1","ALPHA","SA"),
                    ("EXACT2","R2","BETA","SA"),("EXACT3","R3","GAMMA","SB")]:
                with self.subTest(arm=arm,bits=bits,signal=signal):
                    rt,ad,req,calls,eng=self.setup_case(arm,bits,signal,actor,select(ref))
                    expected={"status":"OK","kind":"SELECT","payload":value,"used_refs":[ref]}
                    self.assertEqual(rt.handle(actor,req,ad,eng),expected)
                    self.assertEqual(rt.handle(actor,req,ad,eng),{**expected,"replay":True})
                    self.assertEqual(calls,[ref])
                    self.assertEqual(ad.calls,[])
                    self.assertEqual(rt.attempts,[])
                    self.assertEqual([t["route"] for t in rt.traces],["RULE","RULE"])
                    self.assertEqual(rt.traces[0]["outcome"],expected)
                    self.assertEqual([e for e in rt.traces[0]["events"] if e["kind"]=="rule_execution"],
                                     [{"kind":"rule_execution","ref":ref}])
                    self.assertFalse(any(e["kind"]=="rule_execution" for e in rt.traces[1]["events"]))

    def test_bad_proposals_fail_closed_and_replay(self):
        bad=[("wrong_allowed",select("R2")),("forbidden",select("R3")),
             ("unknown",select("R9")),("missing_used",select("R1",[])),
             ("extra_allowed",select("R1",["R1","R2"])),
             ("duplicate",select("R1",["R1","R1"])),
             ("forbidden_extra",select("R1",["R1","R3"])),
             ("generate",other("GENERATE")),("generate_with_ref",other("GENERATE",["R1"])),
             ("clarify",other("CLARIFY")),("handoff",other("HANDOFF")),
             ("unknown_kind",other("EXECUTE")),("extra_field",{**select("R1"),"extra":1}),
             ("missing_kind",{"ref":"R1","used_refs":["R1"]}),
             ("bad_ref_type",select(1,["R1"])),("bad_used_type",select("R1",("R1",))),
             ("bad_used_member",select("R1",[1])),("bad_kind_type",{"kind":[],"ref":"R1","used_refs":["R1"]}),
             ("none",None),("list",[select("R1")])]
        for arm,bits in ARMS:
            for name,proposal in bad:
                with self.subTest(arm=arm,bits=bits,case=name):
                    rt,ad,req,calls,eng=self.setup_case(arm,bits,proposal=proposal)
                    expected={"status":"INVALID_PROPOSAL"}
                    self.assertEqual(rt.handle("SA",req,ad,eng),expected)
                    self.assertEqual(rt.handle("SA",req,ad,eng),{**expected,"replay":True})
                    self.assertEqual(calls,["R1"])
                    self.assertEqual(ad.calls,[])
                    self.assertEqual(rt.attempts,[])
                    self.assertEqual([t["route"] for t in rt.traces],["RULE","RULE"])
                    self.assertEqual(rt.traces[0]["outcome"],expected)
                    self.assertEqual(rt.traces[1]["outcome"],{**expected,"replay":True})
                    self.assertEqual(next(iter(rt.ledger.values()))["outcome"],expected)
            with self.subTest(arm=arm,bits=bits,case="reverse"):
                rt,ad,req,calls,eng=self.setup_case(arm,bits,"EXACT2",proposal=select("R1"))
                self.assertEqual(rt.handle("SA",req,ad,eng),{"status":"INVALID_PROPOSAL"})
                self.assertEqual(calls,["R2"])
                self.assertEqual(ad.calls,[])

    def test_engine_error_and_current_authority(self):
        for arm,bits in ARMS:
            for event,status in [("exception","ENGINE_ERROR"),("p2","STALE"),("source","STALE")]:
                with self.subTest(arm=arm,bits=bits,event=event):
                    rt,ad,req,calls,eng=self.setup_case(arm,bits,proposal=select("R1"))
                    def changed(ref):
                        if event=="exception":
                            calls.append(ref)
                            raise ValueError("injected")
                        rt.event(event)
                        return eng(ref)
                    self.assertEqual(rt.handle("SA",req,ad,changed),{"status":status})
                    self.assertEqual(calls,["R1"])
                    self.assertEqual(ad.calls,[])
                    self.assertEqual(rt.attempts,[])
            for event,status in [("p2","DENY"),("unknown","CLARIFY")]:
                with self.subTest(arm=arm,bits=bits,before=event):
                    rt,ad,req,calls,eng=self.setup_case(arm,bits,proposal=select("R1"))
                    rt.event(event)
                    req["revision"]=rt.revision
                    self.assertEqual(rt.handle("SA",req,ad,eng),{"status":status})
                    self.assertEqual(calls,[])
                    self.assertEqual(ad.calls,[])
                    self.assertEqual(rt.attempts,[])

    def test_model_route_keeps_proposal_types(self):
        for arm,bits in ARMS+[("A","0000"),("A","0001")]:
            for signal in ("OTHER","AMBIG"):
                for proposal in (select("R1"),other("GENERATE"),other("CLARIFY"),other("HANDOFF")):
                    with self.subTest(arm=arm,bits=bits,signal=signal,kind=proposal["kind"]):
                        rt,ad,req,calls,eng=self.setup_case(arm,bits,signal,model=proposal)
                        expected={"status":"OK","kind":proposal["kind"],
                                  "payload":"ALPHA" if proposal["kind"]=="SELECT" else "NEUTRAL",
                                  "used_refs":proposal["used_refs"]}
                        self.assertEqual(rt.handle("SA",req,ad,eng),expected)
                        self.assertEqual(calls,[])
                        self.assertEqual(len(ad.calls),1)
                        self.assertEqual(len(rt.attempts),1)
                        self.assertEqual(rt.traces[0]["route"],"MODEL")

if __name__ == "__main__":
    unittest.main()
