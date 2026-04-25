from src.Task.task_file import TaskFile
from src.TaskQueue.filters import status_filter, priopity_filter

class TaskQueueFile():
    def __init__(self, tasks: dict, filter: str):
        self.filter = filter
        self.tasks = tasks
        self.max_len = len(tasks)
        self.gen = self.generator()

    def generator(self):
            i = 0
            while i < self.max_len:
                text = self.tasks[i]
                task = TaskFile.create_task(text)
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
            print(self.max_len)
            return next(self.gen)
        except StopIteration:
            self.gen = self.generator()
            return next(self.gen)

        