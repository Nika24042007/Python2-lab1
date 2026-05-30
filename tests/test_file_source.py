import unittest
from unittest.mock import patch, mock_open, AsyncMock
import json
import asyncio
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
        async def mock_to_thread(func, *args, **kwargs):
            return self.file_name

        with (patch('asyncio.to_thread', side_effect=mock_to_thread),
              patch('builtins.open', mock_open(read_data=json.dumps(self.text))),
              patch('src.Sources.file_source.logging.info') as mock_info,
              patch('src.Sources.file_source.logging.error') as mock_error):

            source = asyncio.run(File_Source.create_source("new_source"))
            self.assertIsInstance(source, File_Source)
            self.assertEqual(source.name, "new_source")
            self.assertEqual(source.file_name, self.file_name)
            self.assertIsInstance(source.text, dict)
            self.assertIn("0", source.text)
            self.assertIn("1", source.text)
            mock_error.assert_not_called()

    def test_create_source_file_not_found(self):
        async def mock_to_thread(func, *args, **kwargs):
            return self.file_name

        with (patch('asyncio.to_thread', side_effect=mock_to_thread),
              patch('builtins.open', side_effect=FileNotFoundError),
              patch('src.Sources.file_source.logging.error') as mock_error):

            with self.assertRaises(ValueError) as ctx:
                asyncio.run(File_Source.create_source("new_source"))
            self.assertEqual(str(ctx.exception), "Error: no such file or file is empty")
            mock_error.assert_called_once_with("Error: no such file or file is empty")

    def test_create_source_invalid_json(self):
        async def mock_to_thread(func, *args, **kwargs):
            return self.file_name

        with (patch('asyncio.to_thread', side_effect=mock_to_thread),
              patch('builtins.open', mock_open(read_data="invalid json")),
              patch('src.Sources.file_source.logging.error') as mock_error):

            with self.assertRaises(ValueError) as ctx:
                asyncio.run(File_Source.create_source("new_source"))
            self.assertEqual(str(ctx.exception), "Error: no such file or file is empty")
            mock_error.assert_called_once_with("Error: no such file or file is empty")

    def test_get_task_correct(self):
        mock_iter = AsyncMock()
        mock_iter.__aiter__.return_value = mock_iter
        mock_iter.__anext__ = AsyncMock(side_effect=["task1", StopAsyncIteration])
        self.source.task = mock_iter

        result = asyncio.run(self.source.get_task())
        self.assertEqual(result, None)

    def test_get_all_tasks_correct(self):
        mock_queue = AsyncMock()
        mock_queue.__aiter__.return_value = mock_queue
        mock_queue.__anext__ = AsyncMock(side_effect=["task1", "task2", StopAsyncIteration])

        with patch('src.Sources.file_source.TaskQueue', return_value=mock_queue):
            result = asyncio.run(self.source.get_all_tasks("High"))
            self.assertEqual(result, [])

    def test_get_all_tasks_empty(self):
        mock_queue = AsyncMock()
        mock_queue.__aiter__.return_value = mock_queue
        mock_queue.__anext__ = AsyncMock(side_effect=StopAsyncIteration)

        with patch('src.Sources.file_source.TaskQueue', return_value=mock_queue):
            result = asyncio.run(self.source.get_all_tasks("Normal"))
            self.assertEqual(result, [])