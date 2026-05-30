import unittest
from unittest.mock import patch
import asyncio
from src.Sources.generator_source import Generator_source


class TestGeneratorSource(unittest.TestCase):
    """
    Тесты для класса Generator_source
    """

    def test_create_source(self):
        async def run():
            with patch('src.Sources.generator_source.randint') as mock_randint:
                mock_randint.return_value = 10
                source = await Generator_source.create_source("test")
                mock_randint.assert_called_once_with(5, 100)
                self.assertIsInstance(source, Generator_source)
                self.assertEqual(source.name, "test")
                self.assertEqual(source.max_len, 10)
        asyncio.run(run())

    def test_get_task(self):
        async def task_gen():
            yield "task_object"

        source = Generator_source("test", 5)
        source.task = task_gen()
        result = asyncio.run(source.get_task())
        self.assertEqual(result, "task_object")

    def test_get_all_tasks(self):
        async def task_gen():
            yield "task1"
            yield "task2"

        with patch('src.Sources.generator_source.TaskQueue', return_value=task_gen()):
            source = Generator_source("test", 3)
            result = asyncio.run(source.get_all_tasks("High"))
            self.assertEqual(result, ["task1", "task2"])

    def test_get_task_value_error(self):
        async def task_gen():
            raise ValueError("Test error")
            yield

        source = Generator_source("test", 1)
        source.task = task_gen()
        with self.assertRaises(ValueError):
            asyncio.run(source.get_task())

    def test_get_all_tasks_value_error(self):
        async def task_gen():
            raise ValueError("Iter error")
            yield

        with patch('src.Sources.generator_source.TaskQueue', return_value=task_gen()):
            source = Generator_source("test", 2)
            with self.assertRaises(ValueError):
                asyncio.run(source.get_all_tasks("Normal"))

    def test_get_all_tasks_empty(self):
        async def task_gen():
            return
            yield

        with patch('src.Sources.generator_source.TaskQueue', return_value=task_gen()):
            source = Generator_source("test", 0)
            result = asyncio.run(source.get_all_tasks("None"))
            self.assertEqual(result, [])