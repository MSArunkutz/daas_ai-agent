from typing import List, Dict, Any
from daas.shelter_aid_locator_agent.data_loader import flood_severity_data, facilities_data
from daas.shelter_aid_locator_agent.geo_utils import haversine, find_place_by_name

def find_nearby_facilities(flood_place: str, max_distance_km: float = 10.0) -> List[Dict[str, Any]]:
    p = find_place_by_name(flood_severity_data, flood_place)
    if p is None:
        return []
    flood_lat = float(p["latitude"])
    flood_lon = float(p['longitude'])

    nearby = []
    for facility in facilities_data:
        dist = haversine(flood_lat, flood_lon,
                         float(facility['latitude']), float(facility['longitude']))
        if dist <= max_distance_km:
            fac_with_dist = facility.copy()
            fac_with_dist['distance_km'] = round(dist, 3)
            nearby.append(fac_with_dist)
    
    nearby.sort(key=lambda x: x['distance_km'])
    return nearby