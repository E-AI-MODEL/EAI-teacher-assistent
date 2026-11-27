# Combinatiehypothese | vooraf samenstellen, toestand behouden en selectief uitvoeren

27 november 2026 · Herbeoordeling fase 3b/3c. Fase 4a: NO-GO. Geen nieuwe modelproef, vakinhoud, architectuurkeuze of bewezen besparing.

## Vraag

We onderzoeken welke technische handelingen gewone software betrouwbaar kan uitvoeren, wanneer een taalmodel nog nodig is en wat dat betekent voor de kosten van hetzelfde aangeboden gesprek. Vooraf compileren, adaptief strategiebehoud, toetsbare beslislogica en selectieve inferentie vormen samen een nieuwe onderzoekshypothese. De onderdelen zijn bekend uit eerdere eigen projecten en openbare implementaties; hun combinatie is nog niet getoetst.

De vraag is niet of deze vier technieken bestaan, maar of zij samen minder onnodig werk verrichten bij dezelfde taak en dezelfde toegangs- en kwaliteitsgrenzen. Het is mogelijk dat een goede directe modelroute al voldoende is, dat een enkel mechanisme meer oplevert dan de combinatie of dat voorbereiding en toestandbeheer hun eigen voordeel tenietdoen.

## Factoren die afzonderlijk veranderen

| Factor | Uit | Aan | Bronrecords | Weerlegging |
| --- | --- | --- | --- | --- |
| P – vooraf compileren | Bouw hetzelfde gevalideerde contract per aanvraag op | Compileer bij gewijzigde canonieke bron of beleid; immutable artifact met bron-, compiler- en beleidsrevisie | DPR09–DPR12; R10-01–R10-04; R11-01/02 | Andere betekenis, ongeldig artifact, verouderde kaart of hogere totale kosten bij gelijk gebruik |
| S – strategiebehoud | Bepaal de strategie telkens opnieuw op dezelfde actuele waarnemingen | Expliciete toestand; vaste lock, hysteresis en adaptief venster als afzonderlijke subvarianten; kritieke wijziging verbreekt lock | DPR01–DPR08; R11-09/13 | Onterechte lock, gemiste interrupt, extra modelwerk of verkeerde route |
| R – experimentele regel | Competente modelroute voor dezelfde experimentele aanvraag | MATCH via toetsbare engine; UNKNOWN alleen toegestane modeltaak; DENY niet omzeilen | DPR14/26/36; R11-01/03/04 | Onjuiste match, gemiste toegestane taak of route buiten bevoegdheid |
| M – begrensde modeltaak | Volledige relevante toegestane context met dezelfde gevraagde voorstelvorm | Capsule met benodigde bron-ID's, lokaal doel en voorstelcontract; selectieve context en compacte representatie | DPR10/23/27; R10-09; R11-05/11/12 | Betekenisverlies, ontbrekende noodzakelijke bron, meer herstel of dezelfde/hogere totale kosten |

M verandert niet stiekem de modeltaak of het doel. Een gecombineerde analyse en voorstel is een verdere subproef wanneer beide uitkomsten nodig zijn. Een modelrechter of extra classifier is geen verplichte baseline. P/S/R/M zijn onderzoeksfactoren, geen vier services. Broncontract, scope, gewone lookup en validatie worden altijd gedeeld. A–D blijven de vier hoofdvergelijkingshypothesen; P/S/R/M verduidelijken welke mechanismen daarvoor bijdragen. Onderzoek cachewarmte, modelgewichten, hosting en compressie als afzonderlijke factoren. De lokale variant mag geen externe runtime-inferentie doen, ook niet via embeddings.

## Gedeelde technische grenzen

- Compileer alleen getypeerde, toegestane gegevens en bekende bewerkingen; geen vrije modelcode in een artifact. Een manifest mag geen toestemming toevoegen.
- Hou oorspronkelijke snapshot, runtime-overlay, kandidaat en afgeleverde toestand apart. Stale resultaat weigeren op actuele rechten en monotone revisie, ook bij A→B→A.
- Entropie meet variatie, niet waarheid. Vergelijk eerst met een eenvoudige teller of vaste lock; specificeer de verdeling, gewichten, venster en normalisatie. Onbekende of ontbrekende observaties zijn niet gelijk aan bevestiging.
- Gebruik exact bekende referenties; ambiguous of UNKNOWN is een uitkomst. DENY en uitvoeringsfout mogen niet automatisch naar een modelroute. Een modelvoorstel is nog geen geautoriseerde handeling.
- Registreer een trace per aangeboden aanvraag en een record per poging; lokaal, verzonden, geaccepteerd en gefactureerd blijven afzonderlijke toestanden. Onzekere facturering is onbekend, niet nul. Geen onbegrensde retries of stille externe fallback.
- Controleer de uitkomst én actuele rechten vlak vóór aflevering. Een epoch kan een oud antwoord tegenhouden zonder de onderliggende inferentie te stoppen. Meet annulering en resourcevrijgave apart.

## Voorgestelde vergelijking

Begin met de baseline en P, S, R, M ieder afzonderlijk, daarna PSRM. Indien betekenisvol, laat bij de combinatie steeds één factor weg. Houd fixtures, verwachte uitkomsten, modelcontract, modelrevision bij echte modelproeven, geautoriseerde bron en aangeboden belasting gelijk. Geen echte modelrun in 4a. Deze matrix is een voorstel, geen vastgelegde proefscope; gebruik alleen de gevallen die onderscheidend zijn. Zie [de visuele matrix](../docs/illustraties/atlas/d18-proefmatrix.svg).

| Tegenproef | Verwacht technisch gedrag |
| --- | --- |
| Zelfde abstracte request, bekende directe lookup | Gelijke gewone functie in A–D; geen modelwinst aan hybride variant toeschrijven |
| Experiment met bekende MATCH, UNKNOWN, meerdere kandidaten en DENY | Alleen geldige MATCH modelvrij; UNKNOWN met toestemming naar stub; DENY blijft stop |
| Ontbrekende bron of onbekende manifestnode | Compilatie of aanvraag weigeren; geen vrije code en geen automatische modelreparatie |
| Stabiel signaal, kleine ruis, kritieke wijziging | Route volgens vastgelegde toestandregels; kritieke wijziging verbreekt lock; compare vaste en adaptieve strategie |
| Bron of recht wijzigt tijdens uitvoering; oude waarde komt terug | Geen verouderde uitkomst bij aflevering; nieuwe monotone revisie vereist |
| Onvolledige usage, geweigerde dispatch, timeout, budget op | Alle pogingen zichtbaar; onbekend blijft onbekend; geen ongeautoriseerde herhaling |
| Extra modelcontext verwijderd | Zelfde vereiste bronbetekenis en voorsteltype; stubs bewijzen alleen contract, later semantische beoordeling |
| Koud en warm, parallel en onderbreking | Afzonderlijke cachecondities; geen cross-scope hergebruik; resultaat en werkelijk resource-einde apart |

## Meting en besluit

De totale kosten per aangeboden aanvraag omvatten voorbereiding en updates (afgeschreven over werkelijk gebruik), contextselectie, toestand en routering, alle modelpogingen inclusief mislukking, cacheopbouw, lokale hardware/energie/beheer en herstel. Rapporteer naast kosten per aangeboden aanvraag ook kosten per geldige afgeleverde uitkomst, routebereik, foutsoorten, wachttijd en onbekende usage. Toets geen voordeel op alleen de overgebleven succesvolle aanvragen. Het punt waarop vooraf compileren voordeliger wordt hangt af van hergebruik, wijzigingsfrequentie en werkelijke kosten; geen fictieve gebruiksverdeling invullen als gemeten feit.

EAT Inline: 434 vragen naar exacte registernamen op 100.000 gegenereerde documenten, opgebouwd uit 669 fragmenten van 40 Wikipedia-pagina’s. Unieke naamkoppeling met EAT leverde vaker het correcte bronantwoord dan gewone naamzoekactie. De 100%-controle kreeg de antwoord-ID vooraf. Er draaide geen taalmodel.

NeSy: in P02 bereikten nul van tien echte P0-beurten de bedoelde onderzoeksroute. In P03 werden de acht geplande herbeoordelingen wél uitgevoerd, met zes negatieve controles zonder extra call. De verwachte zetten waren door de auteurs bepaald; nul onafhankelijke menselijke beoordelingen waren afgerond. Geen bewezen kwaliteitswinst.

Shadowseed: de historische 88,24% balanced accuracy bij Qwen2.5-0.5B haalde de vooraf vastgelegde statistische grens niet. Op een nieuwe dataset voldeden nul van vier vooraf vastgelegde toetsen. Gebruik die meetmethode als inspiratie, niet de activatieprobe als routecriterium.

Het voorstel is nog geen herzien architectuurbesluit. Eerst in 3b de serieuze combinaties en negatieve resultaten vergelijken, in 3c het gemeenschappelijke contract en de minimale proeven bijstellen. Pas daarna een nieuw GO/NO-GO. Geen vakinhoud, echte inferentie of betaalde proef vóór toestemming. De technische proeven kunnen geen leerwinst of overdracht aantonen.

## Herleidbaarheid

- [Technische specificatie v0.1, historisch ontwerp](TECHNISCHE-SPECIFICATIE.md)
- [P01–P10, eerdere proefvoorstellen](../benchmarks/TECHNISCHE-PROEVEN.md)
- [Ronde 09, openbare bronvondsten](register/RONDE-09.md) en [afgeleiden](register/RONDE-09-AFGELEID.md)
- [Ronde 10, historische verdieping](register/RONDE-10-VERDIEPING.md) en [ronde 11, externe vergelijking](register/RONDE-11-VERGELIJKING.md)
- [Atlas en bron-ID’s](../docs/illustraties/atlas/README.md)

Technische zelfreview: deze hypothese is niet gevalideerd. Eerdere testcode is niet gelijk aan een nieuwe uitvoering. De oorspronkelijke ToolCompiler-implementatie is niet gevonden; de manifestgedachte is historisch ontwerp. Openbare afgeleiden vervangen besloten vindplaatsen niet. Een verschil in A–D moet een expliciet gewijzigde factor vertegenwoordigen; geen verplichte dure baseline.
