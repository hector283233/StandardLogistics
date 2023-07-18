import os
import datetime

def validate_date(date):
    try:
        datetime.date.fromisoformat(date)
        return True
    except:
        return False