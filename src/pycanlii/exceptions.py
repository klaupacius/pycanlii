class CanLIIError(Exception):
    pass


class ApiError(CanLIIError):
    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        self.message = message
        super().__init__(f"{status_code}: {message}")


class PayloadTooLargeError(CanLIIError):
    def __init__(self, content_length: int) -> None:
        self.content_length = content_length
        super().__init__(
            f"Payload too large ({content_length} bytes). "
            "Use RFC-7233 Range headers to download in chunks."
        )