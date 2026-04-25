from src.Task.task_generator import TaskGenerator
from src.random_text import random_text
from src.TaskQueue.filters import status_filter, priopity_filter

class TaskQueueGen():
    def __init__(self, max_len:int, filter: str):
        self.max_len = max_len
        self.filter = filter
        self.gen = self.generator()

    def generator(self):
        i = 0
        while i <= self.max_len:
            task = TaskGenerator.create_task(i, random_text())

            if self.filter in ["Normal", "High", "Very high"]:
                is_match = priopity_filter(self.filter, task.priority)
            elif self.filter in ["Over", "In work"]:
                is_match = status_filter(self.filter, task.status)
            else:
                is_match = True

            if is_match:
                yield task
            i += 1

    def __iter__(self):
        return self.generator()
    
    def __next__(self):
        try:
            return next(self.gen)
        except StopIteration:
            self.gen = self.generator()
            return next(self.gen)

        