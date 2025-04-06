from typing import Optional
from datetime import timedelta

def to_uint32(value: float, max_value: Optional[int] = None) -> int:
    """
    Converts float value to uint32 with custom max, wrapping via modulo.
    Args:
        value: Value to convert (e.g. time difference).
        max_value: Maximum allowed value (defaults to 2^32 - 1).
    
    Returns:
        The value wrapped within the uint32 range.
    """
    max_val = max_value if max_value is not None else (2**32 - 1)

    return int(value) % max_val

def format_uptime(seconds: int) -> str:
    """
    Format the uptime from seconds to a human-readable string.

    Args:
        seconds (int): The uptime in seconds.

    Returns:
        str: A string representing the uptime in a human-readable format.
             For example, '1 day, 2 hours, 3 minutes, 4 seconds'.
    """ 
    uptime = timedelta(seconds = seconds)

    return str(uptime)
