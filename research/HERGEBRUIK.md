# Hergebruik: eerste inventarisatie

> Status v0.3: Deze bevindingen blijven behouden als voorlopige bronnen. Zij begrenzen de heropende brede verkenning niet. Zie de [onderzoeksindeling](ONDERZOEKSINDELING.md).


Deze lijst is een technisch vertrekpunt, geen toestemming voor overname. Alleen openbare referenties zijn opgenomen. Privébroncode en niet-openbare informatie blijven buiten deze repository.

| Publieke referentie | Te onderzoeken toepassing | Afbakening |
| --- | --- | --- |
| [RAG EAT Starter Kit](https://github.com/E-AI-MODEL/-rag-eat-starter-kit/blob/main/src/ragkit/assistant.py) | Bronselectie, optionele modeladapter, extractieve terugval | Aanscherpen op vakinhoud en bewijs van juistheid; demonstratie is geen productiegarantie |
| [Caveman-eduNL](https://github.com/E-AI-MODEL/Caveman-eduNL/blob/main/docs/OUTPUT_CONTRACTS.md) | Passende antwoordlengte per ondersteuningsvorm | Onderwijskwaliteit toetsen; besparingen meten |
| [EAIwork](https://github.com/E-AI-MODEL/EAIwork-/blob/main/packages/gateway/src/gateway.ts) | Begrensde contextpakketten per taak | Conceptueel referentiepunt; licentie en hergebruik vooraf controleren |
| [EAI Standard](https://github.com/E-AI-MODEL/EAI-standard) | Beschrijving van leerlinghandeling en rol van AI | Specificatie, geen bewezen onderwijsresultaat |
| [EAI Lab](https://github.com/E-AI-MODEL/EAI-lab-) | Gestructureerde observaties en validatie | Experimentele basis, geen complete tutor |

Aanvullende ontwerppatronen: regels vóór modelaanroepen, didactische routering, selectieve context, verwisselbare modeladapters en gecontroleerde terugval. Deze kunnen onafhankelijk worden geïmplementeerd wanneer bestaande code niet beschikbaar of niet herbruikbaar is.

## Verdiepte openbare referenties

| Bron | Geïnspecteerd mechanisme | Beperking / besluit |
| --- | --- | --- |
| [EAI Standard: human-system boundary](https://github.com/E-AI-MODEL/EAI-standard/blob/main/docs/human-system-boundary.md) en [evidence and handback](https://github.com/E-AI-MODEL/EAI-standard/blob/main/docs/evidence-handback-remediation.md) | Menselijke handeling, AI-actie, bewijs en teruggeven van de handeling zijn gescheiden. | Gebruik de actuele 0.5.0-candidate met vastgelegde versie, geen oude rubric-ID's ongemerkt overnemen. [Apache-2.0 scope](https://github.com/E-AI-MODEL/EAI-standard/blob/main/LICENSE-SCOPE.md) sluit rechten op materiaal van derden uit. |
| [EAI Standard: scaffolding and feedback](https://github.com/E-AI-MODEL/EAI-standard/blob/main/registries/microstructures/teacher-scaffolding-and-feedback.yaml) | Concrete handelingen rond hints, feedback, voordoen, afbouw en nieuwe poging. | Gebruik als inhoudelijke bron voor het taakcontract, niet als reeds bewezen automatische tutor. |
| [EAIhome zoekcode](https://github.com/E-AI-MODEL/EAIhome/blob/main/src/eaihome/search.py) en [tests](https://github.com/E-AI-MODEL/EAIhome/blob/main/tests/test_eaihome.py) | Versies behouden, bronhash, toegangsfilter, duplicaten herkennen. | SQLite-proef; geen productie-authenticatie of selectie van de geldige lesversie. De bron is gelezen, tests niet opnieuw uitgevoerd. |
| [EAT_me evaluator](https://github.com/E-AI-MODEL/EAT_me/blob/main/eatme/evaluator.py) | Observeren en ingrijpen als afzonderlijke modi. | Eerst in schaduwmodus vergelijken; heuristische scores niet als waarheidsmeting gebruiken. |
| [EAIspeak browsermodel](https://github.com/E-AI-MODEL/website/blob/main/tools/eaispeak/src/browser-llm.js) | WebGPU-modeladapter, laden en vrijgeven, onderbreking. | Clientgeheugen, downloads, browser/device en kwaliteit apart testen. Controleer licentie van model én code. |
| [Caveman-eduNL technische handleiding](https://github.com/E-AI-MODEL/Caveman-eduNL/blob/main/docs/TECHNICAL_GUIDE.md) | Antwoordcontracten per didactische functie. | De huidige tests controleren vooral instructies, documentatie en installer; geen gemeten onderwijs- of tokenbesparing. |
| [TOON upstream](https://github.com/toon-format/toon) | Compacte representatie van uniforme gestructureerde gegevens. | Vergelijk met minified JSON, gewone korte tekst en daadwerkelijke tokenizer; geen generieke besparingsclaim. Behoud upstreamherkomst. |
| [EAIwork after-action](https://github.com/E-AI-MODEL/EAIwork-/blob/main/docs/validation-3b-7b-after-action.md) | Timeouts per verzoek onderscheiden van niet-beoordeelde cases; kleine modellen kunnen stellig antwoorden bij ontbrekend bewijs. | Bevries testset, meet echte aanroepen en rapporteer uitval apart. Licentie vooraf toetsen. |
| [NeSy postmortem](https://github.com/E-AI-MODEL/eainesy/blob/main/docs/NeSy-P02-run-failure-root-cause-2026-10-23.md) | Betaalde proef bereikte de beoogde experimentele route niet. | Preflight routebereik; stopcriteria en budgetgrens vóór echte inferentie. Geen volledige solver of multi-agentstack overnemen zonder noodzaak. |

De oudere SSOT 17-repository heeft een uitdrukkelijk beperkende [licentie](https://github.com/E-AI-MODEL/SSOT_17/blob/main/LICENSE). Geen overname of redistributie van deze inhoud of implementatie in dit project zonder passende toestemming. Ook voor alle openbare bronnen geldt: openbare leesbaarheid is niet hetzelfde als hergebruikrecht. Voor mechanismen uit niet-openbare repositories is de audit intern; de openbare documentatie bevat geen private bronbestanden of interne testdata.

## Technische selectie

De [technische audit](TECHNIEKAUDIT.md) bevat de geselecteerde mechanismen met vastgelegde bronversies, beperkingen en externe alternatieven. De [proeven](../benchmarks/TECHNISCHE-PROEVEN.md) toetsen deze vóór de architectuurkeuze. Oude EAI-inhoud wordt niet automatisch overgenomen. Directe codeovername blijft afhankelijk van licentie, integratie en testresultaten.

## Audit voor daadwerkelijke overname

Per bestand of functie: exacte commit, pad, oorspronkelijke werking, testdekking en daadwerkelijk uitgevoerde tests, licentie en auteursrecht, eventuele gegevens, beoogde wijziging en integratietest. Pas daarna overnemen. Behoud toepasselijke notices. Niet-commerciële onderdelen niet stilzwijgend gebruiken voor commerciële toepassing.

Langdurig leerlinggeheugen valt buiten de eerste casus. Geen kopieën van bestaande repositories opnemen voordat de hergebruiksaudit is afgerond.
