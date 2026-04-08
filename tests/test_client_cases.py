import datetime

import httpx

from pycanlii.client import CanLII
from pycanlii.models import CaseMetadata, Language


def test_case_databases() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert "/caseBrowse/en/" in str(request.url)
        return httpx.Response(
            200,
            json={
                "caseDatabases": [
                    {
                        "databaseId": "csc-scc",
                        "jurisdiction": "ca",
                        "name": "Supreme Court of Canada",
                    },
                ]
            },
        )

    c = CanLII(api_key="k", transport=httpx.MockTransport(handler))
    result = c.case_databases(Language.EN)
    assert len(result) == 1
    assert result[0].database_id == "csc-scc"


def test_cases() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert "/caseBrowse/en/csc-scc/" in str(request.url)
        assert "offset=0" in str(request.url)
        assert "resultCount=10" in str(request.url)
        return httpx.Response(
            200,
            json={
                "cases": [
                    {
                        "databaseId": "csc-scc",
                        "caseId": {"en": "2023scc1"},
                        "title": "R. v. Smith",
                        "citation": "2023 SCC 1",
                    },
                ]
            },
        )

    c = CanLII(api_key="k", transport=httpx.MockTransport(handler))
    result = c.cases(Language.EN, "csc-scc", offset=0, result_count=10)
    assert len(result) == 1
    assert result[0].case_id.en == "2023scc1"


def test_cases_with_date_filters() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        assert "decisionDateAfter=2023-01-01" in url
        assert "decisionDateBefore=2023-12-31" in url
        return httpx.Response(200, json={"cases": []})

    c = CanLII(api_key="k", transport=httpx.MockTransport(handler))
    result = c.cases(
        Language.EN,
        "csc-scc",
        offset=0,
        result_count=10,
        decision_date_after=datetime.date(2023, 1, 1),
        decision_date_before=datetime.date(2023, 12, 31),
    )
    assert result == []


def test_case() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert "/caseBrowse/en/csc-scc/2023scc1/" in str(request.url)
        return httpx.Response(
            200,
            json={
                "databaseId": "csc-scc",
                "caseId": "2023scc1",
                "url": "https://canlii.ca/t/abc",
                "title": "R. v. Smith",
                "citation": "2023 SCC 1",
                "language": "en",
                "docketNumber": "39345",
                "decisionDate": "2023-01-15",
                "keywords": "criminal law",
                "concatenatedId": "2023scc1",
            },
        )

    c = CanLII(api_key="k", transport=httpx.MockTransport(handler))
    result = c.case(Language.EN, "csc-scc", "2023scc1")
    assert isinstance(result, CaseMetadata)
    assert result.decision_date == datetime.date(2023, 1, 15)
