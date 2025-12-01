from daas.flood_intensity_agent.data_loader import flood_severity_data

def find_place_by_name(data, place_name):
    for place in data:
        if place['place_name'].lower() == place_name.lower():
            return place
    return None

def flood_data_tool(place_name: str) -> dict:
    result = find_place_by_name(flood_severity_data, place_name)
    if result is not None:
        return {"status": "success", "intensity": result["flood_intensity"]}
    else: 
        return {"status": "error", "error_message": "place not found"}