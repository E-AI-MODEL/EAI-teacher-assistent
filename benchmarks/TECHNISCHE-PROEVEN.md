# Fase 4 — minimale vergelijkingsproeven

> Status v0.4 (27 november 2026): fase 4a gereed voor uitvoering op basis van de [technische specificatie v0.1](../research/TECHNISCHE-SPECIFICATIE.md). Nog geen uitgevoerde tests of meetresultaten. P01–P03 zijn de eerste afgebakende contractproeven; geen echte inferentie.


Ontwerp, 27 november 2026. Nog niet uitgevoerd. Eerst technieken toetsen op kleine fictieve gegevens; geen volledige les, geen echte leerlinggegevens. A–D blijven de uiteindelijke vier uitvoeringen. Deze proeven onderzoeken afzonderlijke mechanismen, geen extra chatbots.

## Eerste werkpakket: meten en begrenzen

| ID | Proef | Vergelijking | Uitkomst die de hypothese weerlegt |
| --- | --- | --- | --- |
| P01 | Modeladapter en kostenregistratie | Eén stubprovider versus fouten, retries, ontbrekende usage, caching, afgebroken stream en local usage | Een poging ontbreekt of wordt dubbel gefactureerd; ontbrekende usage wordt nul; responsefout wist gemelde tokens; D gebruikt externe model-API. |
| P02 | Expliciete context en versie | Stabiele servergegevens versus opnieuw modelcontext afleiden; oude en gewijzigde fictieve lesversie | Een model of client verandert het toegewezen leerdoel/beleid; oude bron of hint wordt na wijziging getoond. |
| P03 | Route vóór LLM | Eenvoudige vaste route, vakspecifieke check, onbekend/fallback; vergelijk met één goede modelroute waar nodig | Een onterechte automatische route, relevante hulp ontbreekt of de route met extra calls is duurder zonder aantoonbaar beter resultaat. |
| P04 | Retrieval | Exacte ID, geïndexeerde tekstzoekfunctie, optionele embeddings/reranker | Relevante geldige bron gemist, verboden/verouderde bron teruggegeven, of extra zoeklaag biedt geen gemeten voordeel op dezelfde vragen. |
| P05 | Context- en outputbudget | Volledige relevante context, geselecteerde velden, minified JSON en optioneel TOON; vaste outputactie versus vrije tekst | Essentiële informatie gaat verloren; minder tokens maar slechtere taakuitkomst; overhead of extra vervolgcall maakt route duurder. |
| P06 | Cache | Geen cache, vaste goedgekeurde inhoud, exact gedeelde modelprefix; koude/warme toestand | Persoonlijke of achterhaalde output wordt hergebruikt, of schrijftarief/misses maken totale kosten hoger. |
| P07 | Gelijktijdigheid en herstel | Herhaalde request-ID, concurrente beurten, gewijzigde revisie tijdens call, wachtrij vol, afgebroken verbinding | Dubbele side-effect of stale resultaat, onbeperkte queue, retries buiten budget, of cross-session data. |
| P08 | Kleine modellen en hosting | Zelfde taakcontract voor twee modelgroottes; zelfde gewichten op andere hosting waar haalbaar | Geldige JSON met onjuiste betekenis; onvoldoende kwaliteit of throughput; externe API is goedkoper bij dezelfde kwaliteit en service-eisen. |
| P09 | Observatiemodus en evaluatie | Nieuwe regel alleen registreren, daarna gecontroleerd actief toepassen | Verkeerde voorspelling wordt als uitgevoerde actie geboekt; geen geval bereikt de te onderzoeken route; beoordelaar krijgt gold label of variantidentiteit. |
| P10 | Decentraal model, optioneel | Browsermodel tegenover centraal lokaal model op representatieve apparaten | Model laadt niet, onvoldoende geheugen, vertraging bij generatie of kwaliteit onder afgesproken norm; download-/ondersteuningskosten heffen voordeel op. |

## Proefopbouw

Gebruik één gedeelde abstracte fixture: twee fictieve scopes, een bundel met bijvoorbeeld records R1/R2, revisies V1/V2, neutrale stringwaarden, toegestane en verboden bewerkingen en vaste stubvoorstellen. Geen taal- of rekenopgave, vakinhoud, leerlinggegevens, lespakket of tutorprompt. Bevries fixture, verwachtingen en configuratie vóór uitvoering. Verwachte uitkomsten staan in testasserties, niet als verborgen labels in modelcontext. De proefrunner legt de variant vast. Gebruik een geïnjecteerde adapter zonder API-key, modeldownload of echte inferentie.

### Afgebakende proeven in 4a

| Proef | Gevallen | Vereiste uitkomst |
| --- | --- | --- |
| P01-A Telemetrie | Succes, ontbrekende usage, gedeeltelijke usage bij fout | Eén record per poging; unknown blijft unknown; geen dubbeltelling |
| P01-B Transport en budget | Definitief geweigerde dispatch, expliciet toegestane tweede poging, onzekere dispatch, budget op | Lokale poging, dispatch en facturering apart; geen verborgen retries |
| P01-C D-grens | Lokale stub beschikbaar/onbeschikbaar; verzoek tot externe adapter | Geen externe dispatch in D; onbeschikbaarheid zichtbaar |
| P02-A Autoriteit | Geldige context, vervalste scope, ongeldige referentie en overlay | Alleen geautoriseerde gegevens, geen onbevoegde contextmutatie |
| P02-B Versie | R1 geldig in V1, ingetrokken in V2; oude waarde terug met nieuwe revisie | Stale uitkomst niet afleveren, ook niet na terugkeer van de waarde |
| P02-C Dubbele aanvraag | Zelfde aanvraag; afwijkende invoer met hetzelfde ID; gewijzigde rechten | Eén uitvoering in de enkelprocesproef; conflict of afwijzing waar nodig |
| P03-A Gedeelde functie | Expliciete gewone lookup | A–D dezelfde uitkomst zonder modeltaak; geen kunstmatige winst voor C |
| P03-B Routebereik | Experimentele aanvraag met aantoonbare MATCH | A/B modelstub, C/D gewone uitvoerder; trace toont werkelijk gebruikte route |
| P03-C Onbekend of verboden | UNKNOWN, meerdere matches, DENY | Onzekere toegestane gevallen bereiken modelstub; DENY wordt niet omzeild |
| P03-D Voorstelcontrole | Geldige SELECT, ongeldige referentie, GENERATE, CLARIFY en HANDOFF | Type, toegangsgrens en route kloppen; geen verplichte tweede call |

P04–P07 volgen waar de eerste proef hun contract nodig maakt. P09 begint in observatiemodus en onderscheidt voorspelde van uitgevoerde routes. P08/P10 wachten op een gemotiveerde modelkeuze, beschikbare infrastructuur en een afzonderlijk budgetbesluit. Geen echte modelrun in 4a. Gebruik voor latere servingproeven een bestaande benchmarkclient (zie technische audit).

## Minimaal meetcontract (ontwerp)

Per verzoek: trace-ID, request-ID, variant, geldige inhoudsversie, beleid, route/reasoncode, aangeboden tijd, uitkomst, status en duur.

Per werkelijk gestarte modelpoging: parent trace, attempt-ID, provider/model/revisie, beoogde taak, input/output/cache-read/cache-write/reasoning count indien door provider gerapporteerd, eenheid en betekenis, status, latency, prijsversie en eventuele onzekerheid. Een provider die reasoning al in output telt, mag niet nog eens extra meetellen. Bewaar ontbrekende waarde als null/unknown. Scheid geschatte tokenisatie van providerusage. Tel alleen werkelijk gestarte pogingen als calls; onderscheid aanvragen die afgewezen zijn vóór verzending en aanvragen waarvan facturering onbekend is. Een succesvolle respons en een succesvolle boeking zijn aparte statussen.

Synthetische records, echte providerrecords en geaggregeerde kosten hebben gescheiden opslag/labels. Geen ruwe leerlingtekst in telemetrie; gebruik fictieve IDs en minimale velden. Telemetrie mag een fout in de kostenregistratie niet verbergen: signaleer ontbrekende meetrecords afzonderlijk. Factuurreconciliatie wordt later apart getest.

## Afsluitcriteria

Per proef: vaste bronversie, inputfixture, verwachte eigenschappen, werkelijk antwoord, gemeten waarden en afwijkingen. Test expliciet de negatieve gevallen. Leg vóór de definitieve kwaliteits- en kostenvergelijking de acceptatiegrenzen vast. Een veiligheids-/toegangslek of gebruik van onjuiste bronversie blokkeert die route; een niet-bereikte experimentele route levert geen oordeel op over haar kwaliteit. Maak onderscheid tussen niet gemeten, mislukt, afgewezen en succesvol.

De eerste proef slaagt uitsluitend wanneer alle gespecificeerde technische invarianten in de bevroren fixture slagen. Lek, stale output, ontbrekend attempt-record, onverwachte dispatch of niet-bereikte verplichte route blokkeren het betreffende resultaat. Rapporteer ontbrekende resultaten apart. Stub-usage, kunstmatige timing en routebereik bewijzen geen providerkosten, modelkwaliteit, echte netwerkisolatie of productiecapaciteit. Geen extrapolatie naar leerlingen of schaal. Geen betaalde CI, productieomgeving, UI of vakinhoud. Na 4a bepalen we welke aanvullende proeven nodig zijn vóór een architectuurbesluit.
