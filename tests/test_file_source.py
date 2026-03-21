import unittest
from src.Sources.file_source import File_Source
from unittest.mock import patch, MagicMock, mock_open
import json

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
        tasks_data = json.dumps({"1": "Task 1"})
        with (patch('builtins.open', mock_open(read_data=tasks_data)) as mock_file, \
             patch('src.Sources.file_source.input') as mock_input,
             patch('src.Sources.file_source.print') as mock_print,
             patch('src.Sources.file_source.logging.info') as mock_info,
             patch('src.Sources.file_source.logging.basicConfig') as mock_basic):
            mock_input.return_value = "1"
            result = self.source.get_task()
            self.assertEqual(result, "Task 1")
            mock_file.assert_called_once_with(f"src//File_test//{self.file_name}.json", "r", encoding="utf-8")
            mock_print.assert_called_once_with("Choice id of task: ['1'] ")
            self.assertEqual(mock_info.call_count, 2)
            mock_basic.assert_called_once()

    def test_get_task_uncorrect_id(self):
        tasks_data = json.dumps({"1": "Task 1"})
        with (patch('builtins.open', mock_open(read_data=tasks_data)),
             patch('src.Sources.file_source.input') as mock_input,
             patch('src.Sources.file_source.logging.info'),
             patch('src.Sources.file_source.logging.error') as mock_error,
             patch('src.Sources.file_source.logging.basicConfig') as mock_basic):
            mock_input.return_value = "127"
            result = self.source.get_task()
            self.assertEqual(result, "Error: no such file or file is empty")
            mock_error.assert_called_once_with("Error: no such file or file is empty")
            mock_basic.assert_called_once()

    def test_get_task_file_not_found(self):
        with (patch('builtins.open', side_effect=FileNotFoundError),
             patch('src.Sources.file_source.logging.error') as mock_error,
             patch('src.Sources.file_source.logging.basicConfig') as mock_basic):
            result = self.source.get_task()
            self.assertEqual(result, "Error: no such file or file is empty")
            mock_error.assert_called_once_with("Error: no such file or file is empty")
            mock_basic.assert_called_once()

    def test_get_task_uncorrect_json(self):
        with (patch('builtins.open', mock_open(read_data="uncorrect json")),
             patch('src.Sources.file_source.logging.error') as mock_error,
             patch('src.Sources.file_source.logging.basicConfig') as mock_basic):
            result = self.source.get_task()
            self.assertEqual(result, "Error: no such file or file is empty")
            mock_error.assert_called_once_with("Error: no such file or file is empty")
            mock_basic.assert_called_once()

    def test_get_all_tasks_correct(self):
        tasks_data = json.dumps({"1": "Task 1"})
        with (patch('builtins.open', mock_open(read_data=tasks_data)) as mock_file,
             patch('src.Sources.file_source.logging.basicConfig') as mock_basic):
            result = self.source.get_all_tasks()
            expected = str({"1": "Task 1"})
            self.assertEqual(result, expected)
            mock_file.assert_called_once_with(f"src//File_test//{self.file_name}.json", "r", encoding="utf-8")
            mock_basic.assert_called_once()

    def test_get_all_tasks_file_not_found(self):
        with (patch('builtins.open', side_effect=FileNotFoundError),
             patch('src.Sources.file_source.logging.error') as mock_error,
             patch('src.Sources.file_source.logging.basicConfig') as mock_basic):
            result = self.source.get_all_tasks()
            self.assertEqual(result, "Error: no such file or file is empty")
            mock_error.assert_called_once_with("Error: no such file or file is empty")
            mock_basic.assert_called_once()

    def test_get_all_tasks_uncorrect_json(self):
        with (patch('builtins.open', mock_open(read_data="ucorrect json")),
             patch('src.Sources.file_source.logging.error') as mock_error,
             patch('src.Sources.file_source.logging.basicConfig') as mock_basic):
            result = self.source.get_all_tasks()
            self.assertEqual(result, "Error: no such file or file is empty")
            mock_error.assert_called_once_with("Error: no such file or file is empty")
            mock_basic.assert_called_once()