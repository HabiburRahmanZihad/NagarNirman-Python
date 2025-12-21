"""
Location and Category data loader for NagarNirman
Loads data from divisionsData.json and categoryOptions.json
"""

import json
import os

# Get the base directory (project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load divisions data from JSON
def _load_divisions_data():
    """Load divisions and districts data from JSON file."""
    json_path = os.path.join(BASE_DIR, "divisionsData.json")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading divisions data: {e}")
        return []

# Load category options from JSON
def _load_category_options():
    """Load category options from JSON file."""
    json_path = os.path.join(BASE_DIR, "categoryOptions.json")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading category options: {e}")
        return {}

# Cache the loaded data
DIVISIONS_DATA = _load_divisions_data()
CATEGORY_OPTIONS = _load_category_options()


def get_divisions():
    """
    Get list of all divisions in Bangladesh.
    
    Returns:
        list: List of division names
    """
    return [div["division"] for div in DIVISIONS_DATA]


def get_districts(division):
    """
    Get list of districts for a specific division.
    
    Args:
        division (str): Name of the division
        
    Returns:
        list: List of district names for the given division
    """
    for div in DIVISIONS_DATA:
        if div["division"] == division:
            return [d["name"] for d in div["districts"]]
    return []


def get_district_coordinates(division, district):
    """
    Get latitude and longitude for a specific district.
    
    Args:
        division (str): Name of the division
        district (str): Name of the district
        
    Returns:
        tuple: (latitude, longitude) or (None, None) if not found
    """
    for div in DIVISIONS_DATA:
        if div["division"] == division:
            for d in div["districts"]:
                if d["name"] == district:
                    return (d["latitude"], d["longitude"])
    return (None, None)


def get_division_coordinates(division):
    """
    Get latitude and longitude for a division.
    
    Args:
        division (str): Name of the division
        
    Returns:
        tuple: (latitude, longitude) or (None, None) if not found
    """
    for div in DIVISIONS_DATA:
        if div["division"] == division:
            return (div["latitude"], div["longitude"])
    return (None, None)


def get_all_districts():
    """
    Get list of all districts in Bangladesh.
    
    Returns:
        list: List of all district names sorted alphabetically
    """
    all_districts = []
    for div in DIVISIONS_DATA:
        for d in div["districts"]:
            all_districts.append(d["name"])
    return sorted(all_districts)


def get_categories():
    """
    Get list of all category names (main categories).
    
    Returns:
        list: List of category names
    """
    return list(CATEGORY_OPTIONS.keys())


def get_subcategories(category):
    """
    Get list of subcategories for a specific category.
    
    Args:
        category (str): Name of the category
        
    Returns:
        list: List of subcategory names
    """
    return CATEGORY_OPTIONS.get(category, [])


def get_all_subcategories():
    """
    Get all subcategories as a flat list.
    
    Returns:
        list: List of all subcategory names
    """
    all_subs = []
    for subs in CATEGORY_OPTIONS.values():
        all_subs.extend(subs)
    return all_subs
