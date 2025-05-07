def get_float(val :str):
    try:
        return float(val)
    except:
        return None 

def get_numeric(v, rounding=1, toint=False):
    if v is not None:
        res = float(v)
        if toint:
            res = int(round(res, 0))
        elif rounding:
            res = round(res, rounding)
        return res
    return v


def get_string(v, extra=" -"):
    if v is not None:
        res = str(v)
        if res != "-":
            return res + extra
        return res
    return v

def check_valid(v):
    if v is None:
        return EntryEnum.BROKEN_INSTRUMENT.value
    elif v == EntryEnum.LEAVE_BLANK:
        return None
    else:
        return v

# 2023-09-14 10:12:00 +00:00 to 2023-09-14 10:00:00 +00:00
def round_to_nearest_hour(ts : str) -> str:
    import datetime
    dt = isotodatetime(ts)

    if dt.minute >= 30:
        dt = dt + datetime.timedelta(hours=1)
        dt = dt.replace(minute=0)
    return datetimetoiso(dt)
    
# 2023-09-14 10:12:00 +00:00
def isotodatetime(ts):
    from datetime import datetime
    return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S %z")

def datetimetoiso(dt):
    from datetime import datetime
    ts = datetime.strftime(dt, "%Y-%m-%d %H:%M:%S %z")
    return ts[:-2] + ':' + ts[-2:]
    
from enum import Enum
class EntryEnum(Enum):
    BROKEN_INSTRUMENT = 9999
    LEAVE_BLANK = "blank"

class QueryEnum(Enum):
    SUCCESS = 2
    DUPLICATE = 1
    FAIL = 0