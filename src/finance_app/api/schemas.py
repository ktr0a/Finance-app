from __future__ import annotations

from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class SaveInfo(BaseModel):
    save_id: str
    filename: str
    updated_at: Optional[str] = None
    tx_count: Optional[int] = None


class SaveCreate(BaseModel):
    name: str


class TransactionBase(BaseModel):
    name: str
    category: str
    type: Literal["I", "E"]
    amount: float
    date: str


class TransactionOut(TransactionBase):
    id: str


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    type: Optional[Literal["I", "E"]] = None
    amount: Optional[float] = None
    date: Optional[str] = None


class TransactionsPage(BaseModel):
    items: List[TransactionOut]
    total: int
    limit: int
    offset: int


class SummaryOut(BaseModel):
    income_total: float
    expense_total: float
    net_total: float
    currency: Optional[str] = None
    by_category: Optional[Dict[str, float]] = None
    by_type: Optional[Dict[str, float]] = None
    by_month: Optional[Dict[str, Dict[str, float]]] = None
    warnings: List[str] = Field(default_factory=list)


class HistoryOut(BaseModel):
    undo_available: bool
    redo_available: bool
    undo_depth: Optional[int] = None
    redo_depth: Optional[int] = None


class BackupInfo(BaseModel):
    filename: str
    path: str
    created_at: Optional[str] = None


class RestoreBackupIn(BaseModel):
    path: str


class RestoreResult(BaseModel):
    ok: bool
    message: str


class PdfPreviewItem(BaseModel):
    preview_id: str
    candidate: TransactionBase
    status: Dict[str, str]
    warnings: List[str] = Field(default_factory=list)


class PdfPreviewOut(BaseModel):
    items: List[PdfPreviewItem]
    parser: str
    warnings: List[str] = Field(default_factory=list)
    parser_requested: Optional[str] = None
    parser_used: Optional[str] = None
    parser_display: Optional[str] = None


class PdfParserInfo(BaseModel):
    id: str
    name: str


class PdfParsersOut(BaseModel):
    items: List[PdfParserInfo]


class PdfApplyOut(BaseModel):
    added: int
    skipped: int
    warnings: List[str] = Field(default_factory=list)


class PdfApplyRequest(BaseModel):
    accepted: List[TransactionCreate]
    source: Optional[str] = None
