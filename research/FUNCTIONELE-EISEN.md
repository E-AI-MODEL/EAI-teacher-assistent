# Functionele vergelijking vóór de inhoudelijke use case

Ontwerp v0.2, 27 november 2026. Dit beschrijft voorgestelde functies en onderzoeksvragen, geen vastgestelde productfuncties van Neon. De aanleiding staat in [VERKENNING.md](VERKENNING.md) en [de Neon-bronnen](neon/BRONNEN.md).

## Wie levert welke informatie?

| Actor | Informatie of handeling |
| --- | --- |
| Auteur / vakexpert | Leerdoelen, opdracht, toegestane oplossingsvormen, bronpassages, gecontroleerde hints en voorbeelden, reviewstatus |
| Docent | Gekozen lesversie, context van de les, extra of beperkte ondersteuning, eventuele aanpassingen en vervolgbesluit |
| Leerling | Eigen poging, expliciete hulpvraag, eigen antwoord of uitleg, eventueel eigen zekerheidsoordeel |
| Leeromgeving | Geldige opdracht- en lesidentiteit, versie, rechten, gekozen taal/niveau voor zover beschikbaar |
| Assistent | Selecteert passende hulp binnen bovenstaande grenzen, vraagt om verduidelijking, geeft feedback of meldt dat de benodigde hulp niet betrouwbaar beschikbaar is |

Een signaal van onzekerheid is geen diagnose van een leerstoornis of beheersingsniveau. De leraar blijft verantwoordelijk voor de les. Geen formele beoordeling, rangschikking of automatische consequential beslissing in deze proef.

## Functiematrix

| Functie | Eerste alternatief zonder generatief model | Mogelijk modelgebruik | Beslissende proef / foutgeval |
| --- | --- | --- | --- |
| Lescontext ophalen | Stabiele IDs en toegangscontrole | Alleen intentie duiden bij werkelijk ontbrekende informatie | Gewijzigde opdracht, foutieve clientvelden, reset, versieconflict |
| Leerdoel en hulpgrens bepalen | Vastgelegde opdracht en docentbeleid | Voorstel bij ambiguïteit, niet zelfstandig wijzigen | Vraag om oplossing terwijl alleen hint is toegestaan |
| Hulpvraag begrijpen | Expliciete hulpknoppen, regels of kleine classifier | Vrije tekst/meerduidige intentie | Meertaligheid, dubbelzinnigheid, afwijkende of samengestelde vragen |
| Gesloten antwoord controleren | Antwoordset of betrouwbare toetsfunctie | Doorgaans niet nodig | Gelijkwaardige notatie, meerdere juiste antwoorden, typefout |
| Vrij antwoord controleren | Vakspecifieke controle waar passend, e.g. grammatica of computeralgebra | Open redenering of uitleg die niet door een regel wordt gedekt | Geldig onverwacht antwoord, misleidende woordoverlap, ontbrekend bewijs |
| Hint kiezen | Vooraf beoordeelde hint en beslisregel | Nieuwe, contextgebonden hint indien nodig | Hint te vroeg, verkeerde foutdiagnose, volledige oplossing prijsgeven |
| Wedervraag stellen | Vooraf vastgelegde vraag of beperkte template | Betekenisafhankelijke vraag | Leerling kan eigen benodigde handeling nog uitvoeren |
| Uitleg geven | Bronpassage, voorbeeld of gecontroleerde uitleg | Gericht aanpassen of verduidelijken | Betekenisverlies, ontbrekende voorkennis, te veel uitleg |
| Ondersteuning afbouwen | Expliciete toestand en waargenomen nieuwe poging | Voorstel bij complexe situatie | Te vroeg afbouwen; herhaald succes met hulp niet als zelfstandigheid behandelen |
| Bronselectie | Les-ID, metadata, tekst/embedding retrieval | Reranking bij aantoonbare onzekerheid | Verkeerde lesversie, tegengestelde bron, geen toegestane hit |
| Taalsteun | Beoordeelde vertaling en woordenlijst, eenvoudige templates | Vrije vertaling of extra uitleg | Taalondersteuning neemt niet de taalvaardigheid over die geoefend wordt |
| Docent informeren | Beschrijvende aantallen, hulpvraagtypes, expliciete signalen | Samenvatting bij grotere verzameling | Persoonsgegevens, onbewezen waardeoordelen, verkeerde klas |
| Onderbreken en herstellen | Toestandsmachine, tijdslimiet, idempotente verzoek-ID | Geen model vereist | Dubbele vraag, netwerkuitval, geweigerde toegang, onbereikbare modeldienst |
| Onafhankelijke vervolgtaak | Nieuwe gelijkwaardige opdracht, hulp uitgeschakeld | Geen inhoudelijke modelsteun tijdens meting | Eerder antwoord nog zichtbaar, hulp via zijroute |
| Verbruik registreren | Werkelijke provider- en runtimegegevens, routeregistratie | Geen model vereist | Cachetarief, retries, verborgen redeneertokens, incomplete usage |

De matrix is geen besluit dat alle voorgestelde niet-LLM-routes voldoende kwaliteit hebben. Per taak testen we eenvoudige referentie, gespecialiseerde techniek en modelroute. Een onjuiste automatische beslissing telt als fout, ook als zij goedkoop is.

## Gedeeld inhouds- en sessiecontract (voorstel, nog geen schema)

Minimale objecten: lespakket-ID en revisie, opdracht-ID, leerdoel en beoogde leerlinghandeling, bronankers, toegestane steun, beschikbare hints/uitleg met reviewstatus, vakspecifieke controleconfiguratie, taalinstelling, toegestane toegangsgroep en verantwoordelijke auteur/docent.

Per gesprek: geldige lesversie, actuele opdracht, laatst waargenomen poging, aangeboden ondersteuning, door leerling gekozen hulp, expliciete fase en reden van overgang. Houd modelafgeleide hypothesen apart van waargenomen feiten. Geen blijvend leerlingprofiel in de eerste proef. Werkelijke gegevensvelden en toegang moeten voor een eventuele integratie worden afgestemd.

De versie van het hulpbeleid is deel van de cache- en trace-identiteit. Alleen een geautoriseerde bronrevisie mag worden gebruikt. Een model mag deze niet wijzigen. Wanneer een docent een les wijzigt, moet een ongeldige hint kunnen worden ingetrokken zonder andere scholen te raken.

## Te vergelijken ontwerpen

| Optie | Wanneer interessant | Wat kan tegenvallen |
| --- | --- | --- |
| Bestaande leeromgeving, geen assistent | Vaste feedback of bestaande interactieve activiteit voldoet | Vrije hulpvragen blijven onbeantwoord |
| LLM met een goede beperkte prompt | Diverse, onvoorspelbare vragen | Herhaalde inferentie, foutieve hulp, kosten |
| Gedeelde inhoud + deterministische regels | Veel herhaalde, voorspelbare ondersteuningsbehoeften | Auteurstijd, beperkte dekking, verkeerde herkenning |
| Vakspecifieke controle + gericht LLM | Wiskunde, taal en andere taken vragen verschillende controles | Integratie en onderhoud; onjuiste signalen kunnen verkeerd doorwerken |
| Zelfgehost of lokaal model | Voldoende capaciteit of geschikte apparaten bij passende kwaliteit | Idle-capaciteit, hardwareverschillen, beheerkosten, lagere kwaliteit |
| Zwaardere multi-agent / verificatieketen | Alleen indien eenvoudige aanpak een concreet probleem niet oplost | Extra aanroepen, latency, complexiteit en schijnzekerheid |

De vier hoofdvarianten A–D blijven ongewijzigd. Een bestaande activiteit zonder assistent is een extra referentie voor functies waar dat relevant is, geen vijfde complete chatbot.

## Eerste onderscheidende proeven, vóór uitgebreide lesinhoud

Kies minimale eigen oefenfragmenten uit ten minste twee taaktypen: een Franse vrije formulering en een reken-/wiskundige controle. Maak eerst een kleine set van bekende, onbekende en onverwacht geldige gevallen, verschillende lesversies en expliciete hulpgrenzen. Test routebereik zonder betaalde provider. Daarna kunnen echte modelproeven met een vooraf gekozen budget worden uitgevoerd. De exacte omvang en kwaliteitseisen worden vóór de definitieve run vastgelegd. In deze fase geen uitgebreide curriculumontwikkeling.

Een proef is pas nuttig wanneer zij alternatieven onderscheidt: correcte beslissingen zonder LLM, gevallen die een model nodig hebben, foutieve automatische routes, noodzakelijke informatie in context, werkelijke tokenmeting, extra aanroepen en responstijd. Test nieuwe regels desgewenst eerst in observatiemodus, zonder de werkelijke respons te wijzigen.

## Open integratievragen voor Neon of een andere aanbieder

Welke gegevens levert de leseditor, hoe worden versies en docentaanpassingen geïdentificeerd, wat is het bestaande tutorcontract, welke broninhoud is voor een model toegankelijk, welke gegevens mogen worden opgeslagen, welke functies moeten zelfstandig of bij de docent blijven, welke feedbackgegevens zijn er, welke kwaliteits- en responstijdeisen gelden, hoe verloopt meertalige ondersteuning en wat zijn echte aantallen actieve gebruikers en pieken? Zonder die gegevens blijft dit een onafhankelijke referentie, geen plug-in die bewezen aansluit op hun huidige software.
