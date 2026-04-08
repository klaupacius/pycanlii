import httpx

from pycanlii.client import CanLII


def test_cited_cases() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert "/caseCitator/en/csc-scc/2023scc1/citedCases" in str(request.url)
        return httpx.Response(
            200,
            json={
                "citedCases": [
                    {
                        "databaseId": "csc-scc",
                        "caseId": {"en": "2020scc5"},
                        "title": "R. v. Jones",
                        "citation": "2020 SCC 5",
                    },
                ]
            },
        )

    c = CanLII(api_key="k", transport=httpx.MockTransport(handler))
    result = c.cited_cases("csc-scc", "2023scc1")
    assert len(result) == 1
    assert result[0].citation == "2020 SCC 5"


def test_citing_cases() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert "/caseCitator/en/csc-scc/2023scc1/citingCases" in str(request.url)
        return httpx.Response(
            200,
            json={
                "citingCases": [
                    {
                        "databaseId": "onca",
                        "caseId": {"en": "2024onca100"},
                        "title": "Doe v. Smith",
                        "citation": "2024 ONCA 100",
                    },
                ]
            },
        )

    c = CanLII(api_key="k", transport=httpx.MockTransport(handler))
    result = c.citing_cases("csc-scc", "2023scc1")
    assert len(result) == 1
    assert result[0].database_id == "onca"


def test_cited_legislations() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert "/caseCitator/en/csc-scc/2023scc1/citedLegislations" in str(request.url)
        return httpx.Response(
            200,
            json={
                "citedLegislations": [
                    {
                        "databaseId": "cas",
                        "legislationId": "rsc-1985-c-c-46",
                        "title": "Criminal Code",
                        "citation": "RSC 1985, c C-46",
                        "type": "STATUTE",
                    },
                ]
            },
        )

    c = CanLII(api_key="k", transport=httpx.MockTransport(handler))
    result = c.cited_legislations("csc-scc", "2023scc1")
    assert len(result) == 1
    assert result[0].legislation_id == "rsc-1985-c-c-46"
    assert result[0].title == "Criminal Code"
