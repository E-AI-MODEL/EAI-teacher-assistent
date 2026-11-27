# Ronde 11 | Van bronvondst naar toetsbare techniek

27 november 2026. Vier Exa-zoekrichtingen met twintig gevraagde resultaatplaatsen, vijf openbare repositories op vaste commits en drie historische eigen projecten gericht herlezen. Veertien verdiepingsrecords; geen veertien nieuwe onafhankelijke algoritmen.

Fase 3b en 3c zijn heropend. Fase 4a blijft NO-GO. Geen nieuwe runtime- of modeltests, echte inferentie, vakinhoud, architectuurkeuze of bewezen kostenbesparing. De volledige bronkoppeling blijft intern; een afgeleide is geen extra onafhankelijke bron.

[Onderzoeksatlas](../../docs/illustraties/atlas/README.md)

## Compiler

| ID | Mechanisme | Bronsoort | Bevinding | Grens / tegenproef |
| --- | --- | --- | --- | --- |
| R11-01 | Getypeerd plan uit bestaande bouwstenen | Code en aanwezige tests | Een planner selecteert nodes uit een register; de validator controleert toegestane nodes, verbindingen, typen, parameters, ariteit en cycli. De compiler sorteert topologisch en assembleert templates. | Bewaar een modelvrij manifest als alternatief voor gegenereerde code. Vergelijk identieke fixtures, inclusief ongeldige of ontbrekende parameters. Geen veiligheidsgarantie door typecontrole alleen. |
| R11-02 | Vrije verbindingscode omzeilt de bedoeling van het manifest | Code-inspectie | De compiler neemt niet-lege glue_code rechtstreeks op in het uitvoerbare artifact; anders genereert hij bindings vanuit het plan. Een getypeerde DAG alleen beperkt die vrije code niet. | Voor onze manifestvariant moet vrije code buiten de toegestane uitvoer liggen. Tegenproef: onbekende node, verboden parameter en vrije uitvoeropdracht. Geen extern script uitgevoerd. |
| R11-09 | Toestandsovergangen met guards | Code-inspectie | Een frontendmodule definieert toegestane toestandsovergangen en per overgang expliciete voorwaarden; automatische overgang kiest de eerste toegestane kandidaat. De historische edgefunctie bevat daarnaast eigen faseberekening. | Niet bewezen dat de frontend-FSM de werkelijke runtime aanstuurt. Vergelijk echte backendbeslissing met contract; expliciete fout bij onbekende guard, conflict tussen toegestane routes en verouderde staat. |
| R11-10 | Drift tussen client, SSOT en uitvoerende functie | Code en aanwezige tests | Een versiegebonden 32-bit inhoudshash en tests vergelijken brondata met in de test overgeschreven edge-constanten. | Een 32-bit hash is geen cryptografische authenticatie; een test die gekopieerde constanten vergelijkt ziet niet noodzakelijk actuele edgecode. Genereer beide uit dezelfde bron of test het echte runtimeartifact. |

## Routering

| ID | Mechanisme | Bronsoort | Bevinding | Grens / tegenproef |
| --- | --- | --- | --- | --- |
| R11-03 | Gekalibreerde modelkeuze | Code-inspectie | Controller routeert tussen een sterk en zwak model met een expliciete drempel. De laatste berichtinhoud voedt de router. Kalibratie gebruikt een quantiel van een eerder datasetbestand om een gewenste sterke-model-fractie te benaderen. | Een drempel voor het gewenste aandeel is geen kwaliteitsgrens; toets op nieuwe representatieve input, contextafhankelijkheid en onthouding bij onzekerheid. Houd modelpaar gelijk waar mogelijk. |
| R11-04 | Routerkosten tellen mee | Code-inspectie | De similarity-weighted router vraagt een externe embedding op vóór de generatie. Andere routers gebruiken classificatiemodellen. Het ene zichtbare antwoord kan dus voorafgaande inferentie bevatten. | Neem embedding, classificatie, routinglatentie en modeloproep apart op in de trace. Voor lokaal-only gebruik geen externe embedding toestaan. Vergelijk met modelvrije regels en een gewone baseline. |
| R11-11 | Volg alle aanroeppaden | Code-inspectie met callers en endpoints | Een normaal tekstpad kan vooraf classificeren, een antwoord genereren, achteraf classificeren en conditioneel herschrijven; ieder afbeeldingslabel kan een aparte beeldoproep doen. De streamingroute wijkt af. De drie edgefuncties bevatten echte provider-gateway fetches. | Dit zijn statische routes, geen geobserveerde oproepfrequentie of factuur. Tel per aangeboden verzoek iedere dispatch, ook bij fouten. Meet ook het deel dat door lokale beslisregels kan worden vervangen zonder taakverlies. |
| R11-12 | Tokenmeting en schijnzekerheid | Code-inspectie | Een historische fallback rekent inputtokens uit als tweemaal het aantal invoertekens en outputtokens als tekenlengte; die telling sluit ook de extra modelroutes niet in. De reliability-pipeline mapt onbekende labels en gebruikt vaste confidence-waarden. | Geen tokenfactuur, echte onzekerheid of modelkwaliteit afleiden uit zulke heuristieken. Splits schatting, werkelijke providerusage en onbekende velden; behandel onbekende referenties niet als geldige match door fuzzy repair. |
| R11-13 | Adaptief lockvenster als afzonderlijke hypothese | Code-inspectie | Een deterministische kernel kiest de duur van een lock vanuit een updatewindow en dominant snel/middel/langzaam gewicht; houdt de strategie vast tot een herzieningstrigger of ontbrekende context. Een verwante edgekernel gebruikt meerdere entropiesporen. | Het bestaan van een toestandregel bewijst geen besparing of kwaliteit. Vergelijk vaste lock, adaptieve lock en geen lock met gelijk invoerverloop; gebruik aparte intrekkingsregels. Bestaande afgeleiden aanvullen, niet als onafhankelijk mechanisme dubbel tellen. |

## Cache

| ID | Mechanisme | Bronsoort | Bevinding | Grens / tegenproef |
| --- | --- | --- | --- | --- |
| R11-05 | Cache-identiteit en toegangsgrens | Code en ontwerpdocumentatie | Een prefixcache hergebruikt volledige KV-blokken via een hash van voorgeschiedenis, huidige tokens en extra gegevens, waaronder adapters, multimodale hashes en optionele salt. De salt wordt in het eerste blok verwerkt. | Bind de salt server-side aan de toegestane scope; optionele clientinvoer is geen autorisatie. Cache-hit is minder prefillwerk, niet automatisch minder gefactureerde tokens. Meet warm/koud, gelijk/ander recht en bronrevisie. |
| R11-06 | Warmup mag de meting niet vervalsen | Aanwezige tests | De benchmarktest verwacht dat readiness- en warmuprequests een eigen cache_salt dragen. Bij specifieke serverafwijzing kan de benchmark zonder salt terugvallen. | Voor onze proef expliciete cold/warm condities en geen stille downgrade van isolatie. Testcases met afwijzing, transient fout en hergebruik. Geen gemeten prestatieverschil in deze ronde. |

## Runtime

| ID | Mechanisme | Bronsoort | Bevinding | Grens / tegenproef |
| --- | --- | --- | --- | --- |
| R11-07 | Model-lock, onderbreking en nieuwe sessie | Code en aanwezige tests | De browserengine heeft een lock per geladen model, abortcontroller voor reload en interruptsignaal. Integratietests met mockpipeline controleren reset van interrupt, rebuild van gesprek, usage en vrijgave bij afgebroken streams. | Mockpipeline bewijst geen werkelijke GPU-vrijgave. Meet in-flight werk na stop, stop tijdens load, parallelle sessies en resourcehergebruik. |
| R11-08 | Afzonderlijke meting van prefill, decode en numerieke overeenstemming | Code-inspectie | Een benchmarkworker gebruikt dezelfde referentietokens voor een forced-decode controle tegen een CPU-baseline. Bij te weinig vergeleken tokens markeert hij de score als onvoldoende; een gefaalde consistentiefase kan nog een afzonderlijke performancemeting opleveren. | Geen overeenkomst van vrije tekst verwarren met numerieke overeenkomst. Test op identieke modelrevision, quantisatie en context; rapporteer OOM, eerste laadkosten, temperatuur/throttling en mislukte checks. Geen live benchmark uitgevoerd. |
| R11-14 | Regex-outputcontrole is begrensd | Code-inspectie | Een guard kiest afhankelijk van fase een lijst regex-signalen voor ongewenste antwoordpatronen. Een signaal leidt tot een detectiebit. | Een regex die geen match vindt bewijst geen naleving. Test parafrases, ontkenningen en variatie; gebruik detectie als signaal, niet als universele inhoudsgarantie. |

## Bronverwijzingen

- R11-01: [Openbare bron 1](https://github.com/prnvh/plancompiler/blob/002b9d32014302c48cc58aa9e110b3394ed2e003/core/compiler.py); [Openbare bron 2](https://github.com/prnvh/plancompiler/blob/002b9d32014302c48cc58aa9e110b3394ed2e003/core/validator.py); [Openbare bron 3](https://github.com/prnvh/plancompiler/blob/002b9d32014302c48cc58aa9e110b3394ed2e003/tests/test_validator_contracts.py)
- R11-02: [Openbare bron 1](https://github.com/prnvh/plancompiler/blob/002b9d32014302c48cc58aa9e110b3394ed2e003/core/compiler.py); [Openbare bron 2](https://github.com/prnvh/plancompiler/blob/002b9d32014302c48cc58aa9e110b3394ed2e003/core/validator.py)
- R11-03: [Openbare bron 1](https://github.com/lm-sys/RouteLLM/blob/0b64fdafe049e596a3f5657c219329f24af24198/routellm/controller.py); [Openbare bron 2](https://github.com/lm-sys/RouteLLM/blob/0b64fdafe049e596a3f5657c219329f24af24198/routellm/calibrate_threshold.py); [Openbare bron 3](https://github.com/lm-sys/RouteLLM/blob/0b64fdafe049e596a3f5657c219329f24af24198/routellm/routers/routers.py)
- R11-04: [Openbare bron 1](https://github.com/lm-sys/RouteLLM/blob/0b64fdafe049e596a3f5657c219329f24af24198/routellm/routers/routers.py)
- R11-05: [Openbare bron 1](https://github.com/vllm-project/vllm/blob/2696e76225ebb264dbb284571cacd8c081d7ddf4/docs/design/prefix_caching.md); [Openbare bron 2](https://github.com/vllm-project/vllm/blob/2696e76225ebb264dbb284571cacd8c081d7ddf4/vllm/v1/core/kv_cache_utils.py)
- R11-06: [Openbare bron 1](https://github.com/vllm-project/vllm/blob/2696e76225ebb264dbb284571cacd8c081d7ddf4/tests/benchmarks/test_serve_cache_salt.py); [Openbare bron 2](https://github.com/vllm-project/vllm/blob/2696e76225ebb264dbb284571cacd8c081d7ddf4/benchmarks/benchmark_prefix_caching.py)
- R11-07: [Openbare bron 1](https://github.com/mlc-ai/web-llm/blob/df83db6cb05bd78daf0cb1afd8c5da550c4a7c6e/src/engine.ts); [Openbare bron 2](https://github.com/mlc-ai/web-llm/blob/df83db6cb05bd78daf0cb1afd8c5da550c4a7c6e/tests/engine_integration.test.ts)
- R11-08: [Openbare bron 1](https://github.com/abhijitramesh/webgpu-bench/blob/c5c7d19cf69587aa679e6c31aeca08b94ad5a7d3/site/js/run/bench-worker.js); [Openbare bron 2](https://github.com/abhijitramesh/webgpu-bench/blob/c5c7d19cf69587aa679e6c31aeca08b94ad5a7d3/runner.js)
- R11-09: Toegestane inhoudelijke afgeleide; oorspronkelijke koppeling intern.
- R11-10: Toegestane inhoudelijke afgeleide; oorspronkelijke koppeling intern.
- R11-11: Toegestane inhoudelijke afgeleide; oorspronkelijke koppeling intern.
- R11-12: Toegestane inhoudelijke afgeleide; oorspronkelijke koppeling intern.
- R11-13: Toegestane inhoudelijke afgeleide; oorspronkelijke koppeling intern.
- R11-14: Toegestane inhoudelijke afgeleide; oorspronkelijke koppeling intern.

Vergelijk de mechanismen en serieuze combinaties vóór een nieuw besluit over fase 4a.
