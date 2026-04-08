def test_public_api_imports() -> None:
    from pycanlii import (
        CanLII,
        ApiError,
        CanLIIError,
    )

    # Verify key exports are the right types
    assert callable(CanLII)
    assert issubclass(ApiError, CanLIIError)


def test_all_is_defined() -> None:
    import pycanlii

    assert hasattr(pycanlii, "__all__")
    assert "CanLII" in pycanlii.__all__
    assert "Language" in pycanlii.__all__
