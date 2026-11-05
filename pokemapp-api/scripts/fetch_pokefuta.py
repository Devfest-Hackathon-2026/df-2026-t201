"""Refresh data/pokefuta.json from the open Poké Lid dataset.

Source: https://github.com/nishiokya/pokefuta-tracker (docs/pokefuta.ndjson)
Run from pokemapp-api/:  uv run python -m scripts.fetch_pokefuta
"""

import json
import urllib.request

from app.lids import DEFAULT_DATA_PATH, parse_pokefuta_ndjson

SOURCE_URL = (
    "https://raw.githubusercontent.com/nishiokya/pokefuta-tracker/main/docs/pokefuta.ndjson"
)


def main() -> None:
    req = urllib.request.Request(SOURCE_URL, headers={"User-Agent": "pokemapp-hackathon/0.1"})
    with urllib.request.urlopen(req, timeout=30) as response:
        lids = parse_pokefuta_ndjson(response.read().decode("utf-8"))

    lids.sort(key=lambda lid: int(lid.id) if lid.id.isdigit() else lid.id)
    # One lid per line keeps the committed snapshot compact and diff-friendly.
    rows = ",\n".join(json.dumps(lid.model_dump(), ensure_ascii=False) for lid in lids)
    DEFAULT_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    DEFAULT_DATA_PATH.write_text(f"[\n{rows}\n]\n", encoding="utf-8")
    print(f"Saved {len(lids)} Poke Lids -> {DEFAULT_DATA_PATH}")


if __name__ == "__main__":
    main()
