"""
Common Schemas
==============
Common schemas for pagination, filtering and sorting.

This module defines common data structures used throughout the API:
- PaginatedResponse: Paginated list responses
- FilterParams: Product filtering parameters
- SortOrder: Sort direction
"""

from typing import TypeVar, Generic, List, Optional
from pydantic import BaseModel, Field
from enum import Enum


T = TypeVar("T")


class SortOrder(str, Enum):
    """
    Sort Direction
    
    Specifies the sort direction used in list endpoints.
    
    Values:
    - asc: Ascending order (A-Z, 0-9, oldest-newest)
    - desc: Descending order (Z-A, 9-0, newest-oldest)
    """
    ASC = "asc"
    DESC = "desc"


class ProductSortBy(str, Enum):
    """
    Product Sort Criteria
    
    Sort criteria used in product lists.
    
    Values:
    - price: Sort by price
    - rating: Sort by average rating
    - name: Sort alphabetically by product name
    - created_at: Sort by date added
    - discount: Sort by discount percentage
    - review_count: Sort by number of reviews
    """
    PRICE = "price"
    RATING = "rating"
    NAME = "name"
    CREATED_AT = "created_at"
    DISCOUNT = "discount"
    REVIEW_COUNT = "review_count"


class ReviewSortBy(str, Enum):
    """
    Review Sort Criteria
    
    Sort criteria used in review lists.
    
    Values:
    - date: Sort by review date
    - rating: Sort by rating
    - helpful: Sort by helpful count
    """
    DATE = "date"
    RATING = "rating"
    HELPFUL = "helpful"


class StockStatus(str, Enum):
    """
    Stock Status
    
    Indicates the stock status of a product.
    
    Values:
    - in_stock: In stock
    - low_stock: Running low (less than 5)
    - out_of_stock: Out of stock
    - pre_order: Pre-order
    """
    IN_STOCK = "in_stock"
    LOW_STOCK = "low_stock"
    OUT_OF_STOCK = "out_of_stock"
    PRE_ORDER = "pre_order"


class PaginationParams(BaseModel):
    """
    Pagination Parameters
    
    Used for pagination in list endpoints.
    
    Attributes:
        page: Page number (starts from 1)
        page_size: Items per page (max 100)
    """
    page: int = Field(
        default=1, 
        ge=1, 
        description="Page number. Starts from 1.",
        json_schema_extra={"example": 1}
    )
    page_size: int = Field(
        default=10, 
        ge=1, 
        le=100, 
        description="Items per page. Maximum 100.",
        json_schema_extra={"example": 10}
    )


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Paginated Response
    
    Response structure returned by list endpoints.
    
    Attributes:
        items: List of items on the current page
        total: Total number of items (all pages)
        page: Current page number
        page_size: Items per page
        total_pages: Total number of pages
        has_next: Is there a next page?
        has_previous: Is there a previous page?
    
    Example:
        {
            "items": [...],
            "total": 150,
            "page": 2,
            "page_size": 10,
            "total_pages": 15,
            "has_next": true,
            "has_previous": true
        }
    """
    items: List[T] = Field(description="List of items on the current page")
    total: int = Field(description="Total number of items (filtered)")
    page: int = Field(description="Current page number")
    page_size: int = Field(description="Items per page")
    total_pages: int = Field(description="Total number of pages")
    has_next: bool = Field(description="Is there a next page?")
    has_previous: bool = Field(description="Is there a previous page?")
    
    class Config:
        json_schema_extra = {
            "example": {
                "items": [],
                "total": 150,
                "page": 2,
                "page_size": 10,
                "total_pages": 15,
                "has_next": True,
                "has_previous": True
            }
        }


class FilterParams(BaseModel):
    """
    Product Filter Parameters
    
    Filtering options used in product lists.
    
    Attributes:
        category_id: Filter by category ID
        min_price: Minimum price (inclusive)
        max_price: Maximum price (inclusive)
        min_rating: Minimum average rating (inclusive)
        stock_status: Filter by stock status
        seller_id: Filter by seller ID
        has_discount: Only discounted products
    
    Example:
        {
            "category_id": 1,
            "min_price": 100,
            "max_price": 500,
            "min_rating": 4.0,
            "has_discount": true
        }
    """
    category_id: Optional[int] = Field(
        default=None, 
        description="Filter by category ID",
        json_schema_extra={"example": 1}
    )
    min_price: Optional[float] = Field(
        default=None, 
        ge=0, 
        description="Minimum price (inclusive)",
        json_schema_extra={"example": 100.0}
    )
    max_price: Optional[float] = Field(
        default=None, 
        ge=0, 
        description="Maximum price (inclusive)",
        json_schema_extra={"example": 1000.0}
    )
    min_rating: Optional[float] = Field(
        default=None, 
        ge=0, 
        le=5, 
        description="Minimum average rating (between 0-5)",
        json_schema_extra={"example": 4.0}
    )
    stock_status: Optional[StockStatus] = Field(
        default=None, 
        description="Filter by stock status"
    )
    seller_id: Optional[int] = Field(
        default=None, 
        description="Filter by seller ID",
        json_schema_extra={"example": 1}
    )
    has_discount: Optional[bool] = Field(
        default=None, 
        description="If true, shows only discounted products",
        json_schema_extra={"example": True}
    )


class MessageResponse(BaseModel):
    """
    Message Response
    
    Used for responses containing simple messages.
    
    Attributes:
        message: Response message
        success: Was the operation successful?
    """
    message: str = Field(description="Response message")
    success: bool = Field(default=True, description="Was the operation successful?")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Operation completed successfully",
                "success": True
            }
        }


class ErrorResponse(BaseModel):
    """
    Error Response
    
    Response structure returned for API errors.
    
    Attributes:
        detail: Error detail
        error_code: Error code (optional)
    """
    detail: str = Field(description="Error description")
    error_code: Optional[str] = Field(default=None, description="Error code")
    
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Product not found",
                "error_code": "PRODUCT_NOT_FOUND"
            }
        }
