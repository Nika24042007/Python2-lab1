import logging
from datetime import date
from src.Task.discriprors import ValidateData, ValidatorPriority

class TaskApi():
    data_start = ValidateData()
    data_end = ValidateData()
    priority = ValidatorPriority()

    def __init__(self, id:int, payloud:str, priority:str, data_start:str, data_end:str):
        self.id = id
        self.payloud = payloud
        self.priority = priority
        self.data_start = data_start
        self.data_end = data_end

    @property
    def deadline(self):
        data = list(map(int, self.data_end.split(".")))
        st_data = list(map(int, self.data_start.split(".")))
        return date(data[-1], data[1], data[0])-date(st_data[-1], st_data[1], st_data[0])

    @property
    def status(self):
        if self.deadline.days >= 0:
            return "there's still time"
        else:
            return "deadline over"

    @property
    def data_end(self):
        return self._data_end
    
    @data_end.setter
    def data_end(self, value):
        data = list(map(int, value.split(".")))
        st_data = list(map(int, self.data_start.split(".")))
        if date(data[-1], data[1], data[0]) > date(st_data[-1], st_data[1], st_data[0]):
            self._data_end = value
        else:
            raise ValueError("Uncorrect end data")
    

    @staticmethod
    def create_task(id:int, payloud:str):
        logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")
        data_start = input("Enter start data(dd.mm.yyyy): ")
        logging.info(f"Enter start data(dd.mm.yyyy): {data_start}")
        data_end = input("Enter end data(dd.mm.yyyy): ")
        logging.info(f"Enter end data(dd.mm.yyyy): {data_end}")
        priority = input("Enter priority(High, Normal, Very high): ")
        logging.info(f"Enter prioriti(High, Normal, Very high): {priority}")
        return TaskApi(id, payloud, priority, data_start, data_end)
    
    def __str__(self):
        
        return f"id: {self.id}\n payload: {self.payloud}\n priority: {self.priority}\n status: {self.status}\n start: {self.data_start}\n end: {self.data_end}\n deadline: {self.deadline}\n"
        