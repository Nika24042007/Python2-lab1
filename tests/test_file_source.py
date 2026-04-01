import unittest
from unittest.mock import patch, mock_open
import json
from src.Sources.file_source import File_Source

class TestFileSource(unittest.TestCase):
    """
    Тесты для класса источника-файла
    """
    def setUp(self):
        self.file_name = "test_file"
        self.source = File_Source("test_source", self.file_name)

    def test_create_source(self):
        with (patch('src.Sources.file_source.input') as mock_input,
             patch('src.Sources.file_source.logging.info') as mock_info,
             patch('src.Sources.file_source.logging.basicConfig') as mock_basic):
            mock_input.return_value = self.file_name
            source = File_Source.create_source("new_source")
            self.assertIsInstance(source, File_Source)
            self.assertEqual(source.name, "new_source")
            self.assertEqual(source.file_name, self.file_name)
            mock_input.assert_called_once_with("Enter file name: ")
            mock_info.assert_called_once_with(f"Enter file name: {self.file_name}")
            mock_basic.assert_called_once()

    def test_get_task_correct(self):
        tasks_data = [{"id": 1, "payload": "Task 1"}]
        with (patch('builtins.open', mock_open(read_data=json.dumps(tasks_data))),
             patch('src.Sources.file_source.input') as mock_input,
             patch('src.Sources.file_source.TaskFile.create_task') as mock_create_task,
             patch('src.Sources.file_source.logging.info') as mock_info,
             patch('src.Sources.file_source.logging.basicConfig') as mock_basic):
            mock_input.return_value = "1"
            mock_create_task.return_value = "Task 1"
            result = self.source.get_task()
            self.assertEqual(result, "Task 1")
            mock_input.assert_called_once_with("Enter id from list [1]: ")
            mock_create_task.assert_called_once_with(tasks_data[0])
            self.assertEqual(mock_info.call_count, 1)
            mock_basic.assert_called_once()

    def test_get_task_uncorrect_id(self):
        tasks_data = [{"id": 1, "payload": "Task 1"}]
        with (patch('builtins.open', mock_open(read_data=json.dumps(tasks_data))),
             patch('src.Sources.file_source.input') as mock_input,
             patch('src.Sources.file_source.logging.info'),
             patch('src.Sources.file_source.logging.error') as mock_error,
             patch('src.Sources.file_source.logging.basicConfig') as mock_basic):
            mock_input.return_value = "127"
            with self.assertRaises(ValueError) as context:
                self.source.get_task()
            self.assertEqual(str(context.exception), "Error: no such file or file is empty")
            mock_error.assert_called_once_with("Error: no such file or file is empty")
            mock_basic.assert_called_once()

    def test_get_task_file_not_found(self):
        with (patch('builtins.open', side_effect=FileNotFoundError),
             patch('src.Sources.file_source.logging.error') as mock_error,
             patch('src.Sources.file_source.logging.basicConfig') as mock_basic):
            with self.assertRaises(ValueError) as context:
                self.source.get_task()
            self.assertEqual(str(context.exception), "Error: no such file or file is empty")
            mock_error.assert_called_once_with("Error: no such file or file is empty")
            mock_basic.assert_called_once()

    def test_get_task_uncorrect_json(self):
        with (patch('builtins.open', mock_open(read_data="uncorrect json")),
             patch('src.Sources.file_source.logging.error') as mock_error,
             patch('src.Sources.file_source.logging.basicConfig') as mock_basic):
            with self.assertRaises(ValueError) as context:
                self.source.get_task()
            self.assertEqual(str(context.exception), "Error: no such file or file is empty")
            mock_error.assert_called_once_with("Error: no such file or file is empty")
            mock_basic.assert_called_once()

    def test_get_all_tasks_correct(self):
        tasks_data = [{"id": 1, "payload": "Task 1"}]
        with (patch('builtins.open', mock_open(read_data=json.dumps(tasks_data))),
             patch('builtins.print') as mock_print,
             patch('src.Sources.file_source.TaskFile.create_task') as mock_create_task,
             patch('src.Sources.file_source.logging.basicConfig') as mock_basic):
            mock_create_task.return_value = "Task 1"
            result = self.source.get_all_tasks()
            self.assertEqual(result, ["Task 1"])
            mock_create_task.assert_called_once_with(tasks_data[0])
            mock_print.assert_called_once_with(tasks_data[0])
            mock_basic.assert_called_once()

    def test_get_all_tasks_file_not_found(self):
        with (patch('builtins.open', side_effect=FileNotFoundError),
             patch('src.Sources.file_source.logging.error') as mock_error,
             patch('src.Sources.file_source.logging.basicConfig') as mock_basic):
            with self.assertRaises(ValueError) as context:
                self.source.get_all_tasks()
            self.assertEqual(str(context.exception), "Error: no such file or file is empty")
            mock_error.assert_called_once_with("Error: no such file or file is empty")
            mock_basic.assert_called_once()

    def test_get_all_tasks_uncorrect_json(self):
        with (patch('builtins.open', mock_open(read_data="uncorrect json")),
             patch('src.Sources.file_source.logging.error') as mock_error,
             patch('src.Sources.file_source.logging.basicConfig') as mock_basic):
            with self.assertRaises(ValueError) as context:
                self.source.get_all_tasks()
            self.assertEqual(str(context.exception), "Error: no such file or file is empty")
            mock_error.assert_called_once_with("Error: no such file or file is empty")
            mock_basic.assert_called_once()