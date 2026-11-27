# Bronnenregister: ronde 01

27 november 2026. Fase 3a, eerste brede inventarisatie onder [plan v0.3](../../docs/PLAN.md). Geen selectie voor A–D, geen nieuwe vakinhoud en geen uitvoeringsproeven. Deze ronde bouwt voort op [VERKENNING](../VERKENNING.md) en de [eerdere technische audit](../TECHNIEKAUDIT.md). De afzonderlijke mechanismen blijven onderdeel van hun oorspronkelijke ontwerp.

## Dekking

De volledige huidige onderzoekspopulatie omvat 87 toegankelijke repositories: 83 onder E-AI-MODEL en vier onder eaimodel5. Daarvan zijn 29 openbaar en 58 privé. Het interne register met alle 87 records, vindplaatsen en dekkingsstatus is afzonderlijk opgeslagen in een private werkruimtepagina. In de technische scan van 2 november komen 82 van de 87 huidige repositories voor; vijf staan niet in die scan. De historische dekking is behouden en telt niet als nieuwe broninspectie.

De [openbare repository-index](public-repositories.json) is gecontroleerd tegen de openbare records van het interne register. Hij bevat uitsluitend de 29 openbare repositories. Van zes daarvan is in ronde 01 een boomstructuur en zijn geselecteerde bestanden gelezen, met bronversie hieronder. De overige records hebben in deze ronde alleen metadata; eerdere broninspecties blijven behouden. De inventaris omvat alle toegankelijke repositories ongeacht zichtbaarheid. Niet-openbare vindplaatsen en interne onderzoeksdetails worden niet gepubliceerd. Historische bronnen die niet in de huidige lijsten voorkomen en de bibliotheek vallen eveneens binnen het onderzoek; hun dekking is nog niet compleet. Niet teruggevonden is geen bewijs van verwijdering of vervanging.

Grote repositorybestanden, gekopieerde SDK's, forks en herhaalde fixtures tellen niet als afzonderlijke onderzoeken. Omvang en dekking van uniek materiaal zijn nog niet vastgesteld.

## Vondsten en open vragen

### R01-01 — Lesmateriaal als uitvoerbare gegevens

Sporen: PUR, KNW, ORC, ENG, INT, RUN.

**Bronnen:** WiHTML, commit `449d9d9ec3d0f883bd190fc5287eaccfe1d87854`: [ontwerpafspraken](https://github.com/E-AI-MODEL/wihtml/blob/449d9d9ec3d0f883bd190fc5287eaccfe1d87854/docs/ontwerpafspraken.md), [JSON-lesinhoud](https://github.com/E-AI-MODEL/wihtml/blob/449d9d9ec3d0f883bd190fc5287eaccfe1d87854/docs/json-lesinhoud.md), [normalisatie in index.html](https://github.com/E-AI-MODEL/wihtml/blob/449d9d9ec3d0f883bd190fc5287eaccfe1d87854/index.html#L1168-L1313), [journey-test](https://github.com/E-AI-MODEL/wihtml/blob/449d9d9ec3d0f883bd190fc5287eaccfe1d87854/tests/journey.mjs).

De maker wilde lesinhoud, lesvolgorde, docentgereedschap en afspeelcode onafhankelijk bewerkbaar maken. De code normaliseert gestructureerde lesinvoer naar lokale interactieve onderdelen. Er is een browsertest met import, heropenen en zelfstandige HTML-export. Deze test is niet opnieuw uitgevoerd. Het ontwerp geeft de docent controle over het onthullen van antwoorden. Het is een docentpresentatie, geen bewezen adaptieve leerlingtutor; functies uit het oorspronkelijke lesvoorbeeld zijn niet allemaal gelijkwaardig gegeneraliseerd. Rechten op hergebruik en geschiktheid voor leerlingapparaten blijven open.

**Onderzoeksvraag:** welke ondersteuning kan een leeromgeving als bestaande interactieve activiteit aanbieden, zonder chat of inferentie? Hoe vergelijken we dit met vooraf geschreven hints, vrij taalmodelantwoord en uitgestelde onthulling? Relaties: SSOT 17, EAI Classroom, bestaande intelligente tutorsystemen.

### R01-02 — Expliciete identiteit vóór retrieval

Sporen: KNW, CTX, ENG, AI, RUN.

**Bronnen:** EAT Inline, commit `0bd184f5408bddb9211b9684d7a0ada78a593b8b`: [SPEC 0.3.2](https://github.com/E-AI-MODEL/EAT-inline/blob/0bd184f5408bddb9211b9684d7a0ada78a593b8b/SPEC.md), [benchmarkscript](https://github.com/E-AI-MODEL/EAT-inline/blob/0bd184f5408bddb9211b9684d7a0ada78a593b8b/scripts/run_one_tag_rag_benchmark.py), [resultaten](https://github.com/E-AI-MODEL/EAT-inline/blob/0bd184f5408bddb9211b9684d7a0ada78a593b8b/benchmark/results/wiki-fair-v2-one-tag-rag/one-tag-rag-summary.md).

De specificatie maakt de identiteit van een verwijzing expliciet, maar laat betekenis, resolutiebeleid en autorisatie bij de consumer. In de bestaande proef met 434 exacte registervragen zijn 427 namen uniek gekoppeld; zeven ambigue namen vallen terug op gewone tekstzoekfunctie. De gerapporteerde correcte bronantwoorden zijn 77,42% bij zoeken op naam en 98,85% bij EAT na een unieke naamkoppeling. De twee 100%-routes kregen het correcte ID vooraf uit de testantwoorden. De 100.000 documenten zijn herhalingen van 669 fragmenten uit 40 bronpagina's. Dit meet bronselectie met bekende tags, geen taalmodelkwaliteit, leerlingvraaginterpretatie, landelijk gebruik of bespaarde tokens. De proef is niet opnieuw uitgevoerd.

**Onderzoeksvraag:** hoe ver komen we met door de lesomgeving aangeleverde stabiele opdracht- en bron-ID's, zonder opnieuw een zoekvraag te interpreteren? Vergelijk directe lookup, tekstzoekfunctie en andere retrievers. Geen verplichte EAT-notatie. Een ontbrekend, ambigu of ongeautoriseerd ID moet zichtbaar blijven. Relaties: RAG EAT, bronversies, SSOT-manifesten.

### R01-03 — Bron vinden is niet hetzelfde als bron mogen gebruiken

Sporen: FRM, KNW, LOG, ORC, ENG.

**Bronnen:** Examenreglementcheck, commit `d72dc4806566b9c05f0d8f90f41b972390d5beb5`: [besluiten](https://github.com/E-AI-MODEL/Examenreglementcheck/blob/d72dc4806566b9c05f0d8f90f41b972390d5beb5/docs/DECISIONS.md), [bronbeleid](https://github.com/E-AI-MODEL/Examenreglementcheck/blob/d72dc4806566b9c05f0d8f90f41b972390d5beb5/docs/SOURCE-POLICY.md), [source_gate.py](https://github.com/E-AI-MODEL/Examenreglementcheck/blob/d72dc4806566b9c05f0d8f90f41b972390d5beb5/app/source_gate.py), [analyzer.py](https://github.com/E-AI-MODEL/Examenreglementcheck/blob/d72dc4806566b9c05f0d8f90f41b972390d5beb5/app/analyzer.py), [regressies](https://github.com/E-AI-MODEL/Examenreglementcheck/blob/d72dc4806566b9c05f0d8f90f41b972390d5beb5/tests/test_v33_pipeline.py).

De oorspronkelijke vraag was controle van veranderende normen en documenten zonder juridische schijnzekerheid. De bronpoort controleert identiteit, goedkeuringsstatus, datum, toepasselijk jaar en fragmenthash. Zelfs een geslaagde poort betekent alleen dat de bron in beginsel mag worden gebruikt; de claim vraagt nog passend bewijs. Het huidige analysepad houdt juridische must-claims uitgeschakeld. De tests bevatten onvolledige en niet-toegestane gevallen. Niet opnieuw uitgevoerd. De juridische taxonomie en regels zijn geen onderwijsinhoud.

**Onderzoeksvraag:** kan een methodegebonden assistent geldigheid, inhoudsrevisie, toestemming en passende hulp afzonderlijk controleren? Onderzoek ook eenvoudige bestaande versie- en rechtenfuncties. Een geldige bron of hint is niet automatisch een passend antwoord. Relaties: Shadowseed, versiegebonden lespakketten.

### R01-04 — Eén bronbundel, verschillende gegevensselecties

Sporen: FRM, KNW, LOG, ENG, INT.

**Bronnen:** EAI Gamma Portal, commit `444d1373f83dcd2d5ace6f0ad931c448874b7807`: [ssot-loader.ts](https://github.com/E-AI-MODEL/eai-gamma-portal/blob/444d1373f83dcd2d5ace6f0ad931c448874b7807/src/lib/ssot-loader.ts), [ssot-selectors.ts](https://github.com/E-AI-MODEL/eai-gamma-portal/blob/444d1373f83dcd2d5ace6f0ad931c448874b7807/src/lib/ssot-selectors.ts).

De loader leest een vastgelegde SSOT-snapshot met modules, manifest, adapters en benchmarkgevallen. Selectors leveren gegevens met bronpad en veldverwijzing aan de UI. De oude semantiek is niet automatisch actueel; de code gebruikt ook trefwoorden als aanwijzingen bij analyse. De aanwezigheid van een module of manifest bewijst niet dat een andere runtime zijn gedrag afdwingt. Controleer licenties van zowel portal als bronbundel voor hergebruik.

**Onderzoeksvraag:** kunnen we vooraf verschillende contextpakketten samenstellen uit een gedeelde bron zonder elke beurt het volledige framework naar een model te sturen? Vergelijk versiegebonden selecties, compilatie vooraf, stabiele prefix en eenvoudige directe velden. Relaties: SSOT 17, EAI Machine, UMDT, EAT.

### R01-05 — Gevonden informatie krijgt niet automatisch invloed

Sporen: LOG, ORC, CTX, ENG, AI.

**Bron:** Shadowseed Agent Lab, commit `d50971ac8aed51e1f4442ff3baac9328e36ad75e`: [ADR 0002](https://github.com/E-AI-MODEL/shadowseed-agent-lab/blob/d50971ac8aed51e1f4442ff3baac9328e36ad75e/docs/architecture-decisions/0002-rag-as-evidence-not-influence.md).

Het geaccepteerde ontwerpbesluit maakt een aparte bevoegdheidstoets nodig voordat gevonden bewijs invloed op een kandidaatidee krijgt. Een kandidaat zonder positief gewicht mag geen nieuwe zoek- of antwoordroute aandrijven. Dit is een ontwerpbesluit, geen nieuwe verificatie van het uitvoeringspad. Het upstream geheugencontract en de kandidaatmechanismen worden niet automatisch overgenomen.

**Onderzoeksvraag:** kunnen we bij leerlingondersteuning een foutvermoeden onderscheiden van waargenomen fout en toegestane interventie? Vergelijk een eenvoudige tijdelijke toestand met uitgebreidere bewijsgestuurde mechanismen. Langdurig geheugen is geen uitgangspunt; een goedkopere of eenvoudigere oplossing blijft kandidaat.

### R01-06 — Mislukte proeven bewaren

Sporen: PUR, FRM, ORC, CTX, RUN; relevant voor ieder spoor.

**Bron:** Shadow Seed Study, commit `ff639cc8c079cabef06c4d8cd9bcfb90c72a3b40`: [reproductienotitie van 29 april 2026](https://github.com/E-AI-MODEL/shadow-seed-study/blob/ff639cc8c079cabef06c4d8cd9bcfb90c72a3b40/docs/ssl/notitie_reproductie.md).

De oorspronkelijke onderzoeksopzet verlangt behoud van beslisredenen, ruwe resultaten, model- en promptversies, beoordelaarsinformatie en mislukte runs. Dit is een methodische bron, geen gemeten effect van Shadowseed. Gebruik voor de nieuwe proeven alleen rechtmatig beschikbare, passende gegevens; bewaar geen persoonlijke leerlingtekst in openbare logs. Werkelijke reproductie vraagt de bijbehorende runs, notebooks en configuraties.

**Onderzoeksvraag:** welke bestaande meet- en onderzoeksopzetten kunnen we gebruiken, inclusief eerder verworpen hypothesen? Relaties: EAI Lab, EAIwork, NeSy, EAT Inline.

## Vervolg binnen fase 3a

Breid de broninventaris uit naar eerdere versies, ontwerpdocumenten en empirische resultaten van de projectfamilies, ook buiten de zes hier gelezen bronnen. De bibliotheek en oudere inventarisaties blijven afzonderlijke bronlagen. Volg verwijzingen naar originele documenten in plaats van samenvattingen als onafhankelijk bewijs te tellen. Controleer waar bronbestanden, experimenten en redenen voor wijzigingen ontbreken. Onderzoek naast techniek ook didactische keuzes, niet-modelalternatieven en de oorspronkelijke aannames. De gevonden mechanismen blijven open kandidaten; geen uitspraak over passendheid bij de interne Neon-software.

Geen modellen aangeroepen, geen tests opnieuw uitgevoerd, geen code overgenomen. Het register documenteert de aangetroffen bronnen en vragen, niet bewezen kostenbesparing of leerwinst.
