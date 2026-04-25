import unittest
from unittest.mock import patch, MagicMock, call
from src.Sources.generator_source import Generator_source


class TestGeneratorSource(unittest.TestCase):
    """
    Тесты для класса Generator_source
    """

    def test_create_source(self):
        with (patch('src.Sources.generator_source.randint') as mock_randint):
            mock_randint.return_value = 10
            source = Generator_source.create_source("test")
            mock_randint.assert_called_once_with(5, 100)
            self.assertIsInstance(source, Generator_source)
            self.assertEqual(source.name, "test")
            self.assertEqual(source.max_len, 10)

    def test_get_task(self):
        with (patch('src.Sources.generator_source.TaskQueueGen') as MockTaskQueue,
             patch('builtins.print') as mock_print):

            mock_task = MagicMock()
            mock_task.__str__ = MagicMock(return_value="Task object")
            mock_queue = MagicMock()
            mock_queue.__next__ = MagicMock(return_value=mock_task)
            MockTaskQueue.return_value = mock_queue

            source = Generator_source("test", 5)
            source.get_task()

            MockTaskQueue.assert_called_once_with(5, filter="None")
            mock_queue.__next__.assert_called_once()
            mock_print.assert_called_once()

    def test_get_all_tasks(self):
        with (patch('src.Sources.generator_source.TaskQueueGen') as MockTaskQueue,
             patch('builtins.print') as mock_print):

            task1 = MagicMock()
            task2 = MagicMock()
            tasks_iter = iter([task1, task2])
            mock_task_queue = MagicMock()
            mock_task_queue.__iter__ = MagicMock(return_value=tasks_iter)
            MockTaskQueue.return_value = mock_task_queue

            source = Generator_source("test", 3)
            source.get_all_tasks("High")

            expected_calls = [call(3, filter="None"), call(3, "High")]
            MockTaskQueue.assert_has_calls(expected_calls)
            self.assertEqual(MockTaskQueue.call_count, 2)

            mock_print.assert_any_call(task1)
            mock_print.assert_any_call("\n")
            mock_print.assert_any_call(task2)
            mock_print.assert_any_call("\n")
            self.assertEqual(mock_print.call_count, 4)

    def test_get_task_value_error(self):
        with (patch('src.Sources.generator_source.TaskQueueGen') as MockTaskQueue,
             patch('builtins.print') as mock_print,
             patch('src.Sources.generator_source.logging.error') as mock_log_error):

            mock_queue = MagicMock()
            mock_queue.__next__ = MagicMock(side_effect=ValueError("Test error"))
            MockTaskQueue.return_value = mock_queue

            source = Generator_source("test", 1)
            source.get_task()

            mock_log_error.assert_called_once()
            mock_print.assert_called_once()

    def test_get_all_tasks_value_error(self):
        with (patch('src.Sources.generator_source.TaskQueueGen') as MockTaskQueue,
             patch('builtins.print') as mock_print,
             patch('src.Sources.generator_source.logging.error') as mock_log_error):

            mock_task_queue = MagicMock()
            mock_task_queue.__iter__ = MagicMock(side_effect=ValueError("Iter error"))
            MockTaskQueue.return_value = mock_task_queue

            source = Generator_source("test", 2)
            source.get_all_tasks("Normal")

            mock_log_error.assert_called_once()
            mock_print.assert_called_once()

    def test_get_all_tasks_empty(self):
        with (patch('src.Sources.generator_source.TaskQueueGen') as MockTaskQueue,
             patch('builtins.print') as mock_print):

            mock_task_queue = MagicMock()
            mock_task_queue.__iter__ = MagicMock(return_value=iter([]))
            MockTaskQueue.return_value = mock_task_queue

            source = Generator_source("test", 0)
            source.get_all_tasks("None")

            mock_print.assert_not_called()
