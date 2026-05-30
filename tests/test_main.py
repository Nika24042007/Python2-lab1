import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio
from src.main import main


class TestMain(unittest.TestCase):
    """
    Тесты для главной функции
    """
    def test_exit(self):
        inputs = ['exit']
        async def mock_to_thread(func, *args, **kwargs):
            return inputs.pop(0)
        with patch('asyncio.to_thread', side_effect=mock_to_thread):
            with self.assertRaises(SystemExit):
                asyncio.run(main())

    def test_uncorrrect_command(self):
        inputs = ['unknown', 'exit']
        async def mock_to_thread(func, *args, **kwargs):
            return inputs.pop(0)
        with (patch('asyncio.to_thread', side_effect=mock_to_thread),
              patch('builtins.print') as mock_print,
              patch('src.main.logging.error') as mock_log_error):
            with self.assertRaises(SystemExit):
                asyncio.run(main())
            mock_print.assert_any_call("Error: no such command")
            mock_log_error.assert_called_with("Error: no such command")

    def test_create_source_and_get_task(self):
        inputs = ['create_source', 'src1', 'file', 'get_task', 'src1', 'exit']
        async def mock_to_thread(func, *args, **kwargs):
            return inputs.pop(0)
        with (patch('asyncio.to_thread', side_effect=mock_to_thread),
              patch('builtins.print') as mock_print,
              patch('src.main.TYPE_SOURCE') as mock_type_source,
              patch('src.main.isinstance', return_value=True)):
            mock_source = AsyncMock()
            mock_source.get_task = AsyncMock(return_value='{"1": "task"}')
            mock_s = AsyncMock()
            mock_s.create_source = AsyncMock(return_value=mock_source)
            mock_type_source.__getitem__.return_value = mock_s

            with self.assertRaises(SystemExit):
                asyncio.run(main())
            mock_s.create_source.assert_called_once_with('src1')
            mock_source.get_task.assert_called_once()
            mock_print.assert_any_call('{"1": "task"}')

    def test_create_source_exist(self):
        inputs = ['create_source', 'dup', 'file', 'create_source', 'dup', 'file', 'exit']
        async def mock_to_thread(func, *args, **kwargs):
            return inputs.pop(0)
        with (patch('asyncio.to_thread', side_effect=mock_to_thread),
              patch('builtins.print') as mock_print,
              patch('src.main.logging.error') as mock_log_error,
              patch('src.main.TYPE_SOURCE') as mock_type_source,
              patch('src.main.isinstance', return_value=True)):
            mock_s = AsyncMock()
            mock_s.create_source = AsyncMock(return_value=MagicMock())
            mock_type_source.__getitem__.return_value = mock_s

            with self.assertRaises(SystemExit):
                asyncio.run(main())
            mock_print.assert_any_call("Error: source with such name already exsist. Change name of source")
            mock_log_error.assert_any_call("Error: source with such name already exsist. Change name of source")

    def test_get_task_from_no_exist_source(self):
        inputs = ['get_task', 'unknown', 'exit']
        async def mock_to_thread(func, *args, **kwargs):
            return inputs.pop(0)
        with (patch('asyncio.to_thread', side_effect=mock_to_thread),
              patch('builtins.print') as mock_print,
              patch('src.main.logging.error') as mock_log_error):
            with self.assertRaises(SystemExit):
                asyncio.run(main())
            mock_print.assert_any_call("Error: no such source. Please, create it")
            mock_log_error.assert_any_call("Error: no such source. Please, create it")