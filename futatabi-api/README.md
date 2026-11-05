# futatabi-api

Backend for **FutaTabi (蓋旅)**: plan a design-manhole hunt at your destination, with nearby spots, time and distance.
The hackathon edition covers Poké Lids (ポケふた); the `Manhole` model is generic (`kind`) so other design manholes can be added later.

## Setup

```bash
uv sync
cp .env.example .env   # fill in GEMINI_API_KEY and GOOGLE_MAPS_API_KEY
```

| Task | Command |
| --- | --- |
| Run (local) | `uv run uvicorn app.main:app --reload --port 8080` |
| Run (Docker, from repo root) | `docker compose up --build -d` |
| Test | `uv run pytest` |
| Lint / format | `uv run ruff check . --fix && uv run ruff format .` |
| Refresh Poké Lid data | `uv run python -m scripts.fetch_pokefuta` |

## API

| Method | Path | Description |
| --- | --- | --- |
| GET | `/health` | Liveness |
| GET | `/manholes` | List manholes; filters: `kind`, `prefecture`, `character` |
| GET | `/manholes/{id}` | One manhole (e.g. `pokefuta-1`) |

Interactive docs: `http://localhost:8080/docs`.

## Data source

`data/pokefuta.json` is a trimmed snapshot of the open Poké Lid dataset published by
[nishiokya/pokefuta-tracker](https://github.com/nishiokya/pokefuta-tracker)
(`docs/pokefuta.ndjson`, also shown at [data.pokefuta.com](https://data.pokefuta.com/)).
Each manhole links back to its official page on [local.pokemon.jp](https://local.pokemon.jp/manhole/) via `detail_url`.
