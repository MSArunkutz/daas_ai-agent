import csv 
from . import instrument

from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.genai import types
from google.adk.tools import AgentTool

# For "haversine" Function
from math import radians, cos, sin, asin, sqrt
from typing import List, Dict, Any


print("✅ ADK components imported successfully.")

enforce_output_prompt = """YOUR FINAL ACTION IN A TURN MUST ALWAYS BE TO GENERATE A MODEL RESPONSE FOR THE USER, 
        ESPECIALLY WHEN UTILIZING A TOOL'S OUTPUT. DO NOT WAIT FOR FURTHER USER PROMPTS AFTER A TOOL RETURNS A RESULT."""

retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504], # Retry on these HTTP errors
)

print("✅ Retry configuration done.")

def read_csv_to_list_of_dicts(file_path):
    """Reads a CSV file into a list where each row is a dictionary."""
    data_list = []
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data_list = list(reader)        
    return data_list

print("✅ Helper function defined : Reading CSV to Dictionary")

flood_severity_data = read_csv_to_list_of_dicts("daas/csv_dataset/flood_data_with_coords.csv")
facilities_data = read_csv_to_list_of_dicts("daas/csv_dataset/facilities_with_coords.csv")
flood_safety_tips_data = read_csv_to_list_of_dicts("daas/csv_dataset/curated_flood_safety_tips.csv")


def find_place_by_name(data, place_name):
    """
    Searches for a place in the given data by its name.

    Parameters:
    - data (list): A list of dictionaries, each representing a place with a 'place_name' key.
    - place_name (str): The name of the place to search for (case insensitive).

    Returns:
    - dict: The dictionary representing the matched place if found.
    - None: If no matching place is found.
    """
    for place in data:
        if place['place_name'].lower() == place_name.lower():
            return place
    return None

def get_tips_by_categories(categories: list[str]) -> list:
    """
    Returns tips from a list of dictionaries filtered by multiple categories.

    Parameters:
    - categories (list): A list of category names (strings) to match.

    Returns:
    - List of tips under any of the matching categories.
    """
    normalized = [c.strip().lower() for c in categories]
    return [
        entry["Tip"]
        for entry in flood_safety_tips_data
        if entry["Category"].strip().lower() in normalized
    ]


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great-circle distance between two points on Earth (in kilometers).
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of Earth in kilometers
    return c * r

def find_nearby_facilities(
    flood_place: str ,
    max_distance_km: float = 10.0
) -> List[Dict[str, Any]]:
    """
    Find all facilities within max_distance_km from a given flood-affected place.
    
    Args:
        flood_place: This is the place the user given.
        max_distance_km: Maximum distance in kilometers (default: 10 km)
    
    Returns:
        List of facilities within the specified distance, sorted by distance.
        Each facility dict includes an added key: 'distance_km'
        If none found : [] is returned.
    """
    p = find_place_by_name(flood_severity_data,flood_place)
    if p is None:
        return []
    facilities = facilities_data
    flood_lat = float(p["latitude"])
    flood_lon = float(p['longitude'])

    nearby = []
    
    for facility in facilities:
        dist = haversine(
            flood_lat, flood_lon,
            float(facility['latitude']), float(facility['longitude'])
        )
        
        if dist <= max_distance_km:
            # Create a copy to avoid modifying original data
            fac_with_dist = facility.copy()
            fac_with_dist['distance_km'] = round(dist, 3)
            nearby.append(fac_with_dist)
    
    # Sort by distance (closest first)
    nearby.sort(key=lambda x: x['distance_km'])
    
    return nearby


shelter_aid_locator_agent = Agent(
    name="ShelterAidLocatorAgent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),
    description="An agent that finds the nearby shelters / hospitals based on a radius",
    instruction=f"""
        Your only job is to help users find the nearest safe places during a disaster.

        You have one tool: find_nearby_facilities  
        You must use this tool every time the user asks for a shelter or hospital-use 5km as max_distance.

        Rules you must always follow:

        - Always search within a five kilometer radius of the location given by the user.
        - Shelter means only school, college, or community centre. Never include anything else as shelter.
        - If the user clearly says hospital or medical help, show only hospitals.
        - If the user clearly says shelter or safe place or relief camp, show only schools, colleges, and community centres.
        - If the user does not specify the type, ask once politely: Are you looking for a shelter (school or community centre) or a hospital?
        - Never return more than ten results. Always show the nearest ten only.
        - If the place is not found : respond like 'The place is not found. Please verify the place name for spelling mistakes. Thank you'
        - List the results exactly in this format, one facility per line:

        Name of the facility - distance in kilometers - (occupancy percentage percent full)

        Example Output:
        --> Government Higher Secondary School Kunnam - 1.3 km - (at 45 % capacity )
        --> St. Marys College -2.1 km - (60 % capacity )
        --> Community Hall Vyttila - 4.8 km - (30 %% full)

        Additional rules:
        - Always sort the list from nearest to farthest.
        - Always speak in a calm, kind, and helpful tone.
        - Begin your reply with: Here are the nearest places within five kilometers:
        - If no facility is found within five kilometers, say: 
        I could not find any shelter or hospital within five kilometers. 
        Please share a nearby landmark or main road so I can search again.
        - Never add extra information unless the user asks.
        - {enforce_output_prompt}

    """,
    tools=[
        find_nearby_facilities
    ]
)

print("✅ Shelter Aid Locator Agent defined.")

def flood_data_tool(place_name: str) -> dict:
    """
    This tool is used for fetching the flood data for a given place name( how intense is the flooding )
    This simulates a database fetch.

    Args:
        method: the name of the place. Eg: "east fort"

    Returns
        Returns the status and intensity of flooding
        Success: {"status":"success","intensity":2}
        Error : {"status":"error" , "error_message": "place not found"}
    """
    
    
    result = find_place_by_name(flood_severity_data,place_name)
    if result is not None:
        return {"status": "success", "intensity": result["flood_intensity"]}
    else: 
        return {
            "status": "error",
            "error_message": "place not found",
        }

print("✅ flood_data_tool defined")

flood_intensity_agent = Agent(
    name="FloodIntensityAgent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),
    description="An agent that looks into the current flood situation",
    instruction=f"""
        
        Your only job is to tell people how bad the flooding is in their area in simple, calm words.

        You have one tool: flood_data_tool  
        You must use this tool every time the user mentions a place and asks about flood, water level, or the situation.
        If multiple places are mentioned, understand the question being asked and call the tool multiple times 
        to get the required intensities, compare and interpret the required answer - like safer to move or not

        Rules you must always follow:

        - Call the tool with the exact location the user gave.
        - Never show raw numbers, percentages, or measurements to the user.
        - Convert the data into clear, easy-to-understand verbal descriptions only.
        - Use one of these simple descriptions (choose the one that matches the data best):

            The area is completely dry and safe right now. No flooding at all.

            There is light waterlogging in low-lying areas. Roads are passable with care.

            Water has entered some streets and ground floors. It is unsafe to walk or drive in many places.

            Flooding is severe. Water is knee-deep to waist-deep in most areas. Many homes are flooded.

            Extremely dangerous flooding. Water is above head level in many places. Immediate rescue may be needed.

            The area is under deep floodwater. Only rooftops are visible in several locations. Urgent rescue is required.

        - Speak calmly and with care at all times. Never scare the user, always give hope.
        - For complex queries, compare and interpret a suitable answer - eg: comparing multiple places for the safest etc.
        - Stay in character as a caring flood information assistant.

        - {enforce_output_prompt}
    """,
    tools=[
        flood_data_tool
    ]   
)

print("✅ Flood Intensity Agent defined.")

root_agent = Agent(
    name="DAAS_Coordinator",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction=f"""
        Your name is **Disaster Aversion Agentic System**, called **DAAS**.

        **GREETINGS**: If the user casually says hi, respond with your capabilities in a listed manner for easier understanding.

        Your job is to manage and use the tools provided to you as per the user's input.  
        ### Give answers directly only if the tools cannot answer it.

        **Available tools are as follows**:

        1. **flood_intensity_agent**  
        Use this tool only when the user asks about water level, flood situation, how bad the flooding is,  
        or the current flood intensity in a specific area or location.

        2. **shelter_aid_locator_agent**  
        Use this tool only when the user asks for the nearest relief camp, shelter home, safe place to stay,  
        food distribution point, or medical camp near their location.

        3. **get_tips_by_categories**  
        Use this tool for getting flood safety-related tips, which can be given to the user as unordered list.
        This tool needs a list of categories for finding the tips.  
        There are 5 categories in this:
        a. Evacuation & Movement  
        b. Staying Indoors  
        c. Health & Hygiene  
        d. Communication & Information  
        e. Utilities & Equipment  
        You can use this tool whenever you feel like giving guidance to the user.  
        You may rephrase the output if you feel it is too long, without losing the essence of the tips.

        **Tools end here.**

        **Rules you must always follow**:
        - Use tools for responding.
        - Unless a very generic question, don't answer.
        - Be short on questions with empathy.
        - Do not answer anything outside of Disaster Management.
        - {enforce_output_prompt}
        - When answering queries with other tools, you may use the get_tips_by_category tool to give some relevant tips for safety.

        **Example situations**:
        - User asks: *How deep is the water in my area?* → use only **flood_intensity_agent**
        - User asks: *Where is the nearest relief camp?* → use only **shelter_aid_locator_agent**

        Be a kind, helpful assistant to the struggling.

    """, 
    tools = [ 
        AgentTool(flood_intensity_agent),
        AgentTool(shelter_aid_locator_agent),
        get_tips_by_categories
    ]
)







