from src.TaskQueue.filters import status_filter, priopity_filter
from src.Task.task_api import TaskApi
import logging

class TaskQueueApi():
    def __init__(self, max_len:int, filter: str):
        self.max_len = max_len
        self.filter = filter
        self.gen = self.generator()

    def generator(self):
        logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")
        i = 0
        while i <= self.max_len:
            task = input("Enter payloud: ")
            logging.info(f"Enter payloud: {task}")
            task = TaskApi.create_task(i, task)

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