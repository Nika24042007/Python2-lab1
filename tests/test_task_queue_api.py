import unittest
from unittest.mock import patch, MagicMock
from src.TaskQueue.task_queue_api import TaskQueueApi

class TestTaskQueueApiMinimal(unittest.TestCase):
    """
    Тесты для task_queue_api
    """
    def test_init(self):
        queue = TaskQueueApi(max_len=5, filter="High")
        self.assertEqual(queue.max_len, 5)
        self.assertEqual(queue.filter, "High")
        self.assertIsNotNone(queue.gen) 

    def test_generator_filter_and_yield(self):
        with (patch('builtins.input', side_effect=["payload1", "payload2", "payload3"]),
             patch('src.TaskQueue.task_queue_api.TaskApi.create_task') as mock_create,
             patch('src.TaskQueue.task_queue_api.priopity_filter') as mock_priority,
             patch('src.TaskQueue.task_queue_api.status_filter') as mock_status):

            task1 = MagicMock(priority="High", status="In work")
            task2 = MagicMock(priority="Normal", status="Over")
            task3 = MagicMock(priority="High", status="In work")
            mock_create.side_effect = [task1, task2, task3]

            mock_priority.side_effect = [True, False, True]

            queue = TaskQueueApi(max_len=2, filter="High")
            gen = queue.generator()
            result = list(gen)

            self.assertEqual(result, [task1, task3])
            self.assertEqual(mock_create.call_count, 3)
            expected_calls = [((0, "payload1"),), ((1, "payload2"),), ((2, "payload3"),)]
            self.assertEqual(mock_create.call_args_list, expected_calls)
            mock_priority.assert_any_call("High", "High")
            mock_priority.assert_any_call("High", "Normal")
            mock_priority.assert_any_call("High", "High")
            self.assertEqual(mock_priority.call_count, 3)
            mock_status.assert_not_called()

    def test_next_restarts_generator(self):
        with (patch('builtins.input', return_value="some_payload"),
             patch('src.TaskQueue.task_queue_api.TaskApi.create_task') as mock_create,
             patch('src.TaskQueue.task_queue_api.priopity_filter') as mock_priority):

            task = MagicMock(priority="High")
            mock_create.return_value = task
            mock_priority.return_value = True

            queue = TaskQueueApi(max_len=0, filter="High")
            first = next(queue)
            self.assertEqual(first, task)
            second = next(queue)
            self.assertEqual(second, task)
            self.assertEqual(mock_create.call_count, 2)
