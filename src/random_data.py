import random
from datetime import datetime 

def random_date(start_year=1970, end_year=2030):
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    if month in [4, 6, 9, 11]:
        max_day = 30
    elif month == 2:
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            max_day = 29
        else:
            max_day = 28
    else:
        max_day = 31
    day = random.randint(1, max_day)
    return datetime.date(year, month, day)