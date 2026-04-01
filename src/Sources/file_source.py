import json
import logging
from src.Task.task_file import TaskFile

class File_Source:
    def __init__(self, name: str, file_name: str)->None:
        """
        Иницилизация источника-файла

        :param name: Имя источника
        :param file_name: имя файла формата json
        """
        self.name = name
        self.file_name = file_name

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
        return File_Source(name, file_name)

    def get_task(self) ->object:
        """
        Получение одного задания

        :return: Объект класса TaskFile
        """
        logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")
        try:
            with open(f"src//File_test//{self.file_name}.json", "r", encoding="utf-8") as f:
                text = json.load(f)
                list_id = []
                for task in text:
                    list_id.append(task["id"])
                ch_id = int(input(f"Enter id from list {list_id}: "))
                logging.info(f"Enter id from list {list_id}: {ch_id}")
                count = 0
                for task in text:
                    if task["id"] == ch_id:
                        task_text = TaskFile.create_task(text[count])
                    count += 1
                return task_text
        except:
            logging.error("Error: no such file or file is empty")
            raise ValueError("Error: no such file or file is empty")
            

    def get_all_tasks(self) ->list:
        """
        Получение всех заданий

        :return: Список с объектами класса TaskFile
        """
        logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")
        try:
            with open(f"src//File_test//{self.file_name}.json", "r", encoding="utf-8") as f:
                tasks = json.load(f)
                list_tasks = []
                for task in tasks:
                    print(task)
                    task_st = TaskFile.create_task(task)
                    list_tasks.append(task_st)
                return list_tasks
        except:
            logging.error("Error: no such file or file is empty")
            raise ValueError("Error: no such file or file is empty")

    
        


