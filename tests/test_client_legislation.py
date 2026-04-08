import datetime

import httpx

from pycanlii.client import CanLII
from pycanlii.models import (
    Language,
    LegislationMetadata,
    LegislationType,
)


def test_legislation_databases() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert "/legislationBrowse/en/" in str(request.url)
        return httpx.Response(
            200,
            json={
                "legislationDatabases": [
                    {
                        "databaseId": "ons",
                        "type": "STATUTE",
                        "jurisdiction": "on",
                        "name": "Ontario Statutes",
                    },
                ]
            },
        )

    c = CanLII(api_key="k", transport=httpx.MockTransport(handler))
    result = c.legislation_databases(Language.EN)
    assert len(result) == 1
    assert result[0].type == LegislationType.STATUTE


def test_legislations() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert "/legislationBrowse/en/ons/" in str(request.url)
        return httpx.Response(
            200,
            json={
                "legislations": [
                    {
                        "databaseId": "ons",
                        "legislationId": "rso-1990-c-h8",
                        "title": "Highway Traffic Act",
                        "citation": "RSO 1990, c H.8",
                        "type": "STATUTE",
                    },
                ]
            },
        )

    c = CanLII(api_key="k", transport=httpx.MockTransport(handler))
    result = c.legislations(Language.EN, "ons")
    assert len(result) == 1
    assert result[0].legislation_id == "rso-1990-c-h8"


def test_legislation() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert "/legislationBrowse/en/ons/rso-1990-c-h8/" in str(request.url)
        return httpx.Response(
            200,
            json={
                "legislationId": "rso-1990-c-h8",
                "url": "https://canlii.ca/t/xyz",
                "title": "Highway Traffic Act",
                "citation": "RSO 1990, c H.8",
                "type": "STATUTE",
                "language": "en",
                "dateScheme": "ENTRY_INTO_FORCE",
                "startDate": "1990-12-31",
                "endDate": "2024-01-01",
                "repealed": "NO",
                "content": [{"partId": "p1", "partName": "Part I"}],
            },
        )

    c = CanLII(api_key="k", transport=httpx.MockTransport(handler))
    result = c.legislation(Language.EN, "ons", "rso-1990-c-h8")
    assert isinstance(result, LegislationMetadata)
    assert result.start_date == datetime.date(1990, 12, 31)
    assert result.repealed == "NO"
    assert len(result.content) == 1
