import csv
from datetime import datetime
from pathlib import Path

from customer_loader import load_customers
from entity_resolution import find_matches


PROJECT_DIR = Path(__file__).resolve().parent
SOURCE_A = PROJECT_DIR / "data" / "raw" / "source_a" / "customers.csv"
SOURCE_B = PROJECT_DIR / "data" / "raw" / "source_b" / "customers.csv"
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"
OUTPUT_FILE = PROCESSED_DIR / "entity_resolution_results.csv"
REPORT_FILE = PROCESSED_DIR / "data_quality_report.txt"


def find_duplicates(records, source_name):
    """Find duplicate customer details within one source."""
    seen_records = set()
    duplicate_count = 0

    for record in records:
        record_key = (
            record["full_name"].strip().lower(),
            record["date_of_birth"].strip(),
            record["city"].strip().lower()
        )

        if record_key in seen_records:
            duplicate_count += 1
            print(
                "DUPLICATE:",
                source_name,
                "| Customer ID:",
                record["customer_id"]
            )
        else:
            seen_records.add(record_key)

    if duplicate_count == 0:
        print("PASS:", source_name, "has no duplicate customer records.")
    else:
        print("Duplicates found in", source_name, ":", duplicate_count)

    return duplicate_count


def main():
    """Load, validate, match, and report customer records from both sources."""

    # Load customer records from both CSV sources.
    source_a_records = load_customers(SOURCE_A)
    source_b_records = load_customers(SOURCE_B)

    print("Source A records:", len(source_a_records))
    print("Source B records:", len(source_b_records))
    print("Total records:", len(source_a_records) + len(source_b_records))

    if source_a_records:
        print("\nFirst record from Source A:")
        print(source_a_records[0])

    if source_b_records:
        print("\nFirst record from Source B:")
        print(source_b_records[0])

    # Combine both sources for shared data-quality checks.
    all_records = source_a_records + source_b_records

    print("\nCombined dataset")
    print("Total combined records:", len(all_records))

    print("\nAll customer IDs:")
    for record in all_records:
        print(record["customer_id"])

    # Check for missing or blank values.
    print("\nData Quality Check")
    for record in all_records:
        for column, value in record.items():
            if value is None or str(value).strip() == "":
                print("Missing value found:", record.get("customer_id", "Unknown ID"), column)

    # Check whether customer IDs are unique across both sources.
    print("\nDuplicate Customer ID Check")
    customer_ids = [record["customer_id"] for record in all_records]

    if len(customer_ids) == len(set(customer_ids)):
        print("PASS: All customer IDs are unique.")
    else:
        print("FAIL: Duplicate customer IDs found.")

    # Validate required fields.
    print("\nRequired Field Validation")
    required_fields = ["customer_id", "full_name", "date_of_birth", "city"]
    invalid_record_count = 0

    for record in all_records:
        missing_fields = [
            field for field in required_fields
            if not record.get(field) or not str(record[field]).strip()
        ]

        if missing_fields:
            invalid_record_count += 1
            print(
                "INVALID record:",
                record.get("customer_id", "Unknown ID"),
                "| Missing fields:",
                ", ".join(missing_fields)
            )

    if invalid_record_count == 0:
        print("PASS: All records contain the required fields.")
    else:
        print("Records with missing required fields:", invalid_record_count)

    # Validate dates of birth using YYYY-MM-DD format.
    print("\nDate of Birth Validation")
    invalid_dob_count = 0

    for record in all_records:
        dob = str(record.get("date_of_birth", "")).strip()

        try:
            datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            invalid_dob_count += 1
            print(
                "INVALID date:",
                record.get("customer_id", "Unknown ID"),
                "| Date of birth:",
                dob
            )

    if invalid_dob_count == 0:
        print("PASS: All dates of birth are valid.")
    else:
        print("Records with invalid dates:", invalid_dob_count)

    # Find duplicate customer details within each source.
    print("\nWithin-Source Duplicate Check")
    source_a_duplicates = find_duplicates(source_a_records, "Source A")
    source_b_duplicates = find_duplicates(source_b_records, "Source B")

    # Find exact customer-detail duplicates across the two sources.
    print("\nCross-Source Duplicate Candidate Check")
    source_a_keys = {
        (
            record["full_name"].strip().lower(),
            record["date_of_birth"].strip(),
            record["city"].strip().lower()
        )
        for record in source_a_records
    }

    cross_source_duplicates = 0

    for record in source_b_records:
        record_key = (
            record["full_name"].strip().lower(),
            record["date_of_birth"].strip(),
            record["city"].strip().lower()
        )

        if record_key in source_a_keys:
            cross_source_duplicates += 1
            print(
                "POTENTIAL CROSS-SOURCE DUPLICATE:",
                record["customer_id"],
                "| Name:",
                record["full_name"]
            )

    print("\nDuplicate Check Summary")
    print("Source A duplicates:", source_a_duplicates)
    print("Source B duplicates:", source_b_duplicates)
    print("Cross-source duplicate candidates:", cross_source_duplicates)

    # Run entity resolution using the dedicated matching module.
    match_results = find_matches(source_a_records, source_b_records)

    # Ensure the output directory exists before writing result files.
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # Save entity-resolution results to a CSV file.
    fieldnames = [
        "source_a_id",
        "source_a_name",
        "source_b_id",
        "source_b_name",
        "date_of_birth",
        "city",
        "name_similarity_score",
        "classification"
    ]

    with open(OUTPUT_FILE, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(match_results)

    print("\nEntity Resolution Results")
    print("Candidate pairs saved:", len(match_results))
    print("Output file:", OUTPUT_FILE)

    # Summarize the match classifications.
    print("\nData Quality Summary Report")

    strong_match_count = sum(
        1 for result in match_results
        if result["classification"] == "STRONG MATCH"
    )
    manual_review_count = sum(
        1 for result in match_results
        if result["classification"] == "MANUAL REVIEW"
    )
    weak_match_count = sum(
        1 for result in match_results
        if result["classification"] == "WEAK MATCH"
    )

    print("Total candidate pairs:", len(match_results))
    print("Strong matches:", strong_match_count)
    print("Manual review:", manual_review_count)
    print("Weak matches:", weak_match_count)

    # Save the classification summary to a text report.
    report_lines = [
        "Data Quality Summary Report",
        f"Total candidate pairs: {len(match_results)}",
        f"Strong matches: {strong_match_count}",
        f"Manual review: {manual_review_count}",
        f"Weak matches: {weak_match_count}"
    ]

    with open(REPORT_FILE, mode="w", encoding="utf-8") as file:
        file.write("\n".join(report_lines) + "\n")

    print("\nQuality report saved to:", REPORT_FILE)


if __name__ == "__main__":
    main()
