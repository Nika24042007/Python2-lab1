import unittest
from unittest.mock import patch, MagicMock

from src.Sources.api_source import Api_source

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
        """Проверка метода get_task: ввод одной задачи, возврат словаря с id."""
        with (patch('src.Sources.api_source.input') as mock_input,
             patch('src.Sources.api_source.logging.info') as mock_info,
             patch('src.Sources.api_source.logging.basicConfig') as mock_basic):
            mock_input.return_value = "Task"
            source = Api_source("test")
            result = source.get_task()

            mock_input.assert_called_once_with("Enter task: ")
            mock_info.assert_called_once_with("Enter task: Task")
            mock_basic.assert_called_once()
            self.assertEqual(source.id, 1)
            expected = "{1: 'Task'}"
            self.assertEqual(result, expected)

    def test_get_all_tasks(self):
        with (patch('src.Sources.api_source.input') as mock_input,
             patch('src.Sources.api_source.logging.info') as mock_info,
             patch('src.Sources.api_source.logging.basicConfig') as mock_basic):
            mock_input.side_effect = ["3", "Task 1", "Task 2", "Task 3"]
            source = Api_source("test")
            result = source.get_all_tasks()
            expected_calls = [
                unittest.mock.call("Enter the number of tasks: "),
                unittest.mock.call("Enter task: "),
                unittest.mock.call("Enter task: "),
                unittest.mock.call("Enter task: ")
            ]
            self.assertEqual(mock_input.call_args_list, expected_calls)
            self.assertEqual(mock_info.call_count, 4)
            mock_info.assert_any_call("Enter the number of tasks: 3")
            mock_info.assert_any_call("Enter task: Task 1")
            mock_info.assert_any_call("Enter task: Task 2")
            mock_info.assert_any_call("Enter task: Task 3")
            mock_basic.assert_called_once()
            self.assertEqual(source.id, 3)
            expected_dict = {1: "Task 1", 2: "Task 2", 3: "Task 3"}
            self.assertEqual(result, str(expected_dict))

    def test_get_task_empty_input(self):
        with (patch('src.Sources.api_source.input') as mock_input,
             patch('src.Sources.api_source.logging.info') as mock_info,
             patch('src.Sources.api_source.logging.basicConfig')):
            mock_input.return_value = ""
            source = Api_source("test")
            result = source.get_task()
            mock_input.assert_called_once_with("Enter task: ")
            mock_info.assert_called_once_with("Enter task: ")
            self.assertEqual(source.id, 1)
            self.assertEqual(result, "{1: ''}")

    def test_get_all_tasks_zero_tasks(self):
        with (patch('src.Sources.api_source.input') as mock_input,
             patch('src.Sources.api_source.logging.info') as mock_info,
             patch('src.Sources.api_source.logging.basicConfig')):
            mock_input.side_effect = ["0"]
            source = Api_source("test")
            result = source.get_all_tasks()
            self.assertEqual(mock_input.call_count, 1)
            mock_info.assert_called_once_with("Enter the number of tasks: 0")
            self.assertEqual(source.id, 0)
            self.assertEqual(result, "{}")
