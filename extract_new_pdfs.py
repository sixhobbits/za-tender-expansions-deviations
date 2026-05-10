import re
from pathlib import Path
import pdfplumber


def normalize_header(text):
    text = (text or "").strip().lower()
    text = text.replace("(", "").replace(")", "")
    text = re.sub(r"[/\s\n]+", "_", text)
    text = text.strip("_")
    # collapse multiple underscores
    text = re.sub(r"_+", "_", text)
    return text


def is_header_row(row):
    first = (row[0] or "").strip().lower()
    return first == "number"


def is_banner_row(row):
    first = (row[0] or "").strip().lower()
    return first in ["deviations report", "expansions report"]


def extract_pdf(pdf_path: Path, crop: int = 50):
    csv_path = pdf_path.with_suffix(".csv")
    print(f"Extracting {pdf_path} -> {csv_path}")

    rows_out = []
    headers = None

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            cropped = page.crop((0, crop, page.width, page.height))
            table = cropped.extract_table()
            if not table:
                continue

            for row in table:
                if not any(cell and cell.strip() for cell in row):
                    continue
                if is_banner_row(row):
                    continue
                if is_header_row(row):
                    headers = [normalize_header(cell) for cell in row]
                    continue
                if headers is None:
                    continue

                mapped = {}
                for i, cell in enumerate(row):
                    if i >= len(headers):
                        break
                    header = headers[i]
                    if not header:
                        continue
                    mapped[header] = (cell or "").strip()
                rows_out.append(mapped)

    if not rows_out:
        print(f"  No data extracted from {pdf_path}")
        return

    # Use all unique keys from extracted data as columns
    all_keys = []
    seen = set()
    for row in rows_out:
        for k in row:
            if k not in seen:
                seen.add(k)
                all_keys.append(k)

    with open(csv_path, "w", newline="") as f:
        import csv
        writer = csv.DictWriter(f, fieldnames=all_keys)
        writer.writeheader()
        writer.writerows(rows_out)

    print(f"  Extracted {len(rows_out)} rows with columns: {all_keys}")


def main():
    new_pdfs = [
        "pdfs/2024-2025_q3_deviation.pdf",
        "pdfs/2024-2025_q3_expansion.pdf",
        "pdfs/2024-2025_q4_deviation.pdf",
        "pdfs/2024-2025_q4_expansion.pdf",
        "pdfs/2025-2026_q1_deviation.pdf",
        "pdfs/2025-2026_q1_expansion.pdf",
    ]
    for pdf in new_pdfs:
        extract_pdf(Path(pdf))


if __name__ == "__main__":
    main()
