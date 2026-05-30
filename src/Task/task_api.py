import logging
import asyncio
from datetime import date
from src.Task.discriprors import ValidateData, ValidatorPriority

class TaskApi():
    data_start = ValidateData()
    data_end = ValidateData()
    priority = ValidatorPriority()

    def __init__(self, id:int, payloud:str, priority:str, data_start:str, data_end:str)-> None:
        """
        Иницилизация задания из api

        :param id: id задания
        :param payloud: описание задания
        :param priority: приоритет задания
        :param data_start: дата начала выполнения задания
        :param data_end: дата окончания выполнения задания
        """
        self.id = id
        self.payloud = payloud
        self.priority = priority
        self.data_start = data_start
        self.data_end = data_end

    @property
    def deadline(self)-> date:
        """
        Подсчет дедлайна

        :return: значение дедлайна
        """
        return self.data_end-date.today()

    @property
    def status(self)->str:
        """
        Подсчет статуса

        :return: Статус
        """
        if self.deadline.days >= 0:
            return "there's still time"
        else:
            return "deadline over"

    @property
    def data_end(self)->date:
        return self._data_end
    
    @property
    def data_start(self)->date:
        return self._data_start
    
    @data_start.setter
    def data_start(self, value:str)->None:
        st_data = list(map(int, value.split("-")))
        self._data_start = date(st_data[-1], st_data[1], st_data[0])

    @data_end.setter
    def data_end(self, value:str)->None:
        data = list(map(int, value.split("-")))
        if date(data[-1], data[1], data[0]) > self.data_start:
            self._data_end = date(data[-1], data[1], data[0])
        else:
            raise ValueError("Uncorrect end data")
    

    @staticmethod
    async def create_task(id:int, text:str)->object:
        """
        Создание задания для api

        :param id: id задания
        :param pauloud: описание задания
        :return: Объект класса TaskApi
        """
        logger = logging.getLogger(__name__)
        payloud = await asyncio.to_thread(input, "Enter payloud: ")
        logger.info(f"Enter payloud: {payloud}")
        data_start = await asyncio.to_thread(input, "Enter start data(dd-mm-yyyy): ")
        logger.info(f"Enter start data(dd.mm.yyyy): {data_start}")
        data_end = await asyncio.to_thread(input, "Enter end data(dd-mm-yyyy): ")
        logger.info(f"Enter end data(dd.mm.yyyy): {data_end}")
        priority = await asyncio.to_thread(input, "Enter priority(High, Normal, Very high): ")
        logger.info(f"Enter prioriti(High, Normal, Very high): {priority}")
        return TaskApi(id, payloud, priority, data_start, data_end)
    
    def __str__(self)->str:
        """
        Вывод задания

        :return: Строка с данными
        """
        
        return f"id: {self.id}\n payload: {self.payloud}\n priority: {self.priority}\n status: {self.status}\n start: {self.data_start}\n end: {self.data_end}\n deadline: {self.deadline}\n"
        