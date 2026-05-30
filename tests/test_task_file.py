import unittest
from unittest.mock import patch, MagicMock
from datetime import date
from src.Task.task_file import TaskFile

class TestTaskFile(unittest.TestCase):
    """
    Тесты для задания из файла
    """

    def test_create_task_success(self):
        mock_task = MagicMock(spec=TaskFile)
        mock_task.id = 1
        mock_task.payloud = "Test task"
        mock_task.data_start = "01.01.2025"
        mock_task.data_end = "10.01.2025"
        mock_task.priority = "Normal"

        with patch('src.Task.task_file.TaskFile.create_task', return_value=mock_task):
            data = {
                "id": 1,
                "payloud": "Test task",
                "data_start": "01-01-2025",
                "data_end": "10-01-2025",
                "priority": "Normal"
            }
            text_all = ""
            task = TaskFile.create_task(data, text_all)
            self.assertIsInstance(task, MagicMock)
            self.assertEqual(task.id, 1)
            self.assertEqual(task.payloud, "Test task")
            self.assertEqual(task.data_start, "01.01.2025")
            self.assertEqual(task.data_end, "10.01.2025")
            self.assertEqual(task.priority, "Normal")

    def test_create_task_missing_key(self):
        with patch('src.Task.task_file.TaskFile.create_task', side_effect=ValueError("Some data about the task is missing")):
            data = {
                "id": 1,
                "payloud": "Test task",
                "data_end": "10-01-2025",
                "priority": "Normal"
            }
            text_all = ""
            with self.assertRaises(ValueError) as cm:
                TaskFile.create_task(data, text_all)
            self.assertEqual(str(cm.exception), "Some data about the task is missing")

    def test_deadline_and_status(self):
        class mock_date(date):
            @classmethod
            def today(cls):
                return date(2025, 1, 5)

        with patch('src.Task.task_file.date', mock_date):
            task = TaskFile(1, "task", "01-01-2025", "10-01-2025", "High")
            self.assertEqual(task.deadline, date(2025, 1, 10) - date(2025, 1, 5))
            self.assertEqual(task.status, "there's still time")
            task2 = TaskFile(2, "task2", "01-01-2025", "02-01-2025", "Normal")
            self.assertLess(task2.deadline.days, 0)
            self.assertEqual(task2.status, "deadline over")

    def test_str(self):
        class mock_date(date):
            @classmethod
            def today(cls):
                return date(2025, 1, 5)

        with patch('src.Task.task_file.date', mock_date):
            task = TaskFile(3, "my payload", "01-01-2025", "10-01-2025", "Very high")
            expected = ("id: 3\n payload: my payload\n priority: Very high\n status: there's still time\n start: 2025-01-01\n end: 2025-01-10\n deadline: 5 days, 0:00:00\n")
            self.assertEqual(str(task), expected)