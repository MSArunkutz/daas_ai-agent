from math import radians, cos, sin, asin, sqrt
from typing import List, Dict, Any

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r

def find_place_by_name(data, place_name):
    for place in data:
        if place['place_name'].lower() == place_name.lower():
            return place
    return None