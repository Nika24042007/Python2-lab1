import unittest
from src.random_text import random_text
from unittest.mock import patch

class TestRandomText(unittest.TestCase):
    """
    Тесты для функции получения рандомного текста задания
    """
    def test_get_random_text(self):
        with(patch("src.random_text.randint") as mock_randint,
             patch("src.random_text.choice") as mock_choice):
            mock_randint.return_value = 4
            mock_choice.side_effect = ["Apple", "water", "cat", "dog"]

            result = random_text()

            mock_randint.assert_called_once_with(1, 10)
            self.assertEqual(mock_choice.call_count, 4)
            self.assertEqual(result, "Apple water cat dog ")