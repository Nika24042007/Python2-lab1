import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
from src.Sources.file_source import File_Source


class TestFileSource(unittest.TestCase):
    """Тесты для File_Source"""

    def setUp(self):
        self.file_name = "test_file"
        self.text = {
            "0": '{"id": 1, "payload": "Task 1"}',
            "1": '{"id": 2, "payload": "Task 2"}'
        }
        self.source = File_Source("test_source", self.file_name, self.text)

    def test_create_source_success(self):
        with (patch('builtins.input', return_value=self.file_name),
             patch('builtins.open', mock_open(read_data=json.dumps(self.text))),
             patch('src.Sources.file_source.logging.info') as mock_info,
             patch('src.Sources.file_source.logging.basicConfig') as mock_basic,
             patch('src.Sources.file_source.logging.error') as mock_error):

            source = File_Source.create_source("new_source")
            self.assertIsInstance(source, File_Source)
            self.assertEqual(source.name, "new_source")
            self.assertEqual(source.file_name, self.file_name)
            self.assertIsInstance(source.text, dict)
            self.assertIn("0", source.text)
            self.assertIn("1", source.text)
            mock_basic.assert_called_once()
            mock_info.assert_called_once_with(f"Enter file name: {self.file_name}")
            mock_error.assert_not_called()

    def test_create_source_file_not_found(self):
        with (patch('builtins.input', return_value=self.file_name),
             patch('builtins.open', side_effect=FileNotFoundError),
             patch('src.Sources.file_source.logging.error') as mock_error,
             patch('src.Sources.file_source.logging.basicConfig')):

            with self.assertRaises(ValueError) as ctx:
                File_Source.create_source("new_source")
            self.assertEqual(str(ctx.exception), "Error: no such file or file is empty")
            mock_error.assert_called_once_with("Error: no such file or file is empty")

    def test_create_source_invalid_json(self):
        with (patch('builtins.input', return_value=self.file_name),
             patch('builtins.open', mock_open(read_data="invalid json")),
             patch('src.Sources.file_source.logging.error') as mock_error):

            with self.assertRaises(ValueError) as ctx:
                File_Source.create_source("new_source")
            self.assertEqual(str(ctx.exception), "Error: no such file or file is empty")
            mock_error.assert_called_once_with("Error: no such file or file is empty")

    def test_get_task_correct(self):
        mock_task = MagicMock()
        mock_tasks = MagicMock()
        mock_tasks.__next__ = MagicMock(return_value=mock_task)
        self.source.tasks = mock_tasks

        with (patch('builtins.print') as mock_print,
             patch('src.Sources.file_source.logging.error') as mock_log_error):

            self.source.get_task()
            mock_print.assert_called_once_with(mock_task)
            mock_log_error.assert_not_called()

    def test_get_task_value_error(self):
        mock_tasks = MagicMock()
        mock_tasks.__next__ = MagicMock(side_effect=ValueError("Test error"))
        self.source.tasks = mock_tasks

        with (patch('builtins.print') as mock_print,
             patch('src.Sources.file_source.logging.error') as mock_log_error):

            self.source.get_task()
            mock_print.assert_called_once()
            mock_log_error.assert_called_once()

    def test_get_all_tasks_correct(self):
        tasks = [MagicMock(), MagicMock()]
        mock_task_queue = MagicMock()
        mock_task_queue.__iter__ = MagicMock(return_value=iter(tasks))
        with (patch('src.Sources.file_source.TaskQueueFile', return_value=mock_task_queue),
             patch('builtins.print') as mock_print,
             patch('src.Sources.file_source.logging.error') as mock_log_error):

            self.source.get_all_tasks("High")
            mock_print.assert_any_call(tasks[0])
            mock_print.assert_any_call("\n")
            mock_print.assert_any_call(tasks[1])
            mock_print.assert_any_call("\n")
            self.assertEqual(mock_print.call_count, 4)
            mock_log_error.assert_not_called()

    def test_get_all_tasks_value_error(self):
        mock_task_queue = MagicMock()
        mock_task_queue.__iter__ = MagicMock(side_effect=ValueError("Iter error"))
        with (patch('src.Sources.file_source.TaskQueueFile', return_value=mock_task_queue),
             patch('builtins.print') as mock_print,
             patch('src.Sources.file_source.logging.error') as mock_log_error):

            self.source.get_all_tasks("In work")
            mock_print.assert_called_once()
            mock_log_error.assert_called_once()

    def test_get_all_tasks_empty(self):
        mock_task_queue = MagicMock()
        mock_task_queue.__iter__ = MagicMock(return_value=iter([]))
        with (patch('src.Sources.file_source.TaskQueueFile', return_value=mock_task_queue),
             patch('builtins.print') as mock_print):

            self.source.get_all_tasks("Normal")
            mock_print.assert_not_called()
