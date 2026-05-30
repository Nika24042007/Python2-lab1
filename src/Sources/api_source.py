import logging
import asyncio
from src.TaskQueue.task_queue import TaskQueue


class Api_source:
    def __init__(self, name:str, n: int)->None:
        """
        Иницилизация источника-api

        :param name: Имя источника
        :param n: число задание в источнике
        """
        self.max_len = n
        self.name = name
        self.id = 0
        self.task = TaskQueue(self.max_len,"None", filter="None", type="api")

    async def get_task(self) ->str:
        """
        Получение одного задания и его печать

        """
        async for task in self.task:
            return task
            
    async def get_all_tasks(self, filter:str) ->list:
        """
        Получение всех заданий и их печать

        :param filter: слова для фильтрации
        """
        tasks = TaskQueue(self.max_len,"None", filter, "api")
        tasks_list = []
        async for task in tasks:
            tasks_list.append(task)
        return tasks_list


    @staticmethod
    async def create_source(name:str) -> object:
        """
        Создание источника

        :param name: Имя источника
        :return: Объект-источник
        """
        logger = logging.getLogger(__name__)
        n = await asyncio.to_thread(input, f"Enter the number of tasks: ")
        logger.info(f"Enter the number of tasks: {str(n)}")
        return Api_source(name, int(n))