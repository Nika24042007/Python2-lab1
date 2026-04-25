import unittest
from unittest.mock import patch, MagicMock

from src.Sources.api_source import Api_source


class TestApiSource(unittest.TestCase):
    """Тесты для Api_source"""

    def test_create_source(self):
        source = Api_source.create_source("test_name")
        self.assertIsInstance(source, Api_source)
        self.assertEqual(source.name, "test_name")
        self.assertEqual(source.id, 0)

    def test_get_task(self):
        with (patch('builtins.input', side_effect=["", "01.01.2025", "10.01.2025", "Normal"]),
             patch('sys.stdout.write'), patch('sys.stderr.write')):
            source = Api_source("test")
            source.get_task()

    def test_get_all_tasks(self):
        with (patch('builtins.input', side_effect=["2",
            "Task 1", "01.01.2025", "10.01.2025", "High",
            "Task 2", "02.02.2025", "20.02.2025", "Normal",
            "Task 3", "03.03.2025", "30.03.2025", "Low"]),
             patch('sys.stdout.write'), patch('sys.stderr.write')):
            source = Api_source("test")
            source.get_all_tasks("None")

    def test_get_task_empty_input(self):
        with (patch('builtins.input', side_effect=["", "01.01.2025", "10.01.2025", "Normal"]),
             patch('sys.stdout.write'), patch('sys.stderr.write')):
            source = Api_source("test")
            source.get_task()

    def test_get_all_tasks_zero_tasks(self):
        with (patch('builtins.input', side_effect=["0", "d", "d", "d", "d"]),
             patch('sys.stdout.write'), patch('sys.stderr.write')):
            source = Api_source("test")
            source.get_all_tasks("None")


    def test_get_task_value_error(self):
        mock_task = MagicMock()
        mock_task.__next__ = MagicMock(side_effect=ValueError("Test error"))
        with (patch('src.Sources.api_source.TaskQueueApi', return_value=mock_task),
             patch('builtins.print') as mock_print,
             patch('src.Sources.api_source.logging.error') as mock_log_error):
            source = Api_source("test")
            source.get_task()
            mock_log_error.assert_called_once()
            mock_print.assert_called_once()

    def test_get_all_tasks_value_error(self):
        mock_tasks = MagicMock()
        mock_tasks.__iter__ = MagicMock(side_effect=ValueError("Iteration error"))
        with (patch('src.Sources.api_source.TaskQueueApi', return_value=mock_tasks),
             patch('builtins.input', return_value="2"),
             patch('builtins.print') as mock_print,
             patch('src.Sources.api_source.logging.error') as mock_log_error):
            source = Api_source("test")
            source.get_all_tasks("None")
            mock_log_error.assert_called_once()
            mock_print.assert_called_once()
