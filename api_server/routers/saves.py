from __future__ import annotations

from fastapi import APIRouter
from api_server.schemas import SaveCreate, SaveInfo
from api_server.services import save_registry

router = APIRouter(prefix="/saves", tags=["saves"])


@router.get("", response_model=list[SaveInfo])
def list_saves() -> list[SaveInfo]:
    return save_registry.list_saves()


@router.post("", response_model=SaveInfo)
def create_save(body: SaveCreate) -> SaveInfo:
    return save_registry.create_save(body.name)


@router.get("/{save_id}", response_model=SaveInfo)
def get_save(save_id: str) -> SaveInfo:
    return save_registry.get_save_info(save_id)


@router.delete("/{save_id}")
def delete_save(save_id: str) -> dict:
    deleted = save_registry.delete_save(save_id)
    return {"deleted": deleted}
