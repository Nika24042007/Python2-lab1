import unittest
from src.TaskQueue.filters import priopity_filter, status_filter

class TestPriorityFilter(unittest.TestCase):
    """
    Тесты для фильтров по приоритету
    """

    def test_equal_priority_returns_true(self):
        self.assertTrue(priopity_filter("high", "high"))
        self.assertTrue(priopity_filter("low", "low"))
        self.assertTrue(priopity_filter("", ""))
        self.assertTrue(priopity_filter("high priority", "high priority"))

    def test_not_equal_priority_returns_false(self):
        self.assertFalse(priopity_filter("high", "low"))
        self.assertFalse(priopity_filter("medium", "high"))
        self.assertFalse(priopity_filter("", "not empty"))
        self.assertFalse(priopity_filter("case", "CASE"))

    def test_case_sensitivity(self):
        self.assertFalse(priopity_filter("HIGH", "high"))
        self.assertTrue(priopity_filter("In Work", "In Work"))


class TestStatusFilter(unittest.TestCase):
    """
    Тесты для фильтров по статусу
    """

    def test_valid_in_work(self):
        self.assertTrue(status_filter("there's still time", "In work"))

    def test_valid_deadline_over(self):
        self.assertTrue(status_filter("deadline over", "Over"))

    def test_invalid_combination_must_there_still_time(self):
        self.assertFalse(status_filter("there's still time", "Over"))
        self.assertFalse(status_filter("there's still time", "In progress"))
        self.assertFalse(status_filter("there's still time", ""))

    def test_invalid_combination_must_deadline_over(self):
        self.assertFalse(status_filter("deadline over", "In work"))
        self.assertFalse(status_filter("deadline over", "Pending"))
        self.assertFalse(status_filter("deadline over", ""))

    def test_unknown_must_value(self):
        self.assertFalse(status_filter("any", "In work"))
        self.assertFalse(status_filter("any", "Over"))
        self.assertFalse(status_filter("something else", "In work"))

    def test_unknown_is_st_value_for_known_must(self):
        self.assertFalse(status_filter("there's still time", "Unknown"))
        self.assertFalse(status_filter("deadline over", "Unknown"))

    def test_both_invalid(self):
        self.assertFalse(status_filter("foo", "bar"))
        self.assertFalse(status_filter("", ""))
        self.assertFalse(status_filter("there's still time", "in work"))

    def test_case_sensitive_status(self):
        self.assertFalse(status_filter("there's still time", "IN WORK"))
        self.assertFalse(status_filter("there's still time", "in work"))
        self.assertFalse(status_filter("deadline over", "over"))
        self.assertFalse(status_filter("deadline over", "OVER"))