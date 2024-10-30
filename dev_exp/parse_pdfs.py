import os
from csv import DictWriter
from pathlib import Path
from sys import argv
from typing import Any, Dict, List, Tuple
from pdfplumber.page import Page

from .pdf import parse_pdf_table

# Here, different headings from different files can be mapped to the same column names
KEY_MAPPING = {
    "number": "row_number",
    "period_quarter_use_dropdown_list": "quarter",
    "": "",
    "date_received_by_gmc_yyyy_mm_dd": "date_received_by_gmc",
    "entity_department_use_dropdown_list": "entity_department",
    "project_description": "project_description",
    "supplier_service_provider": "supplier_service_provider",
    "value_of_deviation_r": "value_of_deviation",
    "reason_for_deviation": "reason_for_deviation",
    "award_by_ao_aa_date_yyyy_mm_dd": "award_by_ao_aa_date",
    "contract_start_date_yyyy_mm_dd": "contract_start_date",
    "contract_expiry_yyyy_mm_dd": "contract_expiry",
    "status_use_dropdown_list": "status",
}
FIELD_NAMES = [
    "row_number",
    "quarter",
    "date_received_by_gmc",
    "entity_department",
    "project_description",
    "supplier_service_provider",
    "value_of_deviation",
    "reason_for_deviation",
    "award_by_ao_aa_date",
    "contract_start_date",
    "contract_expiry",
    "status",
    "",
]


def map_keys(row: Dict[str, str]) -> Dict[str, str]:
    return {KEY_MAPPING.get(k, k): v for k, v in row.items()}


def page_settings(page: Page) -> Tuple[Page, Dict[str, Any]]:
    settings = {}
    # im = page.to_image()
    # im.debug_tablefinder(settings)
    # im.save(f"page-{page.page_number}.png")
    return page, settings


def extract_file(pdf_path: Path):
    csv_file_name = f"{pdf_path.stem}.csv"
    with open(csv_file_name, "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=FIELD_NAMES)
        writer.writeheader()
        for row in parse_pdf_table(
            pdf_path,
            skiprows=1,
            headers_per_page=True,
            page_settings=page_settings,
        ):
            row = map_keys(row)
            if not row.get("entity_department") and not row.get("project_description"):
                continue

            writer.writerow(row)


def main(paths: List[str]):
    pdf_files = [Path(p) for p in paths]
    if not pdf_files:
        pdf_files = [
            Path(f"pdfs/{f}") for f in os.listdir("pdfs") if f.endswith(".pdf")
        ]
    for pdf_file in pdf_files:
        extract_file(pdf_file)
    print("Conversion complete.")


if __name__ == "__main__":
    paths = argv[1:]
    main(paths)
