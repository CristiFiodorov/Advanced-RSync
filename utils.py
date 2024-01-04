import datetime
from tzlocal import get_localzone
import pytz

local_tz = get_localzone()


def mdtm_to_unix_timestamp(mdtm: str) -> float:
    """
    This function converts from a string representation of a timestamp to unix timestamp
    :param mdtm: string representation of a timestamp
    :return: unix timestamp
    """
    return datetime.datetime.strptime(mdtm[:14], "%Y%m%d%H%M%S").timestamp()


def mdtm_utc_to_unix_timestamp_localtime(mdtm: str) -> float:
    """
    This function converts from a string representation of utc timestamp to unix timestamp localtime
    :param mdtm: string representation of a timestamp
    :return: unix timestamp
    """
    utc_time = datetime.datetime.strptime(mdtm[:14], "%Y%m%d%H%M%S")
    utc_time = utc_time.replace(tzinfo=pytz.utc)
    return utc_time.astimezone(local_tz).timestamp()
