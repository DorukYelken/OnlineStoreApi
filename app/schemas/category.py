"""
Category Schemas
================
Pydantic models for product categories.

This module defines schemas for categories:
- Category: Basic category info
- CategoryWithCount: Category with product count
"""

from typing import Optional, List
from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    """
    Category Base Schema
    
    Contains common fields for all category schemas.
    """
    name: str = Field(
        ..., 
        min_length=2, 
        max_length=50, 
        description="Category name",
        json_schema_extra={"example": "Electronics"}
    )
    description: str = Field(
        ..., 
        min_length=10, 
        description="Category description",
        json_schema_extra={"example": "Phones, computers, tablets and other electronic devices"}
    )
    icon: Optional[str] = Field(
        default=None, 
        description="Category icon (emoji or icon name)",
        json_schema_extra={"example": "📱"}
    )
    image_url: Optional[str] = Field(
        default=None, 
        description="Category cover image URL",
        json_schema_extra={"example": "https://example.com/categories/electronics.jpg"}
    )


class Category(CategoryBase):
    """
    Category Schema
    
    Basic category data.
    
    Attributes:
        id: Unique category ID
        name: Category name
        description: Category description
        icon: Category icon
        image_url: Cover image
        parent_id: Parent category ID (if subcategory)
    """
    id: int = Field(
        ..., 
        description="Unique category identifier",
        json_schema_extra={"example": 1}
    )
    parent_id: Optional[int] = Field(
        default=None, 
        description="Parent category ID. Null if it's a main category.",
        json_schema_extra={"example": None}
    )
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Electronics",
                "description": "Phones, computers, tablets and other electronic devices",
                "icon": "📱",
                "image_url": "https://example.com/categories/electronics.jpg",
                "parent_id": None
            }
        }


class CategoryWithCount(Category):
    """
    Category with Product Count Schema
    
    Shows category info along with the number of products it contains.
    Used in category listings.
    
    Attributes:
        product_count: Total number of products in this category
        subcategories: List of subcategories (if any)
    """
    product_count: int = Field(
        default=0, 
        ge=0, 
        description="Total number of products in this category",
        json_schema_extra={"example": 156}
    )
    subcategories: List["CategoryWithCount"] = Field(
        default_factory=list, 
        description="Subcategories (for hierarchical structure)"
    )
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Electronics",
                "description": "Phones, computers, tablets and other electronic devices",
                "icon": "📱",
                "image_url": "https://example.com/categories/electronics.jpg",
                "parent_id": None,
                "product_count": 156,
                "subcategories": []
            }
        }


class CategoryCreate(CategoryBase):
    """
    Category Create Schema
    
    Used to add a new category (admin operation).
    """
    parent_id: Optional[int] = Field(
        default=None, 
        description="Parent category ID (to create a subcategory)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Smartphones",
                "description": "iPhone, Samsung, Xiaomi and other smartphones",
                "icon": "📱",
                "parent_id": 1
            }
        }


# Forward reference for recursive model
CategoryWithCount.model_rebuild()
