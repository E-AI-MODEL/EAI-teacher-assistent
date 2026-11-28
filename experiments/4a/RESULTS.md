# Eerste contractproef 4a: resultaat en grenzen

Status: lokaal uitgevoerd met Python 3.13.5, zonder echte modelinferentie, netwerktransport, betaalde CI of vakinhoud. Proef gestart op 2026-11-27T23:24:56.609527+00:00. De invoer en verwachte uitkomsten zijn bevroren in commit `371e721518f17911fff2f9e73d96367535a246cf`, vóór de kandidaatcode. De code is getest en byte-identiek opgeslagen in commit `dd7e4ec74c1ecb703d7686dabfe18e300b88f68a`.

## Resultaat

- 60/60 bevroren scenario's geslaagd; 121 aangeboden aanvragen plus één overlappende aanvraag in een terugkerende callback (122 traces).
- 70 stubpogingen geregistreerd; 5/5 aanvullende regressietests geslaagd.
- Geen ontbrekende verplichte route, onverwachte externe stubaanroep in D, ontbrekend attempt-record of afgeleverde verouderde uitkomst in deze testset.
- De test bewaart ontbrekende usage als onbekend; de gemeten contextomvang is geserialiseerde JSON in bytes, niet providergebruik. De compilerproef controleert gelijke canonieke artifactdigests voor dezelfde bronversies.

Tijdens de zelfreview is het pad van een definitief geweigerde poging gevolgd. Een tweede poging controleert nu opnieuw de huidige rechten en revisie. De regressieproef verandert de rechten vóór de tweede poging en verwacht geen tweede dispatch. De uitgaande scope wordt door het proefharnas buiten de adapterafhandeling gecontroleerd.

## Afzonderlijke factoren

Iedere rij hieronder krijgt dezelfde vijf aangeboden aanvragen, inclusief gewone lookup. De cijfers zijn daadwerkelijk getelde gebeurtenissen in de fixture. P is hier compilatie bij eerste gebruik en hergebruik bij gelijke revisie, niet een volledige vooraf gebouwde productieketen. S is een vaste lock op een neutrale toestand; geen adaptieve entropie of bewezen semantisch strategiebehoud.

| P/S/R/M | Compilaties | Strategiebeoordelingen | Stubpogingen | Contextbytes | Regeluitvoeringen |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0000 | 5 | 4 | 4 | 546 | 0 |
| 1000 | 1 | 4 | 4 | 546 | 0 |
| 0100 | 5 | 2 | 4 | 546 | 0 |
| 0010 | 5 | 4 | 2 | 272 | 2 |
| 0001 | 5 | 4 | 4 | 497 | 0 |
| 1111 | 1 | 2 | 2 | 248 | 2 |
| 0011 | 5 | 4 | 2 | 248 | 2 |
| 0011-D | 5 | 4 | 2 | 248 | 2 |

0011 is C; 0011-D is D met lokale stub. Gewone lookup is gedeeld. Een lagere telling is een voorspeld en in deze neutrale set bereikt routeverschil, geen bewezen effect op werkelijke kosten. De modelvoorstellen zijn ingevoerd door het testharnas; hun inhoudelijke kwaliteit is niet onderzocht.

## Reproduceren

```sh
cd experiments/4a
python run.py --report result.json
python -m unittest -v test_regressions
```

[evidence.json](evidence.json) bevat de feitelijke samenvatting, scenarioresultaten, transportvoorbeelden, bronhashes en digest van de volledige lokale trace-export. De volledige trace-export is reproduceerbaar; duur en starttijd veranderen per run. Geen CI-run of onafhankelijke review van de kandidaatcode uitgevoerd.

## Wat nog niet is aangetoond

De runtime is bewust single-threaded. Overlap is met een synchrone callback gesimuleerd; werkelijke parallelle processen, threadveiligheid, crashherstel, provider-annulering, deadlines en netwerkinferentie zijn niet getest. Ook productie-authenticatie en echte egressisolatie zijn niet aangetoond. De fixtures bevatten uitsluitend fictieve scopes en gegevens. De voorgeschreven fase 4a.1 en de eerste factorconfiguraties zijn uitgevoerd, maar adaptieve strategieproeven (hysteresis, gewogen entropie, herzieningsvensters) staan nog open. Begin daar met vooraf vastgelegde nieuwe gebeurtenisreeksen en vergelijk met de vaste lock. Geen architectuurkeuze of vrijgave voor echte modelproeven.

Bron: [startcontract](../../benchmarks/4A-STARTCONTRACT.md), [technische proeven](../../benchmarks/TECHNISCHE-PROEVEN.md), [combinatiehypothese](../../research/COMBINATIE-HYPOTHESE.md). 
