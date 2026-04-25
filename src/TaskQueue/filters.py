def priopity_filter(must: str, is_pr: str)->bool:
    """
    Фильтрация по приоритету
    :param must: какой должен быть приоритет у задачи
    :param is_pr: какой приоритет у задачи на самом деле

    :return: True или False в зависимости от соответствия фильтру
    """
    if must == is_pr:
        return True
    else:
        return False

def status_filter(must:str, is_st:str)->bool:
    """
    Фильтрация по статусу
    :param must: какой должен быть статус
    :param is_st: какой статус у задачи на самом деле

    :return: True или False в зависимости от соответствия фильтру
    """
    if must == "there's still time" and is_st == "In work":
        return True
    elif must == "deadline over" and is_st == "Over":
        return True
    else:
        return False