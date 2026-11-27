# EAI Teacher Assistant

Onafhankelijk onderzoeks- en ontwikkelproject voor een methodegebonden digitale assistent-leraar.

De vraag: welke ondersteuning kan software geven zonder taalmodel, welke ondersteuning vraagt wel een taalmodel, en wat betekent die keuze voor de kosten en kwaliteit van een volledig leerlinggesprek?

## Vier uitvoeringen, één les

| Variant | Uitvoering |
| --- | --- |
| A | Reguliere LLM-chatbot met vakinhoud, gesprekshistorie en didactische instructies |
| B | Hetzelfde model met begrensde context, caching en passende antwoordlengte |
| C | Hybride assistent: gecontroleerde hints, foutdetectie en beslisregels, met het model van B als terugval |
| D | Dezelfde hybride route als C, met zelfgehoste open-weight modellen in plaats van betaalde modelaanroepen |

Alle vier worden volledig uitgewerkt. De leerlingomgeving, vakinhoud, opdrachten en toetscriteria blijven gelijk.

## Eerste use case

Frans, 2 havo: begeleiding bij het schrijven van korte zinnen over plannen voor het weekend (futur proche). De leerling formuleert en verbetert zelf de zinnen. De assistent bepaalt welke hulp passend is, binnen de door de docent gekozen grenzen.

Deze case is eigen demonstratiemateriaal, geïnspireerd op een publiek beschreven onderwijsopgave. Geen onderdeel van een bestaande Neon-methode en geen officiële samenwerking met Neon.

## Documentatie

- [Plan van aanpak](docs/PLAN.md)
- [Bronnen en aansluiting bij Neon](research/neon/BRONNEN.md)
- [Use case Frans 2 havo](curriculum/french-havo2/USE-CASE.md)
- [Vergelijkingsprotocol](benchmarks/PROTOCOL.md)
- [Hergebruik en rechten](research/HERGEBRUIK.md)

## Status

Onderzoeksopzet v0.1. Er zijn nog geen werkende varianten, modelmetingen of leerlingresultaten in deze repository. De vakinhoud is een ontwerp dat nog door een vakdocent moet worden beoordeeld. Er zijn geen echte leerlinggegevens nodig voor de eerste benchmark.

Geen aangetoonde besparing op een bestaand product. Een eigen model heeft geen externe tokenfactuur, maar wel reken-, hosting- en beheerkosten.
