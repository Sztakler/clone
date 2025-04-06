from typing import Optional

def to_uint32(value: float, max_value: Optional[int] = None) -> int:
    """
    Converts float value to uin32 with custom max, wrapping via modulo.

    Args:
        value: Value to convert (e.g. time difference).
        max_value: Maximum allowed value (defaults to 2^32 - 1).
    
    Returns:
        The value wrapped within the uint32 range.
    """
    max_val = max_value if max_value is not None else (2**32 - 1)

    return int(value) % max_val
