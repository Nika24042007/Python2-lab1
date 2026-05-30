from src.TaskQueue.filters import status_filter, priopity_filter
from src.Constans.constans_type_generator import TYPE_GENERATOR
from src.Handler.handler import HandlerWork
import inspect

class TaskQueue():
    def __init__(self, max_len: int, tasks: dict| str, filter: str, type:str):
        self.filter = filter
        self.tasks = tasks
        self.max_len = max_len
        self.gen = self.generator()
        self.type = type

    async def generator(self):
            i = 0
            while i < self.max_len:
                create_task = TYPE_GENERATOR[self.type].create_task
            
                if inspect.iscoroutinefunction(create_task):
                    task = await create_task(i, self.tasks)
                else:
                    task = create_task(i, self.tasks)

                if self.filter in ["Normal", "High", "Very high"]:
                    is_match = priopity_filter(self.filter, task.priority)
                elif self.filter in ["Over", "In work"]:
                    is_match = status_filter(self.filter, task.status)
                else:
                    is_match = True
                
                if task.priority == "Very high":
                    await HandlerWork.in_work_very_high(task)
                elif task.priority == "High":
                    await HandlerWork.in_work_high(task)
                else:
                    await HandlerWork.in_work_normal(task)

                if is_match:
                    yield task
                i += 1

    def __aiter__(self):
        return self.generator()
    
    async def __anext__(self):
        try:
            return await self.gen.__anext__()
        except StopAsyncIteration:
            self.gen = self.generator()
            return await self.gen.__anext__()