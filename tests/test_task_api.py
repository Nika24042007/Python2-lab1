import unittest
from unittest.mock import patch, call
from datetime import date
from src.Task.task_api import TaskApi

class TestTaskApi(unittest.TestCase):
    """
    Тесты для заданий из api
    """

    def test_deadline_and_status(self):
        from datetime import date

        class mock_date(date):
            @classmethod
            def today(cls):
                return date(2025, 1, 1)
            
        with patch('src.Task.task_api.date', mock_date):
            mock_date.return_value = date(2025, 1, 1)
            task1 = TaskApi(1, "task1", "Normal", "01.01.2025", "10.01.2025")
            self.assertEqual(task1.deadline, date(2025, 1, 10) - date(2025, 1, 1))
            self.assertEqual(task1.status, "there's still time")

            task2 = TaskApi(2, "task2", "High", "01.01.2024", "10.01.2024")
            self.assertLess(task2.deadline.days, 0)
            self.assertEqual(task2.status, "deadline over")

    def test_uncorrect_priority(self):
        with self.assertRaises(ValueError):
            TaskApi(1, "task", "Invalid", "01.01.2025", "10.01.2025")

    def test_uncorrect_start_date(self):
        with self.assertRaises(ValueError):
            TaskApi(1, "task", "Normal", "32.01.2025", "10.01.2025")

    def test_uncorrect_end_date_vs_start(self):
        with self.assertRaises(ValueError) as cm:
            TaskApi(1, "task", "Normal", "10.01.2025", "05.01.2025")
        self.assertEqual(str(cm.exception), "Uncorrect end data")

    def test_create_task(self):
        with (patch('builtins.input') as mock_input,
             patch('src.Task.task_api.logging') as mock_logging):
            mock_input.side_effect = ["01.02.2025", "10.02.2025", "High"]
            task = TaskApi.create_task(10, "test payload")
            expected_input_calls = [call("Enter start data(dd.mm.yyyy): "),
                call("Enter end data(dd.mm.yyyy): "),
                call("Enter priority(High, Normal, Very high): ")]
            mock_input.assert_has_calls(expected_input_calls)
            self.assertEqual(mock_input.call_count, 3)
            mock_logging.basicConfig.assert_called_once()
            self.assertEqual(mock_logging.info.call_count, 3)

            self.assertIsInstance(task, TaskApi)
            self.assertEqual(task.id, 10)
            self.assertEqual(task.payloud, "test payload")
            self.assertEqual(task.priority, "High")
            self.assertEqual(task.data_start, "01.02.2025")
            self.assertEqual(task.data_end, "10.02.2025")

    def test_str(self):
        from datetime import date

        class mock_date(date):
            @classmethod
            def today(cls):
                return date(2025, 1, 1)
        with patch('src.Task.task_api.date', mock_date):
            mock_date.return_value = date(2025, 1, 1)
            task = TaskApi(5, "my task", "Very high", "01.01.2025", "10.01.2025")
            expected = ("id: 5\n payload: my task\n priority: Very high\n status: there's still time\n start: 01.01.2025\n end: 10.01.2025\n deadline: 9 days, 0:00:00\n")
            self.assertEqual(str(task), expected)

