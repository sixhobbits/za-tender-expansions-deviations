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
    "period_quarter": "quarter",
    "period_quarter_use_dropdown_list": "quarter",
    "date_received_by_gmc_yyyy_mm_dd": "date_received_by_gmc",
    "rollover_new_use_dropdown_list": "rollover_or_new",
    "entity_department_use_dropdown_list": "entity_department",
    "project_description": "project_description",
    "supplier_service_provider": "supplier_service_provider",
    "value_of_deviation_r": "value_of_deviation",
    "valueofdeviatio_n_r": "value_of_deviation",
    "reason_for_deviation": "reason_for_deviation",
    "reason_for_deviation_use_dropdown_list": "reason_for_deviation",
    "not_supported_supported_conditi_onal_supported_use_dropdown_list": "supported",
    "supported_not_supported_noting_use_dropdown_list": "supported",
    "award_by_ao_aa_date_yyyy_mm_dd": "award_by_ao_aa_date",
    "award_recommende_d_by_ao_aa_date_yyyy_mm_dd": "award_by_ao_aa_date",
    "award_recommended_by_ao_aa_date_yyyy_mm_dd": "award_by_ao_aa_date",
    "contract_start_date_yyyy_mm_dd": "contract_start_date",
    "contract_expiry_yyyy_mm_dd": "contract_expiry",
    "status_use_dropdown_list": "status",
}
CSV_COLUMNS = [
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
    "award_by_ao_aa_date",
    "contract_start_date",
    "contract_expiry",
    "status",
    "supported",
    "rollover_or_new",
]
REQUIRED_FIELDS = {
    "quarter",
    "entity_department",
    "project_description",
    "supplier_service_provider",
    "value_of_deviation",
    "reason_for_deviation",
    "award_by_ao_aa_date",
    "contract_start_date",
}


def dump_image_page_settings(page: Page) -> Tuple[Page, Dict[str, Any]]:
    settings = {}
    im = page.to_image()
    im.debug_tablefinder(settings)
    im.save(f"page-{page.page_number}.png")
    return page, settings


def settings_2024_25_q1(page: Page) -> Tuple[Page, Dict[str, Any]]:
    settings = {}
    page = page.crop((0, 81, page.width - 130, page.height))
    return page, settings


def settings_2023_24_q4(page: Page) -> Tuple[Page, Dict[str, Any]]:
    settings = {}
    if page.page_number == 1:
        page = page.crop((0, 95, page.width, page.height))
    return page, settings



FILE_ARGS = {
    "pdfs/2024-2025_q1_deviation.pdf": {
        "skiprows": 0,
        "page_settings": settings_2024_25_q1,
    },
    "pdfs/2023-2024_q1_deviation.pdf": {
        "end_page": 13,
        "headers_per_page": False,
        "skiprows": 2,
        "page_settings": lambda page: (page, {"snap_y_tolerance": 2}),
    },
    "pdfs/2022-2023_q4_deviation.pdf": {
        "headers_per_page": False,
        "skiprows": 0,
        "page_settings": settings_2023_24_q4,
    },
    "pdfs/2022-2023_q3_deviation.pdf": {"headers_per_page": False, "skiprows": 2},
}


def map_keys(row: Dict[str, str]) -> Dict[str, str]:
    new_row = {}
    for key, value in row.items():
        new_key = KEY_MAPPING.get(key, key)
        assert new_key not in new_row, f"Duplicate key: {new_key}"
        new_row[new_key] = value
    return new_row


def assert_required_fields(row: Dict[str, str]):
    missing_fields = REQUIRED_FIELDS - set(row.keys())
    assert (
        not missing_fields
    ), f"Missing fields: {missing_fields}. Available fields: {row.keys()}"


def assert_row_number(row: Dict[str, str], last_row_number: int) -> int:
    row_number = int(row["row_number"])
    assert row_number == last_row_number + 1, f"Row number not sequential: {row_number}"
    return row_number


def extract_file(pdf_path: Path):
    csv_file_name = f"{pdf_path.stem}.csv"
    with open(csv_file_name, "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        parse_pdf_args = {
            "skiprows": 1,
            "headers_per_page": True,
        }
        parse_pdf_args.update(FILE_ARGS.get(str(pdf_path), {}))
        last_row_number = 0
        for row in parse_pdf_table(pdf_path, **parse_pdf_args):
            row = map_keys(row)

            if row.get("row_number").lower() == "deviations report":
                continue
            if not row.get("entity_department") and not row.get("project_description"):
                continue

            assert_required_fields(row)
            last_row_number = assert_row_number(row, last_row_number)

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
