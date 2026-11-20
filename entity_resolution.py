
from rapidfuzz.fuzz import ratio

# Define thresholds for classifying customer matches
STRONG_MATCH_THRESHOLD = 85
REVIEW_THRESHOLD = 60


def find_matches(source_a_records, source_b_records):
    """
    Compare customers from Source A and Source B.
    Match candidates using date of birth and city.
    Classify candidates using name similarity.
    """

    match_results = []

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

            # Calculate name similarity (0 to 100)
            name_score = ratio(
                record_a["full_name"].strip().lower(),
                record_b["full_name"].strip().lower()
            )

            # Process only candidates with matching DOB and city
            if dob_matches and city_matches:

                # Classify the candidate
                if name_score >= STRONG_MATCH_THRESHOLD:
                    classification = "STRONG MATCH"
                elif name_score >= REVIEW_THRESHOLD:
                    classification = "MANUAL REVIEW"
                else:
                    classification = "WEAK MATCH"

                # Store the matching details
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

    return match_results
