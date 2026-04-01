from src.random_text import random_text
from random import randint
from src.Task.task_generator import TaskGenerator

class Generator_source:
    def __init__(self, name: str) -> None:
        """
        Иницилизация источника генератора

        :param name: Название источника
        """
        self.name = name
        self.id = 0

    def get_task(self) ->object:
        """
        Получение одного задания

        :return: Объект класса TaskGenerator
        """
        self.id += 1
        return TaskGenerator.create_task(self.id, random_text())

    def get_all_tasks(self) ->list:
        """
        Получение всех заданий из источника

        :return: Список с объектами класса TaskGenerator
        """
        n = randint(1, 20)
        tasks_list = []
        for i in range(n):
            self.id += 1
            tasks_list.append(TaskGenerator.create_task(self.id, random_text()))
        return tasks_list

    @staticmethod
    def create_source(name:str) -> object:
        """
        Создание источника с заданным именем

        :param name: Имя источника
        :retun: Объект-источник
        """
        return Generator_source(name)