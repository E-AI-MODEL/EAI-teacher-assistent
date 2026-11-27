# Ronde 09 | Technische afgeleiden uit besloten bronnen

27 november 2026. De eerdere openbare selectie van 34 records blijft intact. De onderstaande aanvulling brengt ook de bruikbare mechanismen uit besloten projecten in beeld. Overlap tussen afgeleide records en openbare bronvondsten is mogelijk; de aantallen zijn geen aantal unieke algoritmen.

Deze selectie bevat 38 inhoudelijke afgeleiden uit eerder onderzochte besloten bronbestanden, testbestanden en ontwerpstukken. Zij beschrijven de aangetroffen technische ideeën en noodzakelijke tegenproeven in eigen woorden. De oorspronkelijke private bestanden, namen, bronlinks, code en instellingen worden niet gepubliceerd. De afzonderlijke interne bronkoppelingen blijven bewaard in het besloten onderzoek. Publieke lezers kunnen die besloten bronclaims niet zelfstandig via deze afgeleide controleren. De afgeleide is geen extra onafhankelijke bewijsbron, geen uitvoeringsresultaat en geen toestemming voor codehergebruik.

Fase 3b en 3c blijven heropend. Fase 4a: NO-GO. Geen vakinhoud, nieuwe implementatie, echte inferentie of bewezen besparing.

[Openbare bronvondsten ronde 09](RONDE-09.md) · [Onderzoeksatlas](../../docs/illustraties/atlas/README.md)

## Toestand en strategie

Vasthouden, herzien of loslaten.

| ID | Mechanisme | Technische werking | Voorwaarden en tegenproef |
| --- | --- | --- | --- |
| DPR01 | **Gewogen temporele entropie** | Bereken frequenties van discrete toestanden over een begrensd aantal beurten. Gewicht oudere of mechanistisch relevante waarnemingen expliciet; normaliseer Shannon-entropie per veld. | Stabiliteit zegt niets over juistheid. Vergelijk met een eenvoudige toestandsteller en toets lege vensters en ontbrekende waarden. |
| DPR02 | **Gescheiden entropiesporen** | Houd veranderingen in verschillende groepen toestandsvelden apart. Combineer zo nodig per groep met een maximum of gewogen aggregatie; meet ook de frequentie van de volledige toestandsvector. | Een afgevlakte lijst kan variatie tussen velden verwarren met verandering in de tijd. Test per veld met vaste en wisselende vectoren. |
| DPR03 | **Ankerstabiliteit** | Meet voor geselecteerde ankervelden welk aandeel gedurende een venster gelijk blijft. Registreer dit los van de beslissing om een strategie vast te zetten. | Een ontbrekend veld is niet gelijk aan een ander veld. Een stabiel anker geeft geen bewijs voor inhoudelijke juistheid. |
| DPR04 | **Constellation locking en hysteresis** | Bewaar een expliciete strategie en bijbehorende toestand. Gebruik aparte voorwaarden voor vasthouden en wisselen, zodat een korte afwijking niet direct herinterpretatie veroorzaakt. | Vergelijk berekende en werkelijk uitgevoerde strategie. Een lock mag de opgeslagen vector niet stilzwijgend opnieuw vullen. Toets wisselende invoer. |
| DPR05 | **Kwaliteitsinterrupt en passieve invoer** | Laat expliciet gedefinieerde kritieke gebeurtenissen een lock doorbreken. Behandel gebrek aan nieuw signaal niet automatisch als stabiele toestand. | Woordlengte en lexicale signalen zijn heuristieken. Een veto moet echte routekeuze beïnvloeden, niet alleen de prompt. |
| DPR06 | **Selectieve interpretatie van context** | Behoud bekende, geautoriseerde context. Herken expliciete signalen met transparante woord- en zinspatronen; laat ontbrekende velden onbekend of vraag gericht verduidelijking. | Trefwoordmatch en middenwaarde zijn geen observaties. Test ambiguïteit, correcties en botsende bronprioriteiten. |
| DPR07 | **Tijdelijke toestand en commit** | Bereken nieuwe metrieken en fasevoorstel op een kandidaatgeschiedenis voordat de definitieve toestand wordt opgeslagen. Begrens de geschiedenis. | Een tijdelijke lokale kopie is geen atomaire transactie. Controleer gelijktijdige beurten, revisie en terugkeer van een oude waarde. |
| DPR08 | **Adaptieve lockduur** | Laat een getypeerd profiel bepalen hoe lang een strategie geldig blijft. Een snelle veranderingsmodus kan het venster verkorten; een trage modus verlengt het. | Vergelijk met een vaste lockduur en hysteresis zonder entropie. Nul, ontbrekende waarde, reset en overgang apart behandelen. |

## Compiler en context

Eenmalig voorbereiden, gericht gebruiken.

| ID | Mechanisme | Technische werking | Voorwaarden en tegenproef |
| --- | --- | --- | --- |
| DPR09 | **Modelvrije instructiekaart** | Normaliseer gegevens, controleer beleid en voorwaarden, resolveer relevante velden en acties, koppel bewijs, maak een begrensd instructie- en uitvoercontract. Valideer de afgeleide kaart vóór gebruik. | Geen verplichte volledige keten per aanvraag. Controleer ontbrekende modules, onbekende voorwaarden en welke revisies de artifact-identiteit werkelijk bepalen. |
| DPR10 | **Compacte bronprojectie** | Selecteer uit een canonieke bron alleen versie, actuele fase, relevante profielen, toegestane acties en noodzakelijke referenties. Houd bronbetekenis los van de presentatie aan het model. | Test verloren velden, string/object-varianten en caller-supplied allowlists. Minder velden is geen bewezen besparing of betekenisbehoud. |
| DPR11 | **Startsnapshot versus actuele overlay** | Compileer bij de start een zelfstandig gevalideerd artifact. Bewaar latere wijzigingen in een apart runtimeveld. Laat alle relevante consumers de actuele versie via één selector ophalen; behoud het oorspronkelijke snapshot voor vergelijking. | Een fallback naar oud formaat mag geen ingetrokken recht herstellen. Gelezen tests tonen voorrang runtime, snapshot en legacy, niet dat corrumptie of alle races wordt afgevangen. |
| DPR12 | **Modelvrije reeksopbouw** | Zet bestaande goedgekeurde records met een deterministische builder in een geordende reeks. Filter lege items en gebruik expliciete bronidentiteit; nieuwe invoer blijft een aparte categorie. | Geen nieuwe inhoud genereren. Toets stabiele ID bij herordening, ongeldige indices en dubbele invoer. |
| DPR13 | **Expliciete signaal- en readinessregels** | Een pure detector verzamelt getypeerde signalen, berekent een voorstel en geeft bewijs en vereiste toestemming terug. Laat de mutatie buiten de detector. | Unieke waarnemingen tellen, niet alle herhaalde berichten. Geen kwaliteit of leerresultaat afleiden uit een drempel. |
| DPR14 | **Modelvrije fallback met zelfde contract** | Een lokale engine groepeert bestaande signalen en maakt een begrensd voorstel met hetzelfde type uitkomst als een modelroute. Markeer welke uitvoerder is gebruikt. | Contractgelijkheid is geen semantische gelijkwaardigheid. Test onbekende, lege en tegenstrijdige signalen en maak fallback zichtbaar. |
| DPR15 | **Handlerregistry met expliciete simulatie** | Een declaratieve keten kiest geregistreerde uitvoerders. Een niet-geïmplementeerde stap kan als aparte simulatie worden onderzocht, maar mag niet als echt resultaat worden verwerkt. | Ontbrekende handler moet zichtbaar falen of als simulatie worden geregistreerd. Geen verzonnen voorbeeldscore bij productie. |
| DPR16 | **Declaratieve taakassemblage** | Laad een getypeerde configuratie, valideer de structuur en zet alleen toepasselijke instructieblokken om naar één afgebakende taak. Houd uitvoeringsresultaten per stap apart. | Een placeholder, TODO of niet-uitgevoerde stap is geen geslaagde verwerking. Valideer volgorde en ontbrekende velden. |

## Representatie en selectie

Betekenis behouden in compacte gegevens.

| ID | Mechanisme | Technische werking | Voorwaarden en tegenproef |
| --- | --- | --- | --- |
| DPR17 | **Schema-gestuurde LIM-vector** | Codeer discrete kenmerken, flags en relaties in een vastgelegde vectorpositie vanuit een versiegebonden schema. Vergelijk die representatie met expliciete bronvelden en andere compacte formaten. | Variabele kolommen en ontbrekende waarden als nul kunnen vectors onvergelijkbaar maken. Een handgemaakte vector is geen semantische embedding. |
| DPR18 | **Exacte patroonmatch op ID-sets** | Herken een vooraf geregistreerd patroon via een subset van bekende identifiers. Toon alle passende kandidaten voordat een expliciete beslisregel kiest. | Eerste match mag niet stilzwijgend van bestandsvolgorde afhangen. Test overlap, onbekende ID en ontbrekende voorwaarde. |
| DPR19 | **Kandidaten met beperkte levensduur** | Houd intentie, type, identiteit, gewicht en TTL van een kandidaat apart. Expireer op een expliciete klok; beoordeling en gebruikstoestemming zijn afzonderlijke stappen. | Een actief geheugenrecord is niet automatisch geautoriseerd of waar. Test tijdzones, onbegrensde TTL en heractivatie. |
| DPR20 | **Transparante signaalchecks** | Gebruik controleerbare lexicale patronen om mogelijke signalen of een reflectiekandidaat te markeren. Houd de waarneming apart van de afgeleide kandidaat. | Woordaanwezigheid bewijst geen biaspreventie, kwaliteit of toezicht. Een uitlegtemplate is geen bewijs van verborgen modelredenering. |
| DPR21 | **Strict versus tolerant parser** | Scheid AST-constructie, schema-issues en strict/lenient afhandeling. Normaliseer representatie gecontroleerd; behoud formatter en roundtrip-tests. | Stil samengevoegde duplicaten kunnen betekenis wijzigen. Meet semantisch behoud en werkelijke gerenderde tokens afzonderlijk. |
| DPR22 | **Gerichte lokale kennisbundel** | Kies eerst bekende bronidentiteit, haal daarna alleen relevante bronvelden op en bewaar bronversie en onbekende informatie. Een cache is een afgeleide van de bron. | Alias-substring en oude cache kunnen verkeerd koppelen. Exacte identiteit en actuele toestemming vóór ranking en weergave. |
| DPR23 | **Compressie op functiecontract** | Verkort beschrijvingen en selecteer alleen velden die nodig zijn voor de taak, met een vaste betekenis- en structuurtest. Vergelijk ook stabiele prefixcaching. | Tekst afkappen kan voorwaarden verliezen. Karakters, tokens, cachehits en totale kosten zijn verschillende metingen. |
| DPR24 | **Geselecteerde bronnen vóór analyse** | Splits discovery, gecontroleerde bronselectie en daaropvolgende analyse. Laat de analyse alleen bevestigde bronidentiteiten gebruiken. | De caller en server moeten dezelfde selectie afdwingen; retrieval-recall en correcte antwoordkeuze apart meten. |

## Uitvoering en modeltaken

Vergelijk werkelijk bereikte routes.

| ID | Mechanisme | Technische werking | Voorwaarden en tegenproef |
| --- | --- | --- | --- |
| DPR25 | **Symbolisch-neurale fusie** | Vergelijk bekende kandidaattekst met een modelvoorstel via een expliciete overlapmaat. Kies afhankelijk van een grens de kandidaat, het modelvoorstel of een begrensde combinatie; registreer de route. | Lexicale overlap bewijst geen betekenisbehoud. Vergelijk met modelselectie van een bestaande referentie en een directe modeltaak. |
| DPR26 | **Beleidsroute vóór uitvoerder** | Een orchestrator kiest een bekende template, seed, snelle route, model of expliciete overdracht. Controleer zowel het voorstel als de geldige voorwaarden op het werkelijke uitvoerpad. | De naam van een route bewijst geen afwezigheid van inferentie. Trace alle model- en toolaanroepen, inclusief fallback. |
| DPR27 | **Eén gezamenlijke modeltaak** | Laat waar passend één modelaanroep zowel een antwoord als een getypeerd analysevoorstel leveren, in plaats van standaard losse classifier, generator en reviewer. | Een schema bewijst geen semantische juistheid. Vergelijk dezelfde taak en modelrevisie met conditionele extra controle. |
| DPR28 | **Volledige aanroepgrafiek** | Volg een aangeboden beurt van eventuele voorclassificatie via generatie en lokale verwerking naar naclassificatie, herstel en eventuele aparte mediaverwerking. Registreer werkelijk bereikte paden per poging. | Endpointrequests zijn niet automatisch gefactureerde inferentie. Geen kosten uit tekstlengte of zichtbare chatcall alleen afleiden. |
| DPR29 | **Lezen gescheiden van analyseren** | Maak ophalen van bestaande gegevens een echte read-only route. Genereer nieuwe analyses expliciet of op een relevante wijziging; sla een afgeleide met bronrevisie op. | Een refresh mag niet ongemerkt extra modelwerk veroorzaken. Eerder gesignaleerde analysepaden bij lezen nog end-to-end controleren. |
| DPR30 | **Lokale provider-readiness** | Maak onderscheid tussen ingestelde adapter, bereikbaar endpoint, aanwezige gewichten en werkelijk klaarstaande runtime. Laat lokale onbeschikbaarheid expliciet terugkomen. | Geen stille externe fallback. Een healthcheck is geen bewijs van inferentie, semantische kwaliteit of capaciteit. |
| DPR31 | **Begrensde retries en breaker** | Houd foutbudget en wachttijd per afhankelijkheid apart. Laat een breaker tijdelijk stoppen, onderscheid permanente fout, definitief geweigerde verzending en onzekere dispatch. | Een timeout bewijst niet dat werk is beëindigd. Tel alle pogingen mee; onzekere verzending niet blind herhalen. |

## Staat, aflevering en controle

Controle op het punt van gebruik.

| ID | Mechanisme | Technische werking | Voorwaarden en tegenproef |
| --- | --- | --- | --- |
| DPR32 | **Offline queue met bevestiging** | Bewaar lokale aanvragen met eigen IDs, verwijder uitsluitend bevestigde records en voorkom overlappende verwerking binnen één instance. | Clientlock is geen multi-tab of serverdeduplicatie. Toets verloren ACK, herhaling, intrekking en gebruikersscope. |
| DPR33 | **Deterministische adviesprioriteit** | Laat getypeerde predicaten kandidaten aanbieden; gebruik een expliciete volgorde en eerder geziene IDs. Begrens frequentie en houd gebruikersbesluit apart. | Een lokale seen-set en timer garanderen geen globale dedup. Toets meerdere matches, late events, refresh en herbeoordeling. |
| DPR34 | **Controle na de laatste transformatie** | Scheid scrub, structuurvalidatie, vormadaptatie en taalbewerking. Controleer de daadwerkelijk af te leveren bytes of tekst, niet alleen tussenresultaat. | Regexfilter is geen toegangsgrens. Blind inkorten kan tabellen of code beschadigen. Een streamingguard na aflevering is te laat voor eerder verzonden tekst. |
| DPR35 | **Eén authored core voor verschillende runtimes** | Houd gezaghebbende regels en schema's op één plek en genereer runtime-artefacten daaruit. Laat iedere runtime dezelfde contractfixtures verwerken. | Geen handmatige fork van afgeleide bestanden; parity omvat foutgedrag en revisions, niet alleen gelijke exports. |
| DPR36 | **Onbekend of ambigu is een geldige uitkomst** | Een deterministische matcher kan score, kandidaat en marge rapporteren. Een aparte beslisfunctie kiest tussen bekende route, verduidelijking, menselijke beoordeling of observe-only. | Heuristische scores zijn niet gekalibreerde zekerheid. Behoud UNKNOWN en DENY, en laat de caller autoriteit afdwingen. |
| DPR37 | **Expliciete slot- en overgangslogica** | Stuur de volgende vraag of actie via getypeerde ontbrekende velden, actieve toestand en een expliciete overgang. Bekende gegevens niet opnieuw laten afleiden. | Een promptinstructie is geen state-machinecontrole. Toets dubbele aanvragen, terugkeer naar vorige toestand en ongeldige overgang. |
| DPR38 | **Gescheiden voorstel, uitvoering en aflevering** | Gebruik een expliciete uitvoeringsstatus bij herstel en overdracht. Houd een succesvol gevormde fallbacktekst los van een werkelijk geslaagde handeling. | Een foutmelding of escalatie is geen succesvol uitgevoerde actie. Trace fout, voorstel, besluit, dispatch en uitkomst afzonderlijk. |

## Vervolg

Beoordeel de mechanismen onafhankelijk van A–D. De open zoekvraag naar het oorspronkelijke ToolCompiler/ToolManifest blijft staan; een historische ontwerpgedachte is niet gelijk aan aangetroffen werkende code. Geen fase 4a voordat de technische vergelijking opnieuw is vastgesteld.
