# South Africa Tenders Expansions and Deviations

When tenders are expanded or deviated from, that is meant to be documented here http://ocpo.treasury.gov.za/Suppliers_Area/Pages/Deviations-and-Exspansions.aspx.

This links to a bunch of PDF files that have some data about who expanded or deviated from what tender, and how much that expansion was worth.

Some of this data looks a bit suspect. See https://x.com/sajournalist/status/1851565521176604776 for some context.

This project's goal is to 

* Scrape the PDFs from that site
* Extract the data into something more standable 
* Analyse it to look for anything weird or interesting

## Current status

* the `scrape_deviations_expansions.py` pulls down the PDFs and saves them with standard names

* The `parse_pdfs.py` script extracts CSVs, using pdfplumber, but these are still very messy with incorrect headings, lack of standarization etc. This script needs to be updated to produce better and more standard CSVs.
