
import csv


def load_customers(file_path):
    try:
        # Open the CSV file
        with open(file_path, mode="r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)

            # Check whether the CSV file contains headers
            if reader.fieldnames is None:
                raise ValueError("CSV file is empty or missing headers.")

            # Read all customer records
            records = list(reader)

            # Check whether the CSV contains customer records
            if not records:
                raise ValueError("CSV file contains no customer records.")

            return records

    except FileNotFoundError:
        raise FileNotFoundError(f"Source file not found: {file_path}")

    except PermissionError:
        raise PermissionError(f"Permission denied while reading: {file_path}")
