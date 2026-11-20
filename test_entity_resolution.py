
import unittest

from entity_resolution import find_matches


class TestEntityResolution(unittest.TestCase):

    def test_exact_name_match(self):
        source_a = [
            {
                "customer_id": "A001",
                "full_name": "Amit Patil",
                "date_of_birth": "1995-04-12",
                "city": "Pune"
            }
        ]

        source_b = [
            {
                "customer_id": "B001",
                "full_name": "Amit Patil",
                "date_of_birth": "1995-04-12",
                "city": "Pune"
            }
        ]

        results = find_matches(source_a, source_b)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["classification"], "STRONG MATCH")
        self.assertEqual(results[0]["name_similarity_score"], 100.0)




    def test_spelling_difference_strong_match(self):
        source_a = [
            {
                "customer_id": "A002",
                "full_name": "Riya Sharma",
                "date_of_birth": "1995-04-12",
                "city": "Pune"
            }
        ]

        source_b = [
            {
                "customer_id": "B002",
                "full_name": "Riya Sahrma",
                "date_of_birth": "1995-04-12",
                "city": "Pune"
            }
        ]

        results = find_matches(source_a, source_b)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["classification"], "STRONG MATCH")
        self.assertAlmostEqual(
            results[0]["name_similarity_score"], 90.91, places=2
        )


    def test_manual_review_match(self):
        source_a = [
            {
                "customer_id": "A003",
                "full_name": "Neha Kulkarni",
                "date_of_birth": "1995-04-12",
                "city": "Pune"
            }
        ]

        source_b = [
            {
                "customer_id": "B003",
                "full_name": "Neha K",
                "date_of_birth": "1995-04-12",
                "city": "Pune"
            }
        ]

        results = find_matches(source_a, source_b)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["classification"], "MANUAL REVIEW")
        self.assertAlmostEqual(
            results[0]["name_similarity_score"], 63.16, places=2
        )


    def test_different_date_of_birth_returns_no_match(self):
        source_a = [
            {
                "customer_id": "A004",
                "full_name": "Amit Patil",
                "date_of_birth": "1995-04-12",
                "city": "Pune"
            }
        ]

        source_b = [
            {
                "customer_id": "B004",
                "full_name": "Amit Patil",
                "date_of_birth": "1996-04-12",
                "city": "Pune"
            }
        ]

        results = find_matches(source_a, source_b)

        self.assertEqual(len(results), 0)


    def test_different_city_returns_no_match(self):
        source_a = [
            {
                "customer_id": "A005",
                "full_name": "Amit Patil",
                "date_of_birth": "1995-04-12",
                "city": "Pune"
            }
        ]

        source_b = [
            {
                "customer_id": "B005",
                "full_name": "Amit Patil",
                "date_of_birth": "1995-04-12",
                "city": "Mumbai"
            }
        ]

        results = find_matches(source_a, source_b)

        self.assertEqual(len(results), 0)



if __name__ == "__main__":
    unittest.main()


