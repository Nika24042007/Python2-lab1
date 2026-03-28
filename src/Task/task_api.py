import logging
from src.Task.discriprors import ValidateData, ValidatorPriority

class TaskApi():
    start_data = ValidateData()
    end_data = ValidateData()
    priority = ValidatorPriority()

    def __init__(self):
        pass

    @staticmethod
    def create_task(id:int, payloud:str):
        logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")
        start_data = input("Enter start data: ")
        logging.info(f"Enter start data: {start_data}")
        end_data = input("Enter end data:")
        logging.info(f"Enter end data: {end_data}")
        priority = input("Enter prioriti(High, Normal, Very high): ")
        logging.info(f"Enter prioriti(High, Normal, Very high): {priority}")
        