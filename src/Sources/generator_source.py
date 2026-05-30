from random import randint
import logging
from src.TaskQueue.task_queue import TaskQueue

class Generator_source:
    def __init__(self, name: str, n: int) -> None:
        """
        Иницилизация источника генератора

        :param name: Название источника
        :param n: максимальное количество задач в источнике
        """
        self.name = name
        self.max_len = n
        self.task = TaskQueue(self.max_len,"None", filter="None", type="generator")

    async def get_task(self) ->str:
        """
        Получение одного задания и его печать

        """
        async for task in self.task:
            return task
    
    async def get_all_tasks(self, filter: str) ->list:
        """
        Получение всех заданий из источника и их печать

        :param filter: слова для фильтрации
        """
        
        tasks = TaskQueue(self.max_len,"None", filter, "generator")
        tasks_list = []
        async for task in tasks:
            tasks_list.append(task)
        return tasks_list
        

    @staticmethod
    async def create_source(name:str) -> object:
        """
        Создание источника с заданным именем

        :param name: Имя источника
        :retun: Объект-источник
        """
        n = randint(5, 100)
        return Generator_source(name, n)