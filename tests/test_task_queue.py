import unittest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from src.TaskQueue.task_queue import TaskQueue


class TestTaskQueue(unittest.TestCase):
    """тесты для TaskQueue"""
    
    def test_init(self):
        with patch('src.TaskQueue.task_queue.TYPE_GENERATOR'):
            queue = TaskQueue(10, "tasks", "None", "generator")
            self.assertEqual(queue.max_len, 10)
            self.assertEqual(queue.filter, "None")
    
    def test_generator_no_filter(self):
        with (patch('src.TaskQueue.task_queue.HandlerWork') as mock_handler,
             patch('src.TaskQueue.task_queue.TYPE_GENERATOR') as mock_type_gen):
            
            mock_handler.in_work_normal = AsyncMock()
            
            mock_task = MagicMock()
            mock_task.priority = "Normal"
            mock_type_gen["generator"].create_task.return_value = mock_task
            
            queue = TaskQueue(3, "test", "None", "generator")
            
            async def run():
                return [task async for task in queue.generator()]
            
            tasks = asyncio.run(run())
            self.assertEqual(len(tasks), 3)
            self.assertEqual(mock_handler.in_work_normal.call_count, 3)
    
    def test_generator_priority_filter(self):
        with (patch('src.TaskQueue.task_queue.HandlerWork') as mock_handler,
             patch('src.TaskQueue.task_queue.TYPE_GENERATOR') as mock_type_gen,
             patch('src.TaskQueue.task_queue.priopity_filter') as mock_priority):
            
            mock_handler.in_work_very_high = AsyncMock()
            
            mock_task = MagicMock()
            mock_task.priority = "Very high"
            mock_type_gen["generator"].create_task.return_value = mock_task
            mock_priority.return_value = True
            
            queue = TaskQueue(1, "test", "High", "generator")
            
            async def run():
                return [task async for task in queue.generator()]
            
            tasks = asyncio.run(run())
            self.assertEqual(len(tasks), 1)
            mock_priority.assert_called_once()
            mock_handler.in_work_very_high.assert_called_once()
    
    def test_generator_status_filter_and_high(self):
        with (patch('src.TaskQueue.task_queue.HandlerWork') as mock_handler,
             patch('src.TaskQueue.task_queue.TYPE_GENERATOR') as mock_type_gen,
             patch('src.TaskQueue.task_queue.status_filter') as mock_status):
            
            mock_handler.in_work_high = AsyncMock()
            
            mock_task = MagicMock()
            mock_task.priority = "High"
            mock_task.status = "In work"
            mock_type_gen["generator"].create_task.return_value = mock_task
            
            queue = TaskQueue(1, "test", "In work", "generator")
            
            async def run():
                return [task async for task in queue.generator()]
            
            tasks = asyncio.run(run())
            self.assertEqual(len(tasks), 1)
            mock_status.assert_called_once()
            mock_handler.in_work_high.assert_called_once()
    
    def test_generator_empty(self):
        with patch('src.TaskQueue.task_queue.TYPE_GENERATOR'):
            queue = TaskQueue(0, "test", "None", "generator")
            
            async def run():
                return [task async for task in queue.generator()]
            
            tasks = asyncio.run(run())
            self.assertEqual(len(tasks), 0)
    
    def test_anext_and_restart(self):
        with (patch('src.TaskQueue.task_queue.HandlerWork') as mock_handler,
             patch('src.TaskQueue.task_queue.TYPE_GENERATOR') as mock_type_gen):
            
            mock_handler.in_work_normal = AsyncMock()
            mock_handler.in_work_high = AsyncMock()
            mock_handler.in_work_very_high = AsyncMock()
            
            mock_task = MagicMock()
            mock_task.priority = "Normal"
            mock_type_gen["generator"].create_task.return_value = mock_task
            
            queue = TaskQueue(2, "test", "None", "generator")
            
            async def run():
                t1 = await queue.__anext__()
                t2 = await queue.__anext__()
                t3 = await queue.__anext__()
                return t1, t2, t3
            
            t1, t2, t3 = asyncio.run(run())
            self.assertIsNotNone(t1)
            self.assertIsNotNone(t2)
            self.assertIsNotNone(t3)
    
    def test_async_for(self):
        with (patch('src.TaskQueue.task_queue.HandlerWork') as mock_handler,
             patch('src.TaskQueue.task_queue.TYPE_GENERATOR') as mock_type_gen):
            
            mock_handler.in_work_normal = AsyncMock()
            
            mock_task = MagicMock()
            mock_task.priority = "Normal"
            mock_type_gen["generator"].create_task.return_value = mock_task
            
            queue = TaskQueue(2, "test", "None", "generator")
            
            async def run():
                tasks = []
                async for task in queue:
                    tasks.append(task)
                return tasks
            
            tasks = asyncio.run(run())
            self.assertEqual(len(tasks), 2)
    
    def test_filter_rejection(self):
        with (patch('src.TaskQueue.task_queue.HandlerWork') as mock_handler,
             patch('src.TaskQueue.task_queue.TYPE_GENERATOR') as mock_type_gen,
             patch('src.TaskQueue.task_queue.priopity_filter') as mock_priority):
            
            mock_handler.in_work_normal = AsyncMock()
            
            mock_task = MagicMock()
            mock_task.priority = "Normal"
            mock_type_gen["generator"].create_task.return_value = mock_task
            mock_priority.return_value = False
            
            queue = TaskQueue(2, "test", "High", "generator")
            
            async def run():
                return [task async for task in queue.generator()]
            
            tasks = asyncio.run(run())
            self.assertEqual(len(tasks), 0)