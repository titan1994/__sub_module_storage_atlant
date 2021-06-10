from datetime import datetime
from uuid import UUID


def datetime_valid(cls, dt_str):
    "Check if datetime is ISO 8601"
    if dt_str == '':
        return '0000-00-00T00:00:00'
    try:
        datetime.fromisoformat(dt_str)
    except:
        raise ValueError('Incorrect datetime format. Use ISO 8601')

    return dt_str


def uuid_valid(cls, uuid_str):
    """
    Check if uuid_to_test is a valid UUID.
    """
    try:
        UUID(uuid_str, version=4)
    except ValueError:
        raise ValueError('Incorrect UUID')
    return uuid_str


def uint_valid(cls, uint_value):
    """
    Check if uint is positive.
    """
    assert uint_value >= 0, "UInt must be positive"
    return uint_value