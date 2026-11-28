# Tegenproef regelroute 4a

Status: historische tegenproef, geen reparatie en geen vrijgave. PR #4 blijft concept.

## Herkomst en reproduceerbaarheid

- Onderzochte kandidaat: `0a309dc8a90d18b40b0ab3aa1de48afb8ca19086`.
- Bij eerste inspectie en archivering was de PR-head `42e5eb36d5fc7968db46a960ef49692175b47d39`.
- Bevroren fixtures: `371e721518f17911fff2f9e73d96367535a246cf`.
- De meegeleverde runtime.py en fixture.json zijn historische, byte-identieke kopieën; niet de te onderhouden runtime. Blobhashes: `83e399ad256abcc727e1b8eb4c1a6c6292c70dac` en `d4993a49a6c4c66212fe58f97f34a1752ad9a8ee`.
- Het originele counterprobe.py is ongewijzigd overgenomen uit het testarchief (Git-blob `ce8837957b23babae791ff53f4ccad3e065be905`). De oorspronkelijke volledige JSON-uitvoer is verliesloos opgeslagen als compacte gzip-JSON. Een nieuwe lokale uitvoering in Python 3.13.5 leverde een byte-identieke tekstlog op en dezelfde volledige JSON-resultaten na weglaten van duration_ns.
- De oorspronkelijke 60 scenario's zijn bij deze tegenproef niet lokaal opnieuw uitgevoerd. De drie bevroren bestanden zijn via GitHub geïnspecteerd; hun blobhashes zijn gelijk aan die van de bevroren commit. De aanvullende tegenproef is geen bewijs van onafhankelijke menselijke review.

Reproduceer in deze map, met Python 3.13.5 en zonder -O:

```sh
python counterprobe.py > rerun.log
```

Dit schrijft counterprobe-results.json. Het historische bewijsbestand blijft ongewijzigd. De scriptuitgang is geen releasegate: lees de getelde afwijkingen en de individuele observaties.

Herstel de oorspronkelijke JSON-uitvoer byte voor byte (standaardbibliotheek):

```sh
python -c "import gzip,json,pathlib,hashlib; p=(json.dumps(json.loads(gzip.decompress(pathlib.Path('counterprobe-evidence.json.gz').read_bytes())),indent=2)+'\\n').encode(); assert hashlib.sha256(p).hexdigest()=='1b3b62f6211062fecbb681ee73c16ecdafa280bb56c077a6bb43c27d7fd29d2a'; pathlib.Path('original-results.json').write_bytes(p)"
```

## Resultaten

120 primaire proefgevallen, 124 aanvragen inclusief vier replay-aanvragen. 85 conform, 11 afwijkend van de nieuwe proefverwachtingen en 24 verkennend (niet beoordeeld). 16 modelstubaanroepen uitsluitend bij fallback- en modelcontrolegevallen; nul bij unieke regelmatches. Geen echte modelinferentie.

| P/S/R/M | Arm | Conform | Afwijkend | Verkennend |
|---|---|---:|---:|---:|
| 0010 | A | 19 | 5 | 4 |
| 0011 | A | 22 | 2 | 4 |
| 1111 | A | 22 | 2 | 4 |
| 0011 | D | 22 | 2 | 4 |
| 0000 | A | 0 | 0 | 4 |
| 0001 | A | 0 | 0 | 4 |

### Bevestigde uitkomstafwijkingen

- EXACT1 (R1/ALPHA) accepteert SELECT R2/BETA bij 0010. EXACT2 accepteert omgekeerd R1. Dit is een onjuiste geregistreerde uitkomst, niet een overschrijding van de scopes.
- De trace registreert R1 als geselecteerde regel, maar de uitkomst bevat R2. Replay geeft dezelfde verkeerde uitkomst opnieuw terug. Bij 0011, 1111 en 0011-D wordt de verkeerde selectie door de kleinere context geweigerd, niet door een regelspecifieke vergelijking.
- GENERATE NEUTRAL, zowel zonder referenties als met R1, levert bij alle vier R-configuraties status OK in plaats van de geregistreerde regelwaarde. Dit zijn acht afwijkingen van de nieuwe verwachting dat een unieke regeluitkomst niet door een willekeurig payload mag worden vervangen. Het oorspronkelijke contract specificeert de exacte retourtypen van de engine niet; de expliciete fail-closed afspraak moet nog worden vastgelegd.
- De elf afwijkende proefgevallen zijn drie verkeerde-selectieproeven (waaronder één met replay) en acht GENERATE-proeven; geen elf afzonderlijke bugs.

### Wat niet is aangetast

De nieuwe proef bevestigt correcte unieke matches, afwijzing van verboden en onbekende referenties, afwijzing van ongeldige schemas, enginefouten zonder modelbypass, autorisatie en revisiecontroles, en toegestane fallback bij OTHER en AMBIG. De oorspronkelijke runner retourneert bij succesvolle engine-uitvoering steeds de ontvangen referentie en heeft de afwijkende enginevoorstellen niet onderzocht. De 60 eerder gerapporteerde geslaagde scenario's blijven daarom een beperkte, geldige uitkomst.

### Open ontwerpvragen

CLARIFY/HANDOFF bij een unieke regelmatch, extra toegestane herkomstreferenties en dubbele referenties blijven verkennend. Bepaal eerst de precieze betekenis van deze uitvoer. Het startcontract noemt de modelvoorsteltypen, maar legt het retourcontract van de deterministische engine niet volledig vast.

### Vervolg en stop

Advies: leg vóór een nieuwe kandidaatversie expliciet vast dat een unieke neutrale regelmatch alleen de geregistreerde referentie mag afleveren, onafhankelijk van M. Overweeg voor deze fixture een exacte SELECT met uitsluitend de verwachte referentie als herkomst. Een niet-conform voorstel levert geen payload en geen modelbypass; maak trace en replay consistent. Behoud de algemene validator voor de modelroute. Behoud alle oorspronkelijke fixtures, code en uitkomsten in dit archief. Voer de originele suite en de nieuwe, vooraf vastgelegde regressies uit op een afzonderlijke kandidaat. Geen extra modelrechter nodig. Geen productiereparatie of merge in deze archiveringscommit.

Bronnen: [startcontract](../../../../benchmarks/4A-STARTCONTRACT.md), [onderzochte runtime](https://github.com/E-AI-MODEL/EAI-teacher-assistent/blob/0a309dc8a90d18b40b0ab3aa1de48afb8ca19086/experiments/4a/runtime.py), [runner](https://github.com/E-AI-MODEL/EAI-teacher-assistent/blob/0a309dc8a90d18b40b0ab3aa1de48afb8ca19086/experiments/4a/run.py).
