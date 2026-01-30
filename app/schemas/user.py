"""
User and Seller Schemas
=======================
Pydantic models for user and seller data.

This module defines schemas for users and sellers:
- User: Regular user (can write reviews)
- Seller: Seller (can add products, owns API key)
"""

from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    """
    User Base Schema
    
    Contains common fields for all user schemas.
    """
    name: str = Field(
        ..., 
        min_length=2, 
        max_length=100, 
        description="User's full name",
        json_schema_extra={"example": "John Smith"}
    )
    email: str = Field(
        ..., 
        description="User's email address",
        json_schema_extra={"example": "john@example.com"}
    )
    avatar_url: Optional[str] = Field(
        default=None, 
        description="User profile picture URL",
        json_schema_extra={"example": "https://example.com/avatars/john.jpg"}
    )


class User(UserBase):
    """
    User Schema
    
    Regular site user. Can write reviews, view products.
    
    Attributes:
        id: Unique user ID
        name: User name
        email: Email address
        avatar_url: Profile picture
        created_at: Registration date
        review_count: Total number of reviews made
    """
    id: int = Field(
        ..., 
        description="Unique user identifier",
        json_schema_extra={"example": 1}
    )
    created_at: str = Field(
        ..., 
        description="Account creation date (ISO 8601)",
        json_schema_extra={"example": "2024-06-15T10:00:00"}
    )
    review_count: int = Field(
        default=0, 
        description="Total number of reviews made by the user",
        json_schema_extra={"example": 15}
    )
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "John Smith",
                "email": "john@example.com",
                "avatar_url": "https://example.com/avatars/john.jpg",
                "created_at": "2024-06-15T10:00:00",
                "review_count": 15
            }
        }


class SellerBase(BaseModel):
    """
    Seller Base Schema
    
    Contains common fields for all seller schemas.
    """
    name: str = Field(
        ..., 
        min_length=2, 
        max_length=100, 
        description="Store/Seller name",
        json_schema_extra={"example": "TechStore"}
    )
    description: str = Field(
        ..., 
        min_length=10, 
        description="Store description",
        json_schema_extra={"example": "Your trusted technology store. Leading in electronics for 10 years."}
    )
    logo_url: Optional[str] = Field(
        default=None, 
        description="Store logo URL",
        json_schema_extra={"example": "https://example.com/logos/techstore.png"}
    )
    contact_email: str = Field(
        ..., 
        description="Contact email address",
        json_schema_extra={"example": "info@techstore.com"}
    )
    contact_phone: Optional[str] = Field(
        default=None, 
        description="Contact phone number",
        json_schema_extra={"example": "+1 555-0101"}
    )


class Seller(SellerBase):
    """
    Seller Schema
    
    Product seller. Authenticates with API key, can add/update products.
    
    Attributes:
        id: Unique seller ID
        name: Store name
        description: Store description
        logo_url: Store logo
        contact_email: Contact email
        contact_phone: Contact phone
        created_at: Registration date
        product_count: Number of products for sale
        average_rating: Seller average rating
        is_verified: Is verified seller?
    """
    id: int = Field(
        ..., 
        description="Unique seller identifier",
        json_schema_extra={"example": 1}
    )
    created_at: str = Field(
        ..., 
        description="Seller account creation date",
        json_schema_extra={"example": "2023-01-10T09:00:00"}
    )
    product_count: int = Field(
        default=0, 
        description="Number of active products by the seller",
        json_schema_extra={"example": 45}
    )
    average_rating: float = Field(
        default=0.0, 
        description="Average rating of all seller's products",
        json_schema_extra={"example": 4.5}
    )
    is_verified: bool = Field(
        default=False, 
        description="Whether the seller is verified/approved",
        json_schema_extra={"example": True}
    )
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "TechStore",
                "description": "Your trusted technology store.",
                "logo_url": "https://example.com/logos/techstore.png",
                "contact_email": "info@techstore.com",
                "contact_phone": "+1 555-0101",
                "created_at": "2023-01-10T09:00:00",
                "product_count": 45,
                "average_rating": 4.5,
                "is_verified": True
            }
        }


class SellerPublic(BaseModel):
    """
    Seller Public Schema
    
    Public seller information.
    Does not contain sensitive information like API key.
    """
    id: int = Field(description="Seller ID")
    name: str = Field(description="Store name")
    logo_url: Optional[str] = Field(default=None, description="Store logo")
    product_count: int = Field(description="Product count")
    average_rating: float = Field(description="Average rating")
    is_verified: bool = Field(description="Is verified seller")
    
    class Config:
        from_attributes = True
