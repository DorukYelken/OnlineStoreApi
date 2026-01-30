"""
Uygulama Konfigürasyonu
=======================
API ayarları, metadata ve Swagger UI konfigürasyonu için merkezi yapılandırma dosyası.
"""

from typing import Dict, List

# API Metadata
API_TITLE = "Mock Online Store API"
API_DESCRIPTION = """
## 🛒 Mock Online Store API

This API provides a mock backend for e-commerce applications.
Uses in-memory data storage instead of a real database.

### Features

* **Product Management** - Product listing, search, filtering, and CRUD operations
* **User Reviews** - Product reviews and rating system
* **Smart Recommendations** - Similar products, top sellers, discounted products
* **Category System** - Hierarchical category structure
* **API Key Authentication** - Secure access for seller operations

### Authentication

Seller operations (create, update, delete products) require the `X-API-Key` header.

**Test API Keys:**
- `seller_key_001` - TechStore
- `seller_key_002` - FashionHub
- `seller_key_003` - HomeDecor
- `seller_key_004` - SportZone
- `seller_key_005` - BookWorld

### Pagination

List endpoints support `page` and `page_size` parameters.
Default values: `page=1`, `page_size=10`

### MCP Integration

This API is designed to be ready for Model Context Protocol (MCP) conversion.
Each endpoint includes detailed descriptions and example data.
"""

API_VERSION = "1.0.0"

# Tag Metadata for Swagger UI
TAGS_METADATA: List[Dict] = [
    {
        "name": "Products",
        "description": """
**Product Management Endpoints**

Endpoints for product listing, search, filtering, and CRUD operations.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/products` | GET | List all products (filtering, sorting, pagination) |
| `/products/{id}` | GET | Single product detail |
| `/products/search` | GET | Search products |
| `/products/category/{category_id}` | GET | Products by category |
| `/products` | POST | Add new product (API Key required) |
| `/products/{id}` | PUT | Update product (API Key required) |
| `/products/{id}` | DELETE | Delete product (API Key required) |
""",
    },
    {
        "name": "Reviews",
        "description": """
**Product Reviews Endpoints**

User reviews and rating operations.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/products/{product_id}/reviews` | GET | List product reviews |
| `/products/{product_id}/reviews` | POST | Add new review |
| `/reviews/stats/{product_id}` | GET | Rating statistics |
""",
    },
    {
        "name": "Recommendations",
        "description": """
**Product Recommendation Endpoints**

Product recommendations using smart recommendation algorithms.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/recommendations/similar/{product_id}` | GET | Similar products |
| `/recommendations/top-rated` | GET | Highest rated products |
| `/recommendations/deals` | GET | Discounted products |
""",
    },
    {
        "name": "Categories",
        "description": """
**Category Endpoints**

Product category management.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/categories` | GET | List all categories |
| `/categories/{id}` | GET | Category detail |
""",
    },
]

# OpenAPI Examples
OPENAPI_EXAMPLES = {
    "product_create": {
        "summary": "Example Product",
        "description": "Example of adding a new electronics product",
        "value": {
            "name": "Wireless Bluetooth Headphones",
            "description": "Wireless headphones with high quality sound and long battery life",
            "category_id": 1,
            "price": 149.99,
            "discount_percentage": 15.0,
            "stock_status": "in_stock",
            "features": {
                "Bluetooth Version": "5.0",
                "Battery Life": "30 hours",
                "Charging Time": "2 hours",
                "Color": "Black"
            },
            "images": [
                "https://example.com/images/headphone1.jpg",
                "https://example.com/images/headphone2.jpg"
            ]
        }
    },
    "review_create": {
        "summary": "Example Review",
        "description": "Example of adding a review to a product",
        "value": {
            "user_id": 1,
            "rating": 5,
            "title": "Amazing product!",
            "comment": "Sound quality is excellent, battery life is very long as advertised.",
            "pros": ["Sound quality", "Battery life", "Comfort"],
            "cons": ["Price is a bit high"]
        }
    }
}

# Pagination Defaults
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100

# API Key Settings
API_KEY_HEADER = "X-API-Key"
