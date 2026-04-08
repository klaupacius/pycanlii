# pycanlii

Python wrapper for the [CanLII REST API](https://github.com/canlii/API_documentation/blob/master/EN.md). Provides typed access to Canadian legal information — case law, legislation, and citation data.

**NOTE:** Written with the assistance of AI.

## Requirements

Python 3.12+

## Installation

```bash
pip install pycanlii
```

Or with uv:

```bash
uv add pycanlii
```

## Quick Start

```python
from pycanlii import CanLII, Language

with CanLII(api_key="your-api-key") as client:
    # List all case law databases in English
    databases = client.case_databases(Language.EN)
    for db in databases[:3]:
        print(db.database_id, db.name)

    # Browse cases in the Supreme Court of Canada database
    cases = client.cases(Language.EN, "csc-scc", offset=0, result_count=10)
    for case in cases:
        print(case.citation, case.title)
```

## Authentication

All requests require a CanLII API key passed as `api_key` to the `CanLII` constructor. You can obtain a key from [CanLII](https://www.canlii.org/en/info/api.html).

## Usage

### Client

```python
from pycanlii import CanLII, Language

# As a context manager (recommended)
with CanLII(api_key="...") as client:
    ...

# Or manually
client = CanLII(api_key="...")
# ... use client ...
client.close()
```

### Case Law

#### List databases

```python
databases = client.case_databases(Language.EN)
# Returns: list[CaseDatabase]
# Each has: database_id, jurisdiction, name
```

#### Browse cases

```python
import datetime

cases = client.cases(
    Language.EN,
    "csc-scc",
    offset=0,
    result_count=10,
    # Optional date filters (datetime.date values):
    decision_date_after=datetime.date(2020, 1, 1),
    decision_date_before=datetime.date(2023, 12, 31),
    # Also available: published_after/before, modified_after/before, changed_after/before
)
# Returns: list[CaseSummary]
# Each has: database_id, case_id (CaseId), title, citation
```

#### Get case metadata

```python
case = client.case(Language.EN, "csc-scc", "2023scc1")
# Returns: CaseMetadata
# Has: database_id, case_id, url, title, citation, language,
#      decision_date, docket_number, keywords, concatenated_id
```

### Citator

```python
# Cases cited by a given case
cited = client.cited_cases("csc-scc", "2023scc1")
# Returns: list[CaseSummary]

# Cases that cite a given case
citing = client.citing_cases("csc-scc", "2023scc1")
# Returns: list[CaseSummary]

# Legislation cited by a given case
cited_leg = client.cited_legislations("csc-scc", "2023scc1")
# Returns: list[LegislationSummary]
```

### Legislation

#### List databases

```python
databases = client.legislation_databases(Language.EN)
# Returns: list[LegislationDatabase]
# Each has: database_id, type (LegislationType), jurisdiction, name
```

#### Browse legislation

```python
legislations = client.legislations(Language.EN, "can")
# Returns: list[LegislationSummary]
# Each has: database_id, legislation_id, title, citation, type (LegislationType)
```

#### Get legislation metadata

```python
leg = client.legislation(Language.EN, "can", "rsc-1985-c-c-46")
# Returns: LegislationMetadata
# Has: legislation_id, url, title, citation, type, language,
#      date_scheme, start_date, end_date, repealed, content (list[ContentPart])
```

## Models

All models are frozen dataclasses.

| Class | Fields |
|-------|--------|
| `CaseDatabase` | `database_id`, `jurisdiction`, `name` |
| `CaseSummary` | `database_id`, `case_id` (`CaseId`), `title`, `citation` |
| `CaseId` | `en` |
| `CaseMetadata` | `database_id`, `case_id`, `url`, `title`, `citation`, `language`, `decision_date`, `docket_number`, `keywords`, `concatenated_id` |
| `LegislationDatabase` | `database_id`, `type` (`LegislationType`), `jurisdiction`, `name` |
| `LegislationSummary` | `database_id`, `legislation_id`, `title`, `citation`, `type` |
| `LegislationMetadata` | `legislation_id`, `url`, `title`, `citation`, `type`, `language`, `date_scheme`, `start_date`, `end_date`, `repealed`, `content` |
| `ContentPart` | `part_id`, `part_name` |

### Enums

```python
from pycanlii import Language, LegislationType

Language.EN   # "en"
Language.FR   # "fr"

LegislationType.STATUTE
LegislationType.REGULATION
LegislationType.ANNUAL_STATUTE
```

## Error Handling

```python
from pycanlii import CanLII, Language, ApiError, PayloadTooLargeError, CanLIIError

with CanLII(api_key="...") as client:
    try:
        case = client.case(Language.EN, "csc-scc", "invalid-id")
    except ApiError as e:
        print(e.status_code, e.message)   # e.g. 404, "Not Found"
    except PayloadTooLargeError as e:
        print(e.content_length)           # bytes; use Range headers to chunk
    except CanLIIError:
        pass                              # base class for all pycanlii errors
```

## License

See [LICENSE.md](LICENSE.md).
