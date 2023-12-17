import datetime


def mdtm_to_unix_timestamp(mdtm: str) -> float:
    """
    This function converts from a string representation of a timestamp to unix timestamp
    :param mdtm: string representation of a timestamp
    :return: unix timestamp
    """
    return datetime.datetime.strptime(mdtm[:14], "%Y%m%d%H%M%S").timestamp()
