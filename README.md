# Consumer Data Integration & Entity Resolution Pipeline

## Project Overview

A Python-based data engineering project that ingests customer records from two CSV data sources, validates data quality, identifies potential duplicate customers, and generates entity resolution results using fuzzy name matching.

This project uses synthetic customer data for demonstration and learning purposes.

## Features

- **Data Ingestion:** Reads customer records from two CSV sources.
- **Data Quality Validation:** Checks missing values, required fields, duplicate customer IDs, and date-of-birth validity.
- **Duplicate Detection:** Identifies duplicate customer details within and across data sources.
- **Entity Resolution:** Uses RapidFuzz to calculate name similarity scores.
- **Candidate Classification:** Categorizes potential matches as `STRONG MATCH`, `MANUAL REVIEW`, or `WEAK MATCH`.
- **CSV Output:** Saves candidate matching results to a processed CSV file.
- **Quality Reporting:** Generates a summary report in a text file.
- **Unit Testing:** Includes automated tests for CSV loading and entity resolution.

## Technology Stack

- Python
- CSV data processing
- RapidFuzz
- unittest
- Git and GitHub

## Project Structure

```text
consumer-entity-resolution/
│
├── data/
│   ├── raw/
│   │   ├── source_a/
│   │   │   └── customers.csv
│   │   └── source_b/
│   │       └── customers.csv
│   └── processed/
│       ├── entity_resolution_results.csv
│       └── data_quality_report.txt
│
├── customer_loader.py
├── entity_resolution.py
├── ingest_data.py
├── main.py
├── test_customer_loader.py
├── test_entity_resolution.py
├── requirements.txt
├── .gitignore
└── README.md
```

## How Entity Resolution Works

1. Load customer records from both CSV sources.
2. Validate required fields and selected data quality rules.
3. Compare records using date of birth and city to identify candidate pairs.
4. Calculate name similarity using RapidFuzz.
5. Classify candidate pairs using configurable similarity thresholds.
6. Export candidate results and a data quality summary.

### Initial Matching Rules

- Similarity score of 85 or higher: `STRONG MATCH`
- Similarity score from 60 to below 85: `MANUAL REVIEW`
- Similarity score below 60: `WEAK MATCH`

These are initial demonstration thresholds, not universal matching standards. A strong match is a candidate for review, not proof of identity.

## Setup and Execution

### 1. Clone the repository

```bash
git clone https://github.com/kharatjayshri1712-blip/consumer-entity-resolution.git
cd consumer-entity-resolution
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the pipeline

```bash
python main.py
```

The pipeline generates the following files:

- `data/processed/entity_resolution_results.csv`
- `data/processed/data_quality_report.txt`

### 5. Run automated tests

```bash
python -m unittest discover -v
```

The project currently includes 9 automated unit tests covering CSV loading, missing and empty files, exact matches, spelling differences, manual review cases, and mismatched customer details.

## Sample Results

Using the sample synthetic customer datasets:

- Source A records: 5
- Source B records: 5
- Total records: 10
- Candidate pairs identified: 4
- Strong matches: 3
- Manual review: 1
- Weak matches: 0

All 9 automated unit tests passed in the current project version.

## Current Scope and Limitations

This is a learning and portfolio project using a small synthetic dataset. The matching thresholds require further evaluation before real-world use.

Matching based on date of birth, city, and name similarity can produce false positives and false negatives. Candidate matches should be reviewed before treating records as the same customer.

Generated output files are excluded from Git and are recreated when the pipeline runs.

## Future Improvements

- Scale transformations using PySpark.
- Improve match evaluation with labeled examples.
- Store and query records using a database such as MongoDB.
- Add logging and configuration management.
- Implement automated pipeline execution.

## Author

Developed as a data engineering portfolio project to practice data ingestion, data quality validation, Python programming, automated testing, and entity resolution.