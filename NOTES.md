# Notes on Eskom Diesel Tender Cross-Reference

## Context

These notes document a cross-reference between the [amaBhungane investigation into Eskom's R21-billion diesel contract](https://amabhungane.org/inside-eskoms-dodgy-r21-billion-diesel-contract/) and the public deviations/expansions data published by National Treasury.

## Key Findings from Deviations Data

### Astron Emergency Procurement (Jan 2025)

**File:** `pdfs/2024-2025_q4_deviation.pdf` (Entry 180, 20 Jan 2025)

> *"On 1 January 2025 an urgent situation arose for Ankerlig Power Station due the previous Diesel contracts expiring on 31 December 2025... The Supply and Delivery of Diesel 50ppm to Ankerlig Power Station. Astron Energy (Pty) Ltd — R208,610,000.00"*

This matches the amaBhungane report exactly — the emergency memo to Treasury when the new contracts weren't ready. The deviation record states:
- A 5-year contract had "already been made to Astron Energy by the Generation Board"
- The contract was not yet signed due to "availability of delegated authorities"
- Astron was the "only contractor in a position to deliver"

### Itsamaya Holdings Forensic Investigation

**File:** `pdfs/2025-2026_q1_deviation.pdf` (Page 16)

> *"across Eskom Holdings Itsamaya Holdings (Pty) Ltd"*

Itsamaya is the forensic firm appointed by Eskom in March 2025 to investigate the diesel tender (the RAPTOR investigation referenced in the amaBhungane article). It appears in the Q1 2025/26 deviations as an approved supplier.

### Other Diesel-Related Deviations in Same Period

- **Q4 2024-25:** R44.2m to "Women Of Africa Fuels" for Arnot Power Station
- **Q4 2024-25:** R86.5m to "WOA Fuels and Oils" for Kriel/Arnot/Duvha
- **Q1 2025-26:** R52.6m diesel for Arnot (depleted fuel oil stock)
- **Q1 2025-26:** R15.9m diesel for Transtech Afrika

## What's Missing

The **actual R21-billion tender award to Nutinox, Severino, and Lanele** does **not** appear in deviations/expansions data. This is expected — it was supposedly a properly tendered contract (MWP2197GX), not an emergency deviation.

## Data Updates in This Commit

- Fixed `scrape_deviations_expansions.py` to point to the correct Treasury subfolder URL (`/Suppliers_Area/Deviations%20and%20Exspansions/default.aspx`)
- Added new quarters:
  - Q3 2024-25 deviations & expansions
  - Q4 2024-25 deviations & expansions
  - Q1 2025-26 deviations & expansions
- Added `extract_new_pdfs.py` — a simpler extraction script for quarters where the main `parse_pdfs.py` script fails due to dependency issues

## Next Steps for Investigation

To fully trace the diesel tender, someone would need to cross-reference with:
- **Eskom's internal tender register** for MWP2197GX
- **National Treasury eTender portal** (the original advert from October 2023)
- **CIPC company records** for director changes at Severino, Nutinox, and Lanele
- **Eskom annual financial statements** for prepayment disclosures
