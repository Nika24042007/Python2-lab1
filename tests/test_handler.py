import unittest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock, call
from src.Handler.handler import HandlerWork


class TestHandlerWork(unittest.TestCase):
    """тесты для HandlerWork"""
    
    def test_init(self):
        handler = HandlerWork()
        self.assertIsInstance(handler, HandlerWork)
    
    def test_in_work_normal(self):
        with patch('src.Handler.handler.asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            async def run():
                await HandlerWork.in_work_normal(MagicMock())
            asyncio.run(run())
            mock_sleep.assert_called_once_with(3)
    
    def test_in_work_high(self):
        with patch('src.Handler.handler.asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            async def run():
                await HandlerWork.in_work_high(MagicMock())
            asyncio.run(run())
            mock_sleep.assert_called_once_with(2)
    
    def test_in_work_very_high(self):
        with patch('src.Handler.handler.asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            async def run():
                await HandlerWork.in_work_very_high(MagicMock())
            asyncio.run(run())
            mock_sleep.assert_called_once_with(1)