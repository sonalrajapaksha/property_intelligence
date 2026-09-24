# Product

<!-- impeccable:product-schema 1 -->

## Platform
web

## Stack
FastAPI, SQLAlchemy, Alembic, PostgreSQL, pandas, RapidFuzz, openpyxl; Next.js, TypeScript, Tailwind CSS, TanStack Query/Table, Recharts. Specified in `spec.md`.

## Users
Commercial property research analysts assessing New Zealand service stations, quick-service restaurants, and healthcare assets.

## Product Purpose
Turn messy transaction files into an auditable property and transaction database, market analytics, explainable comparable sales, and a professional Excel report.

## Operating Context
Analysts import CSV/XLSX files, review validation and duplicate candidates, research canonical properties and transactions, and export Excel reports.

## Capabilities and Constraints
Five primary destinations: Dashboard, Transactions, Properties, Data Quality, Import. Demo content is synthetic and must be labelled. No authentication, valuation prediction, or market claims from demo figures.

## Evidence on Hand
`spec.md` is the product brief. No real transaction data, brand assets, or external evidence was supplied.

## Product Principles
- Preserve raw observations alongside cleaned records.
- Explain validation, matches, and comparable rankings.
- Keep analyst workflows compact and inspectable.
- Make Excel a first-class output.
