from datetime import timezone
import datetime

def current_datetime_utc():
    dt = datetime.datetime.now(timezone.utc)    
    return dt.replace(tzinfo=timezone.utc)
