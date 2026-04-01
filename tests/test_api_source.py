import unittest
from unittest.mock import patch

from src.Sources.api_source import Api_source
from src.Task.task_api import TaskApi


class TestApiSource(unittest.TestCase):
    """
    Тесты для класса источника-api
    """
    def test_create_source(self):
        source = Api_source.create_source("test_name")
        self.assertIsInstance(source, Api_source)
        self.assertEqual(source.name, "test_name")
        self.assertEqual(source.id, 0)

    def test_get_task(self):
        with (patch('builtins.input') as mock_input,
             patch('src.Sources.api_source.logging.info') as mock_info,
             patch('src.Sources.api_source.logging.basicConfig') as mock_basic):

            mock_input.side_effect = ["Test task", "01.01.2025", "10.01.2025", "Normal"]
            source = Api_source("test")
            result = source.get_task()
            expected_inputs = [
                "Enter payloud: ",
                "Enter start data(dd.mm.yyyy): ",
                "Enter end data(dd.mm.yyyy): ",
                "Enter priority(High, Normal, Very high): "]
            self.assertEqual(mock_input.call_count, 4)
            for expected in expected_inputs:
                mock_input.assert_any_call(expected)

            self.assertEqual(mock_info.call_count, 4)
            mock_info.assert_any_call("Enter payloud: Test task")
            mock_info.assert_any_call("Enter start data(dd.mm.yyyy): 01.01.2025")
            mock_info.assert_any_call("Enter end data(dd.mm.yyyy): 10.01.2025")
            mock_info.assert_any_call("Enter prioriti(High, Normal, Very high): Normal")
            mock_basic.assert_called()
            self.assertIsInstance(result, TaskApi)
            self.assertEqual(result.id, 1)
            self.assertEqual(result.payloud, "Test task")
            self.assertEqual(result.priority, "Normal")
            self.assertEqual(source.id, 1)

    def test_get_all_tasks(self):
        with (patch('builtins.input') as mock_input,
             patch('src.Sources.api_source.logging.info') as mock_info,
             patch('src.Sources.api_source.logging.basicConfig') as mock_basic):

            mock_input.side_effect = ["2",                             
                "Task 1", "01.01.2025", "10.01.2025", "High",
                "Task 2", "02.02.2025", "20.02.2025", "Normal"]
            source = Api_source("test")
            result = source.get_all_tasks()
            self.assertEqual(mock_input.call_count, 9)
            mock_input.assert_any_call("Enter the number of tasks: ")
            for i in range(1, 3):
                mock_input.assert_any_call("Enter payloud: ")
                mock_input.assert_any_call("Enter start data(dd.mm.yyyy): ")
                mock_input.assert_any_call("Enter end data(dd.mm.yyyy): ")
                mock_input.assert_any_call("Enter priority(High, Normal, Very high): ")

            self.assertEqual(mock_info.call_count, 9)
            mock_info.assert_any_call("Enter the number of tasks: 2")
            mock_info.assert_any_call("Enter payloud: Task 1")
            mock_info.assert_any_call("Enter start data(dd.mm.yyyy): 01.01.2025")
            mock_info.assert_any_call("Enter end data(dd.mm.yyyy): 10.01.2025")
            mock_info.assert_any_call("Enter prioriti(High, Normal, Very high): High")
            mock_info.assert_any_call("Enter payloud: Task 2")
            mock_info.assert_any_call("Enter start data(dd.mm.yyyy): 02.02.2025")
            mock_info.assert_any_call("Enter end data(dd.mm.yyyy): 20.02.2025")
            mock_info.assert_any_call("Enter prioriti(High, Normal, Very high): Normal")
            mock_basic.assert_called()
            self.assertIsInstance(result, list)
            self.assertEqual(len(result), 2)
            self.assertIsInstance(result[0], TaskApi)
            self.assertEqual(result[0].id, 1)
            self.assertEqual(result[0].payloud, "Task 1")
            self.assertEqual(result[1].id, 2)
            self.assertEqual(result[1].payloud, "Task 2")
            self.assertEqual(source.id, 2)

    def test_get_task_empty_input(self):
        with (patch('builtins.input') as mock_input):

            mock_input.side_effect = ["", "01.01.2025", "10.01.2025", "Normal"]
            source = Api_source("test")
            result = source.get_task()
            self.assertEqual(result.payloud, "")
            self.assertEqual(source.id, 1)

    def test_get_all_tasks_zero_tasks(self):
        with (patch('builtins.input') as mock_input,
             patch('src.Sources.api_source.logging.info') as mock_info):

            mock_input.side_effect = ["0"]
            source = Api_source("test")
            result = source.get_all_tasks()
            self.assertEqual(mock_input.call_count, 1)
            mock_info.assert_called_once_with("Enter the number of tasks: 0")
            self.assertEqual(source.id, 0)
            self.assertEqual(result, [])