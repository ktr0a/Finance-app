from __future__ import annotations

from fastapi import APIRouter, Depends, File, Form, UploadFile

from finance_app.api.deps import get_finance_service
from finance_app.api.schemas import PdfApplyOut, PdfApplyRequest, PdfParsersOut, PdfPreviewOut
from finance_app.api.services.finance_service import FinanceService

router = APIRouter(tags=["pdf"])


@router.get("/pdf/parsers", response_model=PdfParsersOut)
def list_parsers(
    service: FinanceService = Depends(get_finance_service),
) -> PdfParsersOut:
    data = service.list_pdf_parsers()
    return PdfParsersOut(**data)


@router.post("/pdf/preview", response_model=PdfPreviewOut)
def pdf_preview(
    file: UploadFile = File(...),
    parser: str = Form("auto"),
    year: str | None = Form(None),
    service: FinanceService = Depends(get_finance_service),
) -> PdfPreviewOut:
    payload = file.file.read()
    data = service.pdf_preview(payload, parser=parser, year=year)
    return PdfPreviewOut(**data)


@router.post("/saves/{save_id}/pdf/apply", response_model=PdfApplyOut)
def pdf_apply(
    save_id: str,
    body: PdfApplyRequest,
    service: FinanceService = Depends(get_finance_service),
) -> dict:
    accepted = [item.model_dump() if hasattr(item, "model_dump") else item.dict() for item in body.accepted]
    data = service.pdf_apply(save_id, accepted, source=body.source)
    return data
