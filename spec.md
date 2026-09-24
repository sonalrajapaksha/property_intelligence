# NZ Commercial Property Transaction Intelligence

## 0. Mission

Build a polished **NZ Commercial Property Transaction Intelligence** platform that converts messy commercial-property data into reliable, searchable market intelligence.

The project should demonstrate the workflow:

```text
MESSY PROPERTY DATA
        ↓
INGESTION
        ↓
NORMALISATION + VALIDATION
        ↓
ENTITY RESOLUTION
        ↓
CLEAN TRANSACTION DATABASE
        ↓
MARKET ANALYTICS
        ↓
COMPARABLE SALES
        ↓
PROFESSIONAL EXCEL REPORT
```

This is a focused portfolio project, not an attempt to build an entire commercial-real-estate operating system.

The finished application should be impressive enough to:

* show a commercial-property recruiter,
* demonstrate during an interview in 90 seconds,
* feature prominently on a CV,
* publish publicly on GitHub,
* and demonstrate strong Engineering Science/data-analysis ability.

The project should particularly demonstrate skills relevant to commercial-property research:

* maintaining property databases,
* researching transactions,
* working with large datasets,
* validating market information,
* identifying duplicate/inconsistent records,
* analysing transaction activity,
* producing market intelligence,
* Excel,
* and attention to detail.

---

# 1. Core Product

The platform tracks NZ commercial-property transactions across three sectors:

1. Service Stations
2. Quick-Service Restaurants / Fast Food
3. Healthcare

The user should be able to:

1. import messy CSV/XLSX transaction data,
2. standardise it,
3. detect invalid/suspicious records,
4. resolve duplicate properties,
5. create canonical property records,
6. search and filter transactions,
7. inspect an individual property,
8. analyse market trends,
9. find comparable transactions,
10. export a professional Excel market report.

That is the entire product.

Do not expand the scope unless an addition materially improves this workflow.

---

# 2. Product Philosophy

Prioritise:

```text
DATA QUALITY
    ↓
USEFUL ANALYTICS
    ↓
EXPLAINABILITY
    ↓
EXCELLENT UX
    ↓
VISUAL POLISH
```

Do not prioritise number of features.

A small application in which every workflow feels complete is preferable to a large application containing unfinished functionality.

The application should feel like a tool an analyst could genuinely use.

---

# 3. Required Codex Skills

Before implementation, locate and read the complete instructions for:

* `impeccable`
* `ponytail`
* `uncodixfy`, if available

Apply them throughout development.

Do not merely run them at the end.

## Impeccable

Use `impeccable` to produce an unusually polished interface.

The application should resemble:

**institutional market intelligence × modern data product × commercial real-estate research**

Avoid:

* generic shadcn dashboard appearance,
* excessive cards,
* excessive rounding,
* gradients everywhere,
* enormous headings,
* meaningless icons,
* decorative animations,
* AI SaaS visual clichés,
* excessive badges,
* huge amounts of whitespace,
* and landing-page styling inside the application.

Prefer:

* strong typography,
* restrained colour,
* dense but readable information,
* excellent tables,
* precise alignment,
* subtle borders,
* thoughtful whitespace,
* professional charts,
* excellent number formatting,
* strong visual hierarchy,
* polished filters,
* excellent hover/focus states,
* meaningful loading/empty/error states.

## Ponytail

Read and apply the actual `ponytail` skill instructions.

Use it continuously where relevant.

Do not guess what the skill does.

## Uncodixfy

If available, use `uncodixfy` to remove AI-generated-code patterns.

Avoid:

* unnecessary abstraction,
* obvious comments,
* giant docstrings,
* redundant wrappers,
* meaningless helpers,
* excessive defensive code,
* fake enterprise architecture,
* unnecessary configuration,
* generic naming,
* dead code,
* placeholder implementations,
* and unnecessary dependencies.

The repository should look deliberately engineered.

---

# 4. Technology

Use:

## Backend

* Python 3.12+
* FastAPI
* SQLAlchemy
* Alembic
* PostgreSQL
* pandas
* NumPy
* RapidFuzz
* scikit-learn only where useful
* openpyxl
* Pydantic
* pytest

PostGIS is optional.

Do not add it unless geographic queries materially benefit from it.

## Frontend

* Next.js
* TypeScript
* React
* Tailwind CSS
* shadcn/ui as primitives, not as the visual identity
* TanStack Query
* TanStack Table
* Recharts

For mapping, use MapLibre only if the map is retained.

## Infrastructure

* Docker
* Docker Compose
* `.env.example`
* Makefile

The project should start approximately with:

```bash
cp .env.example .env
docker compose up --build
```

---

# 5. Repository

Use:

```text
nz-property-intelligence/
│
├── README.md
├── MASTER_SPEC.md
├── IMPLEMENTATION_PLAN.md
├── docker-compose.yml
├── Makefile
├── .env.example
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── ingestion/
│   │   ├── cleaning/
│   │   ├── matching/
│   │   ├── analytics/
│   │   ├── reporting/
│   │   └── database/
│   └── tests/
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── features/
│   ├── lib/
│   └── types/
│
├── data/
│   └── sample/
│
└── docs/
    ├── architecture.md
    ├── methodology.md
    ├── entity-resolution.md
    └── screenshots/
```

Do not create excessive nesting.

---

# 6. Data Model

Keep the schema intentionally small.

## Property

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

Sector:

```text
SERVICE_STATION
QSR
HEALTHCARE
OTHER
```

---

# 7. Transaction

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

Derived values should include:

```text
price_per_land_m2
price_per_building_m2
```

Do not store derived values unnecessarily if they can reliably be calculated.

---

# 8. Source

```text
Source
------
id
name
source_type
reference
retrieved_at
```

Every transaction should have a source where possible.

Do not build an elaborate provenance graph.

Simple, visible provenance is enough.

---

# 9. Raw Observation

This is important.

Do not import messy records directly into canonical tables.

Create:

```text
RawObservation
--------------
id
import_job_id
raw_payload
raw_address
raw_owner
raw_tenant
raw_sale_price
raw_sale_date
raw_land_area
raw_building_area
status
created_at
```

The architecture becomes:

```text
SOURCE FILE
    ↓
RAW OBSERVATION
    ↓
NORMALISATION
    ↓
VALIDATION
    ↓
ENTITY RESOLUTION
    ↓
PROPERTY + TRANSACTION
```

This is one of the main technical ideas demonstrated by the project.

---

# 10. Import Job

Create:

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

This provides enough auditability without building a complete audit system.

---

# 11. Data Import

Support:

* CSV
* XLSX

JSON is optional.

Build an import wizard:

### Step 1 — Upload

Upload CSV/XLSX.

### Step 2 — Column Mapping

Example:

```text
Uploaded column       Platform field

Property Address  →   address
Sale Amount       →   sale_price
Settlement Date   →   transaction_date
Site Area         →   land_area
```

### Step 3 — Preview

Show transformed values.

### Step 4 — Validate

Show problems.

### Step 5 — Resolve

Run duplicate detection.

### Step 6 — Import

Create canonical records.

---

# 12. Cleaning Pipeline

This is a flagship component.

## Address Normalisation

Handle:

```text
Street → St
Road → Rd
Avenue → Ave
Mount → Mt
```

Normalise:

* whitespace,
* punctuation,
* casing,
* common abbreviations,
* postcodes.

Preserve the original value.

Example:

```text
" 123 QUEEN STREET, Auckland CBD "
            ↓
"123 Queen St, Auckland CBD"
```

---

# 13. Company Normalisation

Normalise common company suffixes.

Example:

```text
BP Oil NZ Limited
BP OIL NZ LTD
BP Oil NZ Ltd.
```

should have comparable normalised representations.

Do not destroy the original source value.

---

# 14. Currency Parsing

Support:

```text
$4.2m
$4,200,000
4200000
4.2 million
```

→

```text
4200000
```

Test thoroughly.

---

# 15. Area Parsing

Support values such as:

```text
1,250 sqm
1250 m2
1.25 ha
```

Convert internally to square metres.

---

# 16. Date Parsing

Support common NZ date formats.

Normalise to proper date objects.

Ambiguous dates should be flagged rather than silently guessed.

---

# 17. Validation

Create deterministic validation rules.

Examples:

```text
sale_price <= 0
land_area <= 0
building_area <= 0
transaction_date > today
yield < 0
yield > 30%
invalid postcode
coordinates outside NZ
```

Classify:

```text
ERROR
WARNING
```

Errors prevent automatic import.

Warnings allow analyst review.

---

# 18. Suspicious Data

Create useful sanity checks.

Examples:

```text
sale price > $100m
sale price < $50k
yield > 20%
building area extremely large relative to land area
price/m² extreme relative to dataset
```

Do not claim suspicious records are incorrect.

Label them:

**Requires Review**

---

# 19. Entity Resolution

This is the technical centrepiece.

Multiple observations may describe the same physical property.

Example:

```text
123 Queen Street, Auckland
123 Queen St Auckland CBD
123 QUEEN ST, AUCKLAND
```

The system should identify likely duplicates.

---

# 20. Matching Features

Use:

* normalized address similarity,
* street number equality,
* postcode,
* geographic distance where coordinates exist,
* land-area similarity,
* building-area similarity,
* tenant similarity.

Construct an explainable score.

Example:

$$
S =
w_aS_{address}
+
w_gS_{geo}
+
w_lS_{land}
+
w_tS_{tenant}
$$

Keep weights configurable in one obvious location.

Do not use a black-box model unless there is compelling evidence it performs better.

---

# 21. Match Thresholds

Use approximately:

```text
score >= 0.93
→ automatic match

0.75 <= score < 0.93
→ manual review

score < 0.75
→ separate property
```

Tune using a labelled evaluation set.

---

# 22. Duplicate Review UI

Create one excellent review interface.

Example:

```text
Potential Duplicate                           96% MATCH

SOURCE RECORD                   EXISTING PROPERTY

123 Queen Street                123 Queen St
Auckland CBD                    Auckland CBD

Service Station                 Service Station
1,247 m²                        1,250 m²
BP                              BP


MATCH EVIDENCE

Address similarity                  98%
Land-area similarity                99%
Tenant match                       Exact
Geographic distance                 14 m


                 Keep Separate     Merge Records
```

The reviewer should understand exactly why the match was proposed.

---

# 23. Entity Resolution Evaluation

Create a small manually labelled dataset.

Report:

* precision,
* recall,
* F1,
* false merges.

False merges are particularly important.

Document methodology in:

```text
docs/entity-resolution.md
```

---

# 24. Core Application

The final application should have approximately five primary destinations:

```text
Dashboard
Transactions
Properties
Data Quality
Import
```

Do not create fifteen routes.

Comparable sales live inside the property experience.

---

# 25. Dashboard

The dashboard should immediately communicate the state of the tracked market.

Top metrics:

```text
Tracked Properties

Transactions

Tracked Transaction Value

Median Sale Price

Median Yield

Records Requiring Review
```

Show the reporting period.

---

# 26. Dashboard Charts

Include approximately three excellent visualisations.

### Transaction Activity

Quarter → transaction count.

### Transaction Value

Quarter → aggregate sale value.

### Sector Mix

Service stations / QSR / healthcare.

Optionally include a compact regional breakdown.

Do not create charts merely to fill space.

---

# 27. Recent Transactions

The dashboard should include a high-quality recent-transactions table.

Columns:

```text
Date
Property
Region
Sector
Sale Price
Yield
$/m²
Source
```

Rows should link to the relevant property.

---

# 28. Transactions Page

This should be one of the strongest screens.

Build an excellent data table.

Columns:

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

Support:

* sorting,
* filtering,
* pagination,
* search,
* column visibility,
* CSV export.

Filters:

```text
Date
Region
Sector
Sale Price
Yield
```

Make this table genuinely pleasant to use.

---

# 29. Properties Page

Display canonical properties.

Columns:

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

Support search/filter/sort.

---

# 30. Property Detail Page

This is the showcase page.

Header:

```text
42 Example Road
Auckland

SERVICE STATION
```

Show:

```text
Owner
Tenant
Land Area
Building Area
Last Sale
Last Sale Price
```

---

# 31. Transaction History

Show all tracked transactions for the property.

Example:

```text
2026        $5.2m        5.4%
2019        $3.8m        6.1%
2013        $2.9m        —
```

Use a restrained timeline/table.

---

# 32. Source Information

Clearly display where information came from.

Example:

```text
Source
Public transaction record

Retrieved
14 Sep 2026
```

Keep this simple.

---

# 33. Comparable Sales Engine

Given a property, rank similar historical transactions.

This is the second flagship technical feature.

Use factors such as:

* sector,
* geographic distance,
* land area,
* building area,
* transaction recency.

---

# 34. Comparable Distance

Construct an interpretable normalized distance:

$$
D(i,j)
=
w_gD_g
+
w_lD_l
+
w_bD_b
+
w_tD_t
+
w_sD_s
$$

where:

```text
Dg = geographic distance
Dl = land-area difference
Db = building-area difference
Dt = transaction age
Ds = sector mismatch penalty
```

Convert into a user-friendly similarity measure.

Document exactly how this works.

---

# 35. Comparable Results

Return the top five by default.

Display:

```text
Comparable
Distance
Sale Date
Sale Price
Land Area
Building Area
Yield
Similarity
```

---

# 36. Explain Comparables

Do not display only a score.

Example:

```text
93% Similar

✓ Same sector
✓ 1.4 km away
✓ Land area within 5%
✓ Building area within 8%
✓ Sold 6 months ago
```

This makes the analytics much more credible.

---

# 37. Comparable Map

OPTIONAL.

If implementation is straightforward and visually excellent, show:

```text
● Subject property
○ Comparable 1
○ Comparable 2
...
```

Do not retain a mediocre map simply because maps look impressive.

Quality > feature count.

---

# 38. Data Quality Page

This is highly relevant to the project's purpose.

Top metrics:

```text
Potential Duplicates
Validation Warnings
Missing Owner
Missing Tenant
Missing Coordinates
Suspicious Transactions
```

---

# 39. Review Queue

Below the metrics, create a review queue.

Example:

```text
TYPE                 RECORD                  ISSUE

Duplicate            123 Queen St            96% duplicate candidate
Validation           42 Example Rd           Yield = 24.7%
Missing Data         8 High Street           Owner unavailable
Suspicious Value     17 Example Ave          Sale price unusually high
```

Clicking an item should open the relevant review context.

---

# 40. Market Analytics

Calculate:

```text
transaction count
transaction value
median sale price
median yield
median price/land m²
median price/building m²
```

Segment by:

* quarter,
* region,
* sector.

Use medians for skewed variables where appropriate.

Always expose sample sizes where meaningful.

---

# 41. Excel Market Report

This is a mandatory flagship feature.

Generate:

```text
NZ_Commercial_Property_Market_Report.xlsx
```

using `openpyxl`.

The workbook should be visually excellent.

It should not resemble a dataframe dump.

---

# 42. Excel Sheets

Use:

```text
01 Executive Summary
02 Transactions
03 Comparable Sales
04 Sector Analysis
05 Data Quality
```

Only five sheets.

Make them excellent.

---

# 43. Executive Summary

Include:

```text
Reporting Period
Properties Tracked
Transactions
Transaction Value
Median Sale Price
Median Yield
Records Requiring Review
```

Add:

* transaction activity chart,
* transaction value chart,
* sector breakdown.

---

# 44. Transactions Sheet

Create a proper Excel table.

Columns:

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

Use:

* frozen header,
* filters,
* professional widths,
* currency formats,
* percentages,
* date formats,
* alternating rows where appropriate.

---

# 45. Comparable Sales Sheet

Allow export for a selected property.

Include:

```text
Subject Property

Comparable Rank
Address
Distance
Sale Date
Sale Price
Land Area
Building Area
Yield
Similarity
Match Explanation
```

---

# 46. Sector Analysis

Show:

```text
Sector
Transactions
Transaction Value
Median Sale Price
Median Yield
Median $/m²
```

Add one or two useful charts.

---

# 47. Data Quality Sheet

Include:

```text
Potential duplicates
Validation warnings
Missing information
Suspicious records
```

Use conditional formatting intelligently.

---

# 48. Excel Quality

Manually inspect the generated workbook.

Verify:

* formatting,
* widths,
* row heights,
* frozen panes,
* filters,
* tables,
* charts,
* number formats,
* dates,
* percentages,
* print readability,
* source notes.

This feature should visibly demonstrate advanced Excel capability.

---

# 49. Demo Dataset

The project must run without proprietary data.

Create approximately:

```text
500 canonical properties
700 transactions
3 sectors
multiple NZ regions
10 years of history
```

Generate additional messy observations so there are approximately:

```text
800–1,000 raw observations
```

Include:

* duplicate addresses,
* different company spellings,
* missing fields,
* malformed currency,
* conflicting values,
* suspicious yields,
* repeated property transactions,
* different date formats.

The data pipeline needs interesting problems to solve.

---

# 50. Synthetic Data

All synthetic/demo information must be clearly marked:

```text
DEMO DATA — SYNTHETIC
```

Do not imply that synthetic statistics describe the actual NZ market.

---

# 51. Optional Real Data

The architecture should support legally obtained public information.

Do not:

* bypass authentication,
* circumvent CAPTCHAs,
* ignore source terms,
* scrape prohibited sources.

Document potential data sources separately without making them necessary to run the project.

---

# 52. API

Keep the API small.

Implement approximately:

```text
GET  /api/dashboard
GET  /api/properties
GET  /api/properties/{id}
GET  /api/properties/{id}/comparables

GET  /api/transactions

GET  /api/data-quality
GET  /api/data-quality/duplicates

POST /api/import
POST /api/duplicates/{id}/resolve

GET  /api/reports/market.xlsx
GET  /api/reports/transactions.csv
GET  /api/properties/{id}/comparables.xlsx
```

Do not build APIs that have no frontend or reporting use case.

---

# 53. Testing

Testing is mandatory.

## Cleaning

Test:

```text
addresses
currency
areas
dates
company names
missing values
```

## Validation

Test:

```text
invalid prices
future dates
invalid yields
invalid areas
suspicious records
```

## Entity Resolution

Test:

```text
exact duplicates
abbreviated addresses
company spelling differences
near duplicates
different properties with similar names
unit-number differences
false-positive traps
```

## Analytics

Test:

```text
transaction value
medians
yield
price/m²
quarterly aggregation
sector aggregation
```

## Comparables

Test:

```text
distance
area normalization
recency
sector penalties
ranking
explanations
```

## API

Test important routes and filtering.

---

# 54. End-to-End Test

Implement at least one test covering:

```text
CSV
 ↓
IMPORT
 ↓
NORMALISE
 ↓
VALIDATE
 ↓
MATCH
 ↓
DATABASE
 ↓
PROPERTY
 ↓
COMPARABLES
 ↓
EXCEL
```

This is the project's central workflow.

---

# 55. Visual Design

Use `impeccable` aggressively here.

The visual language should be:

```text
professional
analytical
precise
restrained
information-dense
premium
```

Do not make it look like a university assignment.

Do not make it look like an AI startup landing page.

---

# 56. Colour

Use a restrained neutral base with one sophisticated accent.

Do not blindly imitate CBRE branding.

The project should have its own identity.

Ensure:

* WCAG-appropriate contrast,
* meaningful status colours,
* charts remain readable,
* colour is never the only means of communicating status.

---

# 57. Typography

Typography is important.

Use a professional sans-serif family available through the chosen frontend setup.

Numerical data should align cleanly.

Consider tabular numerals for financial tables.

Use hierarchy through:

* size,
* weight,
* spacing,

rather than decorative elements.

---

# 58. Number Formatting

Be meticulous.

Use:

```text
$4.2m
$850k
5.42%
1,240 m²
$3,410/m²
```

where appropriate.

Full precision should remain available when needed.

Dates should follow a consistent NZ-friendly format.

---

# 59. Responsive Behaviour

Desktop is the primary target because this is an analyst application.

Still ensure:

* laptop layouts work,
* tables degrade reasonably,
* no major overflow,
* navigation remains usable.

Do not spend excessive time optimizing tiny mobile screens.

---

# 60. Accessibility

Include:

* keyboard navigation,
* focus states,
* semantic HTML,
* accessible labels,
* chart alternatives/tooltips,
* sufficient contrast.

---

# 61. Loading / Empty / Error States

Every major screen should have intentional states.

Examples:

```text
No transactions match these filters.

No comparable sales satisfy the current criteria.

This import contains 14 records requiring review.

Market report could not be generated.
```

Avoid blank screens.

---

# 62. Implementation Phases

## Phase 1 — Foundation

Build:

* repository structure,
* backend,
* frontend,
* PostgreSQL,
* Docker,
* migrations,
* test infrastructure.

Verify everything starts.

COMMIT.

---

## Phase 2 — Core Data Model

Implement:

* Property
* Transaction
* Source
* RawObservation
* ImportJob

Add migrations and tests.

COMMIT.

---

## Phase 3 — Data Pipeline

Implement:

* CSV/XLSX ingestion,
* column mapping,
* address normalization,
* company normalization,
* currency parsing,
* area parsing,
* date parsing,
* validation.

Test thoroughly.

COMMIT.

---

## Phase 4 — Entity Resolution

Implement:

* matching features,
* scoring,
* thresholds,
* labelled evaluation set,
* duplicate review,
* merge/separate actions.

Measure performance.

COMMIT.

---

## Phase 5 — Core Analyst UI

Build:

* application shell,
* dashboard,
* transactions table,
* properties table,
* property detail.

Apply `impeccable` and `ponytail`.

COMMIT.

---

## Phase 6 — Market Analytics

Implement:

* headline metrics,
* quarterly transaction activity,
* transaction value,
* sector breakdown,
* regional filtering.

COMMIT.

---

## Phase 7 — Comparable Sales

Implement:

* comparable distance,
* ranking,
* explanation generation,
* UI.

Optional map only if excellent.

COMMIT.

---

## Phase 8 — Data Quality

Implement:

* quality metrics,
* review queue,
* validation issues,
* duplicate review integration.

COMMIT.

---

## Phase 9 — Excel

Build the complete five-sheet workbook.

Manually inspect it.

COMMIT.

---

## Phase 10 — Polish

STOP ADDING FEATURES.

Perform:

* impeccable review,
* ponytail review,
* uncodixfy review,
* accessibility review,
* responsive review,
* error-state review,
* performance review.

Fix everything material.

COMMIT.

---

## Phase 11 — Documentation & GitHub Presentation

Create:

* screenshots,
* diagrams,
* methodology,
* architecture documentation,
* final README.

COMMIT.

---

## Phase 12 — Final Verification

Perform clean install.

Run:

```text
backend tests
frontend tests
lint
typecheck
production build
database migrations
seed
Excel generation
```

Verify the complete demo workflow.

Make final cleanup commit.

Push to GitHub if configured.

---

# 63. Git Discipline

Git history is part of the portfolio.

Commit regularly throughout development.

Do not produce one enormous commit.

Before each commit:

```text
git status
git diff
```

Run relevant tests.

Use meaningful conventional commit messages.

Examples:

```text
chore: initialise application infrastructure

feat: add property transaction data model

feat: implement transaction ingestion pipeline

feat: add commercial property validation rules

feat: implement property entity resolution

feat: build market intelligence dashboard

feat: add comparable sales analysis

feat: add data quality review workflow

feat: generate Excel market intelligence report

style: polish analyst interface

refactor: simplify data pipeline implementation

docs: add architecture and methodology

docs: complete portfolio README
```

If a GitHub remote is configured and authentication permits it, push milestones regularly.

Never claim a push succeeded unless it actually did.

Never force-push unless explicitly required.

Never commit:

```text
.env
credentials
API keys
database dumps
node_modules
temporary files
```

---

# 64. Implementation Plan

Create:

```text
IMPLEMENTATION_PLAN.md
```

before substantial coding.

Translate every phase into checkboxes.

Keep it current.

Example:

```markdown
## Phase 3 — Data Pipeline

- [x] CSV reader
- [x] XLSX reader
- [x] column mapper
- [x] currency parser
- [x] area parser
- [ ] date ambiguity handling
- [ ] validation summary
```

Never mark incomplete functionality as complete.

---

# 65. Quality Review After Every Phase

After each phase perform:

### Functional

Does it work?

### Tests

Did relevant tests actually pass?

### Engineering

Is this the simplest robust implementation?

### Uncodixfy

Does anything look generated, bloated or unnecessarily abstract?

### Impeccable

For UI work: does it actually look excellent when rendered?

### Ponytail

Apply relevant Ponytail requirements.

### Scope

Did anything creep into the project that isn't contributing to the central workflow?

Remove unnecessary complexity.

Then commit.

---

# 66. Recruiter Demo

Design everything around a 90-second demonstration.

## 0–15 seconds — Dashboard

Show:

```text
500 properties
700 transactions
$X tracked transaction value
median yield
transaction trend
sector breakdown
```

Explain that the demo uses synthetic data.

---

## 15–35 seconds — Messy Data

Open the import/data-quality workflow.

Show:

```text
123 Queen Street, Auckland
123 QUEEN ST
123 Queen St, Auckland CBD
```

Explain:

> The system standardises incoming data and identifies records that probably refer to the same commercial property.

Show the explainable 96% duplicate match.

---

## 35–55 seconds — Property Intelligence

Open the canonical property.

Show:

```text
property information
owner
tenant
transaction history
source
```

---

## 55–75 seconds — Comparable Sales

Show:

```text
five comparable transactions
similarity scores
distance
area difference
recency
match explanation
```

Explain that the system ranks comparables using transparent characteristics rather than a black-box model.

---

## 75–90 seconds — Excel

Click:

```text
Export Market Report
```

Open the professional Excel workbook.

Finish.

The entire project's value should be understandable from this demonstration.

---

# 67. Screenshots

Once the application is finished and polished, capture real screenshots.

Create:

```text
docs/screenshots/dashboard.png
docs/screenshots/transactions.png
docs/screenshots/property-detail.png
docs/screenshots/comparables.png
docs/screenshots/entity-resolution.png
docs/screenshots/data-quality.png
docs/screenshots/excel-report.png
```

Do not capture screenshots before the UI polish phase.

Do not fabricate screenshots.

Use representative populated states.

Keep dimensions consistent.

Avoid browser/debug clutter where possible.

---

# 68. README

The README is a major part of the finished product.

It should be visually excellent and highly professional.

A recruiter opening the repository should understand the project in **20–30 seconds**.

Do not write a generic generated README.

---

# 69. README Opening

Use approximately:

```markdown
# NZ Commercial Property Intelligence

A market-intelligence platform that transforms messy commercial
property transaction data into a clean, auditable database with
entity resolution, comparable-sales analysis and professional
Excel reporting.

[HERO SCREENSHOT]
```

Then provide a concise explanation.

---

# 70. README Structure

Use:

```text
Hero
↓
What It Does
↓
Product Screenshots
↓
Data Pipeline
↓
Entity Resolution
↓
Comparable Sales
↓
Excel Reporting
↓
Architecture
↓
Technical Decisions
↓
Running Locally
↓
Testing
↓
Methodology
↓
Demo Data
↓
Limitations
```

Do not create unnecessary sections.

---

# 71. README Screenshots

Tell the story visually.

## Market Intelligence

Dashboard screenshot.

Short explanation.

## Transaction Research

Transaction/property screenshot.

Short explanation.

## Entity Resolution

Duplicate-review screenshot.

Explain:

```text
raw observations
→ normalization
→ similarity features
→ review/merge
→ canonical property
```

## Comparable Sales

Screenshot.

Show the formula/methodology briefly.

## Excel Reporting

Workbook screenshot.

Mention that it is generated programmatically using `openpyxl`.

---

# 72. README Architecture Diagram

Use Mermaid.

Example:

```text
CSV / XLSX
    │
    ▼
Raw Observations
    │
    ▼
Cleaning & Validation
    │
    ▼
Entity Resolution
    │
    ▼
PostgreSQL
    │
    ├──────────────┐
    ▼              ▼
Analytics      Data Quality
    │              │
    └──────┬───────┘
           ▼
        FastAPI
           │
      ┌────┴────┐
      ▼         ▼
   Next.js     Excel
```

Keep it attractive and understandable.

---

# 73. README Methodology

Explain enough technical depth to demonstrate competence.

For entity resolution, briefly describe:

$$
S =
w_aS_a+w_gS_g+w_lS_l+w_tS_t
$$

For comparables:

$$
D =
w_gD_g+w_lD_l+w_bD_b+w_tD_t+w_sD_s
$$

Explain what the terms mean.

Do not fill the README with academic derivations.

Link to `/docs` for deeper detail.

---

# 74. README Technical Decisions

Include a short section explaining important decisions:

### Raw observations vs canonical properties

Prevents messy source data from corrupting the clean database.

### Explainable entity resolution

Analysts can inspect why two records are considered duplicates.

### Explainable comparables

Similarity is based on visible market characteristics.

### Excel as a first-class output

Commercial analysts frequently work with spreadsheet-based workflows, so Excel is treated as a core product surface rather than an afterthought.

These explanations are more valuable than listing twenty libraries.

---

# 75. README Demo Data Disclosure

Clearly state:

> The included dataset is synthetic and exists solely to demonstrate the data pipeline and analytics. Statistics shown in screenshots should not be interpreted as actual New Zealand commercial-property market statistics.

This should be visible.

---

# 76. Documentation

Create only useful documentation:

```text
docs/
├── architecture.md
├── methodology.md
├── entity-resolution.md
└── screenshots/
```

Do not create documentation files merely to make the repository appear larger.

---

# 77. Final Impeccable Pass

Once functionality is complete, inspect every actual rendered screen.

Review:

* dashboard,
* transactions,
* properties,
* property detail,
* comparables,
* data quality,
* import flow.

Fix:

* inconsistent spacing,
* weak typography,
* ugly tables,
* chart issues,
* alignment,
* awkward forms,
* poor number formatting,
* weak states,
* responsiveness,
* accessibility.

Do not judge UI quality from source code alone.

---

# 78. Final Ponytail Pass

Apply the actual `ponytail` skill across the completed product.

Fix relevant issues.

---

# 79. Final Uncodixfy Pass

Inspect the entire repository.

Remove:

* dead code,
* unnecessary comments,
* generated-looking prose,
* unnecessary abstractions,
* unused dependencies,
* duplicated helpers,
* stale TODOs,
* placeholder components,
* debug logging,
* unused configuration.

Do not over-refactor working code.

---

# 80. Final GitHub Pass

Before completion:

1. run `git status`,
2. inspect all remaining diffs,
3. check `.gitignore`,
4. check for secrets,
5. verify README,
6. verify screenshot paths,
7. verify Mermaid diagrams,
8. verify local setup instructions,
9. run backend tests,
10. run frontend tests,
11. run lint,
12. run typecheck,
13. run production build,
14. regenerate Excel report,
15. verify fresh database migration and seed.

Make the final commit.

Push to GitHub if configured and permitted.

Confirm the remote contains the final commits.

---

# 81. Definition of Done

The project is complete when a fresh user can:

```text
1. Clone repository
2. Start application
3. Load demo data
4. View market dashboard
5. Search 500+ properties
6. Filter transactions
7. Open a property
8. View its transaction history
9. Import messy CSV/XLSX data
10. See validation problems
11. Review a duplicate candidate
12. Merge/keep duplicate records
13. Find five comparable sales
14. Understand why they are comparable
15. Review data-quality issues
16. Generate a professional Excel report
```

and all major functionality works without editing source code.

---

# 82. Hard Scope Boundary

Do NOT add, unless required to complete an existing workflow:

* authentication,
* user teams,
* permissions,
* billing,
* chatbots,
* LLM features,
* AI agents,
* hedonic valuation ML,
* price prediction,
* ownership graphs,
* lease modelling,
* market alerts,
* saved dashboards,
* full audit systems,
* microservices,
* Redis,
* message queues,
* Kubernetes,
* complex cloud infrastructure,
* mobile apps,
* residential property,
* property listings marketplace.

If tempted to add one of these, improve an existing feature instead.

---

# 83. What To Polish Instead

When core functionality is finished early, do NOT increase scope.

Spend the remaining effort on:

```text
better entity resolution
better tests
better synthetic data
better table UX
better filtering
better comparables
better explanations
better charts
better Excel
better error handling
better performance
better screenshots
better documentation
better README
```

Depth over breadth.

---

# 84. Success Criterion

The finished project should not communicate:

> "I know how to build dashboards."

It should communicate:

> "I understand how messy market information becomes reliable decision-useful data."

The strongest technical elements should therefore be:

**1. Data ingestion and cleaning**

**2. Entity resolution**

**3. Data validation and quality control**

**4. Commercial-property transaction analytics**

**5. Explainable comparable-sales analysis**

**6. Professional Excel reporting**

Everything else exists to make those six capabilities easier to understand and use.

---

# 85. Begin

Before coding:

1. Read this entire specification.
2. Read repository instructions.
3. Locate and read `impeccable`.
4. Locate and read `ponytail`.
5. Locate and read `uncodixfy` if available.
6. Inspect the existing repository.
7. Inspect Git status and configured remotes.
8. Create `IMPLEMENTATION_PLAN.md`.
9. Map the specification into the phases above.
10. Identify tests required for Phase 1.

Then implement **Phase 1 only**.

Verify it.

Run the relevant quality passes.

Commit it.

Push the milestone to GitHub if the remote and credentials are configured.

Then proceed sequentially.

Do not skip phases simply to produce visible functionality faster.

Do not expand scope.

When choosing between another feature and making an existing workflow exceptional, **make the existing workflow exceptional**.
