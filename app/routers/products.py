"""
Product Router
==============
API endpoints for product management.

This module contains all endpoints for product CRUD operations and listing.

Endpoints:
- GET /products - List all products (filtering, sorting, pagination)
- GET /products/search - Search products
- GET /products/{id} - Single product detail
- GET /products/category/{category_id} - Products by category
- POST /products - Add new product (API Key required)
- PUT /products/{id} - Update product (API Key + ownership check)
- DELETE /products/{id} - Delete product (API Key + ownership check)

MCP Conversion Notes:
- Each endpoint includes detailed description
- Request/Response examples available
- Parameter descriptions and validations defined
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from ..database import db
from ..schemas.product import Product, ProductCreate, ProductUpdate, ProductDetail, ProductSummary
from ..schemas.common import (
    PaginatedResponse, 
    ProductSortBy, 
    SortOrder, 
    StockStatus,
    MessageResponse
)
from ..auth.api_key import get_current_seller, verify_product_owner
from ..services.recommendation import RecommendationService


router = APIRouter(prefix="/products", tags=["Products"])


def apply_filters(products: List[dict], **filters) -> List[dict]:
    """Applies filters to products."""
    result = products
    
    if filters.get("category_id"):
        result = [p for p in result if p.get("category_id") == filters["category_id"]]
    
    if filters.get("min_price") is not None:
        result = [p for p in result if p.get("final_price", 0) >= filters["min_price"]]
    
    if filters.get("max_price") is not None:
        result = [p for p in result if p.get("final_price", 0) <= filters["max_price"]]
    
    if filters.get("min_rating") is not None:
        result = [p for p in result if p.get("average_rating", 0) >= filters["min_rating"]]
    
    if filters.get("stock_status"):
        result = [p for p in result if p.get("stock_status") == filters["stock_status"]]
    
    if filters.get("seller_id"):
        result = [p for p in result if p.get("seller_id") == filters["seller_id"]]
    
    if filters.get("has_discount"):
        result = [p for p in result if p.get("discount_percentage", 0) > 0]
    
    return result


def apply_sorting(products: List[dict], sort_by: ProductSortBy, order: SortOrder) -> List[dict]:
    """Sorts products."""
    reverse = order == SortOrder.DESC
    
    key_map = {
        ProductSortBy.PRICE: lambda p: p.get("final_price", 0),
        ProductSortBy.RATING: lambda p: p.get("average_rating", 0),
        ProductSortBy.NAME: lambda p: p.get("name", "").lower(),
        ProductSortBy.CREATED_AT: lambda p: p.get("created_at", ""),
        ProductSortBy.DISCOUNT: lambda p: p.get("discount_percentage", 0),
        ProductSortBy.REVIEW_COUNT: lambda p: p.get("review_count", 0),
    }
    
    return sorted(products, key=key_map.get(sort_by, key_map[ProductSortBy.CREATED_AT]), reverse=reverse)


def paginate(items: List, page: int, page_size: int) -> dict:
    """Paginates the list."""
    total = len(items)
    total_pages = (total + page_size - 1) // page_size if page_size > 0 else 1
    
    start = (page - 1) * page_size
    end = start + page_size
    
    return {
        "items": items[start:end],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_previous": page > 1
    }


@router.get(
    "",
    response_model=PaginatedResponse[Product],
    summary="List All Products",
    description="""
## List All Products

Returns all products in the store in paginated form.
Supports filtering, sorting and pagination.

### Filtering Options

| Parameter | Type | Description |
|-----------|------|-------------|
| category_id | int | Filter by category ID |
| min_price | float | Minimum price (inclusive) |
| max_price | float | Maximum price (inclusive) |
| min_rating | float | Minimum average rating (0-5) |
| stock_status | string | Stock status (in_stock, low_stock, out_of_stock, pre_order) |
| seller_id | int | Filter by seller ID |
| has_discount | bool | Only discounted products |

### Sorting Options

| sort_by | Description |
|---------|-------------|
| price | By price |
| rating | By rating |
| name | Alphabetical |
| created_at | By date added |
| discount | By discount percentage |
| review_count | By number of reviews |

### Example Usage

```
GET /products?category_id=1&min_price=100&max_price=1000&sort_by=rating&order=desc&page=1&page_size=20
```

### MCP Integration

This endpoint can be used for product discovery and filtering operations.
Returned data is in Product schema format.
""",
    responses={
        200: {
            "description": "Product list returned successfully",
            "content": {
                "application/json": {
                    "example": {
                        "items": [
                            {
                                "id": 1,
                                "name": "iPhone 15 Pro",
                                "price": 1199.99,
                                "final_price": 1079.99,
                                "discount_percentage": 10,
                                "average_rating": 4.7,
                                "review_count": 128
                            }
                        ],
                        "total": 150,
                        "page": 1,
                        "page_size": 10,
                        "total_pages": 15,
                        "has_next": True,
                        "has_previous": False
                    }
                }
            }
        }
    }
)
async def list_products(
    category_id: Optional[int] = Query(
        default=None, 
        description="Filter by category ID. Example: 1 (Electronics)",
        ge=1
    ),
    min_price: Optional[float] = Query(
        default=None, 
        description="Minimum price (inclusive). Example: 100.0",
        ge=0
    ),
    max_price: Optional[float] = Query(
        default=None, 
        description="Maximum price (inclusive). Example: 10000.0",
        ge=0
    ),
    min_rating: Optional[float] = Query(
        default=None, 
        description="Minimum average rating. Example: 4.0",
        ge=0, 
        le=5
    ),
    stock_status: Optional[StockStatus] = Query(
        default=None, 
        description="Stock status filter"
    ),
    seller_id: Optional[int] = Query(
        default=None, 
        description="Filter by seller ID",
        ge=1
    ),
    has_discount: Optional[bool] = Query(
        default=None, 
        description="If true, shows only discounted products"
    ),
    sort_by: ProductSortBy = Query(
        default=ProductSortBy.CREATED_AT, 
        description="Sort criteria"
    ),
    order: SortOrder = Query(
        default=SortOrder.DESC, 
        description="Sort direction (asc: ascending, desc: descending)"
    ),
    page: int = Query(
        default=1, 
        ge=1, 
        description="Page number (starts from 1)"
    ),
    page_size: int = Query(
        default=10, 
        ge=1, 
        le=100, 
        description="Items per page (max: 100)"
    )
):
    """
    Lists all products with filtering, sorting and pagination.
    """
    products = db.get_all_products()
    
    # Apply filters
    products = apply_filters(
        products,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        min_rating=min_rating,
        stock_status=stock_status.value if stock_status else None,
        seller_id=seller_id,
        has_discount=has_discount
    )
    
    # Apply sorting
    products = apply_sorting(products, sort_by, order)
    
    # Apply pagination
    return paginate(products, page, page_size)


@router.get(
    "/search",
    response_model=PaginatedResponse[Product],
    summary="Search Products",
    description="""
## Search Products

Performs text search in product name and description.
Search is case-insensitive.

### Search Algorithm

1. Searches in product name
2. Searches in product description
3. Returns all matching products

### Example Usage

```
GET /products/search?q=iphone&min_price=500&sort_by=rating
```

### MCP Integration

This endpoint can be used for product search with natural language queries.
User commands like "search for iPhone" can be routed to this endpoint.
""",
    responses={
        200: {"description": "Search results"},
        400: {"description": "Search term required"}
    }
)
async def search_products(
    q: str = Query(
        ..., 
        min_length=2, 
        description="Search term (minimum 2 characters). Searches in product name and description."
    ),
    category_id: Optional[int] = Query(
        default=None, 
        description="Filter results by category"
    ),
    min_price: Optional[float] = Query(
        default=None, 
        description="Minimum price filter",
        ge=0
    ),
    max_price: Optional[float] = Query(
        default=None, 
        description="Maximum price filter",
        ge=0
    ),
    sort_by: ProductSortBy = Query(
        default=ProductSortBy.RATING, 
        description="Sort criteria"
    ),
    order: SortOrder = Query(
        default=SortOrder.DESC, 
        description="Sort direction"
    ),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100)
):
    """
    Searches in product name and description.
    """
    # Perform search
    products = db.search_products(q)
    
    # Additional filters
    products = apply_filters(
        products,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price
    )
    
    # Sorting
    products = apply_sorting(products, sort_by, order)
    
    return paginate(products, page, page_size)


@router.get(
    "/category/{category_id}",
    response_model=PaginatedResponse[Product],
    summary="Products by Category",
    description="""
## List Products by Category

Returns all products in a specific category.
Supports sorting and pagination.

### Category IDs (Example)

| ID | Category |
|----|----------|
| 1 | Electronics |
| 2 | Fashion |
| 3 | Home & Living |
| 4 | Sports & Outdoor |
| 5 | Books & Hobbies |

### Example Usage

```
GET /products/category/1?sort_by=price&order=asc
```
""",
    responses={
        200: {"description": "Category products"},
        404: {"description": "Category not found"}
    }
)
async def get_products_by_category(
    category_id: int,
    sort_by: ProductSortBy = Query(default=ProductSortBy.RATING),
    order: SortOrder = Query(default=SortOrder.DESC),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100)
):
    """
    Lists products in a specific category.
    """
    # Category check
    category = db.get_category(category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with ID: {category_id} not found."
        )
    
    products = db.get_products_by_category(category_id)
    products = apply_sorting(products, sort_by, order)
    
    return paginate(products, page, page_size)


@router.get(
    "/{product_id}",
    response_model=ProductDetail,
    summary="Product Detail",
    description="""
## Single Product Detail

Returns all details of a specific product.

### Returned Data

- Basic product info (name, description, price, features)
- Seller info
- Category info
- Last 5 reviews
- 5 similar product recommendations
- Rating distribution statistics

### Example Usage

```
GET /products/1
```

### MCP Integration

This endpoint is used to get detailed product information.
Suitable for queries like "give me info about iPhone 15".
""",
    responses={
        200: {"description": "Product detail"},
        404: {"description": "Product not found"}
    }
)
async def get_product(product_id: int):
    """
    Returns all details of a single product along with reviews and similar products.
    """
    product = db.get_product(product_id)
    
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID: {product_id} not found."
        )
    
    # Add seller and category info
    seller = db.get_seller(product.get("seller_id"))
    category = db.get_category(product.get("category_id"))
    
    # Get reviews and add user names
    reviews = db.get_reviews_by_product(product_id)
    for review in reviews:
        user = db.get_user(review.get("user_id"))
        review["user_name"] = user.get("name", "Anonymous") if user else "Anonymous"
    
    # Get last 5 reviews
    recent_reviews = sorted(
        reviews, 
        key=lambda r: r.get("created_at", ""), 
        reverse=True
    )[:5]
    
    # Calculate rating distribution
    rating_distribution = {"5": 0, "4": 0, "3": 0, "2": 0, "1": 0}
    for review in reviews:
        rating = str(review.get("rating", 0))
        if rating in rating_distribution:
            rating_distribution[rating] += 1
    
    # Get similar products
    similar_products = RecommendationService.get_similar_products(product_id, limit=5)
    similar_summaries = []
    for p in similar_products:
        similar_summaries.append({
            "id": p.get("id"),
            "name": p.get("name"),
            "price": p.get("price"),
            "final_price": p.get("final_price"),
            "discount_percentage": p.get("discount_percentage", 0),
            "average_rating": p.get("average_rating", 0),
            "review_count": p.get("review_count", 0),
            "stock_status": p.get("stock_status", "in_stock"),
            "image": p.get("images", [None])[0] if p.get("images") else None
        })
    
    # Build detailed response
    return {
        **product,
        "seller_name": seller.get("name", "Unknown") if seller else "Unknown",
        "category_name": category.get("name", "Unknown") if category else "Unknown",
        "recent_reviews": recent_reviews,
        "similar_products": similar_summaries,
        "rating_distribution": rating_distribution
    }


@router.post(
    "",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
    summary="Add New Product",
    description="""
## Add New Product

Adds a new product to the store.

### Authentication

This endpoint **requires API Key**.
Authenticate with your seller identity using the `X-API-Key` header.

### Test API Keys

| Key | Seller |
|-----|--------|
| seller_key_001 | TechStore |
| seller_key_002 | FashionHub |
| seller_key_003 | HomeDecor |
| seller_key_004 | SportZone |
| seller_key_005 | BookWorld |

### Required Fields

- name: Product name
- description: Product description
- category_id: Category ID
- price: Price

### Example Request

```json
{
    "name": "Samsung Galaxy S24 Ultra",
    "description": "The newest Samsung flagship...",
    "category_id": 1,
    "price": 1399.99,
    "discount_percentage": 10,
    "stock_status": "in_stock",
    "features": {
        "Display": "6.8 inch",
        "RAM": "12GB"
    },
    "images": ["https://example.com/s24.jpg"]
}
```

### MCP Integration

Sellers can add products through this endpoint.
API key authentication should be sent as header in MCP tools.
""",
    responses={
        201: {"description": "Product created successfully"},
        401: {"description": "API key required"},
        403: {"description": "Invalid API key"},
        400: {"description": "Invalid category"}
    }
)
async def create_product(
    product: ProductCreate,
    seller: dict = Depends(get_current_seller)
):
    """
    Creates a new product. Requires API Key for seller authentication.
    """
    # Category check
    category = db.get_category(product.category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with ID: {product.category_id} not found."
        )
    
    # Prepare product data
    product_data = product.model_dump()
    product_data["seller_id"] = seller["id"]
    
    # Create product
    created_product = db.create_product(product_data)
    
    return created_product


@router.put(
    "/{product_id}",
    response_model=Product,
    summary="Update Product",
    description="""
## Update Product

Updates an existing product.

### Authorization

- **API Key** required
- Only **product owner** can update
- Trying to update another seller's product returns 403 error

### Partial Update

Only send the fields you want to change.
Fields not sent remain unchanged.

### Example Request

```json
{
    "price": 1299.99,
    "discount_percentage": 15,
    "stock_status": "low_stock"
}
```
""",
    responses={
        200: {"description": "Product updated"},
        401: {"description": "API key required"},
        403: {"description": "Authorization error - this product doesn't belong to you"},
        404: {"description": "Product not found"}
    }
)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    ownership: dict = Depends(verify_product_owner)
):
    """
    Updates an existing product. Only the product owner can update.
    """
    # Update data
    update_data = product_update.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You must specify at least one field to update."
        )
    
    # Check if category is changing
    if "category_id" in update_data:
        category = db.get_category(update_data["category_id"])
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with ID: {update_data['category_id']} not found."
            )
    
    updated_product = db.update_product(product_id, update_data)
    
    return updated_product


@router.delete(
    "/{product_id}",
    response_model=MessageResponse,
    summary="Delete Product",
    description="""
## Delete Product

Permanently deletes a product.

### Authorization

- **API Key** required
- Only **product owner** can delete

### Warning

This action cannot be undone. Product and all related reviews will be deleted.

### Example Usage

```
DELETE /products/1
Headers: X-API-Key: seller_key_001
```
""",
    responses={
        200: {"description": "Product deleted"},
        401: {"description": "API key required"},
        403: {"description": "Authorization error"},
        404: {"description": "Product not found"}
    }
)
async def delete_product(
    product_id: int,
    ownership: dict = Depends(verify_product_owner)
):
    """
    Deletes a product. Only the product owner can delete.
    """
    db.delete_product(product_id)
    
    return MessageResponse(
        message=f"Product with ID: {product_id} deleted successfully.",
        success=True
    )
