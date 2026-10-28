# Consumer Data Integration & Entity Resolution Pipeline

## Project Overview

A Python-based data engineering project that ingests customer records from two CSV data sources, validates data quality, identifies potential duplicate customers, and generates entity resolution results using fuzzy name matching.

This project uses synthetic customer data for demonstration and learning purposes.

## Features

- **Data Ingestion:** Reads customer records from two CSV sources.
- **Data Quality Validation:** Checks missing values, required fields, duplicate customer IDs, and date-of-birth validity.
- **Duplicate Detection:** Identifies records with matching customer details.
- **Entity Resolution:** Uses RapidFuzz to calculate name similarity scores.
- **Candidate Classification:** Categorizes potential matches as `STRONG MATCH`, `MANUAL REVIEW`, or `WEAK MATCH`.
- **CSV Output:** Saves candidate matching results to a processed CSV file.
- **Quality Reporting:** Generates a summary report in a text file.

## Technology Stack

- Python
- CSV data processing
- RapidFuzz
- Git and GitHub

## Project Structure

```text
consumer-entity-resolution/
├── data/
│   ├── raw/
│   │   ├── source_a/
│   │   │   └── customers.csv
│   │   └── source_b/
│   │       └── customers.csv
│   └── processed/
│       ├── entity_resolution_results.csv
│       └── data_quality_report.txt
├── ingest_data.py
├── main.py
└── requirements.txt
```

## How Entity Resolution Works

1. Load customer records from both source files.
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
git clone YOUR_GITHUB_REPOSITORY_URL
cd consumer-entity-resolution
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with the repository URL after publishing the project.

### 2. Create and activate a virtual environment

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the pipeline

```bash
python ingest_data.py
```

The processed results are written to:

- `data/processed/entity_resolution_results.csv`
- `data/processed/data_quality_report.txt`

## Current Scope and Limitations

This is a learning and portfolio project using a small synthetic dataset. The matching thresholds require further evaluation before real-world use. Matching based on date of birth, city, and name similarity can produce false positives and false negatives.

## Future Improvements

- Scale transformations using PySpark.
- Add automated unit tests.
- Improve match evaluation with labeled examples.
- Store and query records using a database such as MongoDB.
- Add logging, configuration management, and automated pipeline execution.

## Author

Developed as a data engineering portfolio project to practice data ingestion, data quality validation, and entity resolution.
