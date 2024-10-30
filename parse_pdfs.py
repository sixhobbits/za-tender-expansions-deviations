
import pdfplumber
import os
import csv

# List all PDF files in the current directory
pdf_files = [f for f in os.listdir("pdfs") if f.endswith('.pdf')]

for pdf_file in pdf_files:
    with pdfplumber.open(os.path.join("pdfs", pdf_file)) as pdf:
        csv_file_name = f"{os.path.splitext(pdf_file)[0]}.csv"
        with open(csv_file_name, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        csv_writer.writerow(row)

print("Conversion complete.")
