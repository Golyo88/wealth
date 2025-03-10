My first AI project. The coding style is not mine. I'm trying to not write any of the code here...

# How to run

```
docker compose up --build
```

open http://0.0.0.0/wealth

# History

https://telex.hu/belfold/2025/03/09/vagyonnyilatkozat-keresheto-pdf-parlament-kepviselok

# Goal

A parlament képviselőinek vagyonnyilatkozatainak a PDF-jeit szeretném berakni egy adatbázisba. Majd egy API-t csinalni hozza, amivel konnyen lehet keresni, szurni stb.

# Toolok

## Cursor

https://www.cursor.com/

## OpenAI

https://platform.openai.com/

# Folyamat

## Splitter

Mivel eleg nagy a pdf, ezert gondoltam szet szedem a pdf-et a képviselők neve alapján. [splitter.py](wealth/splitter.py)
Ezt a script-et lefuttatva megkapjuk a [split_representatives](split_representatives) mappaban a képviselők neve alapján szétválasztott pdf-eket.

## JSON Schema

Ezután egy dokumentumot odaadtam a chat gpt-nek es kertem, hogy generaljon egy json schema-t. [weath.schema.json](wealth/weath.schema.json)
Ebbol generaltam egy pydantic modelt [wealth/wealth.py](wealth/wealth.py)

## PDF Processor

Ezek utan ezt mondtam a cursor-nak:

```
A split representatives mappaban levo pdf-eket szeretnem odaadni a chat-gpt-nek, hogy generaljon egy json-t a wealth.schema.json file alapjan. Csinaljunk egy chat-gpt kliens-t ami kap egy json-schemat es egy pdf content-et. Megvarja a valaszt majd visszaadja azt. Csinaljunk egy scriptet ami parhuzamosan beolvas x-db pdf-et es meghivja a chat gpt klienst.
```

Kis modositas utan megkaptuk a [wealth.json](wealth/wealth.json), a [pdf_processor.py](wealth/pdf_processor.py) es a [walth/gpt_client.py](wealth/gpt_client.py) file-okat.

Ennek a futtatasahoz, kell egy OpenAI API kulcs. Ezt a [.env](.env) file-ban kell beallitani. A kovetkezo formatumban: `OPENAI_API_KEY=kulcs`

Ezt lefuttatva, megkaptuk az [output](output) mappaban levo file-okat.

Ezeket a file-okat mar konnyu berakni adatbazisba

## Adatbazis

Itt megkertem a cursor-t, hogy a model alapjan csinaljon egy sqlalchemy-sdb modelt. [wealth/database/models.py](wealth/database/models.py).

Aztan megkertem, hogy csinaljon egy init_db scriptet, ami betolti az adatbazisba a json-eket. [wealth/database/init_db.py](wealth/database/init_db.py).

Ezt lefuttatva megvan az adabazisunk.

## API

Aztan megkertem a cursort, hogy csinaljon egy API-t aminek be lehet adni egy raw sql query-t (mindenfele security concerns nelkul) es visszaadja a result-ot json-ben.

Illetve egy masik endpointot amivel AI-al lehet keresni.

[wealth/api/api.py](wealth/api/api.py)
Hat itt mar azert voltak problemak. De a pelda query mukodik:

```
Kik azok, akik tobb mint 1 millio forintot kerestek
```

## UI

Na most mar csak egy fancy UI kellene. Ez viszont eleg zokkenomentesen ment.
