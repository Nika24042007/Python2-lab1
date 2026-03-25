from src.random_text import random_text
from random import randint

class Generator_source:
    def __init__(self, name: str) -> None:
        """
        Иницилизация источника генератора

        :param name: Название источника
        """
        self.name = name
        self.id = 0

    def get_task(self) ->str:
        """
        Получение одного задания

        :return: Строка с задвнием и ее id
        """
        task_dict = {}
        self.id += 1
        task_dict[self.id] = random_text()
        return str(task_dict)

    def get_all_tasks(self) ->str:
        """
        Получение всех заданий из источника

        :return: Строка содержащие id и само задание
        """
        n = randint(1, 20)
        tasks_dict = {}
        for i in range(n):
            self.id += 1
            tasks_dict[self.id] = random_text()
        return str(tasks_dict)

    @staticmethod
    def create_source(name:str) -> object:
        """
        Создание источника с заданным именем

        :param name: Имя источника
        :retun: Объект-источник
        """
        return Generator_source(name)