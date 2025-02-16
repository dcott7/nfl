from datetime import datetime

def convert_to_datetime(date_str: str) -> datetime:
    return datetime.strptime(date_str, '%Y-%m-%dT%H:%MZ')

def get_id_from_url(url: str) -> int:
    return url.split("/")[-1].replace("?lang=en&region=us","")