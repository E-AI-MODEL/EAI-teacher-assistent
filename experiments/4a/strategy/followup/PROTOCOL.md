# 4a.4 | Relevante wijzigingen tegenover entropie

28 november 2026. Vervolg op [4a.3](../RESULTS.md). Geen bestaande code, test, evidence of grenzen uit 4a.3 wijzigen. Nieuwe neutrale, geconstrueerde reeksen; geen vakinhoud, provider of betaalde proef. Dezelfde onderzoeker bepaalt de oracle; geen onafhankelijke evaluatie.

## Vooraf vastgelegde vergelijking

De vier eerdere controllers worden ongewijzigd hergebruikt. Voeg drie armen toe:
- relevant_change: maximaal vijf geldige beurten per beoordeling; eerder herbeoordelen zodra het expliciete A/B-signaal afwijkt van de bewaarde keuze of het anker wijzigt. Geen entropie.
- signal_entropy: zelfde adaptieve venster, recencygewichten, grenzen en hysteresis als 4a.3, maar alleen genormaliseerde Shannon-entropie van A/B berekenen. X/Y beïnvloedt het venster niet. Geen andere entropiesporen berekenen. Ankerwisseling blijft een harde interrupt.
- relevant_debounce: maximaal vijf geldige beurten; twee opeenvolgende afwijkende A/B-signalen verbreken de lock, ook zonder entropie. Afloop geeft opnieuw de huidige kandidaat. Geen andere drempels afstellen.

De nieuwe armen gebruiken dezelfde autorisatie, valide invoer, neutrale executor, reset, scope en revisiecontrole als de oude. X/Y blijft verplicht als invoerveld volgens het bestaande contract, ook waar het niet de keuze stuurt. Onbekend of ongeldig betekent reset en geen uitvoering. Geen stilzwijgende bypass van deze validatie. De gedeelde route geeft geen echte modelaanroep.

## Voorspelling en falsificatie

Een expliciete wijzigingscontrole hoort dezelfde keuzes te maken als per-beurt beoordelen bij gelijke geldige observaties, met minder beoordelingen op stabiele stukken. De relevantievariant van entropie hoort op alleen X/Y-ruis geen vensterverkorting te veroorzaken. Debounce kan korte ruis onderdrukken maar echte wisselingen missen. Twee reeksen hebben exact dezelfde observaties met verschillende gewenste uitkomsten: een tijdelijke B is in de ene wereld ruis, in de andere een echte verandering. Geen controller krijgt de oracle; beide werelden moeten bij dezelfde observaties dezelfde beslissingen en tellers opleveren. Daarmee kan geen van deze controllers zonder extra informatie beide werelden altijd juist onderscheiden.

Meet per arm en reeks herbeoordelingen, hergebruik, verkeerde keuzes (bij hergebruik of herbeoordeling), daadwerkelijk uitgevoerde en afgeleverde referenties, geweigerde en stale resultaten, autorisatiecontroles, invoervelden en daadwerkelijke entropie-evaluaties. Een batch van de oude adaptive bevat vier berekeningen; signal_entropy één. Tel de functies daadwerkelijk aan de uitvoergrens (geen aangenomen aantal per beurt). Controleer expliciete verandering, anker, afloop, onbekend, ongeldige invoer, gescheiden scope, intrekking en ABA vóór aflevering. Stop bij een harde invariantbreuk; bewaar zachte fouten. Geen tijd- of tokenbesparing afleiden uit tellers alleen.

Geen keuze op basis van een opgetelde score met fictieve gebruiksfrequenties. Vergelijk per geval en houd de eenvoudige referentie aan wanneer een extra techniek geen onderscheidend voordeel toont. De fixtures en oracle staan vóór de kandidaatcode vast. Nieuwe tests mogen een fout aan het licht brengen; wijzig geen bevroren verwachtingen na uitvoering.
