import logging
from src.Task.task_api import TaskApi


class Api_source:
    def __init__(self, name:str)->None:
        """
        Иницилизация источника-api

        :param name: Имя источника
        """
        self.name = name
        self.id = 0

    def get_task(self) ->str:
        """
        Получение одного задания

        :return: Строка с заданием и id
        """
        logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")
        task = input("Enter payloud: ")
        logging.info(f"Enter payloud: {task}")
        self.id += 1
        return TaskApi.create_task(self.id, task)

    def get_all_tasks(self) ->list:
        """
        Получение всех заданий

        :return: Строка с заданиями и id
        """
        logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")
        n = int(input("Enter the number of tasks: "))
        logging.info(f"Enter the number of tasks: {str(n)}")
        tasks_list = []
        for i in range(n):
            task = input("Enter payloud: ")
            logging.info(f"Enter payloud: {task}")
            self.id += 1
            tasks_list.append(TaskApi.create_task(self.id, task))
        return tasks_list

    @staticmethod
    def create_source(name:str) -> object:
        """
        Создание источника

        :param name: Имя источника
        :return: Объект-источник
        """
        return Api_source(name)