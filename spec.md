# Property Intel

> A terminal-native market intelligence workstation for New Zealand commercial-property research.

---

# 0. Mission

Build **Property Intel**, a polished keyboard-driven TUI application that converts messy commercial-property transaction data into reliable, searchable market intelligence.

The core workflow is:

```text
CSV / XLSX
     │
     ▼
Raw Observations
     │
     ▼
Cleaning & Normalisation
     │
     ▼
Validation
     │
     ▼
Entity Resolution
     │
     ▼
Canonical SQLite Database
     │
     ├──────────────┬───────────────┐
     ▼              ▼               ▼
 Transactions   Comparables     Data Quality
     │              │               │
     └──────────────┴───────────────┘
                    │
                    ▼
              Textual TUI
                    │
                    ▼
              Excel Reports
```

This is intentionally **not** a web application.

Do not build:

* a website,
* REST API,
* Docker setup,
* cloud infrastructure,
* authentication,
* microservices,
* AI chatbot,
* LLM features,
* complex ML valuation model.

The objective is to build a **small, exceptionally polished analytical tool**.

The final repository should be good enough to:

* feature prominently on a CV,
* show a commercial-property recruiter,
* demonstrate live during an interview,
* publish publicly on GitHub,
* and demonstrate strong data engineering, analytics and software-engineering ability.

---

# 1. Product Context

The application is designed around commercial-property research tasks such as:

* maintaining property databases,
* researching transactions,
* tracking sales,
* validating property information,
* identifying duplicate/inconsistent records,
* analysing market activity,
* finding comparable transactions,
* and producing Excel market intelligence.

Initial sectors:

1. Service Stations
2. Quick-Service Restaurants / Fast Food
3. Healthcare

Initial geography:

**New Zealand**

---

# 2. Product Philosophy

Prioritise:

```text
DATA QUALITY
     ↓
EXPLAINABILITY
     ↓
ANALYTICAL VALUE
     ↓
WORKFLOW SPEED
     ↓
VISUAL POLISH
```

The application should feel like a compact professional analyst workstation.

Think:

**Bloomberg-style keyboard workflow**

combined with:

**modern terminal UI**

combined with:

**commercial-property research**

Do not imitate Bloomberg visually.

Develop a distinct identity.

---

# 3. Scope

The entire application consists of approximately five primary experiences:

```text
1. Market Overview
2. Transactions
3. Properties
4. Data Quality / Entity Resolution
5. Import
```

Comparable sales live within the property workflow.

Excel export is available throughout the application where relevant.

That's it.

Do not expand the primary navigation.

---

# 4. Required Skills

Before implementation, inspect the available Codex skills.

Locate and read:

* `ponytail`
* `impeccable`
* `uncodixfy`, if available

Do not assume what these skills mean.

Read their actual instructions.

## Ponytail

`ponytail` is mandatory.

Apply the actual Ponytail workflow throughout implementation.

Do not merely run it once at the end.

Run relevant Ponytail checks/reviews after substantial product phases and again before completion.

## Impeccable

Apply `impeccable` to the TUI.

The fact that this is a terminal application is not an excuse for mediocre design.

Pay particular attention to:

* information hierarchy,
* spacing,
* borders,
* typography,
* table density,
* selected states,
* focus states,
* command discoverability,
* status messages,
* keyboard workflow,
* empty states,
* modal design,
* charts,
* number formatting,
* consistent visual language.

## Uncodixfy

If available, use `uncodixfy` to remove characteristic low-quality AI-generated code.

Prefer:

* direct implementations,
* precise domain names,
* small cohesive modules,
* minimal dependencies,
* obvious data flow,
* useful comments only.

Avoid:

* unnecessary factories,
* manager classes,
* service layers without purpose,
* generic helper dumping grounds,
* huge docstrings,
* comments restating code,
* premature abstraction,
* needless configuration,
* placeholder functionality,
* excessive defensive programming,
* dead code.

---

# 5. Technology Stack

Use Python.

Recommended stack:

```text
Python 3.12+
Textual
Rich
SQLite
SQLAlchemy
Alembic
pandas
NumPy
RapidFuzz
openpyxl
pytest
Ruff
mypy
```

Use another small dependency only where clearly justified.

Do not use:

```text
Docker
FastAPI
Django
Flask
React
Next.js
PostgreSQL
Redis
Celery
Kubernetes
Electron
```

unless this specification is explicitly changed.

---

# 6. Package Management

Use a modern Python project configuration.

Prefer:

```text
pyproject.toml
```

Support a straightforward development workflow such as:

```bash
uv sync
uv run property-intel
```

or equivalent.

If `uv` is selected, use it consistently.

The application should also expose a CLI entry point:

```bash
property-intel
```

---

# 7. Repository Structure

Keep the repository compact.

Use approximately:

```text
property-intel/
│
├── README.md
├── MASTER_SPEC.md
├── IMPLEMENTATION_PLAN.md
├── pyproject.toml
├── .gitignore
├── .env.example
│
├── src/
│   └── property_intel/
│       ├── app.py
│       ├── config.py
│       │
│       ├── db/
│       │   ├── models.py
│       │   ├── session.py
│       │   └── migrations/
│       │
│       ├── ingestion/
│       │   ├── importer.py
│       │   ├── mapping.py
│       │   └── parsers.py
│       │
│       ├── matching/
│       │   ├── normalise.py
│       │   ├── scoring.py
│       │   └── resolution.py
│       │
│       ├── analytics/
│       │   ├── market.py
│       │   └── comparables.py
│       │
│       ├── reporting/
│       │   └── excel.py
│       │
│       └── ui/
│           ├── screens/
│           ├── widgets/
│           └── styles/
│
├── tests/
│
├── data/
│   ├── demo/
│   └── exports/
│
└── docs/
    ├── architecture.md
    ├── methodology.md
    ├── entity-resolution.md
    └── screenshots/
```

Do not create dozens of tiny modules simply to appear architecturally sophisticated.

---

# 8. Database

Use SQLite.

The application should automatically initialise its local database when necessary.

Default:

```text
data/property_intel.db
```

Allow configuration of the database location.

SQLite is intentional.

The project does not need distributed infrastructure.

---

# 9. Core Data Model

Keep the model small.

There should be approximately five main tables.

---

# 10. Property

```text
Property
--------
id
canonical_address
street_address
suburb
city
region
postcode
latitude
longitude
sector
land_area_m2
building_area_m2
owner_name
tenant_name
created_at
updated_at
```

Sector enum:

```text
SERVICE_STATION
QSR
HEALTHCARE
OTHER
```

---

# 11. Transaction

```text
Transaction
-----------
id
property_id
transaction_date
sale_price
buyer_name
seller_name
reported_yield
land_area_m2
building_area_m2
source_id
created_at
```

Derived metrics:

```text
price_per_land_m2
price_per_building_m2
```

Prefer calculating these rather than unnecessarily persisting them.

---

# 12. Source

```text
Source
------
id
name
source_type
reference
retrieved_at
```

Keep provenance simple.

Every transaction should reference its source where available.

---

# 13. Raw Observation

Never import messy data directly into canonical property records.

Use:

```text
RawObservation
--------------
id
import_job_id
raw_address
raw_owner
raw_tenant
raw_sale_price
raw_sale_date
raw_land_area
raw_building_area
raw_payload_json
status
created_at
```

This distinction is central to the project:

```text
RAW OBSERVATION ≠ CANONICAL PROPERTY
```

---

# 14. Import Job

```text
ImportJob
---------
id
filename
started_at
completed_at
records_received
records_imported
records_rejected
records_flagged
status
```

Do not build a larger audit system.

---

# 15. Demo Dataset

Create a deterministic synthetic dataset containing approximately:

```text
300–500 canonical properties
500–700 transactions
600–900 raw observations
```

Cover:

* Auckland
* Wellington
* Canterbury
* Waikato
* Bay of Plenty
* other NZ regions

and:

* service stations,
* QSR,
* healthcare.

---

# 16. Deliberately Messy Data

The demo data must actually exercise the pipeline.

Include:

### Address variants

```text
123 Queen Street, Auckland CBD
123 QUEEN ST AUCKLAND
123 Queen St, Auckland
```

### Company variants

```text
Example Holdings Limited
EXAMPLE HOLDINGS LTD
Example Holdings Ltd.
```

### Currency variants

```text
$4.2m
4,200,000
$4200000
4.2 million
```

### Area variants

```text
1,250 sqm
1250 m2
0.125 ha
```

### Date variants

```text
14/03/2026
2026-03-14
14 Mar 2026
```

Also include:

* missing fields,
* suspicious yields,
* invalid prices,
* repeated properties,
* similar but distinct addresses,
* conflicting observations.

Use a fixed random seed.

---

# 17. Synthetic Data Disclosure

The TUI must visibly indicate:

```text
DEMO DATA — SYNTHETIC
```

when using bundled demonstration data.

The README must clearly state that the data does not represent actual NZ market statistics.

---

# 18. Ingestion

Support:

```text
CSV
XLSX
```

No additional formats are required.

---

# 19. Import Workflow

The TUI should support:

```text
SELECT FILE
     ↓
MAP COLUMNS
     ↓
PREVIEW
     ↓
NORMALISE
     ↓
VALIDATE
     ↓
DUPLICATE CHECK
     ↓
IMPORT
```

Do not overcomplicate the workflow.

---

# 20. Column Mapping

Allow the user to map incoming columns.

Example:

```text
INPUT COLUMN                    PROPERTY INTEL FIELD

Property Address               address
Settlement Date                transaction_date
Sale Amount                    sale_price
Site Area                      land_area
Purchaser                      buyer
Vendor                         seller
```

Where obvious, automatically suggest mappings.

User must be able to correct them.

---

# 21. Normalisation

Build deterministic normalisers.

This is one of the strongest parts of the project.

---

# 22. Address Normalisation

Handle:

```text
Street → St
Road → Rd
Avenue → Ave
Mount → Mt
Highway → Hwy
```

Normalise:

* case,
* whitespace,
* punctuation,
* postcodes,
* common abbreviations.

Preserve original values.

Do not aggressively transform addresses in ways that increase false matches.

---

# 23. Company Normalisation

Normalise common suffix differences:

```text
Limited
Ltd
Ltd.
```

and:

* whitespace,
* punctuation,
* case.

Preserve original names.

---

# 24. Currency Parsing

Support:

```text
$4.2m
$4,200,000
4200000
4.2 million
850k
$850k
```

Convert to numeric NZD values.

Test edge cases.

---

# 25. Area Parsing

Support:

```text
1,250 sqm
1,250 m²
1250 m2
0.125 ha
```

Convert internally to square metres.

---

# 26. Date Parsing

Support common NZ date formats.

If genuinely ambiguous:

```text
03/04/2026
```

do not silently invent an interpretation unless the import format explicitly establishes one.

Flag ambiguous values for review.

---

# 27. Validation

Implement deterministic rules.

Errors:

```text
sale_price <= 0
land_area <= 0
building_area <= 0
future transaction date
invalid date
```

Warnings:

```text
yield > 20%
very high sale price
very low sale price
extreme $/m²
building area substantially greater than land area
missing owner
missing tenant
```

Do not treat missing optional information as an error.

---

# 28. Validation Results

Represent:

```text
severity
field
rule
message
```

The TUI should explain problems in human-readable language.

Bad:

```text
ERR_VALIDATION_003
```

Good:

```text
Reported yield of 24.8% is unusually high and should be reviewed.
```

---

# 29. Entity Resolution

Entity resolution is the technical centrepiece.

The system must identify raw observations that probably correspond to an existing canonical property.

---

# 30. Matching Signals

Use:

```text
normalized address similarity
street number
postcode
city/suburb
land area similarity
building area similarity
tenant similarity
coordinates if available
```

Do not require every signal.

---

# 31. Explainable Match Score

Implement an interpretable score.

For example:

$$
S(i,j)
=
w_aS_a+
w_gS_g+
w_lS_l+
w_bS_b+
w_tS_t
$$

where:

```text
Sa = address similarity
Sg = geographic similarity
Sl = land-area similarity
Sb = building-area similarity
St = tenant similarity
```

Weights should live in one obvious configuration location.

---

# 32. Match Thresholds

Start approximately with:

```text
S >= 0.93
    automatic match

0.75 <= S < 0.93
    manual review

S < 0.75
    distinct property
```

Tune using labelled examples.

---

# 33. Protect Against False Merges

False merges are worse than false splits.

Explicitly test cases such as:

```text
12 Queen St
123 Queen St
```

and:

```text
Unit 1, 40 Example Rd
Unit 2, 40 Example Rd
```

Do not merge merely because strings are similar.

---

# 34. Evaluation

Create a small labelled duplicate dataset.

Report:

```text
Precision
Recall
F1
False Merge Rate
```

Document methodology.

Do not claim statistical significance from a tiny test set.

---

# 35. TUI Design

Use Textual.

The TUI is a first-class product surface.

Do not treat it as a collection of `print()` statements.

The application should work well at approximately:

```text
120 × 35
```

and scale reasonably beyond that.

---

# 36. Application Shell

Persistent header:

```text
PROPERTY INTEL                  NZ COMMERCIAL PROPERTY INTELLIGENCE
```

Include current dataset/reporting period where useful.

Persistent footer:

```text
[1] Overview  [2] Transactions  [3] Properties  [4] Quality  [5] Import
[/] Search    [E] Export                                      [Q] Quit
```

Exact shortcuts can change if Ponytail or Textual conventions suggest better ones.

Keep shortcuts consistent.

---

# 37. Screen 1 — Market Overview

Create a polished overview.

Example:

```text
┌─ MARKET OVERVIEW ──────────────────────────────────────────────────┐
│                                                                   │
│  Properties      487        Transaction Value       $1.42b        │
│  Transactions    693        Median Sale Price       $3.84m        │
│  Median Yield   5.71%       Records to Review          18         │
│                                                                   │
├─ TRANSACTION ACTIVITY ─────────────────────────────────────────────┤
│                                                                   │
│  60 ┤                                             ╭──╮            │
│  45 ┤                           ╭────╮      ╭─────╯  ╰╮           │
│  30 ┤             ╭────╮  ╭────╯    ╰──────╯         ╰─          │
│  15 ┤      ╭──────╯    ╰──╯                                     │
│     └────────────────────────────────────────────────             │
│       2022      2023      2024      2025      2026                │
│                                                                   │
├─ SECTOR ACTIVITY ──────────────────────────────────────────────────┤
│                                                                   │
│  Service Stations    38%                                          │
│  QSR                 34%                                          │
│  Healthcare          28%                                          │
│                                                                   │
├─ RECENT TRANSACTIONS ──────────────────────────────────────────────┤
│ DATE       PROPERTY                  SECTOR       PRICE    YIELD   │
│ ...                                                               │
└───────────────────────────────────────────────────────────────────┘
```

Use actual Textual/Rich components rather than hardcoded ASCII if that produces better behaviour.

---

# 38. Overview Metrics

Show:

```text
Properties
Transactions
Tracked Transaction Value
Median Sale Price
Median Yield
Records Requiring Review
```

Always show relevant sample sizes for yield where useful.

---

# 39. Market Chart

Keep charting intentionally modest.

One good terminal-native transaction activity chart is enough.

Do not spend days building terminal visualization infrastructure.

If a chart does not look excellent, replace it with a compact trend table or sparkline.

---

# 40. Screen 2 — Transactions

Build an excellent searchable table.

Columns:

```text
Date
Address
Region
Sector
Sale Price
Yield
$/Land m²
Buyer
Seller
```

Allow horizontal detail views if terminal width is constrained.

---

# 41. Transaction Controls

Support:

```text
/
    search

f
    filters

Enter
    inspect

s
    sort

e
    export

Esc
    clear/back
```

Exact shortcuts may be adjusted for consistency.

---

# 42. Transaction Filters

Support:

```text
Sector
Region
Date range
Sale price range
Yield range
```

Do not build a complex query language.

---

# 43. Transaction Detail

Selecting a transaction should show a modal or side panel containing:

```text
Address
Date
Sale Price
Yield
Land Area
Building Area
$/Land m²
$/Building m²
Buyer
Seller
Source
```

---

# 44. Screen 3 — Properties

Display:

```text
Address
Region
Sector
Owner
Tenant
Land Area
Last Sale
Last Sale Price
```

Support:

* search,
* sorting,
* filtering.

---

# 45. Property Detail

Selecting a property opens the primary research view.

Example:

```text
╭─ 42 GREAT SOUTH ROAD, AUCKLAND ───────────────────────────────────╮
│                                                                  │
│ SERVICE STATION                                                  │
│                                                                  │
│ Owner          Example Property Holdings Ltd                     │
│ Tenant         BP                                                │
│ Land           2,140 m²                                          │
│ Building         318 m²                                          │
│                                                                  │
├─ TRANSACTION HISTORY ─────────────────────────────────────────────┤
│                                                                  │
│ DATE          PRICE           YIELD           $/LAND m²           │
│ 14 Mar 2026   $5.20m          5.40%              $2,430           │
│ 08 Nov 2019   $3.85m          6.10%              $1,799           │
│                                                                  │
├─ COMPARABLE SALES ────────────────────────────────────────────────┤
│                                                                  │
│ PROPERTY                  DIST     PRICE     YIELD      MATCH      │
│ 18 Example Rd             1.4km    $4.9m     5.6%        94%      │
│ 72 Example St             2.8km    $5.4m     5.2%        91%      │
│ 91 Example Ave            4.1km    $4.7m     5.8%        87%      │
│                                                                  │
│ [C] Comparables     [S] Source     [E] Export     [Esc] Back      │
╰──────────────────────────────────────────────────────────────────╯
```

---

# 46. Comparable Sales

This is the second major analytical feature.

Given a property, rank historical transactions using:

```text
sector
geographic proximity
land-area similarity
building-area similarity
transaction recency
```

---

# 47. Comparable Distance

Use an interpretable distance:

$$
D(i,j)
=
w_gD_g+
w_lD_l+
w_bD_b+
w_tD_t+
w_sD_s
$$

where:

```text
Dg = geographic distance
Dl = land-area difference
Db = building-area difference
Dt = transaction recency
Ds = sector mismatch
```

Normalize terms appropriately.

Document the calculation.

---

# 48. Comparable Output

Default:

```text
Top 5
```

Show:

```text
Address
Distance
Sale Date
Sale Price
Land Area
Building Area
Yield
Similarity
```

---

# 49. Comparable Explanation

Selecting a comparable should explain the match.

Example:

```text
╭─ WHY THIS PROPERTY? ──────────────────────────────────────────────╮
│                                                                  │
│  Match score                                          94%         │
│                                                                  │
│  Sector                     Same                     ✓            │
│  Distance                   1.4 km                   ✓            │
│  Land area difference       4.8%                     ✓            │
│  Building area difference   7.1%                     ✓            │
│  Transaction age            6 months                 ✓            │
│                                                                  │
╰──────────────────────────────────────────────────────────────────╯
```

Do not provide unexplained scores.

---

# 50. Screen 4 — Data Quality

Create:

```text
╭─ DATA QUALITY ────────────────────────────────────────────────────╮
│                                                                  │
│ Potential Duplicates       8       Missing Owner          14      │
│ Validation Warnings       12       Missing Tenant         21      │
│ Suspicious Transactions    4       Import Errors           2      │
│                                                                  │
├─ REVIEW QUEUE ────────────────────────────────────────────────────┤
│                                                                  │
│ TYPE          PROPERTY               ISSUE                        │
│ Duplicate     123 Queen St           96% duplicate candidate      │
│ Validation    42 Example Rd          Yield 24.7%                  │
│ Missing       8 High St              Owner unavailable            │
│ Suspicious    17 Example Ave         Unusual $/m²                 │
│                                                                  │
╰──────────────────────────────────────────────────────────────────╯
```

---

# 51. Duplicate Review

This should be one of the most polished interactions in the application.

Example:

```text
╭─ POTENTIAL DUPLICATE ─────────────────────────────────────────────╮
│                                                                  │
│ SOURCE OBSERVATION             EXISTING PROPERTY                  │
│                                                                  │
│ 123 Queen Street              123 Queen St                        │
│ Auckland CBD                  Auckland CBD                        │
│ Service Station              Service Station                     │
│ 1,247 m²                     1,250 m²                            │
│ BP                            BP                                  │
│                                                                  │
├─ MATCH EVIDENCE ──────────────────────────────────────────────────┤
│                                                                  │
│ Address             ███████████████████░       98%                │
│ Land Area           ███████████████████░       99%                │
│ Tenant              ████████████████████      100%                │
│                                                                  │
│ Overall                                     96% HIGH              │
│                                                                  │
│               [M] Merge        [S] Separate                       │
╰──────────────────────────────────────────────────────────────────╯
```

Actions must actually modify the underlying data/review state.

---

# 52. Screen 5 — Import

The import screen should support:

```text
Choose File
    ↓
Map Columns
    ↓
Preview 10 rows
    ↓
Validate
    ↓
Import Summary
```

Use modal steps or a focused screen.

Do not build a complicated wizard framework.

---

# 53. Import Summary

After import show:

```text
IMPORT COMPLETE

Rows received                  247
Imported                       221
Matched existing properties     14
Requires review                  8
Rejected                         4

[View Review Queue]       [Done]
```

---

# 54. Global Search

`/` should open search.

Search:

```text
address
owner
tenant
buyer
seller
```

Results should be grouped.

Example:

```text
PROPERTIES

42 Great South Rd
18 Queen St

OWNERS

Example Property Holdings Ltd

TENANTS

BP
```

Keyboard navigation should be excellent.

---

# 55. Market Analytics

Implement only useful metrics:

```text
transaction count
tracked transaction value
median sale price
median yield
median $/land m²
median $/building m²
```

Support grouping by:

```text
quarter
sector
region
```

Do not add predictive modelling.

---

# 56. Statistical Integrity

Follow:

1. Missing data is NULL, not zero.
2. Synthetic data is clearly identified.
3. Medians are preferred for heavily skewed metrics.
4. Yield statistics expose sample size where useful.
5. Do not invent missing values.
6. Do not claim dataset coverage represents the whole NZ market.
7. Derived values are distinguishable from source values.
8. Suspicious values are flagged, not automatically declared wrong.

---

# 57. Excel Export

Excel is a flagship output.

Use `openpyxl`.

Generate:

```text
data/exports/NZ_Commercial_Property_Market_Report.xlsx
```

Allow the destination to be overridden.

---

# 58. Workbook

Keep it to five excellent sheets:

```text
01 Executive Summary
02 Transactions
03 Comparable Sales
04 Sector Analysis
05 Data Quality
```

---

# 59. Executive Summary

Include:

```text
Reporting Period
Properties Tracked
Transactions
Tracked Transaction Value
Median Sale Price
Median Yield
Records Requiring Review
```

Add useful charts.

Do not overcrowd the sheet.

---

# 60. Transactions

Create a proper Excel table containing:

```text
Date
Address
City
Region
Sector
Sale Price
Land Area
Building Area
$/Land m²
$/Building m²
Yield
Buyer
Seller
Source
```

Include:

* autofilter,
* frozen header,
* sensible widths,
* currency formatting,
* percentage formatting,
* date formatting.

---

# 61. Comparable Sales

When exporting from a selected property, include:

```text
SUBJECT PROPERTY

Address
Sector
Land Area
Building Area

COMPARABLES

Rank
Address
Distance
Sale Date
Sale Price
Land Area
Building Area
Yield
Similarity
Why Matched
```

---

# 62. Sector Analysis

Include:

```text
Sector
Properties
Transactions
Transaction Value
Median Sale Price
Median Yield
Median $/Land m²
```

Add one or two useful charts.

---

# 63. Data Quality

Include:

```text
Potential duplicates
Validation warnings
Missing owner
Missing tenant
Suspicious transactions
Import errors
```

Use tasteful conditional formatting.

---

# 64. Excel Standard

The workbook must look professionally prepared.

Verify:

```text
column widths
row heights
freeze panes
filters
tables
chart titles
number formats
currency
percentages
dates
alignment
conditional formatting
print readability
```

Do not produce a pandas dump with colours added.

---

# 65. Keyboard-First UX

The application should be genuinely efficient without a mouse.

Important actions should have keyboard shortcuts.

Examples:

```text
1–5        Navigation
/          Search
f          Filter
Enter      Open/select
Esc        Back/close
e          Export
r          Review
?          Help
q          Quit
```

Avoid shortcut collisions.

Show relevant shortcuts in the footer.

---

# 66. Command Palette

If Textual makes this straightforward, add:

```text
Ctrl+P
```

or an appropriate shortcut for a command palette.

Commands could include:

```text
Go to Overview
Search Properties
Import File
Review Duplicates
Export Market Report
Open Help
```

This is optional but valuable if implemented cleanly.

---

# 67. Help

`?` should display a polished shortcut/help overlay.

Do not require the README to understand basic navigation.

---

# 68. TUI Aesthetic

Use Ponytail and Impeccable heavily.

The interface should be:

```text
restrained
dense
fast
precise
premium
consistent
```

Avoid rainbow terminal styling.

Use a restrained palette.

Use colour semantically:

* selection,
* warning,
* error,
* success,
* muted metadata.

The application should still be understandable in reduced-colour environments where practical.

---

# 69. Borders

Use borders intentionally.

Do not put every piece of information in its own bordered box.

Use grouping, whitespace and alignment.

---

# 70. Financial Numbers

Format consistently.

Examples:

```text
$1.42b
$5.20m
$850k
5.40%
1,240 m²
$2,430/m²
```

Use tabular alignment where possible.

---

# 71. Empty States

Examples:

```text
No transactions match the current filters.

No duplicate candidates require review.

No comparable transactions satisfy the current criteria.

No import has been run in this session.
```

Do not show blank panels.

---

# 72. Error States

Errors should be actionable.

Example:

```text
Could not read "transactions.xlsx".

The workbook does not contain a readable worksheet.

[Choose Another File]
```

Avoid stack traces in normal UI.

Log technical details separately where useful.

---

# 73. Performance

For the bundled dataset, target:

```text
startup                         < 2 seconds
property search                 effectively instant
filtering                       effectively instant
property detail                 effectively instant
comparable ranking              < 500 ms
Excel report                    < 5 seconds
```

These are targets, not reasons to introduce unnecessary complexity.

---

# 74. Tests

Testing is mandatory.

---

# 75. Parsing Tests

Test:

```text
currency
area
dates
addresses
company names
missing values
```

Include ugly inputs.

---

# 76. Validation Tests

Test:

```text
negative price
zero price
future transaction
invalid yield
extreme yield
invalid area
missing optional fields
```

---

# 77. Entity Resolution Tests

Test:

```text
123 Queen Street
123 Queen St
→ MATCH
```

and:

```text
12 Queen Street
123 Queen Street
→ DO NOT MATCH
```

and:

```text
Unit 1, 40 Example Rd
Unit 2, 40 Example Rd
→ DO NOT AUTOMATICALLY MATCH
```

Also test missing fields.

---

# 78. Comparable Tests

Test:

```text
geographic distance
area differences
recency
sector penalty
ranking
similarity conversion
explanation generation
```

---

# 79. Analytics Tests

Test:

```text
transaction count
transaction value
median sale price
median yield
$/m²
quarter aggregation
sector aggregation
```

---

# 80. Excel Tests

Verify:

```text
file created
expected sheets
headers
row counts
number formats
tables
frozen panes
```

Do not attempt to test every visual characteristic programmatically.

Manually inspect the workbook during final QA.

---

# 81. End-to-End Test

Test the central workflow:

```text
CSV
 ↓
READ
 ↓
NORMALISE
 ↓
VALIDATE
 ↓
ENTITY RESOLUTION
 ↓
SQLITE
 ↓
PROPERTY QUERY
 ↓
COMPARABLES
 ↓
EXCEL
```

This is more important than achieving an arbitrary coverage percentage.

---

# 82. No Docker

Explicit requirement:

**DO NOT ADD DOCKER.**

The local setup should be simpler than Docker.

Target:

```bash
git clone <repo>
cd property-intel
uv sync
uv run property-intel
```

Seed/demo setup should be automatic or one obvious command.

For example:

```bash
uv run property-intel --demo
```

---

# 83. CLI

Support useful commands such as:

```bash
property-intel
property-intel --demo
property-intel import transactions.xlsx
property-intel export
```

Do not turn this into a giant CLI framework.

The TUI remains the primary interface.

---

# 84. Implementation Phases

Build sequentially.

---

## Phase 1 — Foundation

Implement:

```text
pyproject
package structure
Textual app
SQLite connection
SQLAlchemy
Alembic
Ruff
mypy
pytest
CLI entry point
```

Create a minimal functioning TUI shell.

Run tests.

Run Ponytail/Uncodixfy checks where relevant.

COMMIT.

PUSH if GitHub is configured.

---

## Phase 2 — Data Model + Demo Data

Implement:

```text
Property
Transaction
Source
RawObservation
ImportJob
```

Create deterministic synthetic generator.

Seed database.

Verify realistic messy observations.

COMMIT.

PUSH.

---

## Phase 3 — Cleaning + Validation

Implement:

```text
address normalization
company normalization
currency parser
area parser
date parser
validation rules
```

Add comprehensive tests.

COMMIT.

PUSH.

---

## Phase 4 — Entity Resolution

Implement:

```text
candidate generation
matching signals
scoring
thresholds
review states
labelled evaluation dataset
metrics
```

Test false merges carefully.

Document methodology.

COMMIT.

PUSH.

---

## Phase 5 — Core TUI

Build:

```text
application shell
Overview
Transactions
Properties
Property Detail
global search
keyboard navigation
help
```

Apply Ponytail.

Apply Impeccable.

Actually run the application and inspect it visually.

COMMIT.

PUSH.

---

## Phase 6 — Comparable Sales

Implement:

```text
distance function
ranking
top-five results
match explanations
property integration
```

Test methodology.

COMMIT.

PUSH.

---

## Phase 7 — Data Quality

Implement:

```text
quality summary
review queue
duplicate review
merge/separate
validation review
```

Make duplicate review exceptional.

COMMIT.

PUSH.

---

## Phase 8 — Import

Implement:

```text
CSV
XLSX
column mapping
preview
validation
duplicate checking
import summary
```

Test the complete workflow.

COMMIT.

PUSH.

---

## Phase 9 — Excel

Implement the five-sheet workbook.

Manually inspect the generated file.

Improve until it genuinely looks professional.

COMMIT.

PUSH.

---

## Phase 10 — Product Polish

STOP ADDING FEATURES.

Run:

```text
Ponytail review
Impeccable review
Uncodixfy review
keyboard UX review
error-state review
empty-state review
performance review
```

Inspect every screen in the running TUI.

Fix inconsistencies.

COMMIT.

PUSH.

---

## Phase 11 — README + Screenshots

Do not treat this as optional documentation work.

This is part of the portfolio deliverable.

Capture screenshots.

Create diagrams.

Write final README.

COMMIT.

PUSH.

---

## Phase 12 — Final Verification

From a clean environment:

```bash
uv sync
uv run pytest
uv run ruff check .
uv run mypy src
uv run property-intel --demo
```

Also verify:

```text
search
filters
property navigation
comparables
duplicate review
CSV import
XLSX import
Excel export
```

Fix all material issues.

Final commit.

Final push.

---

# 85. Git Discipline

Git/GitHub history is part of the project.

Commit regularly.

Do not create one giant commit at the end.

Before every commit:

```bash
git status
git diff
```

Then:

1. inspect changes,
2. remove accidental files,
3. ensure no credentials exist,
4. run relevant tests,
5. commit one coherent unit of work.

---

# 86. Commit Style

Use clear commits such as:

```text
chore: initialise property intel TUI

feat: add commercial property data model

feat: generate synthetic transaction dataset

feat: add property data normalisation

feat: implement property entity resolution

feat: build market overview

feat: add transaction and property explorers

feat: implement comparable sales ranking

feat: add data quality review workflow

feat: support CSV and Excel imports

feat: generate Excel market intelligence report

style: polish terminal interface

refactor: simplify property matching pipeline

test: add end-to-end import workflow

docs: document entity resolution methodology

docs: complete portfolio README
```

Avoid meaningless commits such as:

```text
updates
fix stuff
changes
final
final2
```

---

# 87. GitHub Pushes

If a GitHub remote exists and authentication is available:

**push regularly after stable milestones.**

Do not wait until the entire project is complete.

Suggested:

```text
Phase 1 → commit + push
Phase 2 → commit + push
Phase 3 → commit + push
...
```

Never force-push unless explicitly instructed.

Never overwrite unrelated work.

Never claim a push succeeded without verifying it.

---

# 88. .gitignore

At minimum exclude:

```text
.venv/
__pycache__/
*.pyc
.env
.mypy_cache/
.pytest_cache/
.ruff_cache/
.DS_Store
data/property_intel.db
```

Decide deliberately whether generated exports belong in Git.

Usually exclude routine exports while optionally retaining one polished example report if useful for the portfolio.

---

# 89. IMPLEMENTATION_PLAN.md

Before substantial implementation, create:

```text
IMPLEMENTATION_PLAN.md
```

Translate this specification into checkboxes.

Example:

```text
## Phase 4 — Entity Resolution

- [x] address similarity
- [x] land-area similarity
- [x] tenant similarity
- [ ] geographic similarity
- [ ] candidate generation
- [ ] review thresholds
- [ ] evaluation dataset
- [ ] precision/recall report
```

Keep it accurate.

Never mark incomplete work complete.

---

# 90. Quality Gate After Every Phase

Before committing a phase, ask:

### Functional

Does it actually work?

### Tested

Did relevant tests actually run?

### Scope

Did we introduce anything unnecessary?

### Code

Is this the simplest robust implementation?

### Ponytail

Have applicable Ponytail instructions been followed?

### Impeccable

If visual, have we inspected the rendered TUI?

### Uncodixfy

Does the implementation contain generated-looking bloat?

### Recruiter

Does this improve the project's story?

Then commit.

---

# 91. Recruiter Demo

Design the entire product around a **90-second demonstration**.

---

## 0–15 sec — Overview

Run:

```bash
property-intel --demo
```

Immediately show:

```text
487 properties
693 transactions
$1.42b tracked transaction value
5.71% median yield
18 records requiring review
```

Say clearly that the bundled data is synthetic.

---

## 15–35 sec — Data Quality

Open:

```text
Data Quality
→ Potential Duplicates
```

Show:

```text
123 Queen Street
123 Queen St
```

and the explainable 96% match.

Demonstrate merge/review.

---

## 35–55 sec — Property Research

Search:

```text
/
```

Find a service-station property.

Show:

```text
owner
tenant
land area
transaction history
source
```

---

## 55–75 sec — Comparables

Open comparable sales.

Show:

```text
top five comparables
distance
sale price
yield
similarity
```

Open one and demonstrate why it matched.

---

## 75–90 sec — Excel

Press:

```text
E
```

Generate the professional Excel report.

Show the workbook.

Done.

---

# 92. Screenshots

Once the application is completely polished, capture real terminal screenshots.

Create:

```text
docs/screenshots/
├── overview.png
├── transactions.png
├── property-detail.png
├── comparables.png
├── duplicate-review.png
├── data-quality.png
├── import.png
└── excel-report.png
```

Do not take final screenshots before the polish phase.

Use consistent terminal dimensions.

Recommended:

```text
120 × 35
```

or another size that displays the UI particularly well.

Use a clean terminal environment.

Avoid unrelated shell/browser clutter.

Do not fabricate screenshots.

---

# 93. Optional Demo GIF

If tooling permits, create a short high-quality terminal recording showing:

```text
launch
→ search
→ property
→ comparables
→ duplicate review
→ Excel export
```

Keep it short.

Approximately:

```text
15–30 seconds
```

Do not add a huge slow GIF that makes the README unpleasant.

This is optional.

---

# 94. README Is A Product Surface

The README should be **exceptionally good**.

A recruiter should understand the project within approximately 20 seconds of opening GitHub.

Do not produce a giant wall of text.

Do not produce an obviously AI-generated README.

Use screenshots heavily.

---

# 95. README Hero

Start approximately:

```markdown
# Property Intel

**Terminal-native market intelligence for commercial property research.**

Property Intel transforms messy commercial-property transaction
data into a clean, searchable database with entity resolution,
comparable-sales analysis, data-quality review and professional
Excel reporting.

[large overview screenshot]

`CSV/XLSX → Clean → Validate → Resolve → Analyse → Export`
```

Then move quickly into the product.

---

# 96. README Structure

Use approximately:

```text
Hero
│
├── Screenshot
│
├── What it does
│
├── Demo
│
├── Core workflow
│
├── Entity resolution
│
├── Property research
│
├── Comparable sales
│
├── Excel reporting
│
├── Architecture
│
├── Technical decisions
│
├── Running locally
│
├── Testing
│
├── Methodology
│
└── Limitations
```

Do not create unnecessary sections.

---

# 97. README — What It Does

Keep it concise.

Something like:

```text
Property Intel is a keyboard-driven research workstation for
commercial-property transaction data.

It ingests messy CSV/XLSX records, normalises and validates them,
identifies records referring to the same physical property, and
turns the resulting canonical dataset into searchable market
intelligence and Excel reports.
```

---

# 98. README — Screenshots

Integrate screenshots with the story.

Do not dump screenshots into a gallery without explanation.

Example:

## Market Overview

`overview.png`

Brief explanation.

## Entity Resolution

`duplicate-review.png`

Brief explanation and scoring methodology.

## Property Research

`property-detail.png`

Brief explanation.

## Comparable Sales

`comparables.png`

Brief explanation.

## Excel Reporting

`excel-report.png`

Brief explanation.

---

# 99. README — Data Pipeline

Use Mermaid:

```text
CSV / XLSX
    │
    ▼
Raw Observations
    │
    ▼
Normalisation
    │
    ▼
Validation
    │
    ▼
Entity Resolution
    │
    ▼
Canonical SQLite Database
    │
    ├─────────────┐
    ▼             ▼
Analytics      Data Quality
    │             │
    └──────┬──────┘
           ▼
       Textual TUI
           │
           ▼
       Excel Reports
```

Make the architecture understandable instantly.

---

# 100. README — Entity Resolution

Briefly explain:

$$
S =
w_aS_a+
w_gS_g+
w_lS_l+
w_bS_b+
w_tS_t
$$

Explain each term.

Mention:

* deterministic normalization,
* fuzzy similarity,
* configurable thresholds,
* manual review,
* false-merge protection.

Link to:

```text
docs/entity-resolution.md
```

for detail.

---

# 101. README — Comparables

Explain:

$$
D =
w_gD_g+
w_lD_l+
w_bD_b+
w_tD_t+
w_sD_s
$$

Explain that comparables are ranked using:

```text
location
sector
land area
building area
recency
```

Emphasise explainability.

---

# 102. README — Excel

Show the workbook screenshot.

Explain that the application programmatically generates a five-sheet market-intelligence workbook using `openpyxl`.

Mention:

```text
Executive Summary
Transactions
Comparable Sales
Sector Analysis
Data Quality
```

---

# 103. README — Technical Decisions

Include a short section.

### Why a TUI?

The application is designed around high-density research workflows and keyboard-driven navigation rather than consumer-facing presentation.

### Why SQLite?

The intended workload is a local analytical dataset. SQLite provides sufficient performance while keeping the application trivial to run.

### Why raw observations?

Messy source records should not directly overwrite canonical property information.

### Why explainable matching?

Incorrectly merging two properties can corrupt subsequent analysis, so duplicate decisions should be inspectable.

### Why Excel?

Spreadsheet reporting remains a useful downstream interface for market research and analysis.

Keep this concise.

---

# 104. README — Running

The setup should be beautifully simple:

```bash
git clone <repo>
cd property-intel

uv sync
uv run property-intel --demo
```

No Docker.

No external database.

No API keys required for demo mode.

---

# 105. README — Demo Data

Clearly state:

> The repository includes a deterministic synthetic dataset designed to exercise the ingestion, validation, entity-resolution and analytics pipelines. It does not represent actual New Zealand commercial-property market statistics.

Do not bury this.

---

# 106. README — Badges

Use few or no badges.

If used, only meaningful ones such as:

```text
Python
Tests
Ruff
```

Do not create a wall of technology badges.

---

# 107. Documentation

Keep documentation small and useful:

```text
docs/
├── architecture.md
├── methodology.md
├── entity-resolution.md
└── screenshots/
```

Documentation should explain decisions and methodology.

Do not duplicate source-code documentation.

---

# 108. Final Ponytail Pass

Before completion:

1. Read the Ponytail skill again if necessary.
2. Run the complete relevant Ponytail workflow.
3. Inspect every TUI screen.
4. Fix issues.
5. Re-run affected tests.

Ponytail is mandatory.

Do not merely state that it was used.

---

# 109. Final Impeccable Pass

Inspect:

```text
Overview
Transactions
Transaction Detail
Properties
Property Detail
Comparables
Data Quality
Duplicate Review
Import
Help
```

Check:

```text
alignment
spacing
borders
visual hierarchy
colours
focus
selection
tables
numbers
empty states
errors
keyboard navigation
terminal resizing
```

Fix inconsistencies.

---

# 110. Final Uncodixfy Pass

Review the entire repository.

Remove:

```text
dead code
unused dependencies
obvious comments
unnecessary docstrings
duplicated helpers
needless abstractions
stale TODOs
debug output
placeholder code
over-engineering
```

Do not simplify genuinely useful domain architecture.

---

# 111. Final Verification

Test from a fresh environment.

Run:

```bash
uv sync
uv run pytest
uv run ruff check .
uv run mypy src
uv run property-intel --demo
```

Then manually verify:

```text
Overview
Search
Transactions
Filters
Properties
Property Detail
Comparables
Data Quality
Duplicate Review
CSV Import
XLSX Import
Excel Export
Help
Quit
```

Verify the generated Excel workbook manually.

---

# 112. Final GitHub Review

Before the final push:

```bash
git status
git log --oneline
```

Check:

* sensible commit history,
* no secrets,
* no accidental database,
* no temporary files,
* no debugging files,
* README renders properly,
* screenshots load,
* Mermaid diagrams render,
* setup instructions work,
* links work.

Make a final logical commit if necessary.

Push.

Verify the push succeeded.

---

# 113. Definition of Done

The project is complete when a new user can:

```text
git clone
    ↓
uv sync
    ↓
uv run property-intel --demo
```

and then:

1. view the market overview,
2. search properties,
3. browse transactions,
4. filter transaction data,
5. inspect a property,
6. view its transaction history,
7. retrieve five comparable sales,
8. understand why each comparable was selected,
9. inspect data-quality issues,
10. review duplicate candidates,
11. merge or separate duplicates,
12. import a CSV,
13. import an XLSX workbook,
14. see validation results,
15. generate a professional Excel market report,

without editing source code.

---

# 114. Hard Scope Boundary

DO NOT ADD:

```text
web frontend
web backend
REST API
Docker
PostgreSQL
authentication
accounts
cloud infrastructure
Redis
queues
microservices
AI chatbot
LLM
agents
price prediction
hedonic modelling
portfolio optimisation
ownership graph
lease modelling
residential property
mobile app
```

unless this specification is explicitly changed.

When core functionality is complete, **polish instead of expanding**.

---

# 115. Where Extra Time Goes

If ahead of schedule, improve:

```text
entity-resolution accuracy
false-merge protection
parsers
tests
keyboard UX
search
table usability
data-quality explanations
comparable explanations
TUI aesthetics
Excel formatting
performance
documentation
screenshots
README
```

Do not add features.

---

# 116. Success Criterion

The finished project should not primarily communicate:

> "I can build a terminal application."

It should communicate:

> "I understand how fragmented market data becomes reliable, decision-useful commercial-property intelligence."

The terminal interface is simply a compact and distinctive way to demonstrate that system.

The technical story should remain:

```text
MESSY DATA
    ↓
ROBUST PARSING
    ↓
VALIDATION
    ↓
ENTITY RESOLUTION
    ↓
CANONICAL DATA
    ↓
MARKET ANALYSIS
    ↓
COMPARABLE SALES
    ↓
EXCEL
```

---

# 117. Initial Codex Instructions

Do not immediately begin generating large amounts of code.

First:

1. Read this entire `MASTER_SPEC.md`.
2. Read `AGENTS.md` and other repository instructions.
3. Locate and read the actual `ponytail` skill.
4. Locate and read `impeccable`.
5. Locate and read `uncodixfy` if available.
6. Inspect the existing repository.
7. Run `git status`.
8. Inspect configured Git remotes.
9. Create `IMPLEMENTATION_PLAN.md`.
10. Break the work into the phases specified above.
11. Define the Phase 1 tests.
12. Implement Phase 1 only.
13. Run tests/lint/type checks relevant to Phase 1.
14. Perform the required quality review.
15. Inspect `git diff`.
16. Commit Phase 1.
17. Push if GitHub is configured and authentication permits.
18. Proceed to Phase 2.

Repeat this process sequentially.

Maintain regular, meaningful Git commits throughout the build.

Do not expand scope.

Do not add Docker.

Do not replace the TUI with a web application.

Do not postpone Ponytail until the end.

Do not postpone all Git commits until the end.

Do not write the final README until the product is sufficiently polished to capture representative screenshots.

When the core product works, stop adding functionality and make it exceptional.
