# Implementation plan

The phases follow `spec.md`. A checkbox is complete only after its code and relevant checks pass.

## Phase 1 — Foundation
- [x] FastAPI and Next.js projects with pinned dependencies
- [x] PostgreSQL, Docker Compose, environment example, Makefile
- [x] Alembic configuration and backend/frontend test commands
- [x] Clean startup and foundation smoke tests

## Phase 2 — Core data model
- [ ] Property, Transaction, Source, RawObservation, ImportJob models
- [ ] Initial migration and model tests

## Phase 3 — Data pipeline
- [ ] CSV/XLSX parsing and column mapping
- [ ] Address/company/currency/area/date normalization
- [ ] Deterministic errors, warnings, and suspicious-value checks
- [ ] Import API and tests

## Phase 4 — Entity resolution
- [ ] Explainable matching and thresholds
- [ ] Labelled evaluation set with precision, recall, F1, false merges
- [ ] Duplicate review and merge/separate API

## Phase 5 — Core analyst UI
- [ ] Application shell, dashboard, transaction/property tables, property detail
- [ ] Search, filtering, sorting, pagination, visibility, CSV export

## Phase 6 — Market analytics
- [ ] Headline/quarter/sector/region aggregations and charts

## Phase 7 — Comparable sales
- [ ] Explainable ranking, top-five API, property UI

## Phase 8 — Data quality
- [ ] Quality summary, review queue, duplicate resolution UI

## Phase 9 — Excel
- [ ] Five-sheet market workbook and comparable export
- [ ] Inspect workbook formatting, charts, and print layout

## Phase 10 — Polish
- [ ] Rendered desktop/mobile review, accessibility and state pass
- [ ] Impeccable, Ponytail, and Uncodixfy passes

## Phase 11 — Documentation
- [ ] Architecture, methodology, entity resolution, screenshots, README

## Phase 12 — Final verification
- [ ] Backend tests, frontend checks, lint, typecheck, build
- [ ] Fresh migrations, seed, import-to-Excel flow, final Git review
