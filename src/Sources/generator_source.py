from random import randint
import logging
from src.TaskQueue.task_queue_gen import TaskQueueGen

class Generator_source:
    def __init__(self, name: str, n: int) -> None:
        """
        Иницилизация источника генератора

        :param name: Название источника
        :param n: максимальное количество задач в источнике
        """
        self.name = name
        self.max_len = n
        self.task = TaskQueueGen(self.max_len, filter="None")

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
    def get_all_tasks(self, filter: str) ->None:
        """
        Получение всех заданий из источника и их печать

        :param filter: слова для фильтрации
        """
        logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")
        try:
            tasks = TaskQueueGen(self.max_len, filter)
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
        Создание источника с заданным именем

        :param name: Имя источника
        :retun: Объект-источник
        """
        n = randint(5, 100)
        return Generator_source(name, n)