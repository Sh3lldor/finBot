from datetime import datetime


def get_date():
    current = datetime.now()
    return f"{current.year}-{current.month}-{current.day}"