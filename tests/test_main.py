import unittest
from unittest.mock import patch, MagicMock
from src.main import main


class TestMain(unittest.TestCase):
    """
    Тесты для главной функции
    """
    def test_exit(self):
        """Выход из программы."""
        with (patch('builtins.input', return_value='exit')):
           with self.assertRaises(SystemExit):
                main()

    def test_uncorrrect_command(self):
        with (patch('builtins.input', side_effect=['unknown', 'exit']),
             patch('builtins.print') as mock_print,
             patch('src.main.logging.error') as mock_log_error):
            with self.assertRaises(SystemExit):
                main()
            mock_print.assert_any_call("Error: no such command")
            mock_log_error.assert_called_with("Error: no such command")

    def test_create_source_and_get_task(self):
        with (patch('builtins.input', side_effect=['create_source', 'src1', 'file','get_task', 'src1','exit']),
             patch('builtins.print') as mock_print,
             patch('src.main.TYPE_SOURCE') as mock_type_source,
             patch('src.main.isinstance', return_value=True)):

            mock_source = MagicMock()
            mock_source.get_task.return_value = '{"1": "task"}'
            mock_s = MagicMock()
            mock_s.create_source.return_value = mock_source
            mock_type_source.__getitem__.return_value = mock_s

            with self.assertRaises(SystemExit):
                main()
            mock_s.create_source.assert_called_once_with('src1')
            mock_source.get_task.assert_called_once()
            mock_print.assert_any_call('{"1": "task"}')

    def test_create_source_exist(self):
        with (patch('builtins.input', side_effect=['create_source', 'dup', 'file','create_source', 'dup', 'file','exit']), \
             patch('builtins.print') as mock_print,
             patch('src.main.logging.error') as mock_log_error,
             patch('src.main.TYPE_SOURCE') as mock_type_source,
             patch('src.main.isinstance', return_value=True)):

            mock_s = MagicMock()
            mock_s.create_source.return_value = MagicMock()
            mock_type_source.__getitem__.return_value = mock_s

            with self.assertRaises(SystemExit):
                main()
            mock_print.assert_any_call("Error: source with such name already exsist. Change name of source")
            mock_log_error.assert_any_call("Error: source with such name already exsist. Change name of source")

    def test_get_task_from_no_exist_source(self):
        with (patch('builtins.input', side_effect=['get_task', 'unknown','exit']),
             patch('builtins.print') as mock_print,
             patch('src.main.logging.error') as mock_log_error):

            with self.assertRaises(SystemExit):
                main()
            mock_print.assert_any_call("Error: no such source. Please, create it")
            mock_log_error.assert_any_call("Error: no such source. Please, create it")
