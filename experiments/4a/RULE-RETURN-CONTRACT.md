# Aanvullend retourcontract regelroute 4a.5

Vooraf vastgelegd voor de minimale herstelproef; geen productiecontract of architectuurkeuze. Bronnen: [startcontract](../../benchmarks/4A-STARTCONTRACT.md), [tegenproef](review/rule-route/README.md), PR #4, baseline `4cd22b39230407394e9f6a13b7acfc38de4fde76`. De oorspronkelijke bevroren fixtures, verwachtingen, resultaten en historische tegenproef blijven ongewijzigd.

Bij een unieke toepasselijke regel (`R=1`, precies één match) ontvangt de engine de geregistreerde referentie. Het enige succesvolle voorstel is een gewoon dictionary met exact `kind: SELECT`, `ref: <geregistreerde referentie>` en `used_refs: [<geregistreerde referentie>]`. De vorm en veldtypen moeten kloppen. De waarde wordt door de runtime uit de actuele gecompileerde bron gehaald. Deze keuze geldt voor de neutrale fixture, niet voor alle toekomstige denkbare regelengines.

- Verkeerde, onbekende of verboden referenties, ontbrekende, extra of dubbele herkomst, andere voorsteltypen (ook GENERATE, CLARIFY, HANDOFF), extra velden en ongeldige typen: INVALID_PROPOSAL, geen payload, geen modelpoging. Een engine-exceptie blijft ENGINE_ERROR.
- Regelspecifieke controle is onafhankelijk van P, S en M; contextminimalisatie is geen regelvalidatie.
- De algemene proposalvalidator blijft behouden. MODEL (ook OTHER en AMBIG), voorafgaande strategie-CLARIFY, LOOKUP, autorisatie, revisiecontrole vóór aflevering, replay en conflict behouden hun gedrag.
- Trace moet het werkelijke routebereik, engineaanroep en terminale uitkomst tonen. Replay herhaalt alleen de vastgelegde terminale uitkomst, niet de uitvoering. Geen echte providercalls.
- De nieuwe tests worden eerst op de oude runtime uitgevoerd (verwachte negatieve resultaten), daarna ongewijzigd op de kandidaat. De oorspronkelijke 60 scenario's en vijf regressies moeten opnieuw slagen. Een fout in de oude baseline telt niet als een succesvolle regressietest. Bewaar logs, hashes en aantallen. Geen merge.

De nieuwe afwijzing van CLARIFY/HANDOFF en extra/dubbele herkomst is een expliciete aanvullende ontwerpkeuze voor deze neutrale proef. Het oorspronkelijke startcontract legde dit niet volledig vast. De modelroute houdt de eerder toegestane voorsteltypen.
