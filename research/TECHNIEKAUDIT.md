# Fase 3 — technische selectie

27 november 2026. Gerichte broncodeaudit, geen uitgevoerde runtimeproef. Deze audit onderzoekt overdraagbare technieken. Oudere onderwijsinhoud, rubrics, EAI-versies, modellen, prompts en domeinkennis worden niet als actuele inhoud overgenomen. De geldende onderwijsafspraken en EAI-semantiek worden afzonderlijk gekozen. Geen bestaande applicatie wordt in haar geheel als afhankelijkheid aangewezen.

## Besluiten voor de technische proef

| Mechanisme | Eerste keuze voor proef | Waarom / wat kan tegenvallen |
| --- | --- | --- |
| Antwoordroute vóór generatie | Kleine gewone beslisfunctie met expliciete onbekend-route; gecontroleerde hint of vakspecifieke tool waar passend | Voorkomt een generatieve call wanneer voldoende gegevens beschikbaar zijn; verkeerde automatische beslissingen kunnen de leerling slechter helpen. Geen universele regex-classifier. |
| Lesversie en actuele context | Server-side immutable versie-identiteit, expliciete docentwijziging, aparte tijdelijke beurtcontext | Voorkomt herhaalde extractie en verkeerde bronversies. Een validatieschema alleen verleent geen bevoegdheid. |
| Contextpakket | Selecteer benodigde velden en bronankers; vergelijk met volledige relevante context | Geen volledige SSOT of dossier in iedere prompt. Afkappen op tekens kan benodigde informatie verwijderen. |
| Retrieval | Eerst exacte les-/opdracht-ID; daarna een geïndexeerde tekstzoeklaag; embeddings/reranking alleen bij aantoonbaar tekort | Vermijdt zoeken en genereren waar gegevens al bekend zijn. Meet dekking en foutieve hits per taal en lesversie. |
| Instructie en uitvoer | Vaste begrensde acties, machineleesbaar contract; zo nodig een modelvoorstel met toegestane actie-ID | Gestructureerde uitvoer maakt validatie mogelijk, maar bewijst geen juiste betekenis. Geen automatische volledige rubric-analyse. |
| Cache | Goedgekeurde hints op volledige geldige contextidentiteit; aparte prefixcache voor modelinvoer | Bespaart werk bij echt hergebruik. Semantische gelijkheid van vragen is onvoldoende voor hergebruik van persoonlijke antwoorden. |
| Modeladapter en meetgegevens | Eén providercontract met feitelijke usage per poging, status, deadline, bytes, annulering, optionele cache- en prijsvelden | De kostenvergelijking werkt alleen wanneer ook extra modelcalls, afgebroken uitvoer en retries zichtbaar zijn. |
| Gelijktijdigheid | Begrensde toelating, wachtrij, request-ID, versiecounter, transactie en expliciete overbelasting | Geen onbeperkte retries, lokale process-lock of IP-limiet als landelijke garantie. |
| Gedeelde implementatie | Eén authored set contracten, beleid en fixtures voor A–D; eenvoudige modules achter interfaces | Vermijdt afwijkende definities en vier verschillende codebases. Geen zware generatietoolchain nodig tenzij meerdere runtimes dat vereisen. |
| Evaluatie | Routebereik zonder provider, echte modelcalls apart, regel in observatiemodus vóór activeren | Voorkomt dat een betaalde proef technisch slaagt maar de onderzoeksvraag niet bereikt. |
| Zelfhosting | Ollama voor kleine lokale vergelijkingsproeven; vLLM als kandidaat voor belastingsproef | Ollama-proef op CPU is geen landelijke capaciteitsmeting. Geen GPU-besluit vooraf. |
| Decentraal model | Browser/WebGPU als afzonderlijke optie na de basisproef | Geen externe tokenrekening, maar apparaatondersteuning, downloads, kwaliteit en distributie blijven kosten en voorwaarden. |

## Geïnspecteerde openbare implementaties

Onderstaande verwijzingen wijzen naar de tijdens deze ronde gelezen versie. Een testbestand is gelezen bewijs van de beoogde controle, niet bewijs dat de test opnieuw is geslaagd. Voor private projecten worden alleen algemene ontwerpvoorwaarden gepubliceerd, geen private broncode, interne testgegevens of bevindingen over specifieke kwetsbaarheden.

### Adapter, uitvoer en daadwerkelijke tokenmeting

- [EAIwork: ollama-chat.ts](https://github.com/E-AI-MODEL/EAIwork-/blob/8754936ffe594766339e8f8493c963c41a0b4206/packages/gateway/src/ollama-chat.ts): gedeelde HTTP-mechaniek met begrensde responsebytes, abortsignaal, expliciete transport-/outputstatus en metingen per poging. Leest `prompt_eval_count`, `eval_count` en runtime-durations rechtstreeks uit de Ollama-envelope. Ontbrekende velden blijven ontbrekend. De observer draait in finally en een observerfout verandert het modelresultaat niet.
- [EAIwork: ollama-provider.ts](https://github.com/E-AI-MODEL/EAIwork-/blob/8754936ffe594766339e8f8493c963c41a0b4206/packages/gateway/src/ollama-provider.ts) en [provider-tests](https://github.com/E-AI-MODEL/EAIwork-/blob/8754936ffe594766339e8f8493c963c41a0b4206/tests/ollama-provider.test.ts): afzonderlijke modelcontracten en een geteste bedoeling voor een extra aanvraag bij een niet-ondersteunde think-optie. Die tweede call moet meetellen. De bestaande kansverdelingen en claimvalidatie passen niet rechtstreeks bij tutoring. Geen bewezen factuurreconciliatie.
- [EAIwork: gateway.ts](https://github.com/E-AI-MODEL/EAIwork-/blob/8754936ffe594766339e8f8493c963c41a0b4206/packages/gateway/src/gateway.ts): begrensde broncontext, expliciete toegestane input en afgebakende sessie. De limiet is in tekens, niet tokens; gebruik een tokenizer of providergegevens voor tokenmeting. De complete workerarchitectuur is niet nodig voor de eerste proef.
- Rechten: [PolyForm Noncommercial 1.0.0](https://github.com/E-AI-MODEL/EAIwork-/blob/8754936ffe594766339e8f8493c963c41a0b4206/LICENSE). Het licentiecontract bevat ook een bepaling voor non-profitorganisaties. Controleer het daadwerkelijke gebruik, de afnemer en distributie vóór overname. Hier is alleen het technische patroon geselecteerd.

### Retrieval en bronversie

- [RAG EAT: retrieval.py](https://github.com/E-AI-MODEL/-rag-eat-starter-kit/blob/1c98f0d04a179fc8df40383870c81d032385ee50/src/ragkit/retrieval.py) filtert toegestane chunks en berekent BM25 en TF-IDF opnieuw over toegankelijke chunks. In deze implementatie is dit geen vector-ANN-index. De ASCII-georiënteerde tokenizer is een aandachtspunt bij meertalige invoer. De family-selectie kan meerdere relevante passages tot één passage reduceren en kiest mede op datum. Geen goede algemene keuze voor expliciet toegewezen lesversies. De relatieve scoredrempel is geen gekalibreerde zekerheid.
- [Assistant](https://github.com/E-AI-MODEL/-rag-eat-starter-kit/blob/1c98f0d04a179fc8df40383870c81d032385ee50/src/ragkit/assistant.py) gebruikt een verwisselbaar zoekcontract en kan zonder LLM een extractief antwoord teruggeven. De LLM-route wordt niet automatisch inhoudelijk gevalideerd door bronvermelding. [Tests](https://github.com/E-AI-MODEL/-rag-eat-starter-kit/blob/1c98f0d04a179fc8df40383870c81d032385ee50/tests/test_retriever_protocol.py) bevatten verwisselbare retrievers en toegangs-/geen-brongevallen. Het contract en de MIT-licentie zijn interessant; schaalbare indexering, server-side identiteit en inhoudelijke controles apart ontwerpen.
- [EAIhome: search.py](https://github.com/E-AI-MODEL/EAIhome/blob/52356fc75097da7f6361739f29d49182cc9d0b2a/src/eaihome/search.py) en [store.py](https://github.com/E-AI-MODEL/EAIhome/blob/52356fc75097da7f6361739f29d49182cc9d0b2a/src/eaihome/store.py): versiebehoud, SHA-256, herstelbare SQLite FTS-index en toegangsfilter. De [bestaande tests](https://github.com/E-AI-MODEL/EAIhome/blob/52356fc75097da7f6361739f29d49182cc9d0b2a/tests/test_eaihome.py) beschrijven versiebehoud, duplicaten, gewijzigde bronbytes en toegang. Niet de hele lokale opslagservice overnemen: de groepsparameter is geen geauthenticeerde gebruiker en bronrevisie is niet automatisch actuele geldigheid. Geen LICENSE-bestand via de gebruikte rootverwijzing opgehaald; rechten apart vaststellen.

### Observatiemodus en begrenzing van werk

- [EAT_me: evaluator.py](https://github.com/E-AI-MODEL/EAT_me/blob/deda94ffb80c4c9b78f40afe23d2db09e65673ea/eatme/evaluator.py) bewaart in observatiemodus welke beslissing een regel zou nemen naast de werkelijke actie. [engine.py](https://github.com/E-AI-MODEL/EAT_me/blob/deda94ffb80c4c9b78f40afe23d2db09e65673ea/eatme/engine.py) laat zien wanneer een echte rewritehook volgt en hoe iteraties worden beperkt. Alleen het onderscheid tussen voorstel en uitgevoerde actie hergebruiken; geen oude scores of rubricbetekenis. Rechten nog niet opgehelderd.
- [NeSy: z3-isolated.ts](https://github.com/E-AI-MODEL/eainesy/blob/e8ce553a3c1c16d072078a62c426ce038cc455d3/src/lib/eainesy/z3-isolated.ts): afzonderlijke grenzen voor lopende workers, backlog, queuewacht en uitvoertijd; workerplaats pas vrijgeven na werkelijk afsluiten. De wachtrij geldt per proces. Neem de begrenzing als patroon, niet de solver, therapeutische taxonomie of vaste aantallen.
- [NeSy: model-provider.ts](https://github.com/E-AI-MODEL/eainesy/blob/e8ce553a3c1c16d072078a62c426ce038cc455d3/src/lib/eainesy/model-provider.ts): getypeerde providerfouten, expliciete backend en retry bij onder meer 429/503. Het HTTP-pad heeft een timeout per aanvraag; geen garantie van één totale deadline over alle pogingen. Een nieuwe adapter moet budget, deadline en onzekerheid over een al uitgevoerde aanvraag bewaken. Rechten nog niet opgehelderd.
- [PiM: egressGuard.ts](https://github.com/E-AI-MODEL/project-pim/blob/840ad1f70b5d86eb9058b08f8d9d649b8773f243/src/lib/pim/egressGuard.ts): controle vlak vóór uitvoer van de exacte payload. Browserdetectie is geen complete privacy- of serverautorisatiegrens. MIT-notice aangetroffen; dependencies en modelrechten afzonderlijk controleren.

### Decentrale inferentie en testbewijs

- [EAIspeak: browser-llm.js](https://github.com/E-AI-MODEL/website/blob/396c17224f0e857166f78408ce47109de9125a34/tools/eaispeak/src/browser-llm.js): WebLLM laden na hardwarecheck, model wisselen, engine hergebruiken en generatie onderbreken. De lijst geeft beschikbare modelkandidaten, geen gemeten schoolapparaatdekking. Geen claim dat elke browser/Chromebook/iPad het model kan draaien. Licenties van sitecode, engine en modelgewichten apart.
- [EAI Lab: event_store.py](https://github.com/E-AI-MODEL/EAI-lab-/blob/7c76ed3426e1a478c726ceecc2136e96fe671c95/src/eai_lab/event_store.py): gescheiden real/simulation namespaces, unieke event-ID en defensive copies. In-memory, dus geen productiedatabase; de conversie met bool() is niet hetzelfde als strikte boolean-validatie. Gebruik het concept voor testdata en uitvoeringsbewijs, geen oude formele EAI-labels. Rechten nog niet opgehelderd.

## Externe alternatieven, gecontroleerd 27 november 2026

| Techniek | Keuze voor vergelijking |
| --- | --- |
| [PostgreSQL/pgvector](https://github.com/pgvector/pgvector) | Exacte lookup en FTS als basis; embeddings alleen wanneer nodig. Approximate zoekindexen kunnen door scopefiltering minder relevante kandidaten teruggeven; toets iterative scans of isolatie van indexen. Geen vectorplatform kiezen vóór meting. |
| [OpenAI prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching) | Voorbeeld van werkelijke cache-read en -write tarieven, minimale prefixlengte, cachebehoud en diagnostics. Geen claim dat iedere provider deze regels volgt. Vergelijk korte context met langere stabiele prefix; tel writes én misses. |
| [vLLM prefix caching](https://docs.vllm.ai/en/latest/features/automatic_prefix_caching/) en [structured outputs](https://docs.vllm.ai/en/latest/features/structured_outputs/) | Bestaande servingfunctionaliteit gebruiken in plaats van zelf GPU-scheduling of grammar-constrained generation schrijven. De runtime dwingt vorm af, niet de betekenis van een hint. |
| [Inference Perf](https://github.com/kubernetes-sigs/inference-perf) | Echte inference-capaciteit, aangeboden verkeerspatroon, latency en goodput (aantal verzoeken dat de eisen haalt). Geen eigen landelijke loadgenerator nodig als bestaand gereedschap voldoet. |
| [RouteLLM](https://arxiv.org/abs/2406.18665) | Alleen testen nadat eenvoudige expliciete routing en één goede modelroute zijn gemeten; eigen kwaliteitseisen en taakmix zijn leidend. |
| [STACK](https://docs.stack-assessment.org/en/Authoring/Answer_Tests/) / [LanguageTool](https://github.com/LanguageTool-org/languagetool) | Vakspecifieke controle achter dezelfde adapterinterface, naast eenvoudige deterministische referentie. Geen automatische beoordeling van leervermogen. |
| [TOON](https://github.com/toon-format/toon) | Optionele representatie voor herhaalde uniforme data. Vergelijk met minified JSON, niet met kunstmatig opgeblazen JSON. Eerst betekenisbehoud en werkelijke tokens meten. |

De nuloptie blijft relevant: een bestaande lesfunctie, gewone lookup of gecontroleerde feedback kan voldoende zijn. Een externe engine is pas een betere keuze nadat de integratielast, licentie, kwaliteit en kosten op de concrete taak zijn vergeleken.

## Schaalvoorwaarden

Het [schaalmodel](../benchmarks/SCHAALMODEL.md) blijft van toepassing. De aangenomen pieken zijn ongeveer 187 leerlingbeurten/s bij brede uitrol en 1.037/s bij het maximale scenario. Een route met drie modelcalls per beurt vraagt driemaal zoveel modelverzoeken als een route met één, nog zonder retries. Dit is geen voorspelling van de werkelijke NEON-belasting. Test dezelfde aangeboden stroom, ook wanneer een variant trager wordt. Meet de daadwerkelijk afgehandelde antwoorden binnen de overeengekomen responstijd.

Gebruik per school/leerling/sessie geautoriseerde scope, met aparte per-user en globale providerbudgetten. Een gedeeld school-IP of proceslokale teller is geen passende identiteit. Een request-ID moet dubbele verwerking bij reconnect onderscheiden van een nieuwe hulpvraag; een versiecounter en atomaire opslag beschermen tegen verouderde modelresultaten. Een timeout zegt niet automatisch dat een externe provider niets heeft verwerkt of gefactureerd.

## Selectiestatus

De bovenstaande technieken zijn voldoende onderbouwde kandidaten voor een kleine onderscheidende proef; er is nog geen codehergebruik goedgekeurd of architectuurbesluit genomen. De openbare audit bevat alleen openbare bronverwijzingen. De interne codevergelijking is in het onderzoeksbespreking gehouden. Niet alle 83 repositories zijn in deze ronde diepgaand geaudit. Er zijn geen nieuwe tests, modelruns of belastingmetingen uitgevoerd. Deze eerste selectie is geen afgeronde hergebruiksaudit. Plan v0.3 heropent de brede verkenning: eerst de [onderzoeksindeling](ONDERZOEKSINDELING.md) volgen en A–D specificeren. [TECHNISCHE-PROEVEN.md](../benchmarks/TECHNISCHE-PROEVEN.md) blijft een concept voor de latere uitvoeringsfase.
