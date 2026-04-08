from __future__ import annotations

import datetime
from dataclasses import dataclass
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