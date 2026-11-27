# Verdiepende verkenning — 27 november 2026

> Historische verkenning: deze bevindingen blijven voorlopige bronnen. De huidige technische uitwerking staat in de [specificatie v0.1](TECHNISCHE-SPECIFICATIE.md). Fase 4a toetst technische contracten; inhoudelijke uitwerking en definitieve hergebruikbesluiten blijven open.


## Aanleiding en afbakening

Een methodegebonden assistent ondersteunt leerlingen wanneer zij zelfstandig werken. Neon beschrijft in zijn openbare vacature en pilotberichten een onderzoek naar passende hints, wedervragen en uitleg, afgestemd op vak, niveau en leerdoel. De leraar blijft de les geven. De methodes zijn aanpasbaar; de assistent moet mogelijk ook kunnen omgaan met aangepaste inhoud, ander taalniveau en verschillende ondersteuningsafspraken. Zie [de afzonderlijke Neon-bronnen](neon/BRONNEN.md).

We weten niet hoe de interne chatbot werkt, of welke kosten werkelijk worden gemaakt. Circa 700.000 leerlingen bij aangesloten scholen is bereik en geen gebruiksmeting. De huidige openbare €10 miljoen betreft organisatiekosten, niet bewezen modelkosten. De vergelijking A–D onderzoekt een eigen referentie-implementatie.

## Bevindingen die het ontwerp veranderen

### De methode is een gegevensbron

De school of docent kan een opdracht wijzigen. Een assistent moet daarom de geldige opdrachtversie, het leerdoel, beschikbare bronpassages en de toegestane steun kennen. Hetzelfde vraagwoord kan in twee opdrachten een andere passende reactie vereisen. Versiebeheer, afgeleide inhoud en cache-invalidering zijn onderdeel van de assistent, niet alleen van de contenteditor.

Waar een bestaande leeromgeving gegevens kan aanleveren, is inferentie voor het opnieuw ontdekken van vak, leerjaar, fase of opdracht niet vanzelf nodig. Een generatief model mag ontbrekende gezaghebbende velden niet zelf als feit invullen.

### Bestaande intelligente tutorsystemen

| Bron | Relevant bestaand werk | Bewijsgrens |
| --- | --- | --- |
| [GAIMHE: architectuur](https://gaimhe.github.io/project/) | Adaptieve sequencing blijft bij het tutorprogramma; vooraf genereren van opdrachten, hints en feedback; live generatie bij gerichte behoefte. | Onderzoeksarchitectuur, geen bewijs voor besparing bij Neon. |
| [GAIMHE dataset card](https://huggingface.co/datasets/GAIMHE/Neurips) | De kaart meldt 7.239.840 interacties van 45.848 leerlingen bij 7.845 opdrachten, afkomstig uit Adaptiv'Math en MIA Seconde. Informatie over opdrachten, pogingen en pedagogische grafen. | Geen gebruiksgegevens van Neon, geen vrij toegankelijke productiedata: gated, CC-BY-NC-SA 4.0, uitsluitend niet-commercieel onderzoek, gegevens van minderjarigen. Alleen publieke beschrijving als inspiratie; geen toegang aangevraagd of dataset gedownload. |
| [CTAT](https://tat.pact.cs.cmu.edu/CMUCTAT/CTAT/docs/index.html) / [voorbeeld-tracing onderzoek](https://doi.org/10.1007/s40593-015-0088-2) | Auteurs leggen meerdere geldige oplossingsroutes en hints vast; tutor herkent stappen. | Vereist inhoudsontwikkeling; CTAT is gratis voor onderzoek, niet vanzelf vrij voor elk gebruik. |
| [ASSISTments authoring](https://lib.dr.iastate.edu/imse_pubs/98) | Per opdracht feedback, hints, stapsgewijze hulp en variabelen; hergebruik bij auteurs. | Wiskundige context overheerst in de beschreven implementatie; geen bewijs dat dezelfde aanpak alle vrije taalvragen afdekt. |
| [STACK answer tests](https://docs.stack-assessment.org/en/Authoring/Answer_Tests/) | Controle van algebraïsche equivalentie, numerieke eigenschappen en gerichte feedback met computeralgebra. | Controleert afgesproken eigenschappen van antwoorden; zegt niet zonder meer dat een leerling zelf kan redeneren. |
| [LanguageTool](https://github.com/languagetool-org/languagetool) | Lokaal inzetbare spelling- en grammaticacontrole in verschillende talen. Kerncode LGPL-2.1-or-later volgens repository. | Foutsignaal kan onjuist of irrelevant voor leerdoel zijn; automatisch corrigeren kan de bedoelde leerlinghandeling wegnemen. |
| [H5P branching scenario](https://h5p.com/content-types/branching-scenario) | Vertakkende interactieve activiteiten en vooraf vastgelegde feedback. | Geen algemene conversatietutor; onderzoek of bestaande activiteit al voldoet voordat een chatbot wordt toegevoegd. |

### Aansluiting op bestaande gegevensformaten

[CASE 1.1](https://standards.1edtech.org/case/) beschrijft uitwisseling van leerdoelen, competenties en relaties; [QTI](https://www.1edtech.org/standards/qti) uitwisseling van vragen en tests. Onderzoek aansluiting, gebruik geen nieuw formaat waar een bestaand contract volstaat. Dit betekent niet dat Neon deze standaarden gebruikt. Het oudere Nederlandse NLQTI-profiel wordt niet meer beheerd en heeft [einde registratie](https://www.edustandaard.nl/standaard_werkgroepen/uitwisseling-toetsmateriaal/). Niet als verplichte actuele standaard voorstellen. EAI Standard beschrijft de menselijke handeling en de AI-bijdrage; deze beschrijving vervangt geen content- of uitwisselformaat.

### Wat de EAI-bronnen toevoegen

De actuele [EAI Standard public interface](https://github.com/E-AI-MODEL/EAI-standard/blob/main/standard/public-interface.yaml) vermeldt 0.5.0-candidate. De kandidaat is geen vastgestelde sectorstandaard. Zie [human-system boundary](https://github.com/E-AI-MODEL/EAI-standard/blob/main/docs/human-system-boundary.md), [evidence and handback](https://github.com/E-AI-MODEL/EAI-standard/blob/main/docs/evidence-handback-remediation.md), [scaffolding microstructures](https://github.com/E-AI-MODEL/EAI-standard/blob/main/registries/microstructures/teacher-scaffolding-and-feedback.yaml). Beschrijf welke handeling de leerling zelf uitvoert, welke steun het systeem geeft en wat als bewijs kan worden gebruikt. Ondersteuning met een vooraf geschreven hint is niet automatisch minder of meer didactisch verantwoord dan dezelfde hint uit een model. Beide kunnen de beoogde handeling overnemen.

Oudere technische implementaties tonen dat context en didactische beslisregels buiten een model kunnen bestaan, maar bevatten andere EAI-versies. Gebruik technische patronen niet als automatische formele EAI-classificatie. Beschrijf daadwerkelijke regels, bronversies en bewijs; onbekend is geen negatieve score. Zie [hergebruik](HERGEBRUIK.md).

### Technieken voor efficiëntere inferentie

| Techniek | Te toetsen | Primaire referentie |
| --- | --- | --- |
| Vermijd modelaanroep | Bestaande opdrachtfeedback, precieze bronselectie, regels, vaktools of reeds beoordeelde hint; meet correcte dekking én foutieve automatische routes. | GAIMHE, CTAT, STACK |
| Selecteer context | Minder input zonder noodzakelijke bron- of didactische informatie te verliezen; behoud exacte inhoudsversie. | [RAG EAT](https://github.com/E-AI-MODEL/-rag-eat-starter-kit) |
| Compact formaat | Meet echte tokens en semantische taakprestatie op hetzelfde contextobject; geen winst aannemen bij willekeurige korte of onregelmatige data. | [TOON](https://github.com/toon-format/toon), [Caveman-eduNL](https://github.com/E-AI-MODEL/Caveman-eduNL) |
| Prefixcaching | Identieke stabiele promptdelen hergebruiken; echte cachehit, schrijf-, opslag- en leestarieven per model/provider. Contextcompactie kan cachehits verminderen, vergelijk netto kosten. | [OpenAI caching diagnostics](https://developers.openai.com/api/docs/guides/prompt-caching/diagnostics), [vLLM APC](https://docs.vllm.ai/en/latest/features/automatic_prefix_caching/) |
| Gecontroleerde antwoordcache | Alleen hergebruik van aantoonbaar toepasbare, beoordeelde inhoud; geen cross-user persoonscontext, sleutel op les- en beleidsversie en benodigde scope; meet foute hits. | Ontwerpvoorstel, niet bewezen door prefixcache |
| Modelroutering | Niet-generatieve classifier, router op context of klein model; vergelijken met één model en betaalde cascade inclusief alle extra calls. | [RouteLLM](https://arxiv.org/abs/2406.18665), [FrugalGPT](https://arxiv.org/abs/2305.05176) |
| Zelfhosting / kwantisering / batching | Zelfde model waar mogelijk; capaciteit bij realistische prefill/decode, kwaliteit na kwantisering, idle-kosten en wachtrij. | [vLLM](https://vllm.ai/blog/2025-09-05-anatomy-of-vllm), [Inference Perf](https://github.com/kubernetes-sigs/inference-perf/) |
| Lokaal op apparaat | Toets browserondersteuning, geheugen, laadtijd, netwerk/downloads, update, stroom, kwaliteit en toegangsgelijkheid; aanvullende optie, niet verplicht voor D. | [EAIspeak](https://github.com/E-AI-MODEL/website/tree/main/tools/eaispeak) |
| Specifiek getraind klein model | Pas onderzoeken wanneer gelabelde, rechtmatig bruikbare voorbeelden, kwaliteitseisen en trainingskosten bekend zijn. | GAIMHE onderzoeksrichting; [Intent Matters](https://arxiv.org/html/2506.07626) |

Prefixcaching bespaart herverwerking van het begin van de prompt; niet automatisch nieuwe outputtokens. Een kortere prompt is niet altijd goedkoper dan een langere prompt met veel cachehits. Gzip voor opslag is geen tokencompressie. Een lokaal model heeft geen externe tokenfactuur, maar gebruikt rekenkracht. Een generatieve reviewer kan de besparing tenietdoen. Al deze effecten moeten afzonderlijk worden gemeten.

## Evaluatie buiten onze projecten

- [MRBench / Unifying AI Tutor Evaluation](https://arxiv.org/abs/2412.09416) (2025): 192 gesprekken, 1.596 tutorreacties en annotaties voor acht pedagogische dimensies, onder meer foutlocatie, begeleiding en antwoord prijsgeven. Wiskundige dialoog, geen onafhankelijke leerwinstmeting.
- [TutorBench](https://arxiv.org/abs/2510.02663) (2025): 1.490 expertontworpen voorbeelden voor uitleg, feedback en hints; specifieke rubrics per voorbeeld. De onderzochte modellen scoorden geen 56% of hoger. Automatische beoordeling met LLM-judge en beperkt bereik; geen algemene uitspraak over actuele modelkwaliteit in Nederlands onderwijs.
- [Bastani et al.](https://doi.org/10.1073/pnas.2422633122) (2025): in een middelbare-schoolwiskunde-experiment waren betere prestaties met ondersteuning geen bewijs van betere prestaties zonder AI. De door docenten gevoede tutor beperkte het geobserveerde negatieve effect van de vrijere chatbot. Dit resultaat geldt voor de onderzochte interventies; geen bewijs voor een eigen hybride implementatie.
- [Tutor CoPilot](https://arxiv.org/abs/2410.03017): helpt menselijke tutors tijdens hun werk. Dit is een andere inzetvorm dan een autonome leerlingchatbot. De beschreven kosten per tutor en resultaten kunnen niet rechtstreeks naar kosten per leerlingchat worden vertaald.

Gebruik deze bronnen om de beoordelingsrubrics te ontwerpen en waar rechtmatig mogelijk bestaande gevallen te hergebruiken. Maak eigen Nederlandse gevallen met echte vakinhoudelijke variatie, niet alleen vertaalde wiskundevragen. Laat beoordelaars meerdere geldige antwoorden accepteren. Een technische regeltest, tutorantwoordbeoordeling en onafhankelijke leerlingprestatie zijn afzonderlijke onderzoeksuitkomsten.

## Besluiten voor v0.2

De eerste oplevering is een functie- en techniekvergelijking, niet een volledige Franse les. De twee beoogde contrasten zijn Frans en rekenen. Een kleine verticale proef moet aantonen dat gedeelde functies in verschillende vakken werken en waar een vakspecifieke adapter nodig is.

Neem kosten van het vooraf maken, beoordelen en onderhouden van lesgebonden steun mee. De besparing door hergebruik is afhankelijk van hoeveel leerlingen daadwerkelijk dezelfde goedgekeurde inhoud mogen gebruiken. Bereken daarnaast piekcapaciteit, idle-kosten, uitval en docentverkeer. Zie [schaalmodel](../benchmarks/SCHAALMODEL.md).

## Status en brongebruik

Deze verkenning gebruikt openbare primaire bronnen en selectieve inspectie van bestaande eigen repositories en eerdere onderzoeksverslagen. De openbare bronnen ondersteunen de beschreven mogelijkheden, niet de geschiktheid van onze nog te bouwen oplossing. Er zijn geen nieuwe modelruns, belastingtests, leerlingproeven, security-audits of integraties uitgevoerd. Niet alle eigen repositories zijn regel voor regel opnieuw beoordeeld. Er is geen interne Neon-code of gebruiksdata beschikbaar. De definitieve hergebruiksaudit, licentiebesluiten en technische proeven blijven volgende werkpakketten.
