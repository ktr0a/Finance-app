from __future__ import annotations

import uvicorn

from finance_app.api.settings import API_PORT


def main() -> None:
    base_url = f"http://127.0.0.1:{API_PORT}"
    print(f"API running at {base_url}")
    print(f"Docs: {base_url}/docs")
    uvicorn.run("finance_app.api.app:app", host="127.0.0.1", port=API_PORT, reload=True)


if __name__ == "__main__":
    main()
