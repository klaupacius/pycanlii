from __future__ import annotations

from typing import Any

import httpx

from pycanlii.exceptions import ApiError, PayloadTooLargeError

BASE_URL = "https://api.canlii.org/v1"


class CanLII:
    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = BASE_URL,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url
        self._client = httpx.Client(base_url=base_url, transport=transport)

    def _get(self, path: str, params: dict[str, str] | None = None) -> Any:
        all_params = {"api_key": self._api_key}
        if params:
            all_params.update(params)
        response = self._client.get(path, params=all_params)
        if response.status_code >= 400:
            raise ApiError(
                status_code=response.status_code,
                message=response.text,
            )
        data = response.json()
        if isinstance(data, dict) and data.get("error") == "TOO_LONG":
            raise PayloadTooLargeError(content_length=data["contentLength"])
        return data

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> CanLII:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()