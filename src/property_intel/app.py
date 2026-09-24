import json
from collections.abc import Sequence
from pathlib import Path

from rich.table import Table
from sqlalchemy import select
from sqlalchemy.orm import Session
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, DataTable, Header, Input, Label, Select, Static

from .analytics import comparables, money, overview
from .db import Property, RawObservation, Transaction
from .pipeline import (
    FIELDS,
    import_rows,
    match_score,
    parse_area,
    read_rows,
    resolve,
    suggest_mapping,
)
from .report import export_report


def pct(value: float | None) -> str:
    return f"{value:.2%}" if value is not None else "—"


class Detail(ModalScreen[None]):
    BINDINGS = [
        ("escape", "close_detail", "Close"),
        ("m", "merge", "Merge"),
        ("s", "separate", "Separate"),
    ]

    def __init__(self, body: str, on_decision=None) -> None:
        super().__init__()
        self.body = body
        self.on_decision = on_decision

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Static(self.body, id="dialog_text")
            yield Label(
                "Esc close" + ("   M merge   S separate" if self.on_decision else ""),
                classes="hint",
            )

    def action_close_detail(self) -> None:
        self.dismiss()

    def action_merge(self) -> None:
        if self.on_decision:
            self.on_decision(True)
            self.dismiss()

    def action_separate(self) -> None:
        if self.on_decision:
            self.on_decision(False)
            self.dismiss()


class PropertyIntel(App):
    TITLE = "PROPERTY INTEL"
    SUB_TITLE = "NZ COMMERCIAL PROPERTY INTELLIGENCE"
    CSS = """
    Screen { background: #10191b; color: #e3ece9; }
    Header { background: #1a2b2e; color: #f3f7f4; }
    Footer { background: #1a2b2e; color: #cadbd4; }
    #brand { height: 2; padding: 0 2; background: #1a2b2e; color: #d4b878; text-style: bold; }
    #toolbar { height: 3; padding: 0 1; background: #142124; }
    #toolbar Input { width: 3fr; }
    #toolbar Select { width: 2fr; }
    #advanced { height: 3; background: #142124; padding: 0 1; }
    #advanced Input { width: 1fr; }
    #content { padding: 1 2; }
    #section_title { height: 2; color: #d4b878; text-style: bold; }
    #summary { height: auto; margin-bottom: 1; }
    DataTable { height: 1fr; background: #10191b; }
    DataTable > .datatable--header { background: #1d3435; color: #e7f1ed; text-style: bold; }
    DataTable > .datatable--cursor { background: #285b57; color: #ffffff; }
    DataTable:focus { border: tall #7fb9a5; }
    .hint { color: #a5bdb4; height: 1; }
    #status { height: 1; padding: 0 2; background: #1a2b2e; color: #b8d5ca; }
    #dialog { width: 85%; max-width: 100; height: auto; max-height: 90%; padding: 2 3; background: #1d2d2f; border: round #72a899; align: center middle; }
    #dialog_text { height: auto; }
    ModalScreen { align: center middle; background: #0009; }
    .mapping { height: 3; }
    .mapping Label { width: 32; padding: 1 1; }
    .mapping Select { width: 40; }
    #import_file { width: 1fr; }
    #import_load { width: 12; }
    #import_commit { width: 16; }
    #import_panel > Horizontal { height: 3; }
    """
    BINDINGS = [
        Binding("1", "show('overview')", "Overview"),
        Binding("2", "show('transactions')", "Transactions"),
        Binding("3", "show('properties')", "Properties"),
        Binding("4", "show('quality')", "Quality"),
        Binding("5", "show('import')", "Import"),
        Binding("slash", "search", "Search"),
        Binding("f", "filter", "Filter"),
        Binding("s", "sort", "Sort"),
        Binding("e", "export", "Export"),
        Binding("question_mark", "help", "Help"),
        Binding("escape", "clear_or_return", "Back"),
        Binding("q", "quit", "Quit"),
    ]

    def __init__(self, session: Session, demo: bool = False) -> None:
        super().__init__()
        self.session = session
        self.demo = demo
        self.page = "overview"
        self.search_return = "overview"
        self.subject: Property | None = None
        self.rows: list = []
        self.file_rows: list[dict] = []
        self.file_path: Path | None = None
        self.sort_reverse = True

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("DEMO DATA — SYNTHETIC" if self.demo else "LOCAL DATASET", id="brand")
        with Horizontal(id="toolbar"):
            yield Input(placeholder="Search address, owner, tenant, buyer, seller   /", id="search")
            yield Select(
                [(x, x) for x in ("All sectors", "SERVICE_STATION", "QSR", "HEALTHCARE", "OTHER")],
                value="All sectors",
                id="sector",
            )
            yield Select([("All regions", "All regions")], value="All regions", id="region")
        with Horizontal(id="advanced"):
            yield Input(placeholder="Date from YYYY-MM-DD", id="date_from")
            yield Input(placeholder="Date to YYYY-MM-DD", id="date_to")
            yield Input(placeholder="Price min", id="price_min")
            yield Input(placeholder="Price max", id="price_max")
            yield Input(placeholder="Yield min %", id="yield_min")
            yield Input(placeholder="Yield max %", id="yield_max")
        with VerticalScroll(id="content"):
            yield Static("MARKET OVERVIEW", id="section_title")
            yield Static(id="summary")
            yield DataTable(id="table", cursor_type="row")
            yield Vertical(id="import_panel")
        yield Static(
            "1–5 navigate   / search   f filter   Enter inspect   e export   ? help   q quit",
            id="status",
        )

    def on_mount(self) -> None:
        regions = sorted({p.region for p in self.session.scalars(select(Property)) if p.region})
        self.query_one("#region", Select).set_options(
            [("All regions", "All regions")] + [(r, r) for r in regions]
        )
        self.query_one("#region", Select).value = "All regions"
        self.query_one("#advanced", Horizontal).display = False
        self.show_page()
        self.query_one("#table", DataTable).focus()

    def action_show(self, page: str) -> None:
        self.page = page
        self.subject = None
        self.show_page()

    def action_search(self) -> None:
        if self.page != "search":
            self.search_return = self.page
        self.page = "search"
        self.show_page()
        self.query_one("#search", Input).focus()

    def action_filter(self) -> None:
        panel = self.query_one("#advanced", Horizontal)
        panel.display = not panel.display
        (
            self.query_one("#date_from", Input)
            if panel.display
            else self.query_one("#sector", Select)
        ).focus()

    def action_sort(self) -> None:
        self.sort_reverse = not self.sort_reverse
        self.show_page()

    def action_export(self) -> None:
        try:
            path = export_report(self.session, subject=self.subject)
            self.notify(f"Report saved: {path}", severity="information")
        except OSError as exc:
            self.notify(f"Could not save report: {exc}", severity="error")

    def action_help(self) -> None:
        self.push_screen(
            Detail(
                "PROPERTY INTEL  /  KEYBOARD GUIDE\n\n1–5     Switch sections\n/       Search all research fields\nf       Focus sector filter\ns       Reverse table order\nEnter   Inspect selected record\ne       Export five-sheet Excel report\nEsc     Clear search or return\nq       Quit\n\nIn Quality: open a review row, then M to merge or S to separate.\nIn Import: choose a CSV/XLSX path, inspect mapping and preview, then import."
            )
        )

    def action_clear_or_return(self) -> None:
        search = self.query_one("#search", Input)
        if search.value:
            search.value = ""
        if self.page == "search":
            self.page = self.search_return
            self.show_page()
        elif self.subject:
            self.subject = None
            self.page = "properties"
            self.show_page()
        table = self.query_one("#table", DataTable)
        if table.display:
            table.focus()
        else:
            self.set_focus(None)

    def on_input_changed(self, event: Input.Changed) -> None:
        if (
            event.input.id
            in (
                "search",
                "date_from",
                "date_to",
                "price_min",
                "price_max",
                "yield_min",
                "yield_max",
            )
            and self.page != "import"
        ):
            self.show_page()

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id in ("sector", "region"):
            self.show_page()

    def _filtered(self, items: Sequence) -> list:
        query = self.query_one("#search", Input).value.lower().strip()
        sector = self.query_one("#sector", Select).value
        region = self.query_one("#region", Select).value
        result = []
        for item in items:
            p = item.property if isinstance(item, Transaction) else item
            if sector not in ("All sectors", Select.NULL) and p.sector != sector:
                continue
            if region not in ("All regions", Select.NULL) and p.region != region:
                continue
            fields = [p.canonical_address, p.owner_name, p.tenant_name]
            if isinstance(item, Transaction):
                fields += [item.buyer_name, item.seller_name]
            if query and not any(query in (field or "").lower() for field in fields):
                continue
            if isinstance(item, Transaction):
                try:
                    lower_date = self.query_one("#date_from", Input).value
                    upper_date = self.query_one("#date_to", Input).value
                    lower_price = self.query_one("#price_min", Input).value
                    upper_price = self.query_one("#price_max", Input).value
                    lower_yield = self.query_one("#yield_min", Input).value
                    upper_yield = self.query_one("#yield_max", Input).value
                    if lower_date and str(item.transaction_date) < lower_date:
                        continue
                    if upper_date and str(item.transaction_date) > upper_date:
                        continue
                    if lower_price and item.sale_price < float(lower_price):
                        continue
                    if upper_price and item.sale_price > float(upper_price):
                        continue
                    if lower_yield and (
                        item.reported_yield is None
                        or item.reported_yield < float(lower_yield) / 100
                    ):
                        continue
                    if upper_yield and (
                        item.reported_yield is None
                        or item.reported_yield > float(upper_yield) / 100
                    ):
                        continue
                except ValueError:
                    continue
            result.append(item)
        return result

    def _table(self, columns: list[str], rows: list[list[str]], records: Sequence) -> None:
        table = self.query_one("#table", DataTable)
        table.clear(columns=True)
        widths = {
            "Date": 12,
            "Address": 38,
            "Region": 18,
            "Sector": 18,
            "Price": 12,
            "Sale Price": 12,
            "Yield": 8,
            "$/Land m²": 12,
            "Buyer": 20,
            "Seller": 20,
            "Owner": 25,
            "Tenant": 20,
            "Land m²": 10,
            "Last sale": 12,
            "Type": 14,
            "Observation": 38,
            "Candidate": 38,
            "Match": 8,
            "Issue": 40,
            "Detail": 38,
        }
        for column in columns:
            table.add_column(column, width=widths.get(column, 16))
        for row in rows:
            table.add_row(*[str(value) for value in row])
        self.rows = list(records)
        table.display = True

    def show_page(self) -> None:
        title = self.query_one("#section_title", Static)
        summary = self.query_one("#summary", Static)
        panel = self.query_one("#import_panel", Vertical)
        panel.display = False
        table = self.query_one("#table", DataTable)
        table.display = True
        if self.page == "search":
            title.update("GLOBAL SEARCH")
            query = self.query_one("#search", Input).value.strip()
            if not query:
                summary.update(
                    "Type an address, owner, tenant, buyer or seller to search all records."
                )
                self._table(["Type", "Address", "Region", "Detail"], [], [])
            else:
                properties = self._filtered(self.session.scalars(select(Property)).all())
                transactions = self._filtered(self.session.scalars(select(Transaction)).all())
                records = [*properties[:50], *transactions[:50]]
                summary.update(
                    f"PROPERTIES  {len(properties)}      TRANSACTIONS  {len(transactions)}  ·  Enter inspect"
                )
                self._table(
                    ["Type", "Address", "Region", "Detail"],
                    [
                        [
                            "Property",
                            p.canonical_address,
                            p.region or "—",
                            p.owner_name or p.tenant_name or "—",
                        ]
                        for p in properties[:50]
                    ]
                    + [
                        [
                            "Transaction",
                            t.property.canonical_address,
                            t.property.region or "—",
                            f"{t.transaction_date}  {money(t.sale_price)}  {t.buyer_name or '—'}",
                        ]
                        for t in transactions[:50]
                    ],
                    records,
                )
        elif self.page == "overview":
            stats = overview(self.session)
            title.update("MARKET OVERVIEW")
            trend = "  ".join(
                f"{year} {count:3}" for year, count in sorted(stats["year_counts"].items())
            )
            sectors = "  ·  ".join(
                f"{name.replace('_', ' ').title()} {count}"
                for name, count in stats["sector_counts"].items()
            )
            summary.update(
                f"Properties  {stats['properties']:,}      Transactions  {stats['transactions']:,}      Tracked value  {money(stats['value'])}\nMedian sale  {money(stats['median_price'])}      Median yield  {pct(stats['median_yield'])} (n={stats['yield_count']})      Review  {stats['review']}\nMedian $/land m²  {money(stats['median_land_unit'])}      Median $/building m²  {money(stats['median_building_unit'])}\n\nTRANSACTION ACTIVITY  /  YEAR\n{trend}\n\nSECTOR ACTIVITY\n{sectors}\n\nRECENT TRANSACTIONS"
            )
            sales = self.session.scalars(
                select(Transaction).order_by(Transaction.transaction_date.desc()).limit(12)
            ).all()
            self._table(
                ["Date", "Address", "Sector", "Price", "Yield"],
                [
                    [
                        str(t.transaction_date),
                        t.property.canonical_address,
                        t.property.sector.replace("_", " "),
                        money(t.sale_price),
                        pct(t.reported_yield),
                    ]
                    for t in sales
                ],
                sales,
            )
        elif self.page == "transactions":
            title.update("TRANSACTIONS")
            sales = self._filtered(
                self.session.scalars(
                    select(Transaction).order_by(Transaction.transaction_date.desc())
                ).all()
            )
            if not self.sort_reverse:
                sales.reverse()
            summary.update(
                f"{len(sales)} transactions  ·  Enter inspect  ·  s sort  ·  e export"
                if sales
                else "No transactions match the current filters."
            )
            self._table(
                [
                    "Date",
                    "Address",
                    "Region",
                    "Sector",
                    "Sale Price",
                    "Yield",
                    "$/Land m²",
                    "Buyer",
                    "Seller",
                ],
                [
                    [
                        str(t.transaction_date),
                        t.property.canonical_address,
                        t.property.region or "—",
                        t.property.sector.replace("_", " "),
                        money(t.sale_price),
                        pct(t.reported_yield),
                        money(t.price_per_land_m2),
                        t.buyer_name or "—",
                        t.seller_name or "—",
                    ]
                    for t in sales
                ],
                sales,
            )
        elif self.page == "properties":
            title.update("PROPERTIES")
            props = self._filtered(
                self.session.scalars(select(Property).order_by(Property.canonical_address)).all()
            )
            if self.sort_reverse:
                props.reverse()
            summary.update(
                f"{len(props)} properties  ·  Enter research and comparables"
                if props
                else "No properties match the current filters."
            )
            rows = []
            for p in props:
                latest = (
                    max(p.transactions, key=lambda t: t.transaction_date)
                    if p.transactions
                    else None
                )
                rows.append(
                    [
                        p.canonical_address,
                        p.region or "—",
                        p.sector.replace("_", " "),
                        p.owner_name or "—",
                        p.tenant_name or "—",
                        f"{p.land_area_m2:,.0f}" if p.land_area_m2 else "—",
                        str(latest.transaction_date) if latest else "—",
                        money(latest.sale_price) if latest else "—",
                    ]
                )
            self._table(
                ["Address", "Region", "Sector", "Owner", "Tenant", "Land m²", "Last sale", "Price"],
                rows,
                props,
            )
        elif self.page == "quality":
            title.update("DATA QUALITY  /  REVIEW QUEUE")
            observations = self.session.scalars(
                select(RawObservation).where(RawObservation.status.in_(["REVIEW", "REJECTED"]))
            ).all()
            review = sum(o.status == "REVIEW" for o in observations)
            rejected = len(observations) - review
            quality_props = self.session.scalars(select(Property)).all()
            warnings = sum(
                bool(o.issues_json and '"warning"' in o.issues_json)
                for o in self.session.scalars(select(RawObservation))
            )
            suspicious = sum(
                t.reported_yield is not None and t.reported_yield > 0.2
                for t in self.session.scalars(select(Transaction))
            )
            summary.update(
                f"Potential duplicates  {review}      Validation warnings  {warnings}      Import errors  {rejected}\nMissing owner  {sum(not p.owner_name for p in quality_props)}      Missing tenant  {sum(not p.tenant_name for p in quality_props)}      Suspicious sales  {suspicious}\nEnter inspect  ·  M merge  ·  S separate"
                if observations
                else "No duplicate candidates require review."
            )
            self._table(
                ["Type", "Observation", "Candidate", "Match", "Issue"],
                [
                    [
                        o.status,
                        o.raw_address or "—",
                        (
                            candidate.canonical_address
                            if o.matched_property_id
                            and (candidate := self.session.get(Property, o.matched_property_id))
                            else "—"
                        ),
                        pct(o.match_score),
                        (json.loads(o.issues_json or "[]") or [{}])[0].get(
                            "message", "Potential duplicate"
                        ),
                    ]
                    for o in observations
                ],
                observations,
            )
        else:
            title.update("IMPORT  /  CSV OR XLSX")
            summary.update(
                "Choose a file, inspect the suggested column mapping and first 10 rows, then import."
            )
            table.display = False
            panel.display = True
            if not panel.children:
                panel.mount(
                    Horizontal(
                        Input(placeholder="/path/to/transactions.csv", id="import_file"),
                        Button("Load file", id="import_load"),
                    )
                )

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        if not self.rows:
            return
        item = self.rows[event.cursor_row]
        if isinstance(item, Transaction):
            t = item
            p = t.property
            self.push_screen(
                Detail(
                    f"TRANSACTION  /  {p.canonical_address}\n\nDate                 {t.transaction_date}\nSale price           {money(t.sale_price)}\nYield                {pct(t.reported_yield)}\nLand area            {t.land_area_m2 or '—'} m²\nBuilding area        {t.building_area_m2 or '—'} m²\nPrice / land m²      {money(t.price_per_land_m2)}\nPrice / building m²  {money(t.price_per_building_m2)}\nBuyer                {t.buyer_name or '—'}\nSeller               {t.seller_name or '—'}\nSource               {t.source.name if t.source else '—'}"
                )
            )
        elif isinstance(item, Property):
            self.subject = item
            history = sorted(item.transactions, key=lambda t: t.transaction_date, reverse=True)
            lines = [
                f"PROPERTY  /  {item.canonical_address}",
                f"{item.sector.replace('_', ' ')}  ·  {item.region or '—'}",
                "",
                f"Owner      {item.owner_name or '—'}",
                f"Tenant     {item.tenant_name or '—'}",
                f"Land       {item.land_area_m2:,.0f} m²" if item.land_area_m2 else "Land       —",
                f"Building   {item.building_area_m2:,.0f} m²"
                if item.building_area_m2
                else "Building   —",
                "",
                "TRANSACTION HISTORY",
            ]
            lines += [
                f"{t.transaction_date}   {money(t.sale_price):>10}   {pct(t.reported_yield):>7}   {t.source.name if t.source else '—'}"
                for t in history
            ] or ["No recorded transactions."]
            lines += ["", "COMPARABLE SALES  /  TOP FIVE"]
            for rank, (sale, score, evidence) in enumerate(comparables(self.session, item), 1):
                distance = (
                    f"{evidence['distance_km']:.1f} km"
                    if evidence["distance_km"] is not None
                    else "unknown distance"
                )
                lines.append(
                    f"{rank}. {sale.property.canonical_address}  ·  {money(sale.sale_price)}  ·  {pct(sale.reported_yield)}  ·  {score:.0%}"
                )
                lines.append(
                    f"   {distance}; land {evidence['land_difference']:.0%} diff; building {evidence['building_difference']:.0%} diff; {evidence['age_years']:.1f} years old; {'same' if evidence['same_sector'] else 'different'} sector"
                )
            self.push_screen(Detail("\n".join(lines)))
        elif isinstance(item, RawObservation):
            candidate = (
                self.session.get(Property, item.matched_property_id)
                if item.matched_property_id
                else None
            )
            issues = json.loads(item.issues_json or "[]")
            match_evidence = ""
            if candidate:
                try:
                    _, signals = match_score(
                        {
                            "address": item.raw_address,
                            "land_area_m2": parse_area(item.raw_land_area),
                            "tenant": item.raw_tenant,
                            "city": candidate.city,
                        },
                        candidate,
                    )
                    match_evidence = "\n".join(
                        f"{name.title():<15} {value:.0%}" for name, value in signals.items()
                    )
                except ValueError:
                    match_evidence = "Source area could not be parsed."
            body = (
                f"{'POTENTIAL DUPLICATE' if candidate else 'IMPORT ISSUE'}\n\nSOURCE OBSERVATION                  EXISTING PROPERTY\n{item.raw_address or '—':<35} {candidate.canonical_address if candidate else '—'}\n{item.raw_land_area or '—':<35} {f'{candidate.land_area_m2:,.0f} m²' if candidate and candidate.land_area_m2 else '—'}\n{item.raw_tenant or '—':<35} {candidate.tenant_name if candidate else '—'}\n\nMATCH EVIDENCE\n{match_evidence}\nOverall          {pct(item.match_score)}\n"
                + "\n".join(issue.get("message", "") for issue in issues)
            )
            self.push_screen(
                Detail(body, lambda merge: self._resolve(item, merge))
                if candidate
                else Detail(body)
            )

    def _resolve(self, item: RawObservation, merge: bool) -> None:
        try:
            resolve(self.session, item, merge)
            self.notify(
                "Observation merged." if merge else "Observation kept as a separate property."
            )
            self.show_page()
        except ValueError as exc:
            self.notify(f"Could not resolve observation: {exc}", severity="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "import_load":
            path = Path(self.query_one("#import_file", Input).value).expanduser()
            try:
                self.file_rows = read_rows(path)
                self.file_path = path
            except (OSError, ValueError, StopIteration) as exc:
                self.notify(f"Could not read {path.name}: {exc}", severity="error")
                return
            panel = self.query_one("#import_panel", Vertical)
            for child in list(panel.children)[1:]:
                child.remove()
            headers = list(self.file_rows[0]) if self.file_rows else []
            mapping = suggest_mapping(headers)
            for index, header in enumerate(headers):
                panel.mount(
                    Horizontal(
                        Label(header),
                        Select(
                            [("Skip", ""), *[(field, field) for field in FIELDS]],
                            value=mapping.get(header, ""),
                            id=f"map_{index}",
                        ),
                        classes="mapping",
                    )
                )
            preview = Table(title=f"PREVIEW  /  {len(self.file_rows)} rows; first 10 shown")
            for header in headers[:6]:
                preview.add_column(header[:20])
            for row in self.file_rows[:10]:
                preview.add_row(*[str(row.get(h) or "")[:20] for h in headers[:6]])
            panel.mount(Static(preview), Button("Import rows", id="import_commit"))
            self.notify(f"Loaded {len(self.file_rows)} rows. Check mapping before import.")
        elif event.button.id == "import_commit" and self.file_path:
            headers = list(self.file_rows[0]) if self.file_rows else []
            mapping = {
                header: str(value)
                for index, header in enumerate(headers)
                if (value := self.query_one(f"#map_{index}", Select).value)
            }
            if "address" not in mapping.values():
                self.notify("Map an address column before importing.", severity="error")
                return
            job = import_rows(self.session, self.file_rows, mapping, self.file_path.name)
            self.query_one("#summary", Static).update(
                f"IMPORT COMPLETE  /  {job.filename}\nRows received {job.records_received}  ·  Imported {job.records_imported}  ·  Review {job.records_flagged}  ·  Rejected {job.records_rejected}\nPress 4 to inspect the review queue."
            )
            self.notify("Import complete.")
