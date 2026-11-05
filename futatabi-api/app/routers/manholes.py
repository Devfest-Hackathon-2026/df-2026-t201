from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.manholes import Manhole, ManholeKind, get_manholes

router = APIRouter(prefix="/manholes", tags=["manholes"])

Manholes = Annotated[list[Manhole], Depends(get_manholes)]


@router.get("")
def list_manholes(
    manholes: Manholes,
    kind: ManholeKind | None = None,
    prefecture: str | None = None,
    character: str | None = None,
) -> list[Manhole]:
    """Design manholes, filtered by kind, prefecture (東京都) or character (イーブイ)."""
    return [
        m
        for m in manholes
        if (kind is None or m.kind == kind)
        and (prefecture is None or m.prefecture == prefecture)
        and (character is None or character in m.characters)
    ]


@router.get("/{manhole_id}")
def get_manhole(manhole_id: str, manholes: Manholes) -> Manhole:
    for m in manholes:
        if m.id == manhole_id:
            return m
    raise HTTPException(status_code=404, detail=f"Manhole {manhole_id} not found")
