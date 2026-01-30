"""
Recommendation Router
=====================
Product recommendation endpoints.

This module contains all endpoints for smart product recommendations.

Endpoints:
- GET /recommendations/similar/{product_id} - Similar products
- GET /recommendations/top-rated - Highest rated products
- GET /recommendations/deals - Discounted products
- GET /recommendations/popular - Popular products
- GET /recommendations/new-arrivals - New products

MCP Conversion Notes:
- Recommendation endpoints can be used for discovery
- Filtering and limit parameters supported
- Each endpoint focuses on a specific use case
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from ..database import db
from ..schemas.product import Product
from ..services.recommendation import RecommendationService


router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get(
    "/similar/{product_id}",
    response_model=List[Product],
    summary="Similar Products",
    description="""
## Get Similar Products

Returns products similar to a given product.

### Similarity Criteria

1. **Same Category** (required): Products must be in the same category
2. **Price Similarity** (weighted): Products within ±30% price range are preferred
3. **High Rating** (sorting): Sorted by average rating

### Algorithm Detail

```
score = average_rating + price_similarity_score
price_similarity_score = max(0, 1 - |price_difference_ratio|) × 2
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| limit | int | 5 | Number of products to return (max: 20) |
| include_same_seller | bool | false | Include products from the same seller |

### Example Usage

```
GET /recommendations/similar/1?limit=10
GET /recommendations/similar/1?include_same_seller=true
```

### Use Cases

- "Similar Products" section on product detail page
- "Customers who bought this also bought" recommendations
- Alternatives for product comparison

### MCP Integration

Can be used for commands like "show similar products" or "list iPhone alternatives".
""",
    responses={
        200: {"description": "Similar products list"},
        404: {"description": "Product not found"}
    }
)
async def get_similar_products(
    product_id: int,
    limit: int = Query(
        default=5,
        ge=1,
        le=20,
        description="Maximum number of products to return"
    ),
    include_same_seller: bool = Query(
        default=False,
        description="If true, includes other products from the same seller"
    )
):
    """
    Returns products similar to the given product using recommendation algorithm.
    """
    # Product check
    product = db.get_product(product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID: {product_id} not found."
        )
    
    similar = RecommendationService.get_similar_products(
        product_id=product_id,
        limit=limit,
        include_same_seller=include_same_seller
    )
    
    return similar


@router.get(
    "/top-rated",
    response_model=List[Product],
    summary="Top Rated Products",
    description="""
## Top Rated Products

Returns products with the highest average rating.

### Reliability Filter

A minimum review count filter is applied to prevent misleading results.
High ratings from products with few reviews may not be reliable.

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| category_id | int | - | Optional category filter |
| min_reviews | int | 3 | Minimum number of reviews |
| limit | int | 10 | Number of products to return |

### Sorting

Products are returned in descending order by average rating (highest first).

### Example Usage

```
GET /recommendations/top-rated
GET /recommendations/top-rated?category_id=1&min_reviews=5
GET /recommendations/top-rated?limit=20
```

### Use Cases

- "Most Loved" section on homepage
- "Best" filter on category page
- Gift recommendations ("Recommend the best phone")

### MCP Integration

Used for queries like "What are the best products?", "Highest rated phones".
""",
    responses={
        200: {"description": "Top rated products"}
    }
)
async def get_top_rated(
    category_id: Optional[int] = Query(
        default=None,
        description="Optional category filter. If not specified, all categories are included."
    ),
    min_reviews: int = Query(
        default=3,
        ge=1,
        description="Minimum number of reviews. Products with fewer reviews are excluded."
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=50,
        description="Maximum number of products to return"
    )
):
    """
    Returns products with the highest average rating.
    """
    return RecommendationService.get_top_rated(
        category_id=category_id,
        min_reviews=min_reviews,
        limit=limit
    )


@router.get(
    "/deals",
    response_model=List[Product],
    summary="Discounted Products",
    description="""
## Best Deals

Returns products with the highest discount percentage.

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| category_id | int | - | Optional category filter |
| min_discount | float | 5.0 | Minimum discount percentage |
| limit | int | 10 | Number of products to return |

### Sorting

Products are returned in descending order by discount percentage.
Highest discounts shown first.

### Calculation

```
savings = original_price - discounted_price
discounted_price = original_price × (1 - discount_percentage / 100)
```

### Example Usage

```
GET /recommendations/deals
GET /recommendations/deals?min_discount=20  # At least 20% off
GET /recommendations/deals?category_id=1    # Only electronics
```

### Use Cases

- "Deals of the Day" section on homepage
- Discount campaign page
- Budget-friendly recommendations

### MCP Integration

Used for queries like "show discounted products", "phones with biggest discounts".
""",
    responses={
        200: {"description": "Discounted products list"}
    }
)
async def get_deals(
    category_id: Optional[int] = Query(
        default=None,
        description="Optional category filter"
    ),
    min_discount: float = Query(
        default=5.0,
        ge=0,
        le=100,
        description="Minimum discount percentage. Example: 10 = at least 10% off"
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=50,
        description="Maximum number of products to return"
    )
):
    """
    Returns products with the highest discount percentage.
    """
    return RecommendationService.get_best_deals(
        category_id=category_id,
        min_discount=min_discount,
        limit=limit
    )


@router.get(
    "/popular",
    response_model=List[Product],
    summary="Popular Products",
    description="""
## Popular Products

Returns products with the most reviews (most popular).

### Popularity Criteria

Popularity is determined by total review count.
Products with many reviews have received more attention.

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| category_id | int | - | Optional category filter |
| limit | int | 10 | Number of products to return |

### Sorting

Products are returned in descending order by review count.

### Example Usage

```
GET /recommendations/popular
GET /recommendations/popular?category_id=2&limit=5
```

### Use Cases

- "Trending Products" section on homepage
- "Everyone's buying these" recommendations
- Category-based popularity

### MCP Integration

Used for queries like "most popular products", "trending phones".
""",
    responses={
        200: {"description": "Popular products list"}
    }
)
async def get_popular(
    category_id: Optional[int] = Query(
        default=None,
        description="Optional category filter"
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=50,
        description="Maximum number of products to return"
    )
):
    """
    Returns most popular (most reviewed) products.
    """
    return RecommendationService.get_popular_products(
        category_id=category_id,
        limit=limit
    )


@router.get(
    "/new-arrivals",
    response_model=List[Product],
    summary="New Products",
    description="""
## New Arrivals

Returns the most recently added products.

### Sorting

Products are returned in descending order by date added.
Newest products shown first.

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| category_id | int | - | Optional category filter |
| limit | int | 10 | Number of products to return |

### Example Usage

```
GET /recommendations/new-arrivals
GET /recommendations/new-arrivals?category_id=3
```

### Use Cases

- "New Arrivals" section on homepage
- "New Products" tab on category page
- For users tracking new releases

### MCP Integration

Used for queries like "newly added products", "latest phones".
""",
    responses={
        200: {"description": "New products list"}
    }
)
async def get_new_arrivals(
    category_id: Optional[int] = Query(
        default=None,
        description="Optional category filter"
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=50,
        description="Maximum number of products to return"
    )
):
    """
    Returns most recently added products.
    """
    return RecommendationService.get_new_arrivals(
        category_id=category_id,
        limit=limit
    )


@router.get(
    "/price-range",
    response_model=List[Product],
    summary="Products in Price Range",
    description="""
## Products in Price Range

Returns products within a specific price range.
Useful for budget-based product recommendations.

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| min_price | float | **required** | Minimum price (inclusive) |
| max_price | float | **required** | Maximum price (inclusive) |
| category_id | int | - | Optional category filter |
| limit | int | 10 | Number of products to return |

### Sorting

Products are returned in descending order by average rating.
Best products within budget shown first.

### Example Usage

```
GET /recommendations/price-range?min_price=100&max_price=500
GET /recommendations/price-range?min_price=500&max_price=1000&category_id=1
```

### Use Cases

- "Recommend a phone under $500"
- Budget-filtered product search
- Price comparison

### MCP Integration

Suitable for queries like "recommend phone under $1000", "headphones between $100-200".
""",
    responses={
        200: {"description": "Products in price range"},
        400: {"description": "Invalid price range"}
    }
)
async def get_by_price_range(
    min_price: float = Query(
        ...,
        ge=0,
        description="Minimum price (inclusive)"
    ),
    max_price: float = Query(
        ...,
        ge=0,
        description="Maximum price (inclusive)"
    ),
    category_id: Optional[int] = Query(
        default=None,
        description="Optional category filter"
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=50,
        description="Maximum number of products to return"
    )
):
    """
    Returns best products within a specific price range.
    """
    if min_price > max_price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="min_price cannot be greater than max_price."
        )
    
    return RecommendationService.get_price_range_products(
        min_price=min_price,
        max_price=max_price,
        category_id=category_id,
        limit=limit
    )
