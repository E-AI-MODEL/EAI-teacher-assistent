# Besluit fase 3b en 3c | Afgebakende start van 4a

27 november 2026. Technisch oordeel: **GO voor de afgebakende modelvrije proef, na merge van het onderzoeksbesluit.** De brede onderzoeksbasis is voldoende om het technische contract in één kleine proef te toetsen. Dit is geen GO voor een productiearchitectuur, vakinhoud, echte inferentie of betaalde proeven. PR #3 bevat uitsluitend documentatie en visuele onderzoeksartefacten; de proefcode is nog niet gestart.

## Welke technieken vergelijken we?

De 112 records in rondes 09–11 zijn onderzoeksbevindingen, niet 112 onafhankelijke algoritmen. De eerste technische proef hoeft niet iedere bron te reproduceren. Onderstaande keuzes houden concurrerende verklaringen open.

| Onderzoeksvraag | Eenvoudige referentie | Te toetsen alternatief | Wanneer levert het geen voordeel op? |
| --- | --- | --- | --- |
| P: vooraf samenstellen | Bouw en valideer hetzelfde toegestane contract bij gebruik | Compileer een versiegebonden kaart bij bron- of beleidswijziging | Hergebruik is zeldzaam, hercompilatie kost meer, of oude gegevens kunnen doorwerken. DPR09–DPR12, R10-01–04, R11-01/02. |
| S: strategie behouden | Bepaal dezelfde strategie bij iedere nieuwe aanvraag | Expliciet tijdelijk strategievoorstel; eerst vaste lock, daarna hysteresis en adaptief venster | Gemiste relevante wijziging, onterechte lock of extra interpretatiewerk. DPR01–DPR08, R11-09/13. |
| R: selectief uitvoeren | Eén competente modeltaak voor de experimentele aanvraag | Exacte regel/engine bij bewezen toepasselijkheid, anders UNKNOWN of afwijzing | Verkeerde automatische route, taakverlies, onzichtbare classifierkosten. DPR14/26/36, R11-03/04/11. |
| M: begrensde modelcontext | Volledige relevante én toegestane context voor dezelfde modeltaak | Getypeerde capsule met benodigde bron-ID's en dezelfde voorstelvorm | Ontbrekende informatie, herstelwerk of nieuwe modeltaken. DPR10/23/27, R10-09, R11-05/11/12. |
| Inferentieplaats | Externe adapter | Lokale adapter voor dezelfde taak en waar mogelijk dezelfde gewichten | Onbeschikbaarheid, onvoldoende kwaliteit, geheugen, doorvoer of totale kosten. R10-05–08/16, R11-07/08. |

De alternatieven zijn geen voorgeschreven services. Een eenvoudige directe route kan uiteindelijk beter zijn dan een extra compiler, classifier, cache of strategiecontroller. Gebruik geen door een model geschreven uitvoeringscode, geen automatische fuzzy reparatie van referenties en geen externe embedding in D. Een historische activatieprobe wordt niet gebruikt als besliscriterium: de bekeken replicatie haalde nul van de vier vooraf vastgelegde toetsen. Het oorspronkelijke ToolCompiler-pakket is niet teruggevonden; het manifest blijft een ontwerpgedachte. De open bronvragen, verdere licentiecontrole en echte integratie worden niet als opgelost geboekt.

## Gemeenschappelijk contract vóór varianten

Bronbundel, schema, bekende bewerkingen, scope, revisies en gedeelde gewone functies blijven gelijk. De compiler mag nooit bevoegdheid verlenen. Een opgeslagen artifact is afgeleid en immutable. De runtime autoriseert op het moment van gebruik. Een strategievoorstel heeft een eigen identiteit, afhankelijkheidsbasis en afloopgrens; het is geen recht en geen eerder antwoord.

Houd de monotone aanvraag-/contextrevisie apart van de revisies en expliciete signalen die een strategielock ongeldig maken. Elke nieuwe aanvraag wordt geautoriseerd; een gewone beurt kan de contextrevisie verhogen zonder automatisch alle ongewijzigde strategische afhankelijkheden te wijzigen. Bij intrekking, gewijzigde bron, onbekende vereiste observatie, verlopen venster of kritieke interrupt moet de strategie opnieuw worden beoordeeld. Een oude uitkomst blijft ongeldig na een terugkeer naar dezelfde waarde met een nieuw revisienummer. Geen sleutel of digest vervangt toestemming.

De eerste S-proef gebruikt een vaste lock op een expliciete, neutrale toestandswaarde. Dat maakt behoud, afloop en onderbreking afzonderlijk controleerbaar. Gewogen entropie, dubbele entropiesporen, hysteresis en adaptieve duur worden daarna tegen die vaste referentie onderzocht. Voor de entropieproef moeten toestandscategorieën, weging, venster, normalisatie, behandeling van ontbrekende velden en wisselgrenzen vóór uitvoering vaststaan. Geen drempel uit de proefresultaten afleiden en diezelfde proef als bevestiging gebruiken.

## A–D en P/S/R/M

In de eerste contractproef is P/S uitgeschakeld bij A–D. A gebruikt de gewone relevante context en één modelstub waar een experimentele modeltaak nodig is; B gebruikt dezelfde stub en een gerichte projectie (M); C voegt de experimentele modelvrije regelroute (R) toe; D deelt C en gebruikt uitsluitend de lokale stubadapter. Gewone lookup en verplichte autorisatie zijn altijd gedeeld.

De factorproef gebruikt dezelfde externe stubvariant en dezelfde aangeboden aanvragen: 0000, 1000, 0100, 0010, 0001 en 1111 in volgorde P/S/R/M. C = 0011; D = 0011 met lokale stub. Weglatingsproeven zijn uitsluitend nodig om onduidelijke bijdragen of interacties uit elkaar te halen. Dit is geen vergelijking van tien applicaties; één runtime met vaste proefconfiguraties volstaat. Wanneer vooraf samenstellen of strategiebehoud later gewone gedeelde functies blijken, krijgen alle passende hoofdvarianten die functie. Voorkom dat een bewust inefficiënte baseline winst voor C/D creëert.

## Afbakening van 4a

Werk in één enkelprocesproef met neutrale records, stub-adapters en vaste, vooraf opgeslagen verwachtingen. Het [startcontract](../benchmarks/4A-STARTCONTRACT.md) beschrijft de fixtures, volgorde, negatieve controles en stopvoorwaarden. Eerst de oorspronkelijke P01–P03-invarianten, inclusief minimale compilatie-, strategie- en contextproeven. Voer de zes factorconfiguraties pas uit wanneer die gedeelde contracten de juiste routes bereiken. Geen runtimecode in deze documentatie-PR. De keuze voor taal en testharnas in de daaropvolgende proef blijft beperkt tot wat daarvoor nodig is.

Een mislukte proef is een bevinding. Bevries inputs, verwachtingen en testcontract vóór kandidaatcode; pas een verwachting niet stilzwijgend aan. Toon de daadwerkelijk bereikte routes en tellers, niet alleen het aantal groene tests. Stop bij een lek, stale aflevering, verkeerde route, ontbrekend attempt-record, ongeautoriseerde dispatch of een niet-bereikte verplichte proefroute. Een lokale stub geeft geen bewijs voor productie-egress, echte modelkwaliteit of lagere kosten. Geen extrapolatie van stubwaarden naar gebruik door leerlingen.

## Open beslissingen na 4a

P04–P07/P09 verdiepen retrieval, representatie (waaronder LIM en TOON), cache, gelijktijdigheid, herstel en observatiemodus voor zover de eerste proef dat vraagt. P08/P10 vragen een afzonderlijke model-/hosting- en budgetkeuze. Werkelijke vakinhoud, toegestane steun en kwaliteitscriteria volgen in de daarvoor bedoelde fasen. Er is geen architectuur vastgesteld en er is geen effect op leren aangetoond.

## Controle en herkomst

Technische zelfreview van de eerdere [specificatie](TECHNISCHE-SPECIFICATIE.md), de [combinatiehypothese](COMBINATIE-HYPOTHESE.md) en de [historische verdiepingsrecords](register/RONDE-10-VERDIEPING.md) / [externe vergelijking](register/RONDE-11-VERGELIJKING.md). De volledige [atlas v2](../docs/illustraties/atlas/README.md) en de elf historische diagrammen blijven behouden. De hoofdweergave op commit 73cef05ce9c2ee8ce5da8a282102383f54da5369 is byte-identiek uit GitHub hersteld (Git-blob f8dc49442a851211d6d17b2d4515969ba8671be4) en met Chromium gerenderd. Zeven SVG's, acht interne navigatielinks, horizontaal scrollen en tekstgrenzen op 320, 390, 960 en 1280 CSS-pixels gecontroleerd. Dit betreft lokale browserweergave van de exacte HTML, niet live deployment of een fysieke telefoontest. De historische archieflink wordt in deze wijziging gecorrigeerd. Geen onafhankelijke technische of inhoudelijke review van de nieuwe proefcode, want die bestaat nog niet.
