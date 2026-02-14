from fastapi import APIRouter
from app.core.items import ITEM_CATEGORIES, flatten_items, get_item_summary

router = APIRouter(prefix="/api/items", tags=["items"])


@router.get("/categories")
def get_item_categories():
    """Get all item categories available for donations/shelter needs."""
    return {
        "categories": ITEM_CATEGORIES
    }


@router.get("/flat")
def get_flat_items():
    """Get a flattened list of all items with their paths."""
    return {
        "items": flatten_items()
    }
