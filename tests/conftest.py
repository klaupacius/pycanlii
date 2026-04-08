from typing import Any

import httpx
import pytest

from pycanlii.client import CanLII


def make_response(data: Any, status_code: int = 200) -> httpx.Response:
    return httpx.Response(
        status_code=status_code,
        json=data,
    )


@pytest.fixture
def mock_transport() -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.scheme == "https"
        assert "api_key" in str(request.url)
        return make_response({"ok": True})

    return httpx.MockTransport(handler)


@pytest.fixture
def client(mock_transport: httpx.MockTransport) -> CanLII:
    return CanLII(api_key="test-key", transport=mock_transport)
