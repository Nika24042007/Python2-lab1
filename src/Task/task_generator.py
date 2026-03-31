from src.random_text import random_text
from datetime import date, timedelta
from random import choice, randint
from src.random_data import random_date
from src.Constans.constans_task import PRIORITY_TYPE

class TaskGenerator():
    def __init__(self, id:int, payloud:str, priority :str, data_start: str, data_end: str, deadline: str, status:str)->None:
        self.id = id
        self.payloud = payloud
        self.priority = priority
        self.data_start =data_start
        self.data_end =  data_end
        self.deadline = deadline
        self.status = status 

    @staticmethod
    def create_task(id:int, payloud:str)->object:
        now = date.today()
        priority = choice(PRIORITY_TYPE)
        data_start = random_date()
        data_end = data_start + timedelta(days=randint(1, 365))
        deadline = data_end - now
        if deadline.days <= 0 :
            status = "deadline over"
        else:
            status = "there's still time"
        return TaskGenerator(id, payloud, priority, data_start, data_end, deadline, status)
    

    def __str__(self)->str:
        
        return f"id: {self.id}\n payload: {self.payloud}\n priority: {self.priority}\n status: {self.status}\n start: {self.data_start}\n end: {self.data_end}\n deadline: {self.deadline}\n"

    
