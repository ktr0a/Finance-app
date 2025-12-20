from __future__ import annotations

from fastapi import APIRouter, Depends

from finance_app.api.deps import get_finance_service
from finance_app.api.schemas import BackupInfo, RestoreBackupIn, RestoreResult
from finance_app.api.services.finance_service import FinanceService

router = APIRouter(prefix="/saves/{save_id}/backups", tags=["backups"])


@router.get("", response_model=list[BackupInfo])
def list_backups(
    save_id: str,
    service: FinanceService = Depends(get_finance_service),
) -> list[dict]:
    return service.list_backups(save_id)


@router.post("/restore-latest", response_model=RestoreResult)
def restore_latest(
    save_id: str,
    service: FinanceService = Depends(get_finance_service),
) -> dict:
    return service.restore_latest_backup(save_id)


@router.post("/restore", response_model=RestoreResult)
def restore_by_file(
    save_id: str,
    body: RestoreBackupIn,
    service: FinanceService = Depends(get_finance_service),
) -> dict:
    return service.restore_backup_file(save_id, body.path)
