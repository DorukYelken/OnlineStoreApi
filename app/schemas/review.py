"""
Review Schemas
==============
Pydantic models for user reviews.

This module defines all schemas required for review operations:
- ReviewBase: Common fields
- ReviewCreate: Review creation
- Review: Full review data
- ReviewStats: Rating statistics
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class ReviewBase(BaseModel):
    """
    Review Base Schema
    
    Contains common fields for all review schemas.
    
    Attributes:
        rating: Rating (1-5 stars)
        title: Review title (short summary)
        comment: Review text (detailed evaluation)
        pros: List of pros
        cons: List of cons
    """
    rating: int = Field(
        ..., 
        ge=1, 
        le=5, 
        description="Product rating. Between 1 (very bad) and 5 (excellent).",
        json_schema_extra={"example": 5}
    )
    title: str = Field(
        ..., 
        min_length=3, 
        max_length=100, 
        description="Review title. A short and concise evaluation.",
        json_schema_extra={"example": "Amazing product!"}
    )
    comment: str = Field(
        ..., 
        min_length=10, 
        max_length=2000, 
        description="Detailed review text. Share your product experience.",
        json_schema_extra={"example": "I've been using this phone for 2 months. Camera quality is great and battery life meets my expectations."}
    )
    pros: List[str] = Field(
        default_factory=list, 
        description="List of product pros/liked aspects.",
        json_schema_extra={"example": ["Camera quality", "Battery life", "Fast processor"]}
    )
    cons: List[str] = Field(
        default_factory=list, 
        description="List of product cons/disliked aspects.",
        json_schema_extra={"example": ["Price is high", "Charger not included"]}
    )


class ReviewCreate(ReviewBase):
    """
    Review Create Schema
    
    Used when adding a new review.
    
    Required Fields:
    - user_id: ID of the user making the review
    - rating: Rating (1-5)
    - title: Review title
    - comment: Review text
    
    Optional Fields:
    - pros: List of pros
    - cons: List of cons
    
    Note: product_id is taken from the URL.
    
    Example:
        POST /products/1/reviews
        Body: {
            "user_id": 5,
            "rating": 4,
            "title": "Nice phone but...",
            "comment": "Overall satisfied but there are a few issues...",
            "pros": ["Design", "Display"],
            "cons": ["Battery life short"]
        }
    """
    user_id: int = Field(
        ..., 
        gt=0, 
        description="ID of the user making the review.",
        json_schema_extra={"example": 5}
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 5,
                "rating": 4,
                "title": "Nice phone but battery life is short",
                "comment": "I've been using the phone for 1 month. Overall satisfied, camera is great. However, battery barely lasts a day with heavy use.",
                "pros": ["Camera quality", "Screen brightness", "Fast charging"],
                "cons": ["Battery life", "Heating issue"]
            }
        }


class Review(ReviewBase):
    """
    Review Schema
    
    Full review data returned from the API.
    
    Attributes:
        id: Unique review ID
        product_id: ID of the product the review belongs to
        user_id: ID of the user who made the review
        user_name: Display name of the user
        created_at: Review date
        helpful_count: Number of users who found it helpful
    """
    id: int = Field(
        ..., 
        description="Unique review identifier",
        json_schema_extra={"example": 1}
    )
    product_id: int = Field(
        ..., 
        description="ID of the product the review belongs to",
        json_schema_extra={"example": 1}
    )
    user_id: int = Field(
        ..., 
        description="ID of the user who made the review",
        json_schema_extra={"example": 5}
    )
    user_name: Optional[str] = Field(
        default=None, 
        description="Display name of the user",
        json_schema_extra={"example": "John S."}
    )
    created_at: str = Field(
        ..., 
        description="Date the review was written (ISO 8601)",
        json_schema_extra={"example": "2025-01-20T14:30:00"}
    )
    helpful_count: int = Field(
        default=0, 
        ge=0, 
        description="Number of users who found this review helpful",
        json_schema_extra={"example": 42}
    )
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "product_id": 1,
                "user_id": 5,
                "user_name": "John S.",
                "rating": 5,
                "title": "Amazing product!",
                "comment": "I've been using this phone for 2 months. Camera quality is great.",
                "pros": ["Camera quality", "Battery life", "Fast processor"],
                "cons": ["Price is high"],
                "created_at": "2025-01-20T14:30:00",
                "helpful_count": 42
            }
        }


class ReviewStats(BaseModel):
    """
    Review Statistics Schema
    
    Contains review statistics for a product.
    Rating distribution and summary information.
    
    Attributes:
        product_id: Product ID
        total_reviews: Total number of reviews
        average_rating: Average rating
        rating_distribution: Number of reviews for each rating
        recommendation_percentage: Percentage who recommend (4+ rating)
    
    Example Response:
        {
            "product_id": 1,
            "total_reviews": 128,
            "average_rating": 4.7,
            "rating_distribution": {
                "5": 85,
                "4": 30,
                "3": 10,
                "2": 2,
                "1": 1
            },
            "recommendation_percentage": 89.8
        }
    """
    product_id: int = Field(
        ..., 
        description="ID of the product the statistics belong to",
        json_schema_extra={"example": 1}
    )
    total_reviews: int = Field(
        default=0, 
        description="Total number of reviews",
        json_schema_extra={"example": 128}
    )
    average_rating: float = Field(
        default=0.0, 
        description="Average of all reviews (0-5)",
        json_schema_extra={"example": 4.7}
    )
    rating_distribution: dict = Field(
        default_factory=lambda: {"5": 0, "4": 0, "3": 0, "2": 0, "1": 0}, 
        description="Number of reviews for each rating value",
        json_schema_extra={
            "example": {
                "5": 85,
                "4": 30,
                "3": 10,
                "2": 2,
                "1": 1
            }
        }
    )
    recommendation_percentage: float = Field(
        default=0.0, 
        description="Percentage of users who recommend the product (those who gave 4+ rating)",
        json_schema_extra={"example": 89.8}
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "product_id": 1,
                "total_reviews": 128,
                "average_rating": 4.7,
                "rating_distribution": {
                    "5": 85,
                    "4": 30,
                    "3": 10,
                    "2": 2,
                    "1": 1
                },
                "recommendation_percentage": 89.8
            }
        }
