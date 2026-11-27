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

De eerste lokale uitvoering is geslaagd binnen de vastgelegde neutrale fixture. Geen werkelijke modelinferentie, betaalde CI, vakinhoud of productiearchitectuur. De adaptieve strategieproef volgt afzonderlijk. Zie [startcontract](../../benchmarks/4A-STARTCONTRACT.md).

## Afzonderlijke strategieproef 4a.3

[Resultaten en tegenbewijs](strategy/RESULTS.md). Vier varianten, 12 bevroren reeksen per variant, 48 harde scenario's en zeven regressietests geslaagd. Zachte strategieafwijkingen worden apart gerapporteerd. Niet geïntegreerd in runtime.py; geen variantkeuze.
