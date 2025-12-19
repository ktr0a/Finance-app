from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api_server.errors import InvalidRequestError, SaveNotFoundError, TransactionNotFoundError
from api_server.routers import health, history, import_pdf, saves, summary, transactions
from api_server.settings import CORS_ORIGINS, ENABLE_CORS

app = FastAPI(title="Finance App API", version="0.1.0")

if ENABLE_CORS and CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )


def _error_response(message: str, *, status_code: int, error_code: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"detail": message, "error_code": error_code},
    )


@app.exception_handler(SaveNotFoundError)
def handle_save_not_found(_request: Request, exc: SaveNotFoundError) -> JSONResponse:
    return _error_response(str(exc) or "Save not found", status_code=404, error_code="save_not_found")


@app.exception_handler(TransactionNotFoundError)
def handle_tx_not_found(_request: Request, exc: TransactionNotFoundError) -> JSONResponse:
    return _error_response(str(exc) or "Transaction not found", status_code=404, error_code="transaction_not_found")


@app.exception_handler(InvalidRequestError)
def handle_invalid_request(_request: Request, exc: InvalidRequestError) -> JSONResponse:
    return _error_response(str(exc) or "Invalid request", status_code=400, error_code="invalid_request")


app.include_router(health.router)
app.include_router(saves.router)
app.include_router(transactions.router)
app.include_router(summary.router)
app.include_router(history.router)
app.include_router(import_pdf.router)
