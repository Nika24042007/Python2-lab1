import unittest
from unittest.mock import patch, MagicMock
from src.TaskQueue.task_queue_gen import TaskQueueGen

class TestTaskQueueGen(unittest.TestCase):
    """
    Тесты для task_queue_gen
    """
    def test_filter_correct(self):
        with (patch('src.Task.task_generator.TaskGenerator.create_task') as mock_create,
             patch('src.random_text.random_text'),
             patch('src.TaskQueue.task_queue_gen.priopity_filter') as mock_priority,
             patch('src.TaskQueue.task_queue_gen.status_filter') as mock_status):

            task = MagicMock(priority="High", status="In work")
            mock_create.return_value = task
            mock_priority.return_value = True
            mock_status.return_value = True

            queue1 = TaskQueueGen(max_len=1, filter="High")
            next(queue1.generator())
            mock_priority.assert_called_with("High", "High")
            mock_status.assert_not_called()
            mock_priority.reset_mock()

            queue2 = TaskQueueGen(max_len=1, filter="In work")
            next(queue2.generator())
            mock_status.assert_called_with("In work", "In work")
            mock_priority.assert_not_called()
            mock_status.reset_mock()

            queue3 = TaskQueueGen(max_len=1, filter="None")
            next(queue3.generator())
            mock_priority.assert_not_called()
            mock_status.assert_not_called()

    def test_generator_filters_tasks_and_yields_correct_count(self):
        with (patch('src.Task.task_generator.TaskGenerator.create_task') as mock_create,
            patch('src.random_text.random_text'),
            patch('src.TaskQueue.filters.priopity_filter') as mock_priority):

            tasks = [MagicMock(priority="High"), MagicMock(priority="Normal"), MagicMock(priority="High")]
            mock_create.side_effect = tasks
            mock_priority.side_effect = [True, False, True]

            queue = TaskQueueGen(max_len=2, filter="High")
            gen = queue.generator()
            result = list(gen)

            self.assertEqual(result, [tasks[0], tasks[2]])
            self.assertEqual(mock_create.call_count, 3)

    def test_next_restarts_generator(self):
        with (patch('src.Task.task_generator.TaskGenerator.create_task') as mock_create,
             patch('src.random_text.random_text'),
             patch('src.TaskQueue.filters.priopity_filter') as mock_priority):

            mock_task = MagicMock(priority="High")
            mock_create.return_value = mock_task
            mock_priority.return_value = True

            queue = TaskQueueGen(max_len=9, filter="High")

            first = next(queue)
            self.assertEqual(first, mock_task)
            second = next(queue)
            self.assertEqual(second, mock_task)
            self.assertEqual(mock_create.call_count, 2)