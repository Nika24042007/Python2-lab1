import unittest
from unittest.mock import patch
from datetime import date
from src.Task.task_file import TaskFile

class TestTaskFile(unittest.TestCase):
    """
    Тесты для задания из файла
    """

    def test_create_task_success(self):
        data = {
            "id": 1,
            "payloud": "Test task",
            "data_start": "01.01.2025",
            "data_end": "10.01.2025",
            "priority": "Normal"
        }
        task = TaskFile.create_task(data)
        self.assertIsInstance(task, TaskFile)
        self.assertEqual(task.id, 1)
        self.assertEqual(task.payloud, "Test task")
        self.assertEqual(task.data_start, "01.01.2025")
        self.assertEqual(task.data_end, "10.01.2025")
        self.assertEqual(task.priority, "Normal")

    def test_create_task_missing_key(self):
        data = {
            "id": 1,
            "payloud": "Test task",
            "data_end": "10.01.2025",
            "priority": "Normal"
        }
        with self.assertRaises(ValueError) as cm:
            TaskFile.create_task(data)
        self.assertEqual(str(cm.exception), "Some data about the task is missing")

    def test_deadline_and_status(self):
        class mock_date(date):
            @classmethod
            def today(cls):
                return date(2025, 1, 5)

        with patch('src.Task.task_file.date', mock_date):
            task = TaskFile(1, "task", "01.01.2025", "10.01.2025", "High")
            self.assertEqual(task.deadline, date(2025, 1, 10) - date(2025, 1, 5))
            self.assertEqual(task.status, "there's still time")
            task2 = TaskFile(2, "task2", "01.01.2025", "02.01.2025", "Normal")
            self.assertLess(task2.deadline.days, 0)
            self.assertEqual(task2.status, "deadline over")

    def test_str(self):
        class mock_date(date):
            @classmethod
            def today(cls):
                return date(2025, 1, 5)

        with patch('src.Task.task_file.date', mock_date):
            task = TaskFile(3, "my payload", "01.01.2025", "10.01.2025", "Very high")
            expected = ("id: 3\n payload: my payload\n priority: Very high\n status: there's still time\n start: 01.01.2025\n end: 10.01.2025\n deadline: 5 days, 0:00:00\n")
            self.assertEqual(str(task), expected)
