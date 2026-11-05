# pokemapp-api

FastAPI backend for Pokémapp: finds Poké Lids (ポケふた) near a route and recommends detours with Gemini.

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
| Refresh lid data | `uv run python -m scripts.fetch_pokefuta` |

## Data source

`data/pokefuta.json` is a trimmed snapshot of the open Poké Lid dataset published by
[nishiokya/pokefuta-tracker](https://github.com/nishiokya/pokefuta-tracker)
(`docs/pokefuta.ndjson`, also shown at [data.pokefuta.com](https://data.pokefuta.com/)).
Each lid links back to its official page on [local.pokemon.jp](https://local.pokemon.jp/manhole/) via `detail_url`.
