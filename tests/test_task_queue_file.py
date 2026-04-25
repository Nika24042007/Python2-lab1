import unittest
from unittest.mock import patch, MagicMock
from src.TaskQueue.task_queue_file import TaskQueueFile

class TestTaskQueueFile(unittest.TestCase):
    """
    Тесты для task_queue_file
    """
    def test_init(self):
        tasks = {0: "task0", 1: "task1"}
        queue = TaskQueueFile(tasks, filter="High")
        self.assertEqual(queue.filter, "High")
        self.assertEqual(queue.tasks, tasks)
        self.assertEqual(queue.max_len, 2)
        self.assertIsNotNone(queue.gen)

    def test_generator_filter_and_yields_correct_tasks(self):
        tasks = {0: "t0", 1: "t1", 2: "t2"}

        with(patch('src.TaskQueue.task_queue_file.TaskFile.create_task') as mock_create,
             patch('src.TaskQueue.task_queue_file.priopity_filter') as mock_priority,
             patch('src.TaskQueue.task_queue_file.status_filter') as mock_status):

            task0 = MagicMock(priority="High")
            task1 = MagicMock(priority="Normal")
            task2 = MagicMock(priority="High")
            mock_create.side_effect = [task0, task1, task2]
            mock_priority.side_effect = [True, False, True]

            queue = TaskQueueFile(tasks, filter="High")
            gen = queue.generator()
            result = list(gen)

            self.assertEqual(result, [task0, task2])
            self.assertEqual(mock_create.call_count, 3)
            expected_calls = [((tasks[0],),), ((tasks[1],),), ((tasks[2],),)]
            self.assertEqual(mock_create.call_args_list, expected_calls)
            mock_priority.assert_any_call("High", "High")
            mock_priority.assert_any_call("High", "Normal")
            self.assertEqual(mock_priority.call_count, 3)
            mock_status.assert_not_called()

    def test_next_restarts_generator(self):
        tasks = {0: "only"}

        with (patch('src.TaskQueue.task_queue_file.TaskFile.create_task') as mock_create,
             patch('src.TaskQueue.task_queue_file.priopity_filter') as mock_priority,
             patch('builtins.print') as mock_print):

            task = MagicMock(priority="High")
            mock_create.return_value = task
            mock_priority.return_value = True

            queue = TaskQueueFile(tasks, filter="High")
            first = next(queue)
            self.assertEqual(first, task)
            second = next(queue)
            self.assertEqual(second, task)
            self.assertEqual(mock_create.call_count, 2)
            self.assertEqual(mock_priority.call_count, 2)
            mock_print.assert_called_with(1)
