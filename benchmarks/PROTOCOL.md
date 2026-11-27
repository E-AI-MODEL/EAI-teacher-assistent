# Vergelijkingsprotocol (ontwerp v0.2)

> Status v0.4: dit protocol beschrijft de latere vergelijking van volledige gesprekken. De [neutrale technische contractproeven P01–P03](TECHNISCHE-PROEVEN.md) en de [technische specificatie v0.1](../research/TECHNISCHE-SPECIFICATIE.md) blijven voorstellen. Fase 3b/3c zijn heropend; fase 4a staat stil tot een nieuw besluit. Geen vakinhoud, echte inferentie of definitieve modelkeuze.


## Onderzoekseenheid

Een volledig leerlinggesprek rond een opdracht; daarnaast rapportage per aanroep, beurt en scenariofamilie. Gebruik synthetische dialogen in de eerste technische benchmark. Maak onderscheid tussen vaste replay (gelijke invoer) en interactieve, gesimuleerde gesprekken (reactie afhankelijk van antwoord). Geen echte leerlingprestatie afleiden uit simulaties.

## Gecontroleerde vergelijking

- A en B gebruiken dezelfde modelversie, vakinhoud, didactische opdracht en vergelijkbare generatie-instellingen. A is een competente referentie met normale contextselectie, geen kunstmatig dure variant. B optimaliseert context en antwoordbudget en kan caching benutten.
- C gebruikt dezelfde externe modelversie als B waar de regels geen voldoende antwoord bieden. Nieuwe aanroepen voor classificatie of validatie tellen mee.
- D deelt de regels, contextcontracten en hintbibliotheek van C, maar gebruikt een zelfgehost model voor modeltaken. Meet modelkeuze als afzonderlijke factor; een vergelijking C/D toont het gezamenlijke effect van model en hosting, tenzij hetzelfde open-weight model op beide infrastructuren kan worden vergeleken.
- Meet componenten ook afzonderlijk waar dat praktisch kan (context, output, caching, regels). Houd vaste en variabele kosten uiteen.

## Eerst mechanismen onderzoeken

Het voorgestelde eerste pakket voor fase 4a staat in [TECHNISCHE-PROEVEN.md](TECHNISCHE-PROEVEN.md): P01 (meting en budget), P02 (autoriteit en revisies) en P03 (route en uitvoergrenzen). Het wacht op herbeoordeling. Behoud dezelfde abstracte fixtures en gewone gedeelde softwarefuncties voor alle varianten; die functies tellen niet als besparing van C. De stubproeven zouden technische invarianten toetsen; werkelijke modelkwaliteit en kosten komen later.

Na de abstracte contractproeven en vóór het bouwen van uitgebreide use cases: kleine vergelijkende proeven uit de [functiematrix](../research/FUNCTIONELE-EISEN.md) met dezelfde context en hulpgrens, bekende én onbekende foutgevallen, geldige alternatieve antwoorden en gewijzigde lesversies. Meet de nauwkeurigheid van routekeuze, dekking van veilige niet-LLM-routes, foutieve automatische antwoorden en gemiste noodzaak voor modelhulp. Een gesloten antwoord dat een bestaande regel betrouwbaar kan controleren is een aparte nulmodelreferentie. Verander de vier hoofdvarianten niet.

Binnen B vergelijk dezelfde input met en zonder contextselectie, minified JSON versus compact formaat waar passend, passende antwoordbudgetten en warme/koude prefixcache. Binnen C vergelijk gecontroleerde hints, vakspecifieke controles en eventueel modelroutering afzonderlijk. Binnen D vergelijk hosting en modelversie los waar mogelijk. Leg route-mix en hulpbeleid vast. Stop bij herhaalde niet-bereikte experimentele routes, technische uitval of bereikt kostenplafond; rapporteer niet-beoordeelde gevallen apart. Geen automatische herhalingen van dure runs.

## Registratie

Per gesprek: scenario-ID, les- en hulpbeleidsversie, inhoudsversie, model/provider/versie, parameters, gekozen route per beurt, modelaanroepen inclusief retries en controles, prompt-, output-, cached- en indien beschikbaar redeneertokens, ontbrekende metingen, externe kosten volgens gedateerd tarief, responstijd en technische fouten.

Voor zelfhosting: hardware, runtime, kwantisering, batchgrootte, gelijktijdige verzoeken, GPU-uren, geheugen, energie indien meetbaar, benutting, wachttijd en P50/P95. Meet op representatieve piekbelasting en rapporteer totale hosting- en beheerkosten. Nul externe tokens betekent niet nul totale kosten.

## Kwaliteit

Gebruik per geval vakinhoudelijke criteria, onder meer foutdetectie en locatie, acceptatie van meerdere correcte antwoorden, passende en uitvoerbare hint, contextcoherentie, antwoord niet onnodig weggeven, duidelijkheid en taalniveau. Zie [MRBench en TutorBench in het bronnenonderzoek](../research/VERKENNING.md). Een LLM-beoordelaar kan helpen bij selectie voor menselijke review, maar vervangt die niet. Bevries een ontwikkelset en een aparte ongeziene set. Gebruik geen verwachte testantwoorden als modelcontext, behalve broninhoud die alle varianten rechtmatig nodig hebben; bewaar verwachte beoordeling apart.

Beoordeel vakinhoudelijke juistheid, relevantie, bruikbaarheid, passende hulp, eigen activiteit van de leerling, onterechte diagnose, onnodig weggeven van het antwoord, correcte terugval en brongebruik. Leg criteria en ernstige fouten vooraf vast. Beoordelaars krijgen de variantidentiteit niet te zien waar blind beoordelen mogelijk is.

Een korter antwoord is geen verbetering op zichzelf. Tel extra beurten en onafgeronde taken mee. Leg ook uitval, niet-beschikbaarheid en onbruikbare antwoorden vast; verwijder ze niet uit de kostenvergelijking.

## Bewijs en grenzen

Unit- en integratietests, fictieve modelantwoorden, echte inferentieruns, docentbeoordelingen en eventuele leerlingproeven worden apart gerapporteerd. Geen fictieve kosten of resultaten als metingen presenteren.

Zelfstandig uitvoeren van een nieuwe opdracht zonder materiële hulp wordt apart gemeten bij een eventuele leerlingproef. Geen claim over behoud, transfer of leerwinst zonder passende metingen. Stel het aantal testgevallen, kwaliteitseisen en acceptatiegrenzen vast vóór de definitieve vergelijking.

## Schaalmodel

Zie [SCHAALMODEL.md](SCHAALMODEL.md) voor de gemeenschappelijke belastingsscenario's. Gebruik kosten per gestarte sessie inclusief fouten en retries × aantal gestarte sessies plus nog niet meegerekende vaste kosten. Rapporteer daarnaast totale kosten per succesvol afgeronde sessie (totale kosten / aantal succesvolle sessies). Tel leerlingbeurten, modelaanroepen, actieve sessies en lopende inferentieverzoeken afzonderlijk.

Alle vier varianten krijgen hetzelfde aangeboden verkeer in open-loop belastingtests; een trage variant mag niet kunstmatig goedkoop lijken doordat minder verzoeken zijn afgehandeld. Meet geslaagde doorvoer, wachtrij, P50/P95/P99, time-to-first-token waar van toepassing, timeout- en foutpercentage, retries, uitval en herstel. Gebruik dezelfde vooraf vastgelegde kwaliteits- en responstijdeisen. Test warme en koude caches en gelijktijdige lesstart. C en D tellen ook de niet-LLM-routes, en alle eventuele secundaire modelaanroepen. Meet daadwerkelijke capaciteit per model en configuratie, niet alleen HTTP-throughput van een mock.

Gebruik voor zelfhosting een capaciteitsmodel met schooluren, pieken, beschikbaarheid, redundantie, onderhoud, idle-kosten en afschrijving. Gebruik alleen scenario's zolang werkelijke gebruiksgegevens ontbreken.

Status: nog niet uitgevoerd. Er zijn geen benchmarkresultaten in deze repository.
