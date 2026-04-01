import unittest
from unittest.mock import patch
from src.Sources.generator_source import Generator_source
from src.Task.task_generator import TaskGenerator

class TestGeneratorSource(unittest.TestCase):
    """
    Тесты для класса источника-генератора
    """
    def test_create_source(self):
        source = Generator_source.create_source("test")
        self.assertIsInstance(source, Generator_source)
        self.assertEqual(source.name, "test")
        self.assertEqual(source.id, 0)

    def test_get_task_one(self):
        with (patch('src.Sources.generator_source.random_text') as mock_random_text):
            mock_random_text.return_value = "Task"
            source = Generator_source("test")
            result = source.get_task()
            self.assertEqual(source.id, 1)
            self.assertIsInstance(result, TaskGenerator)
            self.assertEqual(result.id, 1)
            self.assertEqual(result.payloud, "Task")
            mock_random_text.assert_called_once()

    def test_get_all_tasks(self):
        with (patch('src.Sources.generator_source.randint') as mock_randint,
             patch('src.Sources.generator_source.random_text') as mock_random_text):
            mock_randint.return_value = 3
            mock_random_text.side_effect = ["Task 1", "Task 2", "Task 3"]
            source = Generator_source("test")
            result = source.get_all_tasks()
            mock_randint.assert_called_once_with(1, 20)
            self.assertEqual(mock_random_text.call_count, 3)
            self.assertEqual(source.id, 3)
            self.assertIsInstance(result, list)
            self.assertEqual(len(result), 3)
            for i, task in enumerate(result, start=1):
                self.assertIsInstance(task, TaskGenerator)
                self.assertEqual(task.id, i)
                self.assertEqual(task.payloud, f"Task {i}")

    def test_get_all_tasks_min(self):
        with (patch('src.Sources.generator_source.randint') as mock_randint,
             patch('src.Sources.generator_source.random_text') as mock_random_text):
            mock_randint.return_value = 1
            mock_random_text.return_value = "One"
            source = Generator_source("test")
            result = source.get_all_tasks()
            self.assertEqual(source.id, 1)
            self.assertIsInstance(result, list)
            self.assertEqual(len(result), 1)
            self.assertIsInstance(result[0], TaskGenerator)
            self.assertEqual(result[0].id, 1)
            self.assertEqual(result[0].payloud, "One")

    def test_get_all_tasks_max(self):
        with (patch('src.Sources.generator_source.randint') as mock_randint,
             patch('src.Sources.generator_source.random_text') as mock_random_text):
            mock_randint.return_value = 20
            mock_random_text.return_value = "Task"
            source = Generator_source("test2")
            result = source.get_all_tasks()
            self.assertEqual(source.id, 20)
            self.assertIsInstance(result, list)
            self.assertEqual(len(result), 20)
            ids = [task.id for task in result]
            self.assertIn(1, ids)
            self.assertIn(20, ids)
            for task in result:
                self.assertEqual(task.payloud, "Task")
