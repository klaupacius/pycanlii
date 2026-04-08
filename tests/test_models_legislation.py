import datetime
from pycanlii.models import (
    LegislationType,
    LegislationDatabase,
    LegislationSummary,
    LegislationMetadata,
    ContentPart,
)


def test_legislation_type_enum() -> None:
    assert LegislationType.STATUTE.value == "STATUTE"
    assert LegislationType.REGULATION.value == "REGULATION"
    assert LegislationType.ANNUAL_STATUTE.value == "ANNUAL_STATUTE"


def test_legislation_database_from_dict() -> None:
    data = {
        "databaseId": "ons",
        "type": "STATUTE",
        "jurisdiction": "on",
        "name": "Ontario Statutes",
    }
    db = LegislationDatabase.from_dict(data)
    assert db.database_id == "ons"
    assert db.type == LegislationType.STATUTE
    assert db.jurisdiction == "on"
    assert db.name == "Ontario Statutes"


def test_legislation_summary_from_dict() -> None:
    data = {
        "databaseId": "ons",
        "legislationId": "rso-1990-c-h8",
        "title": "Highway Traffic Act",
        "citation": "RSO 1990, c H.8",
        "type": "STATUTE",
    }
    leg = LegislationSummary.from_dict(data)
    assert leg.database_id == "ons"
    assert leg.legislation_id == "rso-1990-c-h8"
    assert leg.title == "Highway Traffic Act"
    assert leg.citation == "RSO 1990, c H.8"
    assert leg.type == LegislationType.STATUTE


def test_content_part_from_dict() -> None:
    data = {"partId": "part-1", "partName": "Part I"}
    part = ContentPart.from_dict(data)
    assert part.part_id == "part-1"
    assert part.part_name == "Part I"


def test_legislation_metadata_from_dict() -> None:
    data = {
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
        "content": [
            {"partId": "part-1", "partName": "Part I"},
        ],
    }
    meta = LegislationMetadata.from_dict(data)
    assert meta.legislation_id == "rso-1990-c-h8"
    assert meta.url == "https://canlii.ca/t/xyz"
    assert meta.type == LegislationType.STATUTE
    assert meta.start_date == datetime.date(1990, 12, 31)
    assert meta.end_date == datetime.date(2024, 1, 1)
    assert meta.repealed == "NO"
    assert len(meta.content) == 1
    assert meta.content[0].part_id == "part-1"


def test_legislation_metadata_optional_fields() -> None:
    data = {
        "legislationId": "rso-1990-c-h8",
        "url": "https://canlii.ca/t/xyz",
        "title": "Highway Traffic Act",
        "citation": "RSO 1990, c H.8",
        "type": "STATUTE",
        "language": "en",
    }
    meta = LegislationMetadata.from_dict(data)
    assert meta.date_scheme is None
    assert meta.start_date is None
    assert meta.end_date is None
    assert meta.repealed is None
    assert meta.content == []