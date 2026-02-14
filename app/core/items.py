"""
Item categories and utilities for donation/shelter items.

Matches the item structure from the legacy Django app.
"""
from typing import Dict, List, Any
from sqlalchemy.dialects.postgresql import JSONB


# Item categories matching the legacy system
ITEM_CATEGORIES = {
    "food": {
        "produce": ["lettuce", "eggplant", "apples", "bananas", "carrots"],
        "non-perishable": ["canned meat", "canned vegetables", "canned soup", "rice", "pasta"],
        "perishable": ["cereal", "eggs", "chips", "donuts", "orange juice", "fruit juice", "milk", "bread"],
        "other": ["coffee", "tea", "bottled water", "gum", "mints", "soda", "sparkling water", "seltzer water"]
    },
    "clothing": {
        "shoes": ["boots", "snow boots", "heels", "sneakers", "wader boots", "dress shoes", "slippers"],
        "legwear": ["jeans", "skirts", "blouses", "dresses", "sweatpants", "shorts", "waders"],
        "winter": ["coats", "jackets", "scarves", "gloves", "hats", "thermal underwear"],
        "underwear": ["socks", "underwear", "bras", "boxers", "panties"]
    },
    "menstrual products": ["tampons", "pads", "liner pads", "cups"],
    "pharmaceuticals": ["antacid", "laxative", "blood thinner", "painkiller", "vitamins"],
    "toiletries": ["toilet paper", "baby wipes", "lipstick", "makeup", "shampoo", "conditioner", "shower gel", "skin lotion", "deodorant", "toothpaste", "toothbrushes"],
    "cleaning supplies": ["paper towels", "bleach", "drain cleaner", "dish soap", "laundry detergent"],
    "sexual health": ["dental dams", "condoms", "lube"],
    "bedding": ["blankets", "pillows", "sheets", "sleeping bags", "mattresses"],
    "electronics": ["phones", "chargers", "laptops", "tablets", "headphones"],
    "other": []
}


def flatten_items() -> Dict[str, str]:
    """Flatten the item categories into a single dict with descriptions."""
    result = {}
    for category, subcategories in ITEM_CATEGORIES.items():
        if isinstance(subcategories, list):
            # Simple category like "menstrual products"
            for item in subcategories:
                result[f"{category}.{item}"] = f"{category}: {item}"
        else:
            # Nested categories like "food" -> "produce"
            for subcategory, items in subcategories.items():
                for item in items:
                    result[f"{category}.{subcategory}.{item}"] = f"{category} > {subcategory}: {item}"
    return result


def get_items_from_form(form_data: Dict[str, Any]) -> Dict[str, int]:
    """
    Convert form data to items dict with quantities.

    Form data format: {"food.produce.lettuce": "5", "clothing.shoes.boots": "2"}
    Returns: {"food": {"produce": {"lettuce": 5}}, "clothing": {"shoes": {"boots": 2}}}
    """
    result = {}

    for key, value in form_data.items():
        if not key.startswith("items.") or not value or int(value) == 0:
            continue

        parts = key.replace("items.", "").split(".")
        set_nested_value(result, parts, int(value))

    return result


def set_nested_value(d: dict, parts: list, value: int):
    """Set a value in a nested dict using a list of keys."""
    if len(parts) == 1:
        d[parts[0]] = value
    elif len(parts) == 2:
        if parts[0] not in d:
            d[parts[0]] = {}
        d[parts[0]][parts[1]] = value
    elif len(parts) == 3:
        if parts[0] not in d:
            d[parts[0]] = {}
        if parts[1] not in d[parts[0]]:
            d[parts[0]][parts[1]] = {}
        d[parts[0]][parts[1]][parts[2]] = value


def get_item_count(items: Dict) -> int:
    """Count total items in a nested items dict."""
    count = 0
    for value in items.values():
        if isinstance(value, dict):
            count += get_item_count(value)
        elif isinstance(value, int):
            count += value
    return count


def get_item_summary(items: Dict) -> List[str]:
    """Get a list of item summaries from a nested items dict."""
    result = []

    for category, subcategories in items.items():
        if isinstance(subcategories, dict):
            for subcategory, item_list in subcategories.items():
                if isinstance(item_list, dict):
                    for item, quantity in item_list.items():
                        if quantity > 0:
                            result.append(f"{quantity} {item}")
                else:
                    if subcategories > 0:
                        result.append(f"{subcategories} {subcategory}")
        else:
            if subcategories > 0:
                result.append(f"{subcategories} {category}")

    return result


def find_matching_items(shelter_needs: Dict, donation_items: Dict) -> List[str]:
    """Find items in donation that match shelter needs."""
    matches = []

    for category in shelter_needs:
        if category not in donation_items:
            continue

        if isinstance(shelter_needs[category], dict):
            for subcategory in shelter_needs[category]:
                if subcategory not in donation_items.get(category, {}):
                    continue

                for item, quantity in shelter_needs[category][subcategory].items():
                    if quantity > 0 and item in donation_items[category][subcategory]:
                        donated = donation_items[category][subcategory].get(item, 0)
                        if donated > 0:
                            matches.append(f"{donated} {item} (need {quantity})")
        else:
            needed = shelter_needs[category]
            donated = donation_items.get(category, 0)
            if needed > 0 and donated > 0:
                matches.append(f"{donated} {category} (need {needed})")

    return matches
