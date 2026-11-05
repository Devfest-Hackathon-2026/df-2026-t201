"""Poké Lid (ポケふた) dataset: parsing the upstream NDJSON and loading our snapshot."""

import json
import math
from pathlib import Path

from pydantic import BaseModel

DEFAULT_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "pokefuta.json"


class PokeLid(BaseModel):
    id: str
    name: str
    pokemons: list[str]
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


def _to_lid(raw: dict) -> PokeLid | None:
    if raw.get("status") != "active":
        return None
    lat, lng = _coord(raw.get("lat")), _coord(raw.get("lng"))
    if lat is None or lng is None:
        return None
    return PokeLid(
        id=str(raw["id"]),
        name=raw.get("place_label") or raw.get("title", ""),
        pokemons=raw.get("pokemons", []),
        prefecture=raw.get("prefecture", ""),
        city=raw.get("city", ""),
        address=raw.get("address", ""),
        lat=lat,
        lng=lng,
        tags=raw.get("tags", []),
        highlights=[t["label"] for t in raw.get("titles", []) if t.get("label")],
        detail_url=raw.get("detail_url", ""),
    )


def parse_pokefuta_ndjson(text: str) -> list[PokeLid]:
    lids = (_to_lid(json.loads(line)) for line in text.splitlines() if line.strip())
    return [lid for lid in lids if lid is not None]


def load_lids(path: Path = DEFAULT_DATA_PATH) -> list[PokeLid]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [PokeLid.model_validate(item) for item in data]
