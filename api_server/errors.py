from __future__ import annotations

from fastapi import HTTPException


class SaveNotFoundError(Exception):
    pass


class TransactionNotFoundError(Exception):
    pass


class InvalidRequestError(Exception):
    pass


def http_exception_from_error(exc: Exception) -> HTTPException:
    if isinstance(exc, (SaveNotFoundError, TransactionNotFoundError)):
        return HTTPException(status_code=404, detail=str(exc) or "Not found")
    if isinstance(exc, InvalidRequestError):
        return HTTPException(status_code=400, detail=str(exc) or "Invalid request")
    return HTTPException(status_code=500, detail="Internal server error")
