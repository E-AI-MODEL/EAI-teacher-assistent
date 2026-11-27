# Vergelijkingsprotocol (ontwerp v0.1)

## Onderzoekseenheid

Een volledig leerlinggesprek rond een opdracht; daarnaast rapportage per aanroep, beurt en scenariofamilie. Gebruik synthetische dialogen in de eerste technische benchmark. Maak onderscheid tussen vaste replay (gelijke invoer) en interactieve, gesimuleerde gesprekken (reactie afhankelijk van antwoord). Geen echte leerlingprestatie afleiden uit simulaties.

## Gecontroleerde vergelijking

- A en B gebruiken dezelfde modelversie, vakinhoud, didactische opdracht en vergelijkbare generatie-instellingen. A is een competente referentie met normale contextselectie, geen kunstmatig dure variant. B optimaliseert context en antwoordbudget en kan caching benutten.
- C gebruikt dezelfde externe modelversie als B waar de regels geen voldoende antwoord bieden. Nieuwe aanroepen voor classificatie of validatie tellen mee.
- D deelt de regels, contextcontracten en hintbibliotheek van C, maar gebruikt een zelfgehost model voor modeltaken. Meet modelkeuze als afzonderlijke factor; een vergelijking C/D toont het gezamenlijke effect van model en hosting, tenzij hetzelfde open-weight model op beide infrastructuren kan worden vergeleken.
- Meet componenten ook afzonderlijk waar dat praktisch kan (context, output, caching, regels). Houd vaste en variabele kosten uiteen.

## Registratie

Per gesprek: scenario-ID, inhoudsversie, model/provider/versie, parameters, gekozen route per beurt, modelaanroepen inclusief retries en controles, prompt-, output-, cached- en indien beschikbaar redeneertokens, ontbrekende metingen, externe kosten volgens gedateerd tarief, responstijd en technische fouten.

Voor zelfhosting: hardware, runtime, kwantisering, batchgrootte, gelijktijdige verzoeken, GPU-uren, geheugen, energie indien meetbaar, benutting, wachttijd en P50/P95. Meet op representatieve piekbelasting en rapporteer totale hosting- en beheerkosten. Nul externe tokens betekent niet nul totale kosten.

## Kwaliteit

Beoordeel vakinhoudelijke juistheid, relevantie, bruikbaarheid, passende hulp, eigen activiteit van de leerling, onterechte diagnose, onnodig weggeven van het antwoord, correcte terugval en brongebruik. Leg criteria en ernstige fouten vooraf vast. Beoordelaars krijgen de variantidentiteit niet te zien waar blind beoordelen mogelijk is.

Een korter antwoord is geen verbetering op zichzelf. Tel extra beurten en onafgeronde taken mee. Leg ook uitval, niet-beschikbaarheid en onbruikbare antwoorden vast; verwijder ze niet uit de kostenvergelijking.

## Bewijs en grenzen

Unit- en integratietests, fictieve modelantwoorden, echte inferentieruns, docentbeoordelingen en eventuele leerlingproeven worden apart gerapporteerd. Geen fictieve kosten of resultaten als metingen presenteren.

Zelfstandig uitvoeren van een nieuwe opdracht zonder materiële hulp wordt apart gemeten bij een eventuele leerlingproef. Geen claim over behoud, transfer of leerwinst zonder passende metingen. Stel het aantal testgevallen, kwaliteitseisen en acceptatiegrenzen vast vóór de definitieve vergelijking.

## Schaalmodel

Jaarlijkse kosten = kosten per geslaagde/afgeronde sessie × representatief aantal sessies, plus niet daarin opgenomen vaste kosten. Rapporteer ook de kosten van alle gestarte sessies inclusief mislukte sessies. Zelfhosting vraagt een capaciteitsmodel met schooluren, pieken, beschikbaarheid, redundantie, onderhoud, idle-kosten en afschrijving. Gebruik alleen scenario's als werkelijke gebruiksgegevens ontbreken.

Status: nog niet uitgevoerd. Er zijn geen benchmarkresultaten in deze repository.
