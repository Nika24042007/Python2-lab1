from datetime import date, datetime

class ValidateData:
    """
    Проверка дат на соответствие
    """
    def __set_name__(self, owner, name:str):
        self.private_name = "_" +name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return getattr(instance, self.private_name, None)

    def __set__(self, instance, value:str):
        if not is_valid_date(value):
            raise ValueError("Uncorrect data format or data")
        return setattr(instance, self.private_name, value)

        
class ValidatorPriority():
    """
    проверка названий на соответствие
    """
    def __set_name__(self, owner, name:str):
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


def is_valid_date(data):
    try:
        datetime.strptime(data, "%d-%m-%Y").date()
        return True
    except:
        return False
