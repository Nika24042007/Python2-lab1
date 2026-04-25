import json
import logging
from src.TaskQueue.task_queue_file import TaskQueueFile

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
        self.tasks = TaskQueueFile(text, filter=None)

    @staticmethod
    def create_source(name:str)->object:
        """
        Создание источника

        :param name: Имя источника
        :return: Объект-источник
        """
        logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")
        file_name = input("Enter file name: ")
        logging.info(f"Enter file name: {file_name}")
        try:
            with open(f"src//File_test//{file_name}.json", "r", encoding="utf-8") as f:
                text = json.load(f)
                return File_Source(name, file_name, text)
        except:
            logging.error("Error: no such file or file is empty")
            raise ValueError("Error: no such file or file is empty")
        

    def get_task(self) ->None:
        """
        Получение одного задания и его печать

        """
        logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")
        try:
            print(next(self.tasks))
        except ValueError as e:
            print(e)
            logging.error(e)

            

    def get_all_tasks(self, filter:str) ->None:
        """
        Получение всех заданий и из печать

        :param filter: слова для фильтрации
        """
        logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")
        try:
            tasks = TaskQueueFile(self.text, filter)
            for task in tasks:
                print(task)
                print("\n")
            return
        except ValueError as e:
            print(e)
            logging.error(e)
        

    
        


