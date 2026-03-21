import logging


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
        task = input("Enter task: ")
        logging.info(f"Enter task: {task}")
        self.id += 1
        task_dict = {}
        task_dict[self.id] = task
        return str(task_dict)

    def get_all_tasks(self) ->str:
        """
        Получение всех заданий

        :return: Строка с заданиями и id
        """
        logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")
        n = int(input("Enter the number of tasks: "))
        logging.info(f"Enter the number of tasks: {str(n)}")
        tasks_dict = {}
        for i in range(n):
            task = input("Enter task: ")
            logging.info(f"Enter task: {task}")
            self.id += 1
            tasks_dict[self.id] = task
        return str(tasks_dict)

    @staticmethod
    def create_source(name:str) -> object:
        """
        Создание источника

        :param name: Имя источника
        :return: Объект-источник
        """
        return Api_source(name)