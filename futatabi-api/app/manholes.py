"""Design manhole datasets: parsing upstream sources and loading our snapshots.

Only Poké Lids (ポケふた, kind="pokefuta") are loaded for now; other kinds
(e.g. Gundam or municipal design manholes) can be added as new parsers + data files.
"""

import json
import math
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
POKEFUTA_DATA_PATH = DATA_DIR / "pokefuta.json"

ManholeKind = Literal["pokefuta"]


class Manhole(BaseModel):
    id: str
    kind: ManholeKind
    name: str
    characters: list[str] = []
    prefecture: str
    city: str
    address: str
    lat: float
    lng: float
    tags: list[str] = []
    highlights: list[str] = []
    detail_url: str


def _coord(value: object) -> float | None:
    if isinstance(value, bool) or not isinstance(value, int | float):
        return None
    return float(value) if math.isfinite(value) else None


def _pokefuta_to_manhole(raw: dict) -> Manhole | None:
    if raw.get("status") != "active":
        return None
    lat, lng = _coord(raw.get("lat")), _coord(raw.get("lng"))
    if lat is None or lng is None:
        return None
    return Manhole(
        id=f"pokefuta-{raw['id']}",
        kind="pokefuta",
        name=raw.get("place_label") or raw.get("title", ""),
        characters=raw.get("pokemons", []),
        prefecture=raw.get("prefecture", ""),
        city=raw.get("city", ""),
        address=raw.get("address", ""),
        lat=lat,
        lng=lng,
        tags=raw.get("tags", []),
        highlights=[t["label"] for t in raw.get("titles", []) if t.get("label")],
        detail_url=raw.get("detail_url", ""),
    )


def parse_pokefuta_ndjson(text: str) -> list[Manhole]:
    manholes = (
        _pokefuta_to_manhole(json.loads(line)) for line in text.splitlines() if line.strip()
    )
    return [m for m in manholes if m is not None]


def load_manholes(path: Path = POKEFUTA_DATA_PATH) -> list[Manhole]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [Manhole.model_validate(item) for item in data]


@lru_cache
def get_manholes() -> list[Manhole]:
    """FastAPI dependency: all manhole snapshots, loaded once per process."""
    return load_manholes()
