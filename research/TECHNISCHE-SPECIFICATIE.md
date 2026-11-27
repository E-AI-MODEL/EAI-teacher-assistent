# Fase 3c: technische specificatie A–D

Versie 0.1, 27 november 2026. Historisch technisch ontwerpvoorstel, in herbeoordeling. Fase 3b en 3c zijn gericht heropend; NO-GO voor fase 4a. Onderzoek de eerder aangetroffen mechanismen en alternatieve combinaties opnieuw voordat deze specificatie wordt vastgesteld. Dit document bewaart de eerdere publieke ontwerpafspraken, niet de private broninhoud. Het is geen productiearchitectuur, implementatie of testresultaat.

Zie ook de [visuele onderzoeksatlas](../docs/illustraties/atlas/README.md) voor openbare bronbevindingen, mechanismen, vergelijking A–D en geplande verificatie.

## Vraag en afbakening

Hoeveel technisch werk is nodig om dezelfde abstracte aanvraag af te handelen via A, B, C en D? Alle vier delen dezelfde geldige bron, bevoegdheden, gewone softwarefuncties en toetsbare technische voorwaarden. In fase 4a gebruiken we neutrale gegevens en stub-adapters. Geen nieuwe vakinhoud, didactische scenario's, tutorprompts, model- of hostingkeuze. De inhoudelijke kwaliteit, leeruitkomsten en werkelijke kosten worden niet met deze stubs gemeten.

## Verantwoordelijkheden

| Onderdeel | Doet | Grens |
| --- | --- | --- |
| Framework | Definieert begrippen, relaties en invarianten | Schrijft geen runtime of provider voor |
| SSOT | Beheert gezaghebbende gegevens, identiteit, revisie en herkomst | Interpreteert geen onbekende vraag |
| Compiler | Normaliseert en valideert bronnen en regels; maakt uitvoerbare gegevens | Voegt geen eigen betekenis of beleid toe |
| Policy | Bepaalt bevoegdheden en toegestane bewerkingen | Bewijst geen vrije semantische juistheid |
| Logic | Past toetsbare regels toe; kan UNKNOWN teruggeven | Behandelt onzekerheid niet als vastgesteld feit |
| Engine | Voert een afgebakende bewerking uit | Wijzigt geen onbevoegde gegevens |
| Pipeline | Voert expliciete transformaties uit | Verplicht niet alle stappen bij elke aanvraag |
| Orchestrator | Kiest toegestane uitvoerder, terugval en budget | Creëert geen bevoegdheid of bronwaarheid |
| Context & Memory | Levert actuele staat en benodigde observaties | Maakt modelvermoedens niet gezaghebbend |
| AI-adapter | Vertaalt modeltaak, voorstel en gebruiksgegevens | Kiest niet zelf provider, route of budget |
| Runtime | Verwerkt aanvragen, deadlines, herstel en meetgegevens | Verwisselt technisch succes niet met inhoudelijke juistheid |

Eén proces met kleine verwisselbare functies en adapters is voldoende voor de eerste proef. Dit zijn verantwoordelijkheden, geen elf verplichte services. Geen solver, vectorstore, permanente agent, autonome planner, productiedatabase of langdurig geheugen in 4a.

## Vergelijking

| | A | B | C | D |
| --- | --- | --- | --- | --- |
| Gewone functies en bron-/beleidsrevisie | Gedeeld | Gedeeld | Gedeeld | Gedeeld |
| Context | Relevante standaardcontext | Geoptimaliseerd | Als B | Als B |
| Experimentele modeltaak | Model | Zelfde modeltaak | Alleen waar nodig; selectie of generatie | Als C |
| Extra modelvrije assistentroute | Geen experimentele bypass | Geen experimentele bypass | Toetsbare regel/engine | Zelfde regels/engine |
| Modeladapter | Extern | Zelfde modelrevisie | Zelfde modelrevisie | Lokaal |
| Externe runtime-inferentie | Binnen budget toegestaan | Als A | Alleen op modelroute | Niet toegestaan |

Alle varianten gebruiken gewone lookup zonder model wanneer de gevraagde functie dat toelaat. Dat is geen besparing van C. Normale caching blijft in A beschikbaar; B onderzoekt gerichte context-, representatie-, prefixcache- en uitvoeroptimalisatie rond dezelfde modeltaak. Een gevalideerde hele-antwoordcache die modelwerk overslaat is een aparte bypassproef bij C/D, niet een verborgen verschil tussen A en B.

D mag geen externe runtime-inferentie gebruiken, ook niet voor embeddings, selectie, samenvatting, classificatie of foutafhandeling. In 4a zijn alle adapters stubs; geen externe of lokale echte inferentie. C/D verschillen later mogelijk in model én hosting. Onderzoek waar haalbaar ook dezelfde gewichten, tokenizer, chattemplate, kwantisering en taakcontract op verschillende infrastructuren. Eigen hosting is niet gratis.

## Voorbereiding en uitvoering

Voorbereiding: bronbundel → schema- en referentiecontrole → compilatie → versiegebonden artifact. Houd brongegevens en afgeleide gegevens apart. Identificeer het artifact met bronrevisie, compilerrevisie, beleid en inhoudsdigest. Dezelfde canonieke invoer en compilerversie moeten hetzelfde logische resultaat opleveren. Willekeurige uitvoer-ID's, tijdstempels en runmetadata horen niet in de inhoudsdigest.

Runtime: aanvraag autoriseren → actuele revisies lezen → context selecteren → uitvoerder kiezen → uitvoeren → voorstel controleren → rechten en revisies opnieuw controleren → afleveren en registreren.

A/B bereiken voor de experimentele aanvraag de modeladapter. C/D proberen een expliciet toepasselijke regel. MATCH geeft een toetsbare bewerking of referentie; UNKNOWN kan naar één modeltaak als policy dit toestaat; DENY mag niet worden omzeild. Een enginefout is niet automatisch UNKNOWN. Een modeltaak mag in één call interpreteren én een voorstel leveren, zonder verplichte classifier of reviewer.

## Gegevenscontract (logisch, nog geen schema)

| Record | Minimaal benodigde velden |
| --- | --- |
| Bundle | bundle_id, revision, schema_version, digest, records met id en payload, source_refs |
| Artifact | bundle_id, revision, compiler_revision, policy_revision, digest, allowed_refs |
| Context | scope_id, session_id, context_revision, bundle_ref, policy_revision, observed_events, allowed_operations |
| Request | request_id, context_revision, operation, input |
| Decision | route, rule_id of null, reason_code, allowed_refs, required_capability |
| Proposal | kind, payload of ref_id, used_refs |
| Outcome | request_id, status, executed_route, payload/ref, revision, reason_code |
| Attempt | attempt_id, request_id, variant, task, provider/model_revision, transport_state, usage, duration, cost_basis, error |
| RunManifest | run_id, variant, code_revision, fixture_digest, config_digest, mode, seed indien ondersteund, budgets, timestamps |

De bevoegde bronhouder bepaalt Bundle; de compiler maakt Artifact; de server bepaalt Context uit gecontroleerde bronnen. De caller levert Request, maar mag de gezaghebbende scope, beleids- en bronrevisie niet bepalen. De orchestrator kiest Decision. Engine of model maakt Proposal; de runtime levert Outcome pas na controle. De meetadapter registreert Attempt en de proefrunner bevriest RunManifest. IDs en hashes zijn geen toegangscontrole. Ontbrekende verplichte gegevens leiden tot een expliciete fout of unknown.

Voorstellen: SELECT (bestaande toegestane referentie met begrensde parameters; de runtime haalt de echte payload op), GENERATE (nieuwe abstracte output), CLARIFY (ontbrekende invoer) of HANDOFF (zichtbare overdracht/onbeschikbaarheid). Een engine kan ook een directe waarde leveren. Een geldige referentie of schema bewijst geen passende keuze of semantische juistheid.

## Functiegrenzen

| Functie | Invoer → uitvoer |
| --- | --- |
| compile | Bundle, policy, compiler_revision → Artifact of validation_error |
| resolve_context | Geauthenticeerde aanvraag en actuele bronnen → Context of reject |
| select_context | Context, Request, strategy → toegestane context |
| decide | Context, Request, capabilities → Decision |
| execute_rule | Decision, begrensde gegevens → Proposal, UNKNOWN of fout |
| infer | ModelTask, geselecteerde context, budget → Proposal en Attempt |
| validate_and_commit | Proposal, huidige revisies en rechten → Outcome of reject |
| observe | Trace, Attempt/Outcome → meetrecord |

Variant en adapter worden door de proefrunner gekozen, nooit door vrije tekst. D krijgt een lokaal uitvoeringsprofiel met externe inferentie verboden. Een test met een fake adapter bewijst geen echte netwerkisolatie; transport en netwerkgrens moeten later daadwerkelijk worden getoetst.

## Staat, fouten en herstel

Request-ID is uniek binnen de geldige scope en sessie. Identieke herhaling mag naar een bestaand resultaat of lopend werk verwijzen na hernieuwde autorisatie; gewijzigde invoer met hetzelfde ID geeft conflict. Bind deduplicatie aan genormaliseerde invoer en relevante revisies. Bewaar een monotone contextrevisie, ook als een waarde terugkeert naar haar oude stand. Een ingetrokken bron of gewijzigd recht blokkeert aflevering van een lopend voorstel. Controleer dit op de aflever-/commitgrens. Een proceslokale map is alleen bewijsbaar voor de enkelprocesproef, niet voor replica's.

| Situatie | Verwachte afhandeling |
| --- | --- |
| Ongeldige scope, revisie, bewerking | Afwijzen vóór dispatch |
| Geen geldige bekende route | UNKNOWN; alleen toegestane modelroute |
| Ongeldige of ingetrokken referentie in voorstel | Afwijzen; niet op gelijkenis vervangen |
| Context verandert tijdens modeltaak | Niet afleveren; poging registreren |
| Dubbele aanvraag of ID-conflict | Geen dubbele uitvoering; conflict expliciet |
| Timeout, uitval, gedeeltelijk resultaat | Onvoltooide uitkomst; behoud gemelde usage |
| Onzekere dispatch of facturering | Unknown; geen blinde retry of nulboeking |
| Lokale adapter D niet beschikbaar | Zichtbare onbeschikbaarheid; geen externe terugval |
| Budget bereikt | Geen nieuwe poging; registreer lopend werk |

Normaal één logische modeltaak per experimentele aanvraag en geen automatische retries. Alleen de aparte test met een definitief geweigerde dispatch mag binnen een vooraf vastgelegd proefbudget een tweede poging starten. Houd lokale poging, daadwerkelijk verzonden request en door provider geaccepteerde/afgerekende request uit elkaar. In een latere echte runtime moeten totale deadline, annulering, wachtrijgrens, attemptbudget en proceslevensduur daadwerkelijk worden afgedwongen.

## Meetcontract

Eén trace per aangeboden aanvraag, ook bij afwijzing of fout. Registreer alle werkelijk gestarte pogingen en uitgevoerde routes apart. Bewaar geen onnodige ruwe input in de telemetrie. Een niet-afgeleverd antwoord kan toch kosten veroorzaken.

Gebruik afzonderlijke velden voor input_total, input_cache_read, input_cache_write, output_total, reasoning_reported en overige providerunits, inclusief bron en definitie. Onbekende waarden blijven null met reden. Sommige usagevelden zijn deelverzamelingen; tel ze niet dubbel. Gesimuleerde of geschatte usage is geen providerusage. Werkelijke facturering vergt het gedateerde providercontract. Meet ook externe requests, lokale inferenties, gewone engine-uitvoeringen, contextbytes, queue-/verwerkingstijd, niet-afgeleverde uitkomsten en afwijkingen.

Rapporteer kosten per aangeboden aanvraag en per technisch geslaagde aanvraag, met aantallen, fout- en uitvalstatus. In een latere echte proef worden inhoudelijke bruikbaarheid, voorbereiding, hardware, idle, beheer, cache, herstel en authoringkosten apart meegewogen. Geen extrapolatie vanuit stubtokens of kunstmatige timings.

## Eerder voorgesteld proefpakket (nog niet starten)

[Proeven P01–P03](../benchmarks/TECHNISCHE-PROEVEN.md) toetsen deze afspraken op één gedeeld technisch proefprogramma. Bevries fixture, verwachtingen en configuratie vooraf. Alle voorgeschreven technische invarianten moeten slagen voordat de eerste proef als geslaagd wordt geboekt. Een ontbrekende route, lek, stale aflevering, onverwachte externe dispatch of ontbrekend attempt-record is een fout, geen ongetest succes.

Geen architectuurbesluit, echte modelrun, kwaliteitsmeting, vakinhoud of betaalde proef in deze fase. P04–P07/P09 volgen waar technisch nodig. P08/P10 wachten op modelkeuze, beschikbare infrastructuur en budgetbesluit. Zie [plan v0.4](../docs/PLAN.md).
