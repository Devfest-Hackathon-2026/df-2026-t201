"""Refresh data/pokefuta.json from the open Poké Lid (ポケふた) dataset.

Source: https://github.com/nishiokya/pokefuta-tracker (docs/pokefuta.ndjson)
Run from futatabi-api/:  uv run python -m scripts.fetch_pokefuta
"""

import json
import urllib.request

from app.manholes import POKEFUTA_DATA_PATH, parse_pokefuta_ndjson

SOURCE_URL = (
    "https://raw.githubusercontent.com/nishiokya/pokefuta-tracker/main/docs/pokefuta.ndjson"
)


def main() -> None:
    req = urllib.request.Request(SOURCE_URL, headers={"User-Agent": "futatabi-hackathon/0.1"})
    with urllib.request.urlopen(req, timeout=30) as response:
        manholes = parse_pokefuta_ndjson(response.read().decode("utf-8"))

    manholes.sort(key=lambda m: int(m.id.rsplit("-", 1)[-1]))
    # One manhole per line keeps the committed snapshot compact and diff-friendly.
    rows = ",\n".join(json.dumps(m.model_dump(), ensure_ascii=False) for m in manholes)
    POKEFUTA_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    POKEFUTA_DATA_PATH.write_text(f"[\n{rows}\n]\n", encoding="utf-8")
    print(f"Saved {len(manholes)} Poke Lids -> {POKEFUTA_DATA_PATH}")


if __name__ == "__main__":
    main()
