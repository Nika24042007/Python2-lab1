import logging
from src.Task.task_api import TaskApi
from src.TaskQueue.task_queue_api import TaskQueueApi


class Api_source:
    def __init__(self, name:str)->None:
        """
        Иницилизация источника-api

        :param name: Имя источника
        """
        self.max_len = 10
        self.name = name
        self.id = 0
        self.task = TaskQueueApi(self.max_len, filter="None")

    def get_task(self) ->None:
        """
        Получение одного задания и его печать

        """
        logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")
        try:
            print(next(self.task))
            return
        except ValueError as e:
            print(e)
            logging.error(e)
            return
            
    def get_all_tasks(self, filter:str) ->None:
        """
        Получение всех заданий и их печать

        :param filter: слова для фильтрации
        """
        logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")
        if self.max_len == 10:
            n = int(input("Enter the number of tasks: "))
            logging.info(f"Enter the number of tasks: {str(n)}")
            self.max_len = n
        try:
            tasks = TaskQueueApi(self.max_len, filter)
            for task in tasks:
                print(task)
                print("\n")
            return
        except ValueError as e:
            print(e)
            logging.error(e)
            return


    @staticmethod
    def create_source(name:str) -> object:
        """
        Создание источника

        :param name: Имя источника
        :return: Объект-источник
        """
        return Api_source(name)