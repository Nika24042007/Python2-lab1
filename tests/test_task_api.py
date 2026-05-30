import unittest
from unittest.mock import patch, call
from datetime import date
import asyncio
from src.Task.task_api import TaskApi


class TestTaskApi(unittest.TestCase):
    """
    Тесты для заданий из api
    """

    def test_deadline_and_status(self):
        class mock_date(date):
            @classmethod
            def today(cls):
                return date(2025, 1, 1)

        with patch('src.Task.task_api.date', mock_date):
            task1 = TaskApi(1, "task1", "Normal", "01-01-2025", "10-01-2025")
            self.assertEqual(task1.deadline, date(2025, 1, 10) - date(2025, 1, 1))
            self.assertEqual(task1.status, "there's still time")

            task2 = TaskApi(2, "task2", "High", "01-01-2024", "10-01-2024")
            self.assertLess(task2.deadline.days, 0)
            self.assertEqual(task2.status, "deadline over")

    def test_uncorrect_start_date(self):
        with self.assertRaises(ValueError):
            TaskApi(1, "task", "Normal", "32-01-2025", "10-01-2025")

    def test_uncorrect_end_date_vs_start(self):
        with self.assertRaises(ValueError) as cm:
            TaskApi(1, "task", "Normal", "10-01-2025", "05-01-2025")
        self.assertEqual(str(cm.exception), "Uncorrect end data")

    def test_create_task(self):
        inputs = ["test payload", "01-02-2025", "10-02-2025", "Normal"]
        async def mock_to_thread(func, *args, **kwargs):
            return inputs.pop(0)

        with (patch('asyncio.to_thread', side_effect=mock_to_thread),
              patch('src.Task.task_api.logging') as mock_logging):
            task = asyncio.run(TaskApi.create_task(10, "ignored text"))
            
            self.assertIsInstance(task, TaskApi)
            self.assertEqual(task.id, 10)
            self.assertEqual(task.payloud, "test payload")
            self.assertEqual(task.priority, "Normal")
            self.assertEqual(task.data_start, date(2025, 2, 1))
            self.assertEqual(task.data_end, date(2025, 2, 10))
            self.assertEqual(mock_logging.info.call_count, 0)

    def test_str(self):
        class mock_date(date):
            @classmethod
            def today(cls):
                return date(2025, 1, 1)

        with patch('src.Task.task_api.date', mock_date):
            task = TaskApi(5, "my task", "Very high", "01-01-2025", "10-01-2025")
            expected = ("id: 5\n payload: my task\n priority: Very high\n status: there's still time\n start: 2025-01-01\n end: 2025-01-10\n deadline: 9 days, 0:00:00\n")
            self.assertEqual(str(task), expected)