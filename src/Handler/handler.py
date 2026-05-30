import asyncio

class HandlerWork:
    def __init__(self):pass

    @staticmethod
    async def in_work_normal(task):
        await asyncio.sleep(3)

    @staticmethod
    async def in_work_high(task):
        await asyncio.sleep(2)
    
    @staticmethod
    async def in_work_very_high(task):
        await asyncio.sleep(1)