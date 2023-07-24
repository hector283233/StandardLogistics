import os
import datetime

def validate_date(date):
    try:
        datetime.date.fromisoformat(date)
        return True
    except:
        return False
    
def calculate_rating(old_rating, rating_count, rating):
    total_rating = old_rating * rating_count
    total_rating = total_rating + rating
    new_rating = total_rating / (rating_count + 1)
    return new_rating