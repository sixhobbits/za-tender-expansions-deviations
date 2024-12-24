import pdfplumber
import os
import csv

# List all PDF files in the specified directory
pdf_dir = "sharepoint_pdfs"
pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]

for pdf_file in pdf_files:
    with pdfplumber.open(os.path.join(pdf_dir, pdf_file)) as pdf:
        csv_file_name = f"{os.path.splitext(pdf_file)[0]}.csv"
        with open(csv_file_name, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            for page in pdf.pages:
                # Extract tables with specified tolerance
                table_settings = {
                        "snap_y_tolerance": 1, # prevents 2 rows being merged into one when they are too narrow
                        "text_y_tolerance": 0  # prevents corrupt text from combining two rows of text in same cell
                }

                tables = page.extract_tables(table_settings)
                for table in tables:
                    for row in table:
                        csv_writer.writerow(row)

print("Conversion complete.")
