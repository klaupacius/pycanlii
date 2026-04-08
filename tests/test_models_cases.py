import datetime
from pycanlii.models import (
    Language,
    CaseDatabase,
    CaseId,
    CaseSummary,
    CaseMetadata,
)


def test_language_enum() -> None:
    assert Language.EN.value == "en"
    assert Language.FR.value == "fr"


def test_case_database_from_dict() -> None:
    data = {"databaseId": "csc-scc", "jurisdiction": "ca", "name": "Supreme Court of Canada"}
    db = CaseDatabase.from_dict(data)
    assert db.database_id == "csc-scc"
    assert db.jurisdiction == "ca"
    assert db.name == "Supreme Court of Canada"


def test_case_id_from_dict() -> None:
    data = {"en": "2023scc1"}
    cid = CaseId.from_dict(data)
    assert cid.en == "2023scc1"


def test_case_summary_from_dict() -> None:
    data = {
        "databaseId": "csc-scc",
        "caseId": {"en": "2023scc1"},
        "title": "R. v. Smith",
        "citation": "2023 SCC 1",
    }
    case = CaseSummary.from_dict(data)
    assert case.database_id == "csc-scc"
    assert case.case_id.en == "2023scc1"
    assert case.title == "R. v. Smith"
    assert case.citation == "2023 SCC 1"


def test_case_metadata_from_dict() -> None:
    data = {
        "databaseId": "csc-scc",
        "caseId": "2023scc1",
        "url": "https://canlii.ca/t/abc",
        "title": "R. v. Smith",
        "citation": "2023 SCC 1",
        "language": "en",
        "docketNumber": "39345",
        "decisionDate": "2023-01-15",
        "keywords": "criminal law — evidence",
        "concatenatedId": "2023scc1",
    }
    meta = CaseMetadata.from_dict(data)
    assert meta.database_id == "csc-scc"
    assert meta.case_id == "2023scc1"
    assert meta.url == "https://canlii.ca/t/abc"
    assert meta.decision_date == datetime.date(2023, 1, 15)
    assert meta.keywords == "criminal law — evidence"


def test_case_metadata_optional_fields() -> None:
    data = {
        "databaseId": "csc-scc",
        "caseId": "2023scc1",
        "url": "https://canlii.ca/t/abc",
        "title": "R. v. Smith",
        "citation": "2023 SCC 1",
        "language": "en",
    }
    meta = CaseMetadata.from_dict(data)
    assert meta.docket_number is None
    assert meta.decision_date is None
    assert meta.keywords is None