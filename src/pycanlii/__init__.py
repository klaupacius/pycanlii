from pycanlii.client import CanLII
from pycanlii.exceptions import ApiError, CanLIIError, PayloadTooLargeError
from pycanlii.models import (
    CaseDatabase,
    CaseId,
    CaseMetadata,
    CaseSummary,
    ContentPart,
    Language,
    LegislationDatabase,
    LegislationMetadata,
    LegislationSummary,
    LegislationType,
)

__all__ = [
    "CanLII",
    "ApiError",
    "CanLIIError",
    "PayloadTooLargeError",
    "CaseDatabase",
    "CaseId",
    "CaseMetadata",
    "CaseSummary",
    "ContentPart",
    "Language",
    "LegislationDatabase",
    "LegislationMetadata",
    "LegislationSummary",
    "LegislationType",
]


def main() -> None:
    print("pycanlii — Python wrapper for the CanLII API")
