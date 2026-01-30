"""
Product Schemas
===============
Pydantic models for product data.

This module defines all schemas required for product CRUD operations:
- ProductBase: Common fields
- ProductCreate: Product creation
- ProductUpdate: Product update
- Product: Full product data
- ProductDetail: Detailed product including reviews and recommendations
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from .common import StockStatus


class ProductBase(BaseModel):
    """
    Product Base Schema
    
    Contains common fields for all product schemas.
    
    Attributes:
        name: Product name (3-200 characters)
        description: Product description (detailed information)
        category_id: ID of the category it belongs to
        price: Original price (USD)
        discount_percentage: Discount percentage (0-100)
        stock_status: Stock status
        features: Product features (key-value)
        images: List of product image URLs
    """
    name: str = Field(
        ..., 
        min_length=3, 
        max_length=200, 
        description="Product name. Must be between 3-200 characters.",
        json_schema_extra={"example": "Apple iPhone 15 Pro 256GB"}
    )
    description: str = Field(
        ..., 
        min_length=10, 
        description="Product description. Should contain detailed information.",
        json_schema_extra={"example": "Apple's newest flagship phone. A17 Pro chip, 48MP camera system and titanium design."}
    )
    category_id: int = Field(
        ..., 
        gt=0, 
        description="ID of the category the product belongs to.",
        json_schema_extra={"example": 1}
    )
    price: float = Field(
        ..., 
        gt=0, 
        description="Original price of the product (USD). Price before discount.",
        json_schema_extra={"example": 1199.99}
    )
    discount_percentage: float = Field(
        default=0, 
        ge=0, 
        le=100, 
        description="Discount percentage. A value between 0-100.",
        json_schema_extra={"example": 10.0}
    )
    stock_status: StockStatus = Field(
        default=StockStatus.IN_STOCK, 
        description="Stock status of the product."
    )
    features: Dict[str, str] = Field(
        default_factory=dict, 
        description="Product features. As key-value pairs.",
        json_schema_extra={
            "example": {
                "Display": "6.1 inch Super Retina XDR",
                "Processor": "A17 Pro",
                "RAM": "8GB",
                "Storage": "256GB",
                "Camera": "48MP + 12MP + 12MP"
            }
        }
    )
    images: List[str] = Field(
        default_factory=list, 
        description="List of product image URLs.",
        json_schema_extra={
            "example": [
                "https://example.com/iphone15-1.jpg",
                "https://example.com/iphone15-2.jpg"
            ]
        }
    )


class ProductCreate(ProductBase):
    """
    Product Create Schema
    
    Used when adding a new product.
    Inherits all fields from ProductBase.
    seller_id is automatically determined from the API key.
    
    Required Fields:
    - name: Product name
    - description: Product description
    - category_id: Category ID
    - price: Price
    
    Optional Fields:
    - discount_percentage: Discount (default: 0)
    - stock_status: Stock status (default: in_stock)
    - features: Features (default: {})
    - images: Images (default: [])
    
    Example:
        POST /products
        Headers: X-API-Key: seller_key_001
        Body: {
            "name": "Samsung Galaxy S24",
            "description": "Samsung's new flagship...",
            "category_id": 1,
            "price": 999.99,
            "discount_percentage": 5,
            "features": {"Display": "6.2 inch", "RAM": "8GB"},
            "images": ["https://..."]
        }
    """
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Samsung Galaxy S24 Ultra 512GB",
                "description": "Samsung's most powerful phone. Snapdragon 8 Gen 3, 200MP camera and S Pen support.",
                "category_id": 1,
                "price": 1399.99,
                "discount_percentage": 8.0,
                "stock_status": "in_stock",
                "features": {
                    "Display": "6.8 inch Dynamic AMOLED 2X",
                    "Processor": "Snapdragon 8 Gen 3",
                    "RAM": "12GB",
                    "Storage": "512GB",
                    "Camera": "200MP + 12MP + 50MP + 10MP"
                },
                "images": [
                    "https://example.com/s24ultra-1.jpg",
                    "https://example.com/s24ultra-2.jpg"
                ]
            }
        }


class ProductUpdate(BaseModel):
    """
    Product Update Schema
    
    Used when updating an existing product.
    All fields are optional, only send the ones you want to change.
    
    Security: Only the product owner (seller) can update.
    
    Example:
        PUT /products/1
        Headers: X-API-Key: seller_key_001
        Body: {
            "price": 1099.99,
            "discount_percentage": 15,
            "stock_status": "low_stock"
        }
    """
    name: Optional[str] = Field(
        default=None, 
        min_length=3, 
        max_length=200, 
        description="New product name"
    )
    description: Optional[str] = Field(
        default=None, 
        min_length=10, 
        description="New product description"
    )
    category_id: Optional[int] = Field(
        default=None, 
        gt=0, 
        description="New category ID"
    )
    price: Optional[float] = Field(
        default=None, 
        gt=0, 
        description="New price"
    )
    discount_percentage: Optional[float] = Field(
        default=None, 
        ge=0, 
        le=100, 
        description="New discount percentage"
    )
    stock_status: Optional[StockStatus] = Field(
        default=None, 
        description="New stock status"
    )
    features: Optional[Dict[str, str]] = Field(
        default=None, 
        description="New features (completely replaces)"
    )
    images: Optional[List[str]] = Field(
        default=None, 
        description="New image list (completely replaces)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "price": 1099.99,
                "discount_percentage": 15.0,
                "stock_status": "low_stock"
            }
        }


class Product(ProductBase):
    """
    Product Schema
    
    Full product data returned from the API.
    Contains all fields of the product in the database.
    
    Attributes:
        id: Unique product ID
        seller_id: ID of the seller who added the product
        final_price: Calculated price after discount
        average_rating: Average rating (0-5)
        review_count: Total number of reviews
        created_at: Date added
        updated_at: Last update date
    """
    id: int = Field(
        ..., 
        description="Unique product identifier (auto-generated)",
        json_schema_extra={"example": 1}
    )
    seller_id: int = Field(
        ..., 
        description="ID of the seller who added the product",
        json_schema_extra={"example": 1}
    )
    final_price: float = Field(
        ..., 
        description="Calculated final price after discount (USD)",
        json_schema_extra={"example": 1079.99}
    )
    average_rating: float = Field(
        default=0.0, 
        ge=0, 
        le=5, 
        description="Average rating based on user reviews (0-5)",
        json_schema_extra={"example": 4.7}
    )
    review_count: int = Field(
        default=0, 
        ge=0, 
        description="Total number of reviews",
        json_schema_extra={"example": 128}
    )
    created_at: str = Field(
        ..., 
        description="Date the product was added (ISO 8601)",
        json_schema_extra={"example": "2025-01-15T10:30:00"}
    )
    updated_at: str = Field(
        ..., 
        description="Last update date (ISO 8601)",
        json_schema_extra={"example": "2025-01-20T14:45:00"}
    )
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Apple iPhone 15 Pro 256GB",
                "description": "Apple's newest flagship phone.",
                "category_id": 1,
                "price": 1199.99,
                "discount_percentage": 10.0,
                "final_price": 1079.99,
                "stock_status": "in_stock",
                "features": {
                    "Display": "6.1 inch Super Retina XDR",
                    "Processor": "A17 Pro"
                },
                "images": ["https://example.com/iphone15.jpg"],
                "seller_id": 1,
                "average_rating": 4.7,
                "review_count": 128,
                "created_at": "2025-01-15T10:30:00",
                "updated_at": "2025-01-20T14:45:00"
            }
        }


class ProductSummary(BaseModel):
    """
    Product Summary Schema
    
    Short product info used in list views.
    Contains only important fields instead of full details.
    """
    id: int = Field(description="Product ID")
    name: str = Field(description="Product name")
    price: float = Field(description="Original price")
    final_price: float = Field(description="Discounted price")
    discount_percentage: float = Field(description="Discount percentage")
    average_rating: float = Field(description="Average rating")
    review_count: int = Field(description="Number of reviews")
    stock_status: StockStatus = Field(description="Stock status")
    image: Optional[str] = Field(default=None, description="Main image URL")
    
    class Config:
        from_attributes = True


class ProductDetail(Product):
    """
    Product Detail Schema
    
    Extended information used on single product detail page.
    Contains related data in addition to the Product schema.
    
    Attributes:
        seller_name: Seller name
        category_name: Category name
        recent_reviews: Last 5 reviews
        similar_products: 5 similar products
        rating_distribution: Rating distribution (1-5 stars)
    """
    seller_name: str = Field(
        ..., 
        description="Name of the seller selling the product",
        json_schema_extra={"example": "TechStore"}
    )
    category_name: str = Field(
        ..., 
        description="Name of the product's category",
        json_schema_extra={"example": "Electronics"}
    )
    recent_reviews: List[Any] = Field(
        default_factory=list, 
        description="Last 5 reviews added"
    )
    similar_products: List[ProductSummary] = Field(
        default_factory=list, 
        description="5 similar product recommendations"
    )
    rating_distribution: Dict[str, int] = Field(
        default_factory=dict, 
        description="Rating distribution (review counts for 1-5 stars)",
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
    
    class Config:
        from_attributes = True
