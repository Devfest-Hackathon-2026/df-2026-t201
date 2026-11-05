import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.manholes import Manhole, get_manholes


def _manhole(id: str, prefecture: str, characters: list[str]) -> Manhole:
    return Manhole(
        id=f"pokefuta-{id}",
        kind="pokefuta",
        name=f"manhole {id}",
        characters=characters,
        prefecture=prefecture,
        city="",
        address="",
        lat=35.0,
        lng=139.0,
        detail_url=f"https://local.pokemon.jp/manhole/desc/{id}/",
    )


FAKE_MANHOLES = [
    _manhole("1", "鹿児島県", ["イーブイ"]),
    _manhole("2", "東京都", ["ピカチュウ", "イーブイ"]),
    _manhole("3", "東京都", ["ラッキー"]),
]


@pytest.fixture
def client() -> TestClient:
    app = create_app()
    app.dependency_overrides[get_manholes] = lambda: FAKE_MANHOLES
    return TestClient(app)


def _ids(response) -> list[str]:
    return [m["id"] for m in response.json()]


def test_list_manholes_returns_all(client):
    response = client.get("/manholes")

    assert response.status_code == 200
    assert _ids(response) == ["pokefuta-1", "pokefuta-2", "pokefuta-3"]


def test_list_manholes_filters_by_kind(client):
    assert len(_ids(client.get("/manholes", params={"kind": "pokefuta"}))) == 3
    assert client.get("/manholes", params={"kind": "unknown"}).status_code == 422


def test_list_manholes_filters_by_prefecture(client):
    response = client.get("/manholes", params={"prefecture": "東京都"})

    assert _ids(response) == ["pokefuta-2", "pokefuta-3"]


def test_list_manholes_filters_by_character(client):
    response = client.get("/manholes", params={"character": "イーブイ"})

    assert _ids(response) == ["pokefuta-1", "pokefuta-2"]


def test_get_manhole_by_id(client):
    response = client.get("/manholes/pokefuta-2")

    assert response.status_code == 200
    assert response.json()["characters"] == ["ピカチュウ", "イーブイ"]


def test_get_unknown_manhole_returns_404(client):
    assert client.get("/manholes/pokefuta-999").status_code == 404
