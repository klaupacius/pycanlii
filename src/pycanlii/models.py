from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Language(Enum):
    EN = "en"
    FR = "fr"


@dataclass(frozen=True)
class CaseDatabase:
    database_id: str
    jurisdiction: str
    name: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CaseDatabase:
        return cls(
            database_id=data["databaseId"],
            jurisdiction=data["jurisdiction"],
            name=data["name"],
        )


@dataclass(frozen=True)
class CaseId:
    en: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CaseId:
        return cls(en=data["en"])


@dataclass(frozen=True)
class CaseSummary:
    database_id: str
    case_id: CaseId
    title: str
    citation: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CaseSummary:
        return cls(
            database_id=data["databaseId"],
            case_id=CaseId.from_dict(data["caseId"]),
            title=data["title"],
            citation=data["citation"],
        )


@dataclass(frozen=True)
class CaseMetadata:
    database_id: str
    case_id: str
    url: str
    title: str
    citation: str
    language: str
    docket_number: str | None = None
    decision_date: datetime.date | None = None
    keywords: str | None = None
    concatenated_id: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CaseMetadata:
        raw_date = data.get("decisionDate")
        return cls(
            database_id=data["databaseId"],
            case_id=data["caseId"],
            url=data["url"],
            title=data["title"],
            citation=data["citation"],
            language=data["language"],
            docket_number=data.get("docketNumber"),
            decision_date=datetime.date.fromisoformat(raw_date) if raw_date else None,
            keywords=data.get("keywords"),
            concatenated_id=data.get("concatenatedId"),
        )


class LegislationType(Enum):
    STATUTE = "STATUTE"
    REGULATION = "REGULATION"
    ANNUAL_STATUTE = "ANNUAL_STATUTE"


@dataclass(frozen=True)
class LegislationDatabase:
    database_id: str
    type: LegislationType
    jurisdiction: str
    name: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> LegislationDatabase:
        return cls(
            database_id=data["databaseId"],
            type=LegislationType(data["type"]),
            jurisdiction=data["jurisdiction"],
            name=data["name"],
        )


@dataclass(frozen=True)
class LegislationSummary:
    database_id: str
    legislation_id: str
    title: str
    citation: str
    type: LegislationType

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> LegislationSummary:
        return cls(
            database_id=data["databaseId"],
            legislation_id=data["legislationId"],
            title=data["title"],
            citation=data["citation"],
            type=LegislationType(data["type"]),
        )


@dataclass(frozen=True)
class ContentPart:
    part_id: str
    part_name: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ContentPart:
        return cls(
            part_id=data["partId"],
            part_name=data["partName"],
        )


@dataclass(frozen=True)
class LegislationMetadata:
    legislation_id: str
    url: str
    title: str
    citation: str
    type: LegislationType
    language: str
    date_scheme: str | None = None
    start_date: datetime.date | None = None
    end_date: datetime.date | None = None
    repealed: str | None = None
    content: list[ContentPart] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> LegislationMetadata:
        raw_start = data.get("startDate")
        raw_end = data.get("endDate")
        return cls(
            legislation_id=data["legislationId"],
            url=data["url"],
            title=data["title"],
            citation=data["citation"],
            type=LegislationType(data["type"]),
            language=data["language"],
            date_scheme=data.get("dateScheme"),
            start_date=datetime.date.fromisoformat(raw_start) if raw_start else None,
            end_date=datetime.date.fromisoformat(raw_end) if raw_end else None,
            repealed=data.get("repealed"),
            content=[ContentPart.from_dict(c) for c in data.get("content", [])],
        )
