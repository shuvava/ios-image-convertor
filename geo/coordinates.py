# encoding: utf-8
import math


def to_dec_deg(direction, coord) -> str:
    """converts heic GPS coordinates into string with float"""
    negative = -1 if str(direction).lower().startswith(('w', 's')) else 1
    if coord is None: # metadata is not found
        return ''
    if len(coord.values) != 3:
        raise ValueError("coordinate is incorrect type")
    d = coord.values[0].numerator / coord.values[0].denominator
    m = coord.values[1].numerator / coord.values[1].denominator
    s = coord.values[2].numerator / coord.values[2].denominator
    if not (0 <= m <= 60 and 0 <= s <= 60):
        raise ValueError("Minutes and seconds have to be between 0 and 60")

    if abs(d) > 180:
        raise ValueError("Degrees have to be between -180 and 180")

    if d != int(d) and (m != 0 or s != 0):
        raise ValueError("degrees cannot have fraction unless both minutes and seconds are zero")

    if m != int(m) and s != 0:
        raise ValueError("minutes cannot have fraction unless seconds are zero")

    res = math.copysign(abs(d) + m / 60 + s / 3600, d)
    return f'{math.copysign(res, negative):.2f}'
