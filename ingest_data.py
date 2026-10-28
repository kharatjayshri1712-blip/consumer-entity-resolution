
import csv
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent

SOURCE_A = PROJECT_DIR / "data" / "raw" / "source_a" / "customers.csv"
SOURCE_B = PROJECT_DIR / "data" / "raw" / "source_b" / "customers.csv"


def load_customers(file_path):
    with open(file_path, mode="r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        records = list(reader)

    return records


source_a_records = load_customers(SOURCE_A)
source_b_records = load_customers(SOURCE_B)

print("Source A records:", len(source_a_records))
print("Source B records:", len(source_b_records))
print("Total records:", len(source_a_records) + len(source_b_records))

print("\nFirst record from Source A:")
print(source_a_records[0])

print("\nFirst record from Source B:")
print(source_b_records[0])


all_records = source_a_records + source_b_records

print("\nCombined dataset")
print("Total combined records:", len(all_records))

print("\nAll customer IDs:")
for record in all_records:
    print(record["customer_id"])

print("\nData Quality Check")

for record in all_records:
    for column, value in record.items():
        if value is None or value.strip() == "":
            print("Missing value found:", record["customer_id"], column)


# Display a heading for the duplicate customer ID validation
print("\nDuplicate Customer ID Check")

# Extract the customer ID from every record in the combined dataset
customer_ids = [record["customer_id"] for record in all_records]

# Compare the total number of IDs with the number of unique IDs
if len(customer_ids) == len(set(customer_ids)):
    # If both counts match, no duplicate IDs exist
    print("PASS: All customer IDs are unique.")
else:
    # If the counts differ, at least one duplicate ID exists
    print("FAIL: Duplicate customer IDs found.")


# Display a heading for the exact-match candidate check
print("\nExact-Match Candidate Check")

# Compare records from Source A against records from Source B
for record_a in source_a_records:
    for record_b in source_b_records:

        # Check whether the date of birth and city match
        if (
                record_a["date_of_birth"] == record_b["date_of_birth"]
                and record_a["city"].strip().lower()
                == record_b["city"].strip().lower()
        ):
            # Display the IDs of records that match on these two fields
            print(
                "Potential match:",
                record_a["customer_id"],
                "and",
                record_b["customer_id"]
            )


# Display a heading for the exact-match candidate check
print("\nExact-Match Candidate Check")

# Compare each Source A record with each Source B record
for record_a in source_a_records:
    for record_b in source_b_records:

        # Check whether the date of birth and city match
        dob_matches = (
                record_a["date_of_birth"] == record_b["date_of_birth"]
        )
        city_matches = (
                record_a["city"].strip().lower()
                == record_b["city"].strip().lower()
        )

        # Check whether the full names match exactly, ignoring case
        name_matches = (
                record_a["full_name"].strip().lower()
                == record_b["full_name"].strip().lower()
        )

        # Report candidates when date of birth and city both match
        if dob_matches and city_matches:
            print(
                "Source A:", record_a["customer_id"],
                "| Name:", record_a["full_name"],
                "|| Source B:", record_b["customer_id"],
                "| Name:", record_b["full_name"],
                "| Exact name match:", name_matches
            )


# Import the function used to calculate name similarity
from rapidfuzz.fuzz import ratio

# Display a heading for the name similarity check
print("\nName Similarity Check")

# Compare each customer record from Source A with Source B
for record_a in source_a_records:
    for record_b in source_b_records:

        # Check whether date of birth and city match
        dob_matches = (
                record_a["date_of_birth"] == record_b["date_of_birth"]
        )
        city_matches = (
                record_a["city"].strip().lower()
                == record_b["city"].strip().lower()
        )

        # Calculate name similarity as a score from 0 to 100
        name_score = ratio(
            record_a["full_name"].strip().lower(),
            record_b["full_name"].strip().lower()
        )

        # Show scores only when date of birth and city match
        if dob_matches and city_matches:
            print(
                record_a["customer_id"],
                "<->",
                record_b["customer_id"],
                "| Name score:",
                round(name_score, 2)
            )



# Import CSV support so we can save the results to a file
import csv

# Import Path to build a reliable output file path
from pathlib import Path

# Define the output location for the entity resolution results
PROJECT_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = PROJECT_DIR / "data" / "processed" / "entity_resolution_results.csv"

# Define the initial thresholds for classifying name similarity
STRONG_MATCH_THRESHOLD = 85
REVIEW_THRESHOLD = 60

# Create an empty list to collect the matching results
match_results = []

# Compare each Source A record with each Source B record
for record_a in source_a_records:
    for record_b in source_b_records:

        # Check whether the date of birth and city match
        dob_matches = (
                record_a["date_of_birth"] == record_b["date_of_birth"]
        )
        city_matches = (
                record_a["city"].strip().lower()
                == record_b["city"].strip().lower()
        )

        # Calculate name similarity on a scale from 0 to 100
        name_score = ratio(
            record_a["full_name"].strip().lower(),
            record_b["full_name"].strip().lower()
        )

        # Process only candidates whose date of birth and city match
        if dob_matches and city_matches:

            # Classify the candidate using the name similarity score
            if name_score >= STRONG_MATCH_THRESHOLD:
                classification = "STRONG MATCH"
            elif name_score >= REVIEW_THRESHOLD:
                classification = "MANUAL REVIEW"
            else:
                classification = "WEAK MATCH"

            # Store the candidate details as a dictionary
            match_results.append({
                "source_a_id": record_a["customer_id"],
                "source_a_name": record_a["full_name"],
                "source_b_id": record_b["customer_id"],
                "source_b_name": record_b["full_name"],
                "date_of_birth": record_a["date_of_birth"],
                "city": record_a["city"],
                "name_similarity_score": round(name_score, 2),
                "classification": classification
            })

# Open the output CSV file for writing
with open(OUTPUT_FILE, mode="w", encoding="utf-8", newline="") as file:

    # Define the column names for the output CSV
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

    # Create a CSV writer that writes dictionaries as rows
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    # Write the header row first
    writer.writeheader()

    # Write all candidate results into the CSV file
    writer.writerows(match_results)

# Confirm that the results were saved successfully
print("\nEntity Resolution Results")
print("Candidate pairs saved:", len(match_results))
print("Output file:", OUTPUT_FILE)


# Display a heading for the classification summary report
print("\nData Quality Summary Report")

# Count how many candidate pairs belong to each classification
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

# Display the total number of candidate pairs processed
print("Total candidate pairs:", len(match_results))

# Display the count for each classification
print("Strong matches:", strong_match_count)
print("Manual review:", manual_review_count)
print("Weak matches:", weak_match_count)


# Define the file path where the quality report will be saved
REPORT_FILE = PROJECT_DIR / "data" / "processed" / "data_quality_report.txt"

# Create a list of report lines using the calculated summary values
report_lines = [
    "Data Quality Summary Report",
    f"Total candidate pairs: {len(match_results)}",
    f"Strong matches: {strong_match_count}",
    f"Manual review: {manual_review_count}",
    f"Weak matches: {weak_match_count}"
]

# Open the report file in write mode
with open(REPORT_FILE, mode="w", encoding="utf-8") as file:

    # Write each report line on a separate line
    file.write("\n".join(report_lines) + "\n")

# Confirm where the report was saved
print("\nQuality report saved to:", REPORT_FILE)


# Display a heading for required-field validation
print("\nRequired Field Validation")

# Define the fields that every customer record must contain
required_fields = [
    "customer_id",
    "full_name",
    "date_of_birth",
    "city"
]

# Track how many records have missing required fields
invalid_record_count = 0

# Check every customer record in the combined dataset
for record in all_records:

    # Store the names of required fields that are missing or blank
    missing_fields = [
        field for field in required_fields
        if not record.get(field) or not record[field].strip()
    ]

    # Report records that have missing required fields
    if missing_fields:
        invalid_record_count += 1
        print(
            "INVALID record:",
            record.get("customer_id", "Unknown ID"),
            "| Missing fields:",
            ", ".join(missing_fields)
        )

# Print a summary of the validation results
if invalid_record_count == 0:
    print("PASS: All records contain the required fields.")
else:
    print("Records with missing required fields:", invalid_record_count)


# Import date utilities to validate calendar dates
from datetime import datetime

# Display a heading for date-of-birth validation
print("\nDate of Birth Validation")

# Count records that contain invalid dates
invalid_dob_count = 0

# Check the date of birth in every customer record
for record in all_records:
    dob = record.get("date_of_birth", "").strip()

    # Attempt to parse the date using the required YYYY-MM-DD format
    try:
        datetime.strptime(dob, "%Y-%m-%d")

    # Handle missing or incorrectly formatted calendar dates
    except ValueError:
        invalid_dob_count += 1
        print(
            "INVALID date:",
            record.get("customer_id", "Unknown ID"),
            "| Date of birth:",
            dob
        )

# Print the date validation summary
if invalid_dob_count == 0:
    print("PASS: All dates of birth are valid.")
else:
    print("Records with invalid dates:", invalid_dob_count)



# Display a heading for duplicate-record validation
print("\nDuplicate Record Check")

# Track the customer details already seen in each source
seen_records = set()

# Count duplicate records found in the combined dataset
duplicate_record_count = 0

# Examine every customer record from both sources
for record in all_records:

    # Normalize customer details to make comparisons consistent
    record_key = (
        record["full_name"].strip().lower(),
        record["date_of_birth"].strip(),
        record["city"].strip().lower()
    )

    # Check whether these customer details have appeared before
    if record_key in seen_records:
        duplicate_record_count += 1
        print(
            "POTENTIAL DUPLICATE:",
            record["customer_id"],
            "| Name:",
            record["full_name"]
        )
    else:
        # Remember these details for subsequent comparisons
        seen_records.add(record_key)

# Print the duplicate-record validation summary
if duplicate_record_count == 0:
    print("PASS: No duplicate customer details found.")
else:
    print("Potential duplicate records found:", duplicate_record_count)
