import unittest
from unittest.mock import patch
from datetime import date
from src.random_data import random_date

class TestRandomDate(unittest.TestCase):
    def test_random_date_return_date(self):
        result = random_date()
        self.assertIsInstance(result, date)

    def test_random_date_range(self):
        for i in range(100):
            d = random_date(2000, 2020)
            self.assertIn(d.year, range(2000, 2021))
            self.assertIn(d.month, range(1, 13))
            self.assertGreaterEqual(d.day, 1)
            self.assertLessEqual(d.day, 31)

    def test_random_date_values(self):
        with patch('random.randint') as mock_randint:
            mock_randint.side_effect = [2023, 2, 28]
            d = random_date()
            self.assertEqual(d, date(2023, 2, 28))

            mock_randint.side_effect = [2024, 2, 29]
            d = random_date()
            self.assertEqual(d, date(2024, 2, 29))

            mock_randint.side_effect = [2023, 4, 30]
            d = random_date()
            self.assertEqual(d, date(2023, 4, 30))

            mock_randint.side_effect = [2023, 1, 31]
            d = random_date()
            self.assertEqual(d, date(2023, 1, 31))