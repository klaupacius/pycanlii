from pycanlii.exceptions import CanLIIError, ApiError, PayloadTooLargeError


def test_canlii_error_is_base_exception() -> None:
    err = CanLIIError("something went wrong")
    assert isinstance(err, Exception)
    assert str(err) == "something went wrong"


def test_api_error_has_status_code() -> None:
    err = ApiError(status_code=404, message="Not Found")
    assert err.status_code == 404
    assert err.message == "Not Found"
    assert isinstance(err, CanLIIError)


def test_payload_too_large_error_has_content_length() -> None:
    err = PayloadTooLargeError(content_length=15_000_000)
    assert err.content_length == 15_000_000
    assert isinstance(err, CanLIIError)