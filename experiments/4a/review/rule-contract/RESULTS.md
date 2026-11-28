# 4a.5 | Herstel unieke regelroute

28 november 2026. Technische zelfreview, lokale Python 3.13.5, geen CI of onafhankelijke goedkeuring. Baseline `ebb2a12b23264b54313a7e9aa70912f654bbcb34`; kandidaat `e473219307d5edb2feb9411e3ff43263b8fab155`. Zie [vooraf bevroren retourcontract](../../RULE-RETURN-CONTRACT.md). Geen wijziging van de oude fixtures, verwachtingen, eerdere meetgegevens of strategieproeven.

De nieuwe tests op de oude runtime geven 57 falende subtests: verkeerde toegestane referentie (4), extra toegestane herkomst (4), omgekeerde selectie (4), dubbele herkomst (9), GENERATE (9), GENERATE met referentie (9), CLARIFY (9), HANDOFF (9). Dit zijn subtests, geen 57 afzonderlijke bugs. De extra contractkeuzes zijn beperkt tot de unieke regelroute in deze neutrale proef. Dezelfde tests op de gerepareerde runtime slagen. Zes regels toegevoegd vóór de algemene proposalvalidator; geen modelbypass.

| Uitvoering | Resultaat | Log |
|---|---|---|
| Oude runtime, vier nieuwe testmethoden | 57 falende subtests | [baseline](baseline.log.gz) |
| Kandidaat, vijf bestaande en vier nieuwe testmethoden | 9/9, geen falende subtests | [regressies](candidate-all.log.gz) |
| Kandidaat, oorspronkelijke runner | 60/60, 122 traces, 70 stubpogingen, geen overgeslagen cases | [runner](candidate-run.log.gz) |

De aanvullende regressies bestrijken alle acht P/S/M-factorcombinaties met R=1 plus de lokale stubarm. Modelvoorsteltypen, enginefouten, stale/revisiecontroles en replay blijven in de uitgevoerde tests conform. Geen semantische garantie voor willekeurige modeloutput. De oorspronkelijke factorvergelijking blijft numeriek gelijk; geen echte inferentie of kostenbewijs.

## Herkomst

Git-blobhashes van lokaal uitgevoerde bronbestanden:
- oude runtime: `83e399ad256abcc727e1b8eb4c1a6c6292c70dac`
- nieuwe runtime: `1dec025dceb02c8af9e6c327935cb7f76726e199`
- runner: `4db93c646e2012a90a9bc90476e5b9d8a84f930f`
- oude regressies: `1303aabf9c7723809278489dbf6a16c9ea847763`
- nieuwe regressies: `bfd69ef039875c010858cb65038fdb17d0bc7041`
- fixture: `d4993a49a6c4c66212fe58f97f34a1752ad9a8ee`
- cases: `c1fa7f3688b321f63c6a02589dfbc520fbd466a9`
- expected: `d5ddd199406cf3bc67c2e6e13f99bd142e5ad395`

De volledige lokale runner-JSON is gegenereerd op 2026-11-28T08:37:26.306063+00:00. Het gecomprimeerde bestand heeft SHA-256 `9071c25d78a5b09c0435ffefb0885cce15fb278a04a5a501cb5d503aa9321ea1`; de volledige JSON is lokaal bewaard, nog niet in deze commit opgenomen. De drie ongewijzigde, gecomprimeerde tekstlogs zijn byte-identiek opgeslagen in deze map.

Reproduceer op de kandidaat vanuit experiments/4a:
```sh
python -m unittest -v test_regressions test_rule_contract
python run.py --report candidate-evidence.json
```

**Vervolg:** onafhankelijke beoordeling van de kandidaat en de grenzen van PR #4. De afzonderlijke wijzigingscontrole uit 4a.4 is nog niet geïntegreerd. Geen merge, productiearchitectuurkeuze, echte providerproef of betaalde CI.
