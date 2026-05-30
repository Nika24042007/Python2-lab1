import unittest
from unittest.mock import patch
from datetime import date, timedelta
from src.Task.task_generator import TaskGenerator

class TestTaskGenerator(unittest.TestCase):
    """
    Тесты для генерируемого задания
    """
    def test_init(self):
        task = TaskGenerator(id=1,
            payloud="payload",
            priority="High",
            data_start="01.01.2025",
            data_end="10.01.2025",
            deadline=timedelta(days=9),
            status="there's still time")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.payloud, "payload")
        self.assertEqual(task.priority, "High")
        self.assertEqual(task.data_start, "01.01.2025")
        self.assertEqual(task.data_end, "10.01.2025")
        self.assertEqual(task.deadline, timedelta(days=9))
        self.assertEqual(task.status, "there's still time")

    def test_create_task(self):
        with (patch('src.Task.task_generator.choice') as mock_choice,
             patch('src.Task.task_generator.random_date') as mock_rand_date,
             patch('src.Task.task_generator.randint') as mock_randint,
             patch('src.Task.task_generator.date') as mock_date,
             patch('src.Task.task_generator.random_text') as mock_random_text):

            mock_choice.return_value = "Normal"
            mock_rand_date.return_value = date(2025, 1, 1)
            mock_randint.return_value = 10
            mock_date.today.return_value = date(2025, 1, 5)
            mock_random_text.return_value = "some payloud" 

            task1 = TaskGenerator.create_task(42, "some payloud")

            mock_choice.assert_called_once()
            mock_rand_date.assert_called_once()
            mock_randint.assert_called_once_with(1, 365)
            mock_date.today.assert_called_once()
            mock_random_text.assert_called_once()

            self.assertEqual(task1.id, 42)
            self.assertEqual(task1.payloud, "some payloud")
            self.assertEqual(task1.priority, "Normal")
            self.assertEqual(task1.data_start, date(2025, 1, 1))
            self.assertEqual(task1.data_end, date(2025, 1, 11))
            self.assertEqual(task1.deadline, date(2025, 1, 11) - date(2025, 1, 5))
            self.assertEqual(task1.status, "there's still time")

            mock_randint.return_value = 10
            mock_date.today.return_value = date(2025, 1, 20)
            mock_random_text.return_value = "another payloud"
            task2 = TaskGenerator.create_task(43, "another payloud")
            self.assertEqual(task2.deadline.days, -9)
            self.assertEqual(task2.status, "deadline over")

    def test_str(self):
        task = TaskGenerator(id=1,
            payloud="Test payloud",
            priority="Very high",
            data_start="01.01.2025",
            data_end="10.01.2025",
            deadline=timedelta(days=9),
            status="there's still time")
        expected = ("id: 1\n payload: Test payloud\n priority: Very high\n status: there's still time\n start: 01.01.2025\n end: 10.01.2025\n deadline: 9 days, 0:00:00\n")
        self.assertEqual(str(task), expected)