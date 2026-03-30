import re

class ValidateData:
    def __set_name__(self, owner, name):
        self.private_name = "_" +name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return getattr(instance, self.private_name, None)

    def __set__(self, instance, value:str):
        if re.search(r"\d{2}.\d{2}.\d{4}", value):
            day = int(value.split(".")[0])
            month = int(value.split(".")[1])
            year = int(value.split(".")[-1])
            if month > 0 and month < 13 and year > 2020 and day > 0:
                if month in [1, 3, 5, 7, 8, 10, 12] and day < 32:
                    return setattr(instance, self.private_name, value)
                elif month in [4, 6, 9, 11] and day < 31:
                    return setattr(instance, self.private_name, value)
                elif month == 2 and year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                    return setattr(instance, self.private_name, value)
                else:
                    raise ValueError("No such day in calander")
            else:
                raise ValueError("No such month or year in calander")
        else: 
            raise ValueError("Uncorrect type of data")
        
class ValidatorPriority():
    def __set_name__(self, owner, name):
        self.private_name = "_" + name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return getattr(instance, self.private_name, None)

    def __set__(self, instance, value:str):
        if value in ["High", "Normal", "Very high"]:
            return setattr(instance, self.private_name, value)
        else:
            raise ValueError("No such privaty")
