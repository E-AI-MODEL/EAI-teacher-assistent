# Gebruikersomvang, piekbelasting en kosten

Versie 0.2 — 27 november 2026. Ontwerpscenario's, geen gemeten gebruik of voorspelling.

## Bron en afbakening

[Neon meldde op 28 september 2026](https://www.neon.nl/nieuws/je-kunt-weer-lid-worden-van-neon-schrijf-jouw-bestuur-nu-in) ruim 1.500 aangesloten scholen met samen ongeveer 700.000 leerlingen. Zie ook [het bronnenregister](../research/neon/BRONNEN.md). Het is het bereik van de coöperatie in PO en VO, niet de huidige actieve gebruikerspopulatie van de digitale assistent. De eerste use case Frans 2 havo is een eigen inhoudelijke proef. Het volledige bereik dient als stressscenario voor een bredere assistent en zegt niets over het aantal leerlingen Frans.

## Instelbare aannames

- Bereik: 700.000 leerlingen (afgeronde bronwaarde).
- 40 onderwijsweken, 5 schooldagen per week, 6 gebruiksuren per schooldag (aannames).
- Piekfactor 4 boven het gemiddelde binnen schooluren (aanname, geen bovengrens).
- Gemiddelde gespreksduur 10 minuten (aanname; open sessie is niet hetzelfde als actief GPU-verzoek).
- Een leerlingvraag is één beurt waarvoor de assistent een reactie moet leveren, niet noodzakelijk één LLM-aanroep.
- Alleen leerlingverkeer in de tabel. Docentgebruik, lesvoorbereiding, offline generatie en beheer apart bijtellen; omvang daarvan nog onbekend.

| Grootheid | Beperkte uitrol | Brede uitrol | Maximale belasting binnen scenario |
| --- | ---: | ---: | ---: |
| Adoptie onder bereik | 10% | 40% | 100% |
| Actieve leerlingen | 70.000 | 280.000 | 700.000 |
| Gestarte sessies per leerling per week | 1 | 3 | 5 |
| Leerlingbeurten per sessie | 4 | 6 | 8 |
| Gestarte sessies per jaar | 2.800.000 | 33.600.000 | 140.000.000 |
| Leerlingbeurten per jaar | 11.200.000 | 201.600.000 | 1.120.000.000 |
| Gemiddelde beurten/s tijdens schooluren | 2,6 | 46,7 | 259,3 |
| Piekbeurten/s (factor 4) | 10,4 | 186,7 | 1.037,0 |
| Indicatieve gelijktijdig open sessies tijdens piek | 1.556 | 18.667 | 77.778 |

De laatste rij veronderstelt een tijdelijk stabiele piekaanvoerstroom en gemiddelde duur van 10 minuten; de uitkomst is afgerond naar boven. Er kunnen hogere lokale of landelijke pieken optreden. Thuisgebruik, vakanties, toekomstige groei en docentverkeer zijn nog niet opgenomen. Dit is geen absoluut maximum; modelleer kortere synchroon verlopende klasstarts, meerdere vakken per dag, wisselende tijdvensters en hoge vraagintensiteit afzonderlijk. Onderzoek ook hoeveel leerlingen dezelfde geldige lesversie gebruiken, aangezien personalisatie en lokale aanpassingen het hergebruik kunnen beperken.

## Herleidbare berekeningen

- Actieve leerlingen = bereik × adoptie.
- Jaarlijkse sessies = actieve leerlingen × sessies per week × schoolweken.
- Jaarlijkse beurten = sessies × beurten per sessie.
- Schoolseconden per jaar = schoolweken × schooldagen × schooluren × 3.600.
- Gemiddelde beurten/s = jaarlijkse beurten / schoolseconden; piek = gemiddelde × piekfactor.
- Open sessies tijdens een stabiele piek ≈ (jaarlijkse sessies / schoolseconden) × piekfactor × gemiddelde sessieduur in seconden (Little's law).
- Modelaanroepen per seconde = beurten per seconde × gemeten gemiddeld aantal modelaanroepen per beurt, inclusief classificatie, validatie en retries. Route- en taakmix bij de piek afzonderlijk meten.
- In-flight modelaanroepen tijdens stabiele belasting ≈ aankomstsnelheid modelaanroepen × gemiddelde totale modelresponstijd in seconden. Dit is niet hetzelfde als open sessies.

## Belastingsproef

Gebruik identieke synthetische verzoekstromen voor A–D. Begin met één klas (30 open sessies) en schaal via 300 en 3.000 open sessies naar de indicatieve scenario's. Test in stappen, met kostenplafond en technische stopcriteria. Test ook korte gesynchroniseerde bursts van klasgroepen bij lesstart; spreid normale vragen gedurende de les. Meet externe providerquota, wachttijden, doorvoer, modelroutering, foutpercentages, cache-hits, timeouts, terugval, tenant-isolatie en herstel. Test de gewone applicatie en de echte inferentielaag afzonderlijk; rapporteer de grens van de daadwerkelijk geteste belasting. Hoge HTTP-load met fictieve modelantwoorden bewijst geen LLM-doorvoer.

Voor zelfhosting: meet prefill/input- en decode/output-doorvoer bij realistische contextlengtes, GPU-geheugen, gelijktijdigheid, batchgedrag, modelkwantisering en latency. Schat het aantal replicas op basis van gemeten duurzame doorvoer onder de afgesproken responstijd- en kwaliteitsgrens, met reserve en redundantie; valideer door belastingtest. Bereken niet simpelweg GPU-aantal uit het totale aantal accounts.

## Kosten

Gebruik werkelijke betaalde tokens en gedateerde prijzen, met onderscheid tussen gewone input, cache-input, output en eventueel afzonderlijk gefactureerde redeneertokens. Voorkom dubbeltelling van redeneertokens die al in output zijn opgenomen. Tel alle modelaanroepen, inclusief retries, mee.

- API-kosten per jaar = som over taak- en routetypes van aantal aanroepen × kosten per aanroep.
- Zelfhostingkosten = GPU-huur of afschrijving + energie waar niet inbegrepen + opslag/netwerk + redundantie + beheer/monitoring.
- Totale jaarkosten per variant = API-kosten + infrastructuur + beheer + terugkerende inhoudsontwikkeling en validatie, zonder dubbeltelling. Rapporteer eenmalige ontwikkelkosten apart.
- Kosten per actieve leerling = totale jaarkosten / actieve leerlingen.
- Kosten per gestarte sessie = totale jaarkosten / alle gestarte sessies; kosten per succesvolle sessie = totale jaarkosten / alle succesvol afgeronde sessies.

Meet kosten en kwaliteit per gesprek. Een variant mag niet goedkoper worden door verzoeken te weigeren of extra interacties buiten de meting te houden.

## Kosten vóór en tijdens het leren

De methodegebonden aanpak verplaatst mogelijk werk van live inferentie naar het vooraf produceren, controleren en onderhouden van ondersteuning. Tel per lesversie de werkelijke auteurstijd, menselijke controle, eventuele offline inferentie, herziening en distributie mee. Neem ook de kosten van het bijwerken van afgeleide hints en caches na wijziging mee.

Voor een gegeven geldige, beoordeelde hint: laat F de extra vaste kosten van voorbereiding en onderhoud in de gekozen periode zijn; laat c_online de gemiddelde vermeden online kosten per werkelijk toepasbare beurt zijn en c_reuse de resterende variabele kosten van selectie, controle en distributie. Indien c_online > c_reuse, is het rekenkundige omslagpunt N = F / (c_online - c_reuse). Vergelijk het aantal werkelijke correcte hergebruiksmomenten met N. Bij geen positieve variabele besparing is er geen dergelijk omslagpunt. Een foutieve cachehit telt niet als kwalitatief geslaagde besparing.

Voor zelfhosting: vergelijk de totale kosten van een gemeten, voldoende beschikbare installatie tegen de externe API voor dezelfde vraagmix, kwaliteit en responstijd. Bij een vaste capaciteit zijn F_host de vaste jaarlasten en v_host de aanvullende variabele kosten per beurt; voor een API met variabele kosten v_api ligt het vereenvoudigde omslagpunt bij (F_host - F_api)/(v_api - v_host), alleen als de relevante verschillen positief zijn en de installatie de benodigde pieken aankan. Bij groei van capaciteit in stappen of verschillende modellen, maak een volledige scenariovergelijking in plaats van deze formule als uitkomst te gebruiken. Lage bezetting kan een API goedkoper maken.

Neem kosten van lokale/browsermodellen apart op: distributie van modelbestanden, bandbreedte, updates, ondersteuning, compatibiliteit, energie en zo nodig alternatieve route voor ongeschikte apparaten. Geen centrale tokenfactuur is niet hetzelfde als kosteloos gebruik.

## Gevoeligheid en validatie

Adoptie, gebruiksfrequentie, beurten per sessie en tokens per aanroep bepalen het jaarlijkse volume; piekfactor, contextlengte, antwoordlengte, gelijktijdigheid, route-mix en beschikbaarheidsnorm bepalen benodigde capaciteit. Varieer deze parameters afzonderlijk. Gebruik ook een scenario waarin eigen hosting duurder is dan een geoptimaliseerde API (lage GPU-benutting, goedkope API, veel reserve).

Voor een NEON-specifieke businesscase zijn nodig: actieve leerlingen per school/vak/periode, docenten, sessies en beurten, uur- en minutenverdeling, context- en antwoordlengtes, factuur- en prijsverdeling, cache-hits, modelroutes, huidige kwaliteitsgrenzen, beveiligings- en beschikbaarheidseisen. Er is nog geen bewezen kostenreductie. Er is geen infrastructuur besteld en geen live belastingtest uitgevoerd.

Machineleesbare ontwerpaannames: [scale-scenarios.json](scale-scenarios.json).
