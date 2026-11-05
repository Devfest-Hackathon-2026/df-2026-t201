import json

from app.lids import PokeLid, load_lids, parse_pokefuta_ndjson


def _raw(**overrides) -> dict:
    record = {
        "id": "1",
        "title": "鹿児島県/指宿市",
        "place_label": "指宿市 指宿警察署 指宿中央交番",
        "pokemons": ["イーブイ"],
        "prefecture": "鹿児島県",
        "city": "指宿",
        "address": "鹿児島県指宿市湊1丁目1-1",
        "lat": 31.237194,
        "lng": 130.642861,
        "tags": ["station_front", "tourism"],
        "titles": [{"key": "tourism", "label": "観光地のポケふた", "priority": 36}],
        "detail_url": "https://local.pokemon.jp/manhole/desc/1/?is_modal=1",
        "status": "active",
        "first_seen": "2025-10-26T15:16:55Z",
    }
    record.update(overrides)
    return record


def _ndjson(*records: dict) -> str:
    return "\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n"


def test_parses_record_into_trimmed_lid():
    [lid] = parse_pokefuta_ndjson(_ndjson(_raw()))

    assert lid == PokeLid(
        id="1",
        name="指宿市 指宿警察署 指宿中央交番",
        pokemons=["イーブイ"],
        prefecture="鹿児島県",
        city="指宿",
        address="鹿児島県指宿市湊1丁目1-1",
        lat=31.237194,
        lng=130.642861,
        tags=["station_front", "tourism"],
        highlights=["観光地のポケふた"],
        detail_url="https://local.pokemon.jp/manhole/desc/1/?is_modal=1",
    )


def test_name_falls_back_to_title_without_place_label():
    raw = _raw()
    del raw["place_label"]

    [lid] = parse_pokefuta_ndjson(_ndjson(raw))

    assert lid.name == "鹿児島県/指宿市"


def test_optional_lists_default_to_empty():
    raw = _raw()
    del raw["tags"], raw["titles"]

    [lid] = parse_pokefuta_ndjson(_ndjson(raw))

    assert lid.tags == [] and lid.highlights == []


def test_skips_inactive_records_and_blank_lines():
    text = _ndjson(_raw(id="1"), _raw(id="2", status="deleted")) + "\n\n"

    assert [lid.id for lid in parse_pokefuta_ndjson(text)] == ["1"]


def test_skips_records_without_valid_coordinates():
    text = _ndjson(_raw(id="1"), _raw(id="2", lat=None), _raw(id="3", lng="abc"))

    assert [lid.id for lid in parse_pokefuta_ndjson(text)] == ["1"]


def test_load_lids_reads_saved_json(tmp_path):
    [lid] = parse_pokefuta_ndjson(_ndjson(_raw()))
    path = tmp_path / "pokefuta.json"
    path.write_text(json.dumps([lid.model_dump()], ensure_ascii=False), encoding="utf-8")

    assert load_lids(path) == [lid]
