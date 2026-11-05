import pytest
from fastapi.testclient import TestClient

from app.lids import PokeLid, get_lids
from app.main import create_app


def _lid(id: str, prefecture: str, pokemons: list[str]) -> PokeLid:
    return PokeLid(
        id=id,
        name=f"lid {id}",
        pokemons=pokemons,
        prefecture=prefecture,
        city="",
        address="",
        lat=35.0,
        lng=139.0,
        detail_url=f"https://local.pokemon.jp/manhole/desc/{id}/",
    )


FAKE_LIDS = [
    _lid("1", "鹿児島県", ["イーブイ"]),
    _lid("2", "東京都", ["ピカチュウ", "イーブイ"]),
    _lid("3", "東京都", ["ラッキー"]),
]


@pytest.fixture
def client() -> TestClient:
    app = create_app()
    app.dependency_overrides[get_lids] = lambda: FAKE_LIDS
    return TestClient(app)


def test_list_lids_returns_all(client):
    response = client.get("/lids")

    assert response.status_code == 200
    assert [lid["id"] for lid in response.json()] == ["1", "2", "3"]


def test_list_lids_filters_by_prefecture(client):
    response = client.get("/lids", params={"prefecture": "東京都"})

    assert [lid["id"] for lid in response.json()] == ["2", "3"]


def test_list_lids_filters_by_pokemon(client):
    response = client.get("/lids", params={"pokemon": "イーブイ"})

    assert [lid["id"] for lid in response.json()] == ["1", "2"]


def test_get_lid_by_id(client):
    response = client.get("/lids/2")

    assert response.status_code == 200
    assert response.json()["pokemons"] == ["ピカチュウ", "イーブイ"]


def test_get_unknown_lid_returns_404(client):
    assert client.get("/lids/999").status_code == 404
