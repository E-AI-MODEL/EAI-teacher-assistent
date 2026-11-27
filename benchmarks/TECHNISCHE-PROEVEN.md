# Fase 4 — minimale vergelijkingsproeven

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

Begin met P01–P03 en één gedeelde set minimale contractfixtures: expliciete context, een toegewezen versie, één gecontroleerde respons, een bekende invoer die gewone logica kan verwerken en een onbekende invoer. Neem twee taaktypen op met uitsluitend de kleinste noodzakelijke fictieve inhoud (taal en rekenen). Verwachte uitkomsten staan buiten de modelcontext. Nog geen keuze van framework, provider of model.

P04–P07 gebruiken dezelfde contextidentiteit en het meetcontract uit P01. P09 begint in dezelfde stubproeven. P08 en P10 vergen echte modellen; start lokaal indien beschikbaar, pas betaalde calls toe na afzonderlijk budgetbesluit. Een mocktest meet geen werkelijke modelkwaliteit of capaciteit. Gebruik voor echte servingproeven een bestaande benchmarkclient (zie technische audit).

## Minimaal meetcontract (ontwerp)

Per verzoek: trace-ID, request-ID, variant, geldige inhoudsversie, beleid, route/reasoncode, aangeboden tijd, uitkomst, status en duur.

Per werkelijk gestarte modelpoging: parent trace, attempt-ID, provider/model/revisie, beoogde taak, input/output/cache-read/cache-write/reasoning count indien door provider gerapporteerd, eenheid en betekenis, status, latency, prijsversie en eventuele onzekerheid. Een provider die reasoning al in output telt, mag niet nog eens extra meetellen. Bewaar ontbrekende waarde als null/unknown. Scheid geschatte tokenisatie van providerusage. Tel alleen werkelijk gestarte pogingen als calls; onderscheid aanvragen die afgewezen zijn vóór verzending en aanvragen waarvan facturering onbekend is. Een succesvolle respons en een succesvolle boeking zijn aparte statussen.

Synthetische records, echte providerrecords en geaggregeerde kosten hebben gescheiden opslag/labels. Geen ruwe leerlingtekst in telemetrie; gebruik fictieve IDs en minimale velden. Telemetrie mag een fout in de kostenregistratie niet verbergen: signaleer ontbrekende meetrecords afzonderlijk. Factuurreconciliatie wordt later apart getest.

## Afsluitcriteria

Per proef: vaste bronversie, inputfixture, verwachte eigenschappen, werkelijk antwoord, gemeten waarden en afwijkingen. Test expliciet de negatieve gevallen. Leg vóór de definitieve kwaliteits- en kostenvergelijking de acceptatiegrenzen vast. Een veiligheids-/toegangslek of gebruik van onjuiste bronversie blokkeert die route; een niet-bereikte experimentele route levert geen oordeel op over haar kwaliteit. Maak onderscheid tussen niet gemeten, mislukt, afgewezen en succesvol.

Geen nieuwe betaalde CI, geen productieomgeving, geen omvangrijk lespakket. De eerste technische oplevering is een kleine uitvoerbare proef met herhaalbare meetgegevens. Pas na die proef besluiten we welke technologieën de gedeelde architectuur dragen.
