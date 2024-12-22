# South Africa Tenders Expansions and Deviations

When tenders are expanded or deviated from, that is meant to be documented here http://ocpo.treasury.gov.za/Suppliers_Area/Pages/Deviations-and-Exspansions.aspx.

This links to a bunch of PDF files that have some data about who expanded or deviated from what tender, and how much that expansion was worth.

Some of this data looks a bit suspect. See https://x.com/sajournalist/status/1851565521176604776 for some context.

This project's goal is to 

* Scrape the PDFs from that site
* Extract the data into something more standard
* Analyse it to look for anything weird or interesting

# Installation

    python -m venv env
    source env/bin/activate
    pip install -r requirements.txt


# Running

## Extracting tabular data from PDFs

If you don't give paths to PDFs as arguments, it will extract all PDFs in the pdfs directory.

    python -m dev_exp.parse_pdfs


## Manual sheets

* Here's one [manually cleaned Google Sheet](https://docs.google.com/spreadsheets/d/10EyyN1siQEyB-KAEvoTIsGCRPI5kRScZ39RT2iadoR8/edit?gid=1446977861#gid=1446977861) with some stats

e.g. it lets us filter by keyword in project and see that correctional services spent R4M more on toothbrushes (in a single quarter) than they planned, contracts awarded to various small businesses.

![screenshot 2024-11-05 at 12 54 35@2x](https://github.com/user-attachments/assets/4334c818-4c57-48e3-b2a4-5de2d9d9cb69)


## Loading data into database

The data can be loaded all into one table by running the following command once for each file.

    csvsql --insert --create-if-not-exists --no-constraints  --tables deviations --db sqlite:///deviations.db 2024-2025_q2_deviation.csv


## Exploring the data

The data can be explored using datasette by running

    datasette serve deviations.db


## Current status

* the `scrape_deviations_expansions.py` pulls down the PDFs and saves them with standard names

* The `parse_pdfs.py` script extracts CSVs, using pdfplumber, but these are still very messy with incorrect headings, lack of standarization etc. This script needs to be updated to produce better and more standard CSVs.


## Slack conversation

We're on ZATech slack in #tender-data, which started on [this thread](https://zatech.slack.com/archives/CG4HBE0NB/p1730291620057199).

## Contributing

However you can - looking for help for automated cleaning, manual cleaning, data analysis, etc.

Also interesting to look up the company information on BizPortal and find director information and see if there are links to anything else dodgy.

Feel free to open PRs, open issues, or if you have time and want to contribute but aren't sure how then let me know here or on Slack what your skills are and we can figure it out.

## License

MIT
