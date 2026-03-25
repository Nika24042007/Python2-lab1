from random import randint, choice

from src.Constans.constants import RANDOM_DATA

def random_text() -> str:
    """
    Составление рандомного тектса задания

    :return: Строка задания
    """
    lenght = randint(1, 10)
    text = ""
    for i in range(lenght):
        text += choice(RANDOM_DATA) + " "
    return text
    