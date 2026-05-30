import json
import asyncio
import logging
from src.TaskQueue.task_queue import TaskQueue

class File_Source:
    def __init__(self, name: str, file_name: str, text:dict)->None:
        """
        Иницилизация источника-файла

        :param name: Имя источника
        :param file_name: имя файла формата json
        :param text: содержание файла
        """
        self.name = name
        self.file_name = file_name
        self.text = text
        self.tasks = TaskQueue(len(text), text, filter=None, type="file")

    @staticmethod
    async def create_source(name:str)->object:
        """
        Создание источника

        :param name: Имя источника
        :return: Объект-источник
        """
        logger = logging.getLogger(__name__)
        file_name = await asyncio.to_thread(input, "Enter file name: ")
        logger.info(f"Enter file name: {file_name}")
        try:
            with open(f"src//File_test//{file_name}.json", "r", encoding="utf-8") as f:
                text = json.load(f)
                return File_Source(name, file_name, text)
        except:
            logging.error("Error: no such file or file is empty")
            raise ValueError("Error: no such file or file is empty")
        

    async def get_task(self) ->str:
        """
        Получение одного задания и его печать

        """
        async for task in self.task:
            return task

            

    async def get_all_tasks(self, filter:str) ->list:
        """
        Получение всех заданий и из печать

        :param filter: слова для фильтрации
        """
        tasks = TaskQueue(len(self.text), self.text, filter, "file")
        tasks_list = []
        async for task in tasks:
            tasks_list.append(task)
        return tasks_list
        

    
        


