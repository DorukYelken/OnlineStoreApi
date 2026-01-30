"""
Category Router
===============
API endpoints for product categories.

This module contains all endpoints for category listing and details.

Endpoints:
- GET /categories - List all categories
- GET /categories/{id} - Category detail

MCP Conversion Notes:
- Categories are the fundamental structure for product discovery
- Each category is returned with product count
"""

from typing import List
from fastapi import APIRouter, HTTPException, status
from ..database import db
from ..schemas.category import Category, CategoryWithCount


router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get(
    "",
    response_model=List[CategoryWithCount],
    summary="List All Categories",
    description="""
## List All Categories

Returns all categories in the store with their product counts.

### Returned Data

For each category:
- id: Unique category ID
- name: Category name
- description: Category description
- icon: Category icon (emoji)
- image_url: Cover image URL
- product_count: Number of products in this category

### Example Usage

```
GET /categories
```

### Example Response

```json
[
    {
        "id": 1,
        "name": "Electronics",
        "description": "Phones, computers, tablets...",
        "icon": "📱",
        "product_count": 156
    },
    {
        "id": 2,
        "name": "Fashion",
        "description": "Clothing, shoes, accessories...",
        "icon": "👔",
        "product_count": 89
    }
]
```

### Use Cases

- Homepage category menu
- Sidebar navigation categories
- Category-based filtering options

### MCP Integration

Used for queries like "What categories are there?", "List categories".
""",
    responses={
        200: {"description": "Category list"}
    }
)
async def list_categories():
    """
    Returns all categories with their product counts.
    """
    categories = db.get_all_categories()
    
    # Add product count to each category
    result = []
    for cat in categories:
        product_count = db.get_category_product_count(cat["id"])
        result.append({
            **cat,
            "product_count": product_count,
            "subcategories": []
        })
    
    return result


@router.get(
    "/{category_id}",
    response_model=CategoryWithCount,
    summary="Category Detail",
    description="""
## Category Detail

Returns detailed information for a specific category.

### Returned Data

- Basic category info
- Total product count in this category
- Subcategories (if any)

### Example Usage

```
GET /categories/1
```

### Example Response

```json
{
    "id": 1,
    "name": "Electronics",
    "description": "Phones, computers, tablets and other electronic devices",
    "icon": "📱",
    "image_url": "https://example.com/categories/electronics.jpg",
    "parent_id": null,
    "product_count": 156,
    "subcategories": []
}
```

### MCP Integration

Used for queries like "info about Electronics category".
""",
    responses={
        200: {"description": "Category detail"},
        404: {"description": "Category not found"}
    }
)
async def get_category(category_id: int):
    """
    Returns detailed information for a single category.
    """
    category = db.get_category(category_id)
    
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with ID: {category_id} not found."
        )
    
    product_count = db.get_category_product_count(category_id)
    
    return {
        **category,
        "product_count": product_count,
        "subcategories": []
    }
