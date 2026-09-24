import argparse
from pathlib import Path

from sqlalchemy import select

from .app import PropertyIntel
from .db import ImportJob, open_db
from .demo import seed
from .pipeline import import_rows, read_rows, suggest_mapping
from .report import export_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Property Intel market research workstation")
    parser.add_argument("command", nargs="?", choices=["import", "export"])
    parser.add_argument("file", nargs="?")
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--db", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    session = open_db(args.db) if args.db else open_db()
    if args.demo:
        seed(session)
    if args.command == "import":
        if not args.file:
            parser.error("import requires a CSV or XLSX file")
        rows = read_rows(Path(args.file))
        job = import_rows(
            session, rows, suggest_mapping(list(rows[0])) if rows else {}, Path(args.file).name
        )
        print(
            f"Received {job.records_received}; imported {job.records_imported}; review {job.records_flagged}; rejected {job.records_rejected}"
        )
    elif args.command == "export":
        print(
            export_report(
                session,
                args.output or Path("data/exports/NZ_Commercial_Property_Market_Report.xlsx"),
            )
        )
    else:
        demo = bool(
            session.scalar(select(ImportJob.id).where(ImportJob.filename == "synthetic_demo.csv"))
        )
        PropertyIntel(session, demo=demo).run()


if __name__ == "__main__":
    main()
