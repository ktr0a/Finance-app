from __future__ import annotations

from typing import Any

import requests
import streamlit as st

from finance_ui.state import keys
from finance_ui.utils.http import ApiError


class ApiClient:
    def __init__(self) -> None:
        self._session = requests.Session()

    @property
    def base_url(self) -> str:
        url = st.session_state.get(keys.API_BASE_URL, "http://127.0.0.1:8000")
        return url.rstrip("/")

    def _handle(self, resp: requests.Response) -> Any:
        if 200 <= resp.status_code < 300:
            if resp.content:
                try:
                    return resp.json()
                except Exception:
                    return resp.text
            return None

        detail: Any = None
        try:
            detail = resp.json()
        except Exception:
            detail = resp.text

        raise ApiError(
            message="Backend request failed. Is FastAPI running?",
            status_code=resp.status_code,
            detail=detail,
        )

    def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        resp = self._session.get(f"{self.base_url}{path}", params=params, timeout=30)
        return self._handle(resp)

    def post(self, path: str, json: Any | None = None, files: Any | None = None, data: Any | None = None) -> Any:
        resp = self._session.post(f"{self.base_url}{path}", json=json, files=files, data=data, timeout=60)
        return self._handle(resp)

    def put(self, path: str, json: Any | None = None) -> Any:
        resp = self._session.put(f"{self.base_url}{path}", json=json, timeout=30)
        return self._handle(resp)

    def delete(self, path: str) -> Any:
        resp = self._session.delete(f"{self.base_url}{path}", timeout=30)
        return self._handle(resp)
