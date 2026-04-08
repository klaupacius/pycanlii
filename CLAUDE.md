# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

pycanlii — Python wrapper for the [CanLII REST API](https://github.com/canlii/API_documentation/blob/master/EN.md). Provides typed access to Canadian legal information including case law, legislation, and citation data.

- Python >=3.12, source layout: `src/pycanlii/`
- Entry point: `pycanlii:main` (registered as `pycanlii` CLI script)
- HTTP client: `httpx`

## Source Layout

```
src/pycanlii/
  __init__.py      # Public API exports + main() entry point
  client.py        # CanLII class — all API methods, httpx-backed
  models.py        # Frozen dataclasses: CaseDatabase, CaseSummary, CaseMetadata,
                   #   LegislationDatabase, LegislationSummary, LegislationMetadata,
                   #   CaseId, ContentPart, Language (enum), LegislationType (enum)
  exceptions.py    # CanLIIError (base), ApiError (status_code+message),
                   #   PayloadTooLargeError (content_length)
tests/
  conftest.py
  test_exceptions.py
  test_models_cases.py
  test_models_legislation.py
  test_client_base.py
  test_client_cases.py
  test_client_citator.py
  test_client_legislation.py
  test_package.py
```

## CanLII API Coverage

Base URL: `https://api.canlii.org/v1/`. All endpoints require HTTPS and an API key.

| Method | Endpoint |
|--------|----------|
| `case_databases(language)` | `GET /caseBrowse/{lang}/` |
| `cases(language, database_id, *, offset, result_count, **date_filters)` | `GET /caseBrowse/{lang}/{db}/` |
| `case(language, database_id, case_id)` | `GET /caseBrowse/{lang}/{db}/{id}/` |
| `cited_cases(database_id, case_id)` | `GET /caseCitator/en/{db}/{id}/citedCases` |
| `citing_cases(database_id, case_id)` | `GET /caseCitator/en/{db}/{id}/citingCases` |
| `cited_legislations(database_id, case_id)` | `GET /caseCitator/en/{db}/{id}/citedLegislations` |
| `legislation_databases(language)` | `GET /legislationBrowse/{lang}/` |
| `legislations(language, database_id)` | `GET /legislationBrowse/{lang}/{db}/` |
| `legislation(language, database_id, legislation_id)` | `GET /legislationBrowse/{lang}/{db}/{id}/` |

`Language.EN` / `Language.FR` are the two valid language values. Dates use ISO-8601. Max payload 10 MB; responses larger than that raise `PayloadTooLargeError`.

## Commands

All CLI commands must be prefixed with `rtk`.

```bash
rtk uv sync                      # Install/sync dependencies
rtk uv run pycanlii              # Run the CLI
rtk uv run pytest                # Run all tests
rtk uv run pytest -k "name"     # Run a single test by name
rtk ty check                     # Type check (must pass with zero errors)
rtk ruff check src/              # Lint
rtk ruff format src/             # Format
```

## Quality Gates (all must pass before commit)

- **Type checking**: `ty` — all code must be fully type-hinted and pass with no errors
- **Linting**: `ruff` — all errors must be fixed
- **Tests**: full test coverage for all functions
