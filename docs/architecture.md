# Architecture

The CLI opens a local SQLite database and initializes the five core tables. Imports create an `ImportJob`, `Source` and one `RawObservation` per incoming row before producing any canonical `Property` or `Transaction`. A rejected or review row remains visible in Quality. Accepted transactions point to canonical properties and sources.

`pipeline.py` owns parsing, validation, matching, CSV/XLSX reading and import decisions. `analytics.py` calculates market metrics and comparable ranks. `report.py` creates the five-sheet workbook. `app.py` presents those operations through Textual. The schema also has an Alembic initial revision for inspection and future migrations.

The default database is local, configurable and excluded from Git. Routine exports are also excluded.
