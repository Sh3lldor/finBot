from datetime import datetime


def get_date():
    current = datetime.now()
    return f"{current.year}-{current.month}-{current.day}"


def init_income():
    return {
        "category" : "↕️ Account Transfer",
        "service"   : None,
        "cost"      : None,
        "method"    : "💳 Credit Card",
        "date"      : None
    }


def init_outcome():
    return {
        "category" : None,
        "category_display_name": None,
        "service"  : None,
        "cost"     : None,
        "date"     : None
    }