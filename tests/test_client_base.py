import httpx
import pytest

from pycanlii.client import CanLII
from pycanlii.exceptions import ApiError, PayloadTooLargeError


def test_client_injects_api_key(mock_transport: httpx.MockTransport, client: CanLII) -> None:
    # The mock_transport asserts api_key is present; this just verifies no error
    result = client._get("/caseBrowse/en/")
    assert result == {"ok": True}


def test_client_raises_api_error_on_http_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code=404, json={"message": "Not Found"})

    transport = httpx.MockTransport(handler)
    c = CanLII(api_key="test-key", transport=transport)
    with pytest.raises(ApiError) as exc_info:
        c._get("/caseBrowse/en/nonexistent/")
    assert exc_info.value.status_code == 404


def test_client_raises_payload_too_large_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status_code=200,
            json={
                "error": "TOO_LONG",
                "contentLength": 15_000_000,
                "message": "Content too large",
            },
        )

    transport = httpx.MockTransport(handler)
    c = CanLII(api_key="test-key", transport=transport)
    with pytest.raises(PayloadTooLargeError) as exc_info:
        c._get("/caseBrowse/en/some-db/some-case/")
    assert exc_info.value.content_length == 15_000_000