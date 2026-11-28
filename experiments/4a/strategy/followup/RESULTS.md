# 4a.4 | Vervolgproef: relevante verandering

28 november 2026. De zeven controllers zijn lokaal uitgevoerd met Python 3.13.5 op vijftien nieuwe, vooraf vastgelegde reeksen. De fixture en oracle zijn bevroren in commit `2af175c3716e547cd3c4b5a05422c54e53bdccb1`. De oorspronkelijke vier controllers, autorisatie en neutrale executor van 4a.3 zijn ongewijzigd hergebruikt. De nieuwe code controleert de oorspronkelijke bronhash en de fixturehashes.

## Resultaten

| Strategie | Aangeboden | Herbeoordelingen | Hergebruik | Afwijkingen | Bij hergebruik | Entropieberekeningen |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Iedere beurt | 188 | 182 | 0 | 4 | 0 | 0 |
| Vaste lock | 188 | 75 | 107 | 23 | 21 | 0 |
| Hysteresis | 188 | 77 | 105 | 20 | 18 | 0 |
| Adaptieve entropie | 188 | 135 | 47 | 4 | 0 | 728 |
| Relevante wijzigingscontrole | 188 | 75 | 107 | 4 | 1 | 0 |
| Entropie op relevant signaal | 188 | 100 | 82 | 4 | 0 | 182 |
| Twee afwijkingen afwachten | 188 | 63 | 119 | 20 | 18 | 0 |

105/105 harde arm-reekscombinaties en 6/6 unittest-tests (inclusief volledige vergelijking) geslaagd. Per arm: 188 aangeboden aanvragen, 736 autorisatiecontroles, 561 verwerkte velden, 182 neutrale uitvoeringen en 179 afleveringen. Drie resultaten per arm zijn na revisiewijziging tegengehouden; drie aanvragen zijn afgewezen, drie onbekende/ongeldige aanvragen zijn niet uitgevoerd. De entropieteller meet de werkelijk aangeroepen functie, niet een geschat aantal per beurt. Er is geen latentiemeting.

## Tegenbewijs en keuze

- Relevante wijzigingscontrole kiest bij alle reeksen precies dezelfde route als per-beurt beoordelen, met 75 in plaats van 182 herbeoordelingen. Vier afwijkingen van de synthetische oracle blijven bestaan; in deze arm valt één daarvan op een hergebruikte keuze. De keuze is geen bewijs dat het signaal correct is.
- Bij alleen wisselende X/Y-cue: de oorspronkelijke adaptieve arm herbeoordeelt 16 keer; relevante wijzigingscontrole en signaalentropie vier keer. De laatste berekent nog steeds 16 keer entropie. De cue blijft een verplicht gevalideerd veld, maar bepaalt in deze armen de strategie niet.
- Bij de identieke observatiereeksen ambiguous_burst_noise en ambiguous_burst_real kiezen alle controllers per arm dezelfde uitkomsten. De twee gewenste reeksen verschillen op twee posities. Geen controller kan beide reeksen met deze waarnemingen foutloos afhandelen. Extra informatie, een expliciete onzekerheidsuitkomst of een gerichte verduidelijking is nodig wanneer het onderscheid ertoe doet.
- De simpele relevante-wijzigingsarm heeft op deze dataset hetzelfde aantal verkeerde keuzes en minder beoordelingen dan beide entropievarianten. Debounce bespaart nog beoordelingen, maar mist echte wisselingen. Dit is geen bewijs dat entropie in iedere andere configuratie overbodig is.

**Besluit voor de volgende technische integratie:** neem de eenvoudige controle op relevante veranderingen als eerste kandidaat; bewaar de vaste lock en entropievarianten als referenties. Leg de relevante afhankelijkheidsvelden expliciet vast en toets of de eerdere contractruntime de controller daadwerkelijk gebruikt bij routekeuze en aflevering. De bestaande autorisatie- en revisiecontroles mogen niet vervallen. De vijfbeurtenlimiet en de synthetische A/B-signalen zijn proefkeuzes, geen vastgestelde productinstellingen.

Geen architectuur-, kosten-, semantische kwaliteits- of leerclaim. De proef geeft de signalen al expliciet aan de controller en meet de kosten van het verkrijgen van die signalen niet. Herbeoordelingen zijn geen modelaanroepen. De oracle is door dezelfde onderzoeker geconstrueerd, niet onafhankelijk beoordeeld. De reeksen zijn geen steekproef van werkelijk gebruik.

## Reproduceren

```sh
cd experiments/4a/strategy/followup
python compare_followup.py
python -m unittest -v test_followup
```

De runner schrijft evidence.json en reproduceerbare traces.json. [Meetgegevens](evidence.json) bevatten alle 105 samenvattingen en de SHA-256 van de volledige trace-export. De geteste lokale bestanden hebben Git-blobhashes:
- compare_followup.py: `03aa84be4b59da2c8f952a86cdf8db9686399fc2`
- test_followup.py: `e669616031846ec768b2863066553439184a25a3`
- evidence.json: `6d8baf78dbbcf44d60261ee590e68f606f23d983`

Zie [vooraf bevroren protocol](PROTOCOL.md) en [4a.3](../RESULTS.md). Geen echte inferentie of betaalde CI. De nieuwe controller is nog niet geïntegreerd in runtime.py.
