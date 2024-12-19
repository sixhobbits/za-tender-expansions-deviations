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
                tables = page.extract_tables({"snap_tolerance": 3, "join_tolerance": 0, "edge_min_length": 3, "min_words_vertical": 3, "min_words_horizontal": 1, "text_x_tolerance": 3, "text_y_tolerance": 0, "intersection_tolerance": 3})
                for table in tables:
                    for row in table:
                        csv_writer.writerow(row)

print("Conversion complete.")
