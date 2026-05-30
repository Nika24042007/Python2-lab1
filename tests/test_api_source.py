import unittest
from unittest.mock import patch, AsyncMock
import asyncio
from src.Sources.api_source import Api_source


class TestApiSource(unittest.TestCase):
    """Тесты для Api_source"""

    def test_create_source(self):
        async def mock_to_thread(func, *args, **kwargs):
            return "5"
        with patch('asyncio.to_thread', side_effect=mock_to_thread):
            source = asyncio.run(Api_source.create_source("test_name"))
            self.assertIsInstance(source, Api_source)
            self.assertEqual(source.name, "test_name")
            self.assertEqual(source.max_len, 5)

    def test_get_task(self):
        source = Api_source("test", 5)
        async def task_gen():
            yield "task1"
        source.task = task_gen()
        result = asyncio.run(source.get_task())
        self.assertEqual(result, "task1")

    def test_get_all_tasks(self):
        async def task_gen():
            yield "task1"
            yield "task2"
        with patch('src.Sources.api_source.TaskQueue', return_value=task_gen()):
            source = Api_source("test", 5)
            result = asyncio.run(source.get_all_tasks("None"))
            self.assertEqual(result, ["task1", "task2"])

    def test_get_task_value_error(self):
        source = Api_source("test", 5)
        async def task_gen():
            raise ValueError("Test error")
            yield
        source.task = task_gen()
        with self.assertRaises(ValueError):
            asyncio.run(source.get_task())

    def test_get_all_tasks_value_error(self):
        async def task_gen():
            raise ValueError("Iter error")
            yield
        with patch('src.Sources.api_source.TaskQueue', return_value=task_gen()):
            source = Api_source("test", 5)
            with self.assertRaises(ValueError):
                asyncio.run(source.get_all_tasks("None"))

    def test_get_all_tasks_empty(self):
        async def task_gen():
            return
            yield
        with patch('src.Sources.api_source.TaskQueue', return_value=task_gen()):
            source = Api_source("test", 0)
            result = asyncio.run(source.get_all_tasks("None"))
            self.assertEqual(result, [])