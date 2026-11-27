# Plan van aanpak

Versie 0.1 — 27 november 2026

## Onderzoeksvraag

Welke combinatie van vooraf gecontroleerde lesinhoud, gewone programmacode en generatieve AI kan een methodegebonden assistent goedkoper laten werken, zonder verlies van vooraf vastgestelde vakinhoudelijke en didactische kwaliteit?

Onderzoek zowel kostenefficiëntie als de kwaliteit van ondersteuning. Leren, zelfstandigheid en transfer vragen afzonderlijk bewijs van leerlingprestaties. Technische testresultaten bewijzen dat niet.

## Werkvolgorde

| Fase | Werk | Oplevering / voorwaarde voor afronding |
| --- | --- | --- |
| 1 | Publieke bronnen en bestaande praktijk onderzoeken | Bronnenregister, herkomst, gebruikersbereik, adoptie en onbekende punten; geen aannames over de interne architectuur als feiten presenteren |
| 2 | Use case volledig uitwerken | Eigen lesreeks Frans 2 havo, doelen, opdrachten, feedback, hints, typische fouten, vrije vragen, docentgrenzen en onafhankelijke vervolgopdrachten; review door vakdocent |
| 3 | Repository-audit | Per functie bronversie, werking, tests, licentie, direct hergebruik versus nieuwe implementatie; geen onrechtmatige kopieën |
| 4 | Applicatie en varianten A–D | Eén leerlinginterface, één inhoudscontract, vier daadwerkelijk uitvoerbare antwoordroutes, server-side modeladapters en traceerbare kostenregistratie |
| 5 | Benchmark | Vastgelegde scenario's met dezelfde startcondities, testmanifest, ruwe modelantwoorden, bronverwijzingen, routekeuzes, foutgevallen en reproduceerbare runconfiguratie |
| 6 | Model- en belastingtests | Echte externe en lokaal gehoste modelaanroepen, gemeten kwaliteit, doorvoer, wachttijd en capaciteit tijdens gelijktijdige schoolbelasting; gesimuleerde tests apart |
| 7 | Didactische beoordeling | Onafhankelijke vakdocentbeoordeling van antwoorden en gesprekken; eventuele leerlingproef apart en onder passende voorwaarden |
| 8 | Kosten en schaalbaarheid | Kosten per gesprek en voltooide taak, tokenverbruik, GPU-bezetting en piekcapaciteit; transparante scenario's voor 70.000, 280.000 en 700.000 actieve leerlingen, schoolpieken en onzekerheid |
| 9 | Demonstratie en overdracht | Werkende vier-variantendemo, documentatie, reproduceerbare resultaten en expliciete beperkingen |

Fasen 1–3 leveren het bouwontwerp op; geen verplicht framework of model voordat de randvoorwaarden duidelijk zijn. De uiteindelijke oplevering omvat alle vier varianten, niet alleen een mock.

## Ontwerpvoorwaarden

- De docent bepaalt lesdoel, ondersteuningsniveau en de beschikbare hulp. Geen autonoom hoog-risico-oordeel over een leerling.
- Eén versie van vakinhoud en opdrachtcontracten; varianten delen dezelfde inhoud maar verschillen in antwoordmechanisme.
- Gebruik alleen de benodigde broninhoud. Geen volledige lesmethode of persoonsdossier meesturen.
- Bij ontbrekende context: gerichte vraag, gecontroleerde terugval of verwijzing naar de docent. Geen verzonnen vakinhoud of stille extra modelroute.
- Voor D: zonder externe model-API; een lokaal model dat niet bereikbaar is, wordt als niet beschikbaar gemeld.
- API-sleutels blijven server-side; geen echte leerlinggegevens, schoolinformatie of vertrouwelijke documenten in deze openbare repo.
- Beperk CI tot snelle, relevante checks. Live modelvergelijkingen apart en handmatig, met expliciet budget. Geen betaalde inferentie op iedere commit.
- Leg wijzigingen vast in één samenhangende PR per logisch werkpakket; geen grote stapel parallelle branches.

## Schaal als ontwerpvoorwaarde

Zie [het schaalmodel](../benchmarks/SCHAALMODEL.md). Gebruik vanaf fase 2 een gedeeld sessie- en requestcontract dat gelijktijdige klassen, scholen en vakken kan ondersteunen. Houd de eerste inhoudelijke use case klein; schaal technische belasting onafhankelijk op. Geen claim dat één Franse les de volledige landelijke vraagmix representeert.

Fase 6 bevat stapsgewijze capaciteitstests, gesynchroniseerde lesstart, aanhoudende piekbelasting, overbelasting, herstel en uitval. De benodigde GPU-capaciteit, externe API-quota, opslag, cache-isolatie en totale kosten volgen uit metingen; niet uit alleen het aantal geregistreerde accounts. Live externe tests hebben een vooraf vastgesteld budget. Grote synthetische transporttests zijn geen bewijs van werkelijke LLM-capaciteit.

## Open besluiten

Model, runtime, hosting, framework, licentie voor nieuw projectmateriaal en kwaliteitseisen worden na fase 1–3 onderbouwd gekozen. De projectopzet is geen claim van productiegeschiktheid.
