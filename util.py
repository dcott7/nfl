from datetime import datetime

def convert_to_datetime(date_str: str) -> datetime:
    return datetime.strptime(date_str, '%Y-%m-%dT%H:%MZ')