# EAI Teacher Assistant

Onafhankelijk onderzoeks- en ontwikkelproject voor een methodegebonden digitale assistent-leraar.

De vraag: welke ondersteuning kan software geven zonder taalmodel, welke ondersteuning vraagt wel een taalmodel, en wat betekent die keuze voor de kosten en kwaliteit van een volledig leerlinggesprek?

## Vier vergelijkingshypothesen

| Variant | Uitvoering |
| --- | --- |
| A | Reguliere LLM-chatbot met vakinhoud, gesprekshistorie en didactische instructies |
| B | Hetzelfde model met begrensde context, caching en passende antwoordlengte |
| C | Hybride assistent: gecontroleerde hints, foutdetectie en beslisregels, met het model van B als terugval |
| D | Dezelfde hybride route als C, met zelfgehoste open-weight modellen in plaats van betaalde modelaanroepen |

De technische uitwerking van A–D staat in de [specificatie v0.1](research/TECHNISCHE-SPECIFICATIE.md). Alle varianten delen gewone lesfuncties, bevoegdheden, bronversies en dezelfde aangeboden aanvragen. A en B gebruiken dezelfde modeltaak; C onderzoekt welke extra modeltaken gewone software kan afhandelen; D onderzoekt lokale inferentie met dezelfde hybride route. Dit zijn vergelijkingshypothesen, geen architectuurkeuze. De uiteindelijke onderwijsfuncties, vakinhoud en kwaliteitscriteria blijven gelijk.

## Onderzoek: eerst breed, daarna kiezen

![Onderzoeksindeling met tien sporen en vier terugkerende onderwerpen](docs/illustraties/onderzoeksindeling.svg)

We onderzoeken oorspronkelijke ontwerpgedachten, technische mechanismen, bewijs en eerdere fouten uit de repositories, oudere versies, boeken, bibliotheek en externe bronnen. Een vondst kan bij meerdere sporen horen. Zie de [onderzoeksindeling en werkwijze](research/ONDERZOEKSINDELING.md).

## Eerst de techniek, daarna de les

Het project onderzoekt een assistent die in bestaande digitale lessen kan worden aangesloten. De software krijgt de geldige lesversie, het leerdoel en de grenzen van de ondersteuning uit de leeromgeving. Welke beslissingen zonder model kunnen worden genomen en waar een model nodig blijft, is een onderzoeksvraag.

Frans 2 havo en rekenen in groep 7 zijn eerdere kandidaten voor latere demonstraties. De bestaande casusschets blijft voorlopig. In fase 4a gebruiken we uitsluitend neutrale technische gegevens: geen vakinhoud, lespakket of tutorprompt. De inhoudelijke uitwerking volgt pas na de technische vergelijking en architectuurkeuze.

Dit is onafhankelijk onderzoek, geïnspireerd op publieke onderwijsopgaven. Geen onderdeel van een bestaande Neon-methode en geen officiële samenwerking met Neon.

## Gebruikersomvang en belasting

Neon meldde op 28 september 2026 ruim 1.500 aangesloten scholen met samen ongeveer 700.000 leerlingen. Dat is potentieel bereik, geen vastgesteld gebruik van de assistent. Het onderzoek bevat drie schaalniveaus: 70.000, 280.000 en 700.000 actieve leerlingen, met verschillende gebruiksintensiteiten. De vier varianten worden op dezelfde belasting vergeleken; gelijktijdigheid en schoolpieken tellen mee.

## Documentatie

- [Plan van aanpak v0.4](docs/PLAN.md)
- [Technische specificatie A–D v0.1](research/TECHNISCHE-SPECIFICATIE.md)
- [Onderzoeksindeling en werkwijze](research/ONDERZOEKSINDELING.md)
- [Bronnenregister: ronde 01](research/register/RONDE-01.md)
- [Openbare afgeleide van het bronnenregister (29 van 87 repositories)](research/register/public-repositories.json)
- [Verdiepend bronnenonderzoek](research/VERKENNING.md)
- [Functionele vergelijking en ontwerpvoorwaarden](research/FUNCTIONELE-EISEN.md)
- [Technische hergebruiksaudit](research/TECHNIEKAUDIT.md)
- [Minimale technische proeven](benchmarks/TECHNISCHE-PROEVEN.md)
- [Bronnen en aansluiting bij Neon](research/neon/BRONNEN.md)
- [Use case Frans 2 havo](curriculum/french-havo2/USE-CASE.md)
- [Vergelijkingsprotocol](benchmarks/PROTOCOL.md)
- [Gebruikersomvang, capaciteits- en kostenmodel](benchmarks/SCHAALMODEL.md)
- [Hergebruik en rechten](research/HERGEBRUIK.md)

## Status

**27 november 2026: fase 4a gereed voor uitvoering.** De brede bronneninventarisatie (3a) en vergelijking van mechanismen (3b) zijn voor deze onderzoeksronde afgerond. De technische specificatie (3c) legt de verantwoordelijkheden, gegevenscontracten, uitvoeringsroutes, foutpaden en meting vast. Het interne onderzoeksregister blijft leidend voor de onderliggende bronnen en open vragen. De openbare index bevat de openbare afgeleide van de eerste inventarisatie (29 van 87 repositories), geen volledige actuele onderzoeksdekking.

De volgende stap is één klein proefprogramma voor P01–P03: telemetrie en budget, toegangs- en versiegrenzen, routekeuze en uitvoercontrole. Gebruik neutrale gegevens, geïnjecteerde testadapters en nul echte inferentie. Er is nog geen proefcode uitgevoerd en er zijn geen modelmetingen of leerlingresultaten. De definitieve architectuur, hergebruikrechten, vakinhoud, modellen, hosting en budget voor echte inferentie blijven open.

Geen aangetoonde besparing op een bestaand product. Een eigen model heeft geen externe tokenfactuur, maar wel reken-, hosting- en beheerkosten.
