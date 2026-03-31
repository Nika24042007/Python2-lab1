from src.Task.discriprors import ValidateData, ValidatorPriority
from datetime import date

class TaskFile():
    data_start = ValidateData
    data_end = ValidateData
    priority = ValidatorPriority

    def __init__(self, id:int, payloud: str, data_start:str, data_end:str, priority:str):
        self.id = id
        self.payloud = payloud
        self.data_start = data_start
        self.data_end = data_end
        self.priority = priority

    @property
    def data_end(self)->str:
        return self._data_end
    
    @data_end.setter
    def data_end(self, value)->None:
        data = list(map(int, value.split(".")))
        st_data = list(map(int, self.data_start.split(".")))
        if date(data[-1], data[1], data[0]) > date(st_data[-1], st_data[1], st_data[0]):
            self._data_end = value
        else:
            raise ValueError("Uncorrect end data")

    @property
    def deadline(self)->str:
        end = list(map(int, self.data_end.split(".")))
        return date(end[-1], end[-2], end[-3]) - date.today()
    
    @property
    def status(self)->str:
        if self.deadline.days <= 0:
            return "deadline over"
        else:
            return "there's still time"

    @staticmethod
    def create_task(text: dict)->object:
        try:
            id = text["id"]
            payloud = text["payloud"]
            data_start = text["data_start"]
            data_end = text["data_end"]
            priority = text["priority"]
            return TaskFile(id, payloud, data_start, data_end, priority)
        except:
            raise ValueError("Some data about the task is missing")
        
    def __str__(self)->str:
        
        return f"id: {self.id}\n payload: {self.payloud}\n priority: {self.priority}\n status: {self.status}\n start: {self.data_start}\n end: {self.data_end}\n deadline: {self.deadline}\n"