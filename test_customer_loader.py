
import unittest
import tempfile
from pathlib import Path

from customer_loader import load_customers


class TestCustomerLoader(unittest.TestCase):

    def test_load_valid_csv(self):
        # Create a temporary CSV file with one customer
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "customers.csv"

            csv_path.write_text(
                "customer_id,full_name,date_of_birth,city\n"
                "A001,Riya Sharma,1995-04-12,Pune\n",
                encoding="utf-8"
            )

            records = load_customers(csv_path)

            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]["customer_id"], "A001")

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "missing.csv"

            with self.assertRaises(FileNotFoundError):
                load_customers(csv_path)

    def test_empty_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "empty.csv"
            csv_path.write_text("", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "empty or missing headers"):
                load_customers(csv_path)

    def test_csv_with_headers_but_no_records(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "no_records.csv"

            csv_path.write_text(
                "customer_id,full_name,date_of_birth,city\n",
                encoding="utf-8"
            )

            with self.assertRaisesRegex(ValueError, "no customer records"):
                load_customers(csv_path)


if __name__ == "__main__":
    unittest.main()
