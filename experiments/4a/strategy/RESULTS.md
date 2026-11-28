# 4a.3 | Strategieproef: resultaten

28 november 2026. Lokaal uitgevoerd met Python 3.13.5. De vier armen kregen dezelfde twaalf vooraf vastgelegde neutrale reeksen. De fixtures en oracle zijn bevroren in commit `abd6680cbdab2618e504b12d81d383a84926fc33` vóór de implementatie. De strategiecontroller is afzonderlijk getest; de eerdere contractruntime is niet gewijzigd.

## Uitkomst

| Variant | Aangeboden | Herbeoordelingen | Hergebruik | Afgeleverd | Afwijkingen van oracle | Daarvan bij hergebruik | Entropiebatches |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Per beurt | 120 | 113 | 0 | 110 | 4 | 0 | 0 |
| Vaste lock | 120 | 47 | 66 | 110 | 8 | 8 | 0 |
| Hysteresis | 120 | 50 | 63 | 110 | 8 | 7 | 0 |
| Adaptief | 120 | 75 | 38 | 110 | 4 | 0 | 113 |

48/48 arm-reekscombinaties voldoen aan de harde verwachtingen. 7/7 unittest-tests geslaagd, waaronder de volledige vergelijking. Iedere arm registreerde 461 autorisatiecontroles, 357 verwerkte invoervelden, 113 neutrale uitvoeringen en 110 afleveringen. Drie uitgevoerde resultaten per arm zijn na een revisiewijziging niet afgeleverd. Onbekende en ongeldige signalen of afgewezen scopeclaims leveren geen resultaat af. Een entropiebatch omvat vier berekeningen (signaal, cue, anker, volledige vector); het is geen modelaanroep.

## Waarom de totaalrij niet voldoende is

| Reeks | Per beurt: fouten / reviews | Vaste lock | Hysteresis | Adaptief |
| --- | --- | --- | --- | --- |
| Stabiel | 0 / 12 | 0 / 4 | 0 / 4 | 0 / 3 |
| Eenmalige ruis | 2 / 12 | 0 / 4 | 0 / 4 | 2 / 7 |
| Blijvende wissel | 0 / 12 | 2 / 4 | 1 / 5 | 0 / 5 |
| Iedere beurt echte wissel | 0 / 12 | 4 / 4 | 4 / 4 | 0 / 12 |
| Ruis in twee opeenvolgende beurten | 2 / 12 | 0 / 4 | 2 / 5 | 2 / 7 |
| Alleen tweede cue wisselt | 0 / 12 | 0 / 4 | 0 / 4 | 0 / 12 |
| Late wissel | 0 / 12 | 2 / 4 | 1 / 5 | 0 / 7 |

De adaptieve arm behoudt het foutaantal van herbeoordeling per beurt met 38 minder beoordelingen. Hij voorkomt de acht fouten door onterecht hergebruik van de vaste lock, maar volgt eenmalige ruis nog steeds. Hysteresis halveert de vertraging bij twee blijvende wisselreeksen van twee naar één fout, maar introduceert fouten in de ruisburstreeks. De tweede cue kan het venster onnodig verkorten: bij een stabiel A/B-signaal en wisselende X/Y-cue volgen twaalf beoordelingen in plaats van vier, zonder betere uitkomst. Een hoge entropie is dus niet automatisch een relevante verandering.

**Besluit:** geen strategievariant kiezen op basis van deze dataset. Behoud de vaste lock als eenvoudige referentie. Onderzoek in een nieuwe, vooraf bevroren proef een goedkope, expliciete afhankelijkheids- of wijzigingscontrole, een adaptieve variant zonder irrelevante cue en een afzonderlijke ruisgevoelige vergelijking. De huidige scores zijn geen bewijs voor semantische kwaliteit, inferentiebesparing, latencywinst of leereffect. De oracle is geconstrueerd door dezelfde onderzoeker; geen onafhankelijke beoordeling. De verdeling van de synthetische reeksen is geen gemeten gebruiksverdeling. Een aanvullende vergelijking moet op nieuwe reeksen plaatsvinden, niet op achteraf aangepaste grenzen in deze proef.

## Reproduceren

```sh
cd experiments/4a/strategy
python compare.py
python -m unittest -v test_compare
```

[evidence.json](evidence.json) bevat alle arm-reekssamenvattingen en de digest van de volledige trace-export. De runner maakt de individuele traces reproduceerbaar in traces.json. De bytes van de lokaal geteste bronnen en evidence zijn gecontroleerd met Git-blobhashes: compare.py a1153edeedaf20e4388c68adcf8a44125ebd6f2a; test_compare.py f1901f77febc283988b6036ae0c77d70c920a900; evidence.json ac97e0b645f0c1ad14a6bd9edb1f9d8bd0ca7edc. Geen externe adapter, echte modelinferentie, betaalde CI of vakinhoud.

Zie [vooraf bevroren protocol](PROTOCOL.md) en [de eerdere 4a-proef](../RESULTS.md).
