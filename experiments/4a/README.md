# Fase 4a: neutrale contractproef

De eerste uitvoerbare versie gebruikt uitsluitend Python-standaardbibliotheek. Zie [de resultaten](RESULTS.md) en [meetgegevens](evidence.json).

- fixture.json, cases.jsonl en expected.jsonl: bevroren vóór de kandidaatcode; de verwachte uitkomsten gaan nooit naar de runtime.
- runtime.py: compiler, revisie- en bevoegdheidscontrole, vaste lock, regeluitvoering en modelstubcontract.
- run.py: proefharnas, onafhankelijke registratie van stubaanroepen, controle van bevroren bronnen en rapportage.
- test_regressions.py: aanvullende negatieve controles na technische zelfreview.

```sh
python run.py --report result.json
python -m unittest -v test_regressions
```

De eerste lokale uitvoering is geslaagd binnen de vastgelegde neutrale fixture. Geen werkelijke modelinferentie, betaalde CI, vakinhoud of productiearchitectuur. De afzonderlijke strategieproef is uitgevoerd; zie hieronder. Zie [startcontract](../../benchmarks/4A-STARTCONTRACT.md).

## Afzonderlijke strategieproef 4a.3

[Resultaten en tegenbewijs](strategy/RESULTS.md). Vier varianten, 12 bevroren reeksen per variant, 48 harde scenario's en zeven regressietests geslaagd. Zachte strategieafwijkingen worden apart gerapporteerd. Niet geïntegreerd in runtime.py; geen variantkeuze.

## Vervolgproef strategie 4a.4

[Resultaten relevante wijzigingscontrole](strategy/followup/RESULTS.md). Zeven armen op vijftien vooraf bevroren reeksen. 105/105 harde scenario's en 6/6 unittest-tests lokaal geslaagd. De eenvoudige wijzigingscontrole is de eerste integratiekandidaat, geen definitieve architectuurkeuze. De eerdere runtime en 4a.3 blijven ongewijzigd.
