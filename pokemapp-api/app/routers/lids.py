from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.lids import PokeLid, get_lids

router = APIRouter(prefix="/lids", tags=["lids"])

Lids = Annotated[list[PokeLid], Depends(get_lids)]


@router.get("")
def list_lids(
    lids: Lids, prefecture: str | None = None, pokemon: str | None = None
) -> list[PokeLid]:
    """All Poké Lids, optionally filtered by prefecture (e.g. 東京都) or Pokémon (e.g. イーブイ)."""
    return [
        lid
        for lid in lids
        if (prefecture is None or lid.prefecture == prefecture)
        and (pokemon is None or pokemon in lid.pokemons)
    ]


@router.get("/{lid_id}")
def get_lid(lid_id: str, lids: Lids) -> PokeLid:
    for lid in lids:
        if lid.id == lid_id:
            return lid
    raise HTTPException(status_code=404, detail=f"Poké Lid {lid_id} not found")
