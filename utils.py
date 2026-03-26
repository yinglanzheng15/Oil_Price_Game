from datetime import datetime

def get_week_number():
    """Get current ISO week number"""
    return datetime.now().isocalendar()[1]
