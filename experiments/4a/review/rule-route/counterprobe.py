"""Read-only counterprobe for PR #4. Run beside the original runtime.py and fixture.json.
No production changes, provider calls, dependencies, or edits to frozen expectations.
"""
from copy import deepcopy
from hashlib import sha1
from pathlib import Path
import json
import sys
from runtime import Runtime

ROOT = Path(__file__).resolve().parent
COMMIT = '0a309dc8a90d18b40b0ab3aa1de48afb8ca19086'
BLOBS = {'runtime.py':'83e399ad256abcc727e1b8eb4c1a6c6292c70dac',
         'fixture.json':'d4993a49a6c4c66212fe58f97f34a1752ad9a8ee'}
for name, expected in BLOBS.items():
    data = (ROOT / name).read_bytes()
    assert sha1(f'blob {len(data)}\0'.encode() + data).hexdigest() == expected, name
fixture = json.loads((ROOT / 'fixture.json').read_text())

class Adapter:
    def __init__(self, kind, proposal=None):
        self.kind, self.available = kind, True
        self.proposal, self.calls = proposal, []
    def invoke(self, task, trace_id):
        self.calls.append({'task': deepcopy(task), 'trace_id': trace_id})
        return {'transport':'accepted','proposal':deepcopy(self.proposal),'usage':{}}


def select(ref, used=None):
    return {'kind':'SELECT','ref':ref,'used_refs':[ref] if used is None else used}


def other(kind, refs=None):
    return {'kind':kind,'payload':'NEUTRAL','used_refs':[] if refs is None else refs}

# Independent expectations: exact positive outcomes in the frozen factor cases;
# wrong selections may never be successful on a unique registered rule.
# Unexpected kinds and provenance details are also tested, but their exact
# rejection codes/strictness are not frozen in the original contract.
variants = [
    ('exact1_correct','EXACT1',select('R1'),'positive'),
    ('exact2_correct','EXACT2',select('R2'),'positive'),
    ('exact1_wrong_allowed','EXACT1',select('R2'),'must_not_deliver'),
    ('exact2_wrong_allowed','EXACT2',select('R1'),'must_not_deliver'),
    ('forbidden_ref','EXACT1',select('R3'),'must_not_deliver'),
    ('unknown_ref','EXACT1',select('R9'),'must_not_deliver'),
    ('generate_empty','EXACT1',other('GENERATE'),'must_not_deliver'),
    ('generate_correct_ref','EXACT1',other('GENERATE',['R1']),'must_not_deliver'),
    ('clarify','EXACT1',other('CLARIFY'),'design'),
    ('handoff','EXACT1',other('HANDOFF'),'design'),
    ('select_extra_allowed_ref','EXACT1',select('R1',['R1','R2']),'design'),
    ('select_duplicate_refs','EXACT1',select('R1',['R1','R1']),'design'),
    ('select_missing_used_ref','EXACT1',select('R1',[]),'must_not_deliver'),
    ('select_forbidden_extra_ref','EXACT1',select('R1',['R1','R3']),'must_not_deliver'),
    ('extra_field','EXACT1',{**select('R1'),'execute':'no'},'must_not_deliver'),
    ('unknown_kind','EXACT1',other('EXECUTE'),'must_not_deliver'),
    ('none','EXACT1',None,'must_not_deliver'),
    ('list','EXACT1',[select('R1')],'must_not_deliver'),
    ('engine_exception','EXACT1',None,'engine_error'),
]

rows = []

def exercise(name, bits, arm, arg, proposal, expectation, *, actor='SA',
             event_before=None, event_during=None, repeat=False, model_proposal=None):
    rt = Runtime(fixture, {'arm':arm,'factors':bits})
    if event_before:
        rt.event(event_before)
    adapter = Adapter('local' if arm == 'D' else 'external',model_proposal)
    engine_calls=[]
    def engine(ref):
        engine_calls.append(ref)
        if name == 'engine_exception':
            raise ValueError('injected failure')
        if event_during:
            rt.event(event_during)
        return deepcopy(proposal)
    request = {'id':'probe-1','scope':actor,'session':'S','revision':rt.revision,'op':'RESOLVE','arg':arg}
    result = rt.handle(actor,request,adapter,engine)
    replay = rt.handle(actor,request,adapter,engine) if repeat else None
    trace = rt.traces[0]
    registered = fixture['bundle']['rules'].get(arg,[])
    expected_payload = fixture['bundle']['records'].get(registered[0]) if len(registered)==1 else None
    if expectation == 'positive':
        ok = result['status']=='OK' and result['kind']=='SELECT' and result['payload']==expected_payload and result['used_refs']==registered
    elif expectation == 'must_not_deliver':
        ok = result['status']!='OK' and 'payload' not in result
    elif expectation == 'engine_error':
        ok = result == {'status':'ENGINE_ERROR'}
    elif expectation == 'design':
        ok = None
    elif expectation == 'model_ok':
        ok = result['status']=='OK' and trace['route']=='MODEL' and len(adapter.calls)==1 and not engine_calls
    elif expectation == 'deny':
        ok = result=={'status':'DENY'} and not engine_calls and not adapter.calls
    elif expectation == 'stale':
        ok = result=={'status':'STALE'} and len(engine_calls)==1 and not adapter.calls
    elif expectation == 'clarify_before_route':
        ok = result=={'status':'CLARIFY'} and not engine_calls and not adapter.calls
    else:
        raise AssertionError(expectation)
    if expectation in ('positive','must_not_deliver','engine_error','design'):
        assert trace['route']=='RULE' and engine_calls==registered
        assert not adapter.calls and not rt.attempts
    assert len(rt.attempts)==len(adapter.calls)
    assert len(rt.traces)==(2 if repeat else 1)
    assert trace['outcome']==result
    rows.append({'name':name,'bits':bits,'arm':arm,'request':request,
                 'engine_proposal':proposal,'model_proposal':model_proposal,
                 'expected_rule_refs':registered,'expectation':expectation,'conforms':ok,
                 'result':result,'replay':replay,'engine_calls':engine_calls,
                 'observed_adapter_calls':adapter.calls,'traces':rt.traces,'attempts':rt.attempts,
                 'ledger':list(rt.ledger.values())})

for bits,arm in [('0010','A'),('0011','A'),('1111','A'),('0011','D')]:
    for name,arg,proposal,expectation in variants:
        exercise(name,bits,arm,arg,proposal,expectation)
    exercise('scope_sb_correct',bits,arm,'EXACT3',select('R3'),'positive',actor='SB')
    exercise('scope_sa_denied',bits,arm,'EXACT3',select('R3'),'deny')
    exercise('revoked_before_engine',bits,arm,'EXACT1',select('R1'),'deny',event_before='p2')
    exercise('revoked_during_engine',bits,arm,'EXACT1',select('R1'),'stale',event_during='p2')
    exercise('source_change_during_engine',bits,arm,'EXACT1',select('R1'),'stale',event_during='source')
    exercise('unknown_before_route',bits,arm,'EXACT1',select('R1'),'clarify_before_route',event_before='unknown')
    for arg in ['OTHER','AMBIG']:
        exercise('fallback_'+arg.lower(),bits,arm,arg,None,'model_ok',model_proposal=select('R1'))
    exercise('wrong_rule_replay',bits,arm,'EXACT1',select('R2'),'must_not_deliver',repeat=True)

# R disabled: a model selection in the larger authorized context is allowed by
# the proposal validator, but the same selection is rejected when M projects R2 out.
# Observations, not new gold labels about model quality.
for bits in ('0000','0001'):
    for kind,p in [('wrong_allowed',select('R2')),('generate',other('GENERATE')),('clarify',other('CLARIFY')),('handoff',other('HANDOFF'))]:
        rt=Runtime(fixture,{'arm':'A','factors':bits})
        adapter=Adapter('external',p)
        def unexpected_engine(ref):
            raise AssertionError('R disabled')
        request={'id':'model-1','scope':'SA','session':'S','revision':rt.revision,'op':'RESOLVE','arg':'EXACT1'}
        result=rt.handle('SA',request,adapter,unexpected_engine)
        assert rt.traces[0]['route']=='MODEL' and len(adapter.calls)==len(rt.attempts)==1
        rows.append({'name':'model_'+kind,'bits':bits,'arm':'A','request':request,'model_proposal':p,
                     'expectation':'model_control_observation','conforms':None,'result':result,
                     'observed_adapter_calls':adapter.calls,'traces':rt.traces,'attempts':rt.attempts})

summary={'commit':COMMIT,'verified_git_blobs':BLOBS,'python':sys.version.split()[0],
         'primary_probes':len(rows),'requests_including_replay':sum(len(r['traces']) for r in rows),
         'conform':sum(r['conforms'] is True for r in rows),'nonconform':sum(r['conforms'] is False for r in rows),
         'unscored_observations':sum(r['conforms'] is None for r in rows),
         'model_stub_calls':sum(len(r['attempts']) for r in rows),
         'by_arm':[]}
for bits,arm in [('0010','A'),('0011','A'),('1111','A'),('0011','D'),('0000','A'),('0001','A')]:
    selected=[r for r in rows if r['bits']==bits and r['arm']==arm]
    summary['by_arm'].append({'bits':bits,'arm':arm,'n':len(selected),'conform':sum(r['conforms'] is True for r in selected),
                              'nonconform':sum(r['conforms'] is False for r in selected),'unscored':sum(r['conforms'] is None for r in selected)})
(ROOT/'counterprobe-results.json').write_text(json.dumps({'summary':summary,'probes':rows},indent=2)+'\n')
print(json.dumps(summary,indent=2))
for r in rows:
    if r['conforms'] is False or r['expectation'] in ('design','model_control_observation') or r['name']=='wrong_rule_replay':
        print(r['bits'],r['arm'],r['name'],r['result'], 'replay='+str(r.get('replay')) if r.get('replay') else '')
