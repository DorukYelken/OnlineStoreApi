"""
Review Router
=============
API endpoints for user reviews.

This module contains all endpoints for product reviews.

Endpoints:
- GET /products/{product_id}/reviews - List product reviews
- POST /products/{product_id}/reviews - Add new review
- GET /reviews/stats/{product_id} - Rating statistics
- POST /reviews/{review_id}/helpful - Mark review as helpful

MCP Conversion Notes:
- Each endpoint includes detailed description
- Adding reviews requires user interaction
- Statistics can be used for analysis
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from ..database import db
from ..schemas.review import Review, ReviewCreate, ReviewStats
from ..schemas.common import PaginatedResponse, ReviewSortBy, SortOrder


router = APIRouter(tags=["Reviews"])


def apply_review_sorting(reviews: List[dict], sort_by: ReviewSortBy, order: SortOrder) -> List[dict]:
    """Sorts reviews."""
    reverse = order == SortOrder.DESC
    
    key_map = {
        ReviewSortBy.DATE: lambda r: r.get("created_at", ""),
        ReviewSortBy.RATING: lambda r: r.get("rating", 0),
        ReviewSortBy.HELPFUL: lambda r: r.get("helpful_count", 0),
    }
    
    return sorted(reviews, key=key_map.get(sort_by, key_map[ReviewSortBy.DATE]), reverse=reverse)


def paginate_reviews(items: List, page: int, page_size: int) -> dict:
    """Paginates reviews."""
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
    "/products/{product_id}/reviews",
    response_model=PaginatedResponse[Review],
    summary="List Product Reviews",
    description="""
## List Product Reviews

Returns all reviews of a specific product in paginated form.

### Sorting Options

| sort_by | Description |
|---------|-------------|
| date | By review date |
| rating | By rating |
| helpful | By helpful count |

### Filtering

| Parameter | Description |
|-----------|-------------|
| rating | Filter reviews by specific rating (1-5) |

### Example Usage

```
GET /products/1/reviews?sort_by=helpful&order=desc&page=1
GET /products/1/reviews?rating=5  # Only 5-star reviews
```

### Response Content

Each review includes:
- User info (name)
- Rating (1-5)
- Title and detailed comment
- Pros/cons list
- Helpful count
- Review date

### MCP Integration

This endpoint is used to analyze product reviews or display them to users.
Suitable for commands like "show reviews for this product".
""",
    responses={
        200: {"description": "Review list"},
        404: {"description": "Product not found"}
    }
)
async def get_product_reviews(
    product_id: int,
    rating: Optional[int] = Query(
        default=None,
        ge=1,
        le=5,
        description="Filter by rating (1-5). Example: rating=5 returns only 5-star reviews."
    ),
    sort_by: ReviewSortBy = Query(
        default=ReviewSortBy.DATE,
        description="Sort criteria"
    ),
    order: SortOrder = Query(
        default=SortOrder.DESC,
        description="Sort direction. DESC: Newest first / Highest first"
    ),
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=10, ge=1, le=50, description="Reviews per page (max: 50)")
):
    """
    Lists, sorts and paginates product reviews.
    """
    # Product check
    product = db.get_product(product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID: {product_id} not found."
        )
    
    # Get reviews
    reviews = db.get_reviews_by_product(product_id)
    
    # Add user names
    for review in reviews:
        user = db.get_user(review.get("user_id"))
        review["user_name"] = user.get("name", "Anonymous") if user else "Anonymous"
    
    # Filter by rating
    if rating is not None:
        reviews = [r for r in reviews if r.get("rating") == rating]
    
    # Sort
    reviews = apply_review_sorting(reviews, sort_by, order)
    
    # Paginate
    return paginate_reviews(reviews, page, page_size)


@router.post(
    "/products/{product_id}/reviews",
    response_model=Review,
    status_code=status.HTTP_201_CREATED,
    summary="Add New Review",
    description="""
## Add New Review

Adds a new review to a product.

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| user_id | int | ID of user making the review |
| rating | int | Rating (1-5) |
| title | string | Review title (3-100 characters) |
| comment | string | Detailed review (10-2000 characters) |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| pros | array | List of pros |
| cons | array | List of cons |

### Example Request

```json
{
    "user_id": 5,
    "rating": 4,
    "title": "Nice product but has some issues",
    "comment": "The product generally met my expectations...",
    "pros": ["Fast shipping", "Quality packaging", "Matches description"],
    "cons": ["User manual is insufficient"]
}
```

### Result

After adding a review:
- Product's average rating is automatically updated
- Product's review count is incremented

### MCP Integration

Can be used to collect user feedback.
Note: In a real application, user authentication would be required.
""",
    responses={
        201: {"description": "Review added successfully"},
        404: {"description": "Product or user not found"},
        400: {"description": "Invalid data"}
    }
)
async def create_review(
    product_id: int,
    review: ReviewCreate
):
    """
    Adds a new review to a product and updates the product rating.
    """
    # Product check
    product = db.get_product(product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID: {product_id} not found."
        )
    
    # User check
    user = db.get_user(review.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID: {review.user_id} not found."
        )
    
    # Prepare review data
    review_data = review.model_dump()
    review_data["product_id"] = product_id
    
    # Create review (this automatically updates product rating)
    created_review = db.create_review(review_data)
    
    # Add user name
    created_review["user_name"] = user.get("name", "Anonymous")
    
    return created_review


@router.get(
    "/reviews/stats/{product_id}",
    response_model=ReviewStats,
    summary="Rating Statistics",
    description="""
## Product Rating Statistics

Returns review and rating statistics for a product.

### Returned Data

| Field | Description |
|-------|-------------|
| total_reviews | Total number of reviews |
| average_rating | Average rating (0-5) |
| rating_distribution | Number of reviews for each rating |
| recommendation_percentage | Percentage who recommend (4+ rating) |

### Rating Distribution

```json
{
    "rating_distribution": {
        "5": 85,  // Number of 5-star reviews
        "4": 30,
        "3": 10,
        "2": 2,
        "1": 1
    }
}
```

### Recommendation Percentage

Percentage of users who gave 4 or 5 stars.
For example, if 115 out of 128 reviews are 4+ stars: 89.8%

### Example Usage

```
GET /reviews/stats/1
```

### MCP Integration

This endpoint can be used to get a quick summary about a product.
Suitable for questions like "What's the rating of this product?".
""",
    responses={
        200: {"description": "Rating statistics"},
        404: {"description": "Product not found"}
    }
)
async def get_review_stats(product_id: int):
    """
    Returns rating distribution and review statistics for a product.
    """
    # Product check
    product = db.get_product(product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID: {product_id} not found."
        )
    
    # Get reviews
    reviews = db.get_reviews_by_product(product_id)
    
    # Calculate statistics
    total_reviews = len(reviews)
    
    if total_reviews == 0:
        return ReviewStats(
            product_id=product_id,
            total_reviews=0,
            average_rating=0.0,
            rating_distribution={"5": 0, "4": 0, "3": 0, "2": 0, "1": 0},
            recommendation_percentage=0.0
        )
    
    # Rating distribution
    rating_distribution = {"5": 0, "4": 0, "3": 0, "2": 0, "1": 0}
    total_rating = 0
    positive_reviews = 0
    
    for review in reviews:
        rating = review.get("rating", 0)
        total_rating += rating
        
        rating_str = str(rating)
        if rating_str in rating_distribution:
            rating_distribution[rating_str] += 1
        
        if rating >= 4:
            positive_reviews += 1
    
    average_rating = round(total_rating / total_reviews, 2)
    recommendation_percentage = round((positive_reviews / total_reviews) * 100, 1)
    
    return ReviewStats(
        product_id=product_id,
        total_reviews=total_reviews,
        average_rating=average_rating,
        rating_distribution=rating_distribution,
        recommendation_percentage=recommendation_percentage
    )


@router.post(
    "/reviews/{review_id}/helpful",
    response_model=dict,
    summary="Mark Review as Helpful",
    description="""
## Mark Review as Helpful

Increments the "helpful" counter of a review by 1.

### Usage

```
POST /reviews/42/helpful
```

### Response

```json
{
    "message": "Review marked as helpful",
    "helpful_count": 43
}
```

### Note

This endpoint does not have rate limiting.
In a real application, there should be a single vote limit per user.
""",
    responses={
        200: {"description": "Helpful counter incremented"},
        404: {"description": "Review not found"}
    }
)
async def mark_review_helpful(review_id: int):
    """
    Increments the review's helpful counter.
    """
    success = db.increment_helpful(review_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with ID: {review_id} not found."
        )
    
    review = db.get_review(review_id)
    
    return {
        "message": "Review marked as helpful",
        "helpful_count": review.get("helpful_count", 0)
    }
