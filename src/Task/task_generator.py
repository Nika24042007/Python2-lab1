from src.random_text import random_text
from datetime import datetime, timedelta
from random import choice, randint
from src.random_data import random_date
from src.Constans.constans_task import PRIORITY_TYPE

class TaskGenerator():
    def __init__(self, id:int, payloud:str, priority, data_start, data_end, deadline, status)->None:
        self.id = id
        self.payloud = payloud
        self.priority = priority,
        self.data_start =data_start
        self.data_end =  data_end
        self.deadline = deadline
        self.status = status 

    @staticmethod
    def creat_task(id:int, payloud:str):
        now = datetime.now()
        priority = choice(PRIORITY_TYPE)
        data_start = random_date()
        data_end = data_start + timedelta(days=randint(1, 365))
        deadline = data_end - now
        if deadline <= 0:
            status = "deadline over"
        else:
            status = "there's still time"
        return TaskGenerator(id, payloud, priority, data_start, data_end, deadline, status)

    def __str__(self):
        
        return f"id:{self.id} payload:{self.payloud} priority:{self.priority} status:{self.status} start:{self.data_start} end:{self.data_end} deadline:{self.deadline}"

    
