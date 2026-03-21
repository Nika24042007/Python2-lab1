import json
import logging

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

    def get_task(self) ->str:
        """
        Получение одного задания

        :return: Строка с заданием
        """
        logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")
        try:
            with open(f"src//File_test//{self.file_name}.json", "r", encoding="utf-8") as f:
                tasks = json.load(f)
                print(f"Choice id of task: {list(tasks.keys())} ")
                logging.info(f"Choice id if task: {list(tasks.keys())} ")
                id = input("id: ")
                logging.info(f"id: {id}")
                return tasks[id]
        except:
            logging.error("Error: no such file or file is empty")
            return "Error: no such file or file is empty"
            

    def get_all_tasks(self) ->str:
        """
        Получение всех заданий

        :return: Строка с заданиями и их id
        """
        logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")
        try:
            with open(f"src//File_test//{self.file_name}.json", "r", encoding="utf-8") as f:
                tasks = json.load(f)
                return str(tasks)
        except:
            logging.error("Error: no such file or file is empty")
            return "Error: no such file or file is empty"

    
        


