from __future__ import annotations

import datetime
from typing import Any

import httpx

from pycanlii.exceptions import ApiError, PayloadTooLargeError
from pycanlii.models import (
    CaseDatabase,
    CaseMetadata,
    CaseSummary,
    Language,
    LegislationSummary,
)

BASE_URL = "https://api.canlii.org/v1"


class CanLII:
    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = BASE_URL,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url
        self._client = httpx.Client(base_url=base_url, transport=transport)

    def _get(self, path: str, params: dict[str, str] | None = None) -> Any:
        all_params = {"api_key": self._api_key}
        if params:
            all_params.update(params)
        response = self._client.get(path, params=all_params)
        if response.status_code >= 400:
            raise ApiError(
                status_code=response.status_code,
                message=response.text,
            )
        data = response.json()
        if isinstance(data, dict) and data.get("error") == "TOO_LONG":
            raise PayloadTooLargeError(content_length=data["contentLength"])
        return data

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> CanLII:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def case_databases(self, language: Language) -> list[CaseDatabase]:
        data = self._get(f"/caseBrowse/{language.value}/")
        return [CaseDatabase.from_dict(d) for d in data["caseDatabases"]]

    def cases(
        self,
        language: Language,
        database_id: str,
        *,
        offset: int,
        result_count: int,
        published_before: datetime.date | None = None,
        published_after: datetime.date | None = None,
        modified_before: datetime.date | None = None,
        modified_after: datetime.date | None = None,
        changed_before: datetime.date | None = None,
        changed_after: datetime.date | None = None,
        decision_date_before: datetime.date | None = None,
        decision_date_after: datetime.date | None = None,
    ) -> list[CaseSummary]:
        params: dict[str, str] = {
            "offset": str(offset),
            "resultCount": str(result_count),
        }
        date_filters = {
            "publishedBefore": published_before,
            "publishedAfter": published_after,
            "modifiedBefore": modified_before,
            "modifiedAfter": modified_after,
            "changedBefore": changed_before,
            "changedAfter": changed_after,
            "decisionDateBefore": decision_date_before,
            "decisionDateAfter": decision_date_after,
        }
        for key, value in date_filters.items():
            if value is not None:
                params[key] = value.isoformat()
        data = self._get(f"/caseBrowse/{language.value}/{database_id}/", params=params)
        return [CaseSummary.from_dict(d) for d in data["cases"]]

    def case(
        self,
        language: Language,
        database_id: str,
        case_id: str,
    ) -> CaseMetadata:
        data = self._get(f"/caseBrowse/{language.value}/{database_id}/{case_id}/")
        return CaseMetadata.from_dict(data)

    def cited_cases(self, database_id: str, case_id: str) -> list[CaseSummary]:
        data = self._get(f"/caseCitator/en/{database_id}/{case_id}/citedCases")
        return [CaseSummary.from_dict(d) for d in data["citedCases"]]

    def citing_cases(self, database_id: str, case_id: str) -> list[CaseSummary]:
        data = self._get(f"/caseCitator/en/{database_id}/{case_id}/citingCases")
        return [CaseSummary.from_dict(d) for d in data["citingCases"]]

    def cited_legislations(
        self, database_id: str, case_id: str
    ) -> list[LegislationSummary]:
        data = self._get(f"/caseCitator/en/{database_id}/{case_id}/citedLegislations")
        return [LegislationSummary.from_dict(d) for d in data["citedLegislations"]]
