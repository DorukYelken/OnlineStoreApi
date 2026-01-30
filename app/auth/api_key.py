"""
API Key Authentication
======================
API key based authentication for seller operations.

This module provides API key authentication for seller operations
like adding/updating/deleting products.

Usage:
    - Header: X-API-Key: seller_key_001
    - Dependency: Depends(get_current_seller)

Test API Keys:
    - seller_key_001: TechStore
    - seller_key_002: FashionHub
    - seller_key_003: HomeDecor
    - seller_key_004: SportZone
    - seller_key_005: BookWorld
"""

from typing import Optional
from fastapi import Header, HTTPException, status, Depends
from ..database import db
from ..config import API_KEY_HEADER


async def verify_api_key(
    x_api_key: Optional[str] = Header(
        default=None,
        alias="X-API-Key",
        description="Seller API key. Required for adding, updating and deleting products."
    )
) -> str:
    """
    API Key Verification
    
    Checks the X-API-Key header in the incoming request.
    Returns 401 or 403 error for invalid or missing API key.
    
    Args:
        x_api_key: X-API-Key header value
    
    Returns:
        str: Verified API key
    
    Raises:
        HTTPException 401: API key header missing
        HTTPException 403: API key invalid
    
    Example:
        ```python
        @router.post("/products")
        async def create_product(
            api_key: str = Depends(verify_api_key)
        ):
            # api_key is verified
            ...
        ```
    """
    if x_api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required. Please send it with the X-API-Key header.",
            headers={"WWW-Authenticate": "ApiKey"}
        )
    
    if not db.verify_api_key(x_api_key):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key. Please make sure you are using the correct API key."
        )
    
    return x_api_key


async def get_current_seller(
    api_key: str = Depends(verify_api_key)
) -> dict:
    """
    Get Current Seller
    
    Returns seller information for the verified API key.
    This dependency is used in seller operations.
    
    Args:
        api_key: Verified API key (from verify_api_key)
    
    Returns:
        dict: Seller information
    
    Raises:
        HTTPException 403: Seller not found
    
    Example:
        ```python
        @router.post("/products")
        async def create_product(
            product: ProductCreate,
            seller: dict = Depends(get_current_seller)
        ):
            # Access seller ID with seller["id"]
            product_data = product.model_dump()
            product_data["seller_id"] = seller["id"]
            ...
        ```
    """
    seller = db.get_seller_by_api_key(api_key)
    
    if seller is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No seller found for this API key."
        )
    
    return seller


async def get_optional_seller(
    x_api_key: Optional[str] = Header(
        default=None,
        alias="X-API-Key",
        description="Optional seller API key"
    )
) -> Optional[dict]:
    """
    Optional Seller Info
    
    Returns seller info if API key exists, None otherwise.
    Used in endpoints that allow both anonymous and authenticated access.
    
    Args:
        x_api_key: Optional X-API-Key header value
    
    Returns:
        Optional[dict]: Seller info or None
    
    Example:
        ```python
        @router.get("/products/{id}")
        async def get_product(
            id: int,
            seller: Optional[dict] = Depends(get_optional_seller)
        ):
            # seller can be None (anonymous access)
            # seller can be dict (seller access)
            ...
        ```
    """
    if x_api_key is None:
        return None
    
    if not db.verify_api_key(x_api_key):
        return None
    
    return db.get_seller_by_api_key(x_api_key)


def check_product_ownership(product: dict, seller: dict) -> bool:
    """
    Product Ownership Check
    
    Checks if a seller owns a specific product.
    Used in update and delete operations.
    
    Args:
        product: Product data (must contain seller_id)
        seller: Seller data (must contain id)
    
    Returns:
        bool: Is the seller the product owner?
    
    Example:
        ```python
        if not check_product_ownership(product, seller):
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to update this product"
            )
        ```
    """
    return product.get("seller_id") == seller.get("id")


async def verify_product_owner(
    product_id: int,
    seller: dict = Depends(get_current_seller)
) -> dict:
    """
    Verify Product Owner
    
    Verifies that the seller owns a specific product.
    Used in PUT and DELETE endpoints.
    
    Args:
        product_id: Product ID
        seller: Current seller info
    
    Returns:
        dict: Dict containing product and seller info
    
    Raises:
        HTTPException 404: Product not found
        HTTPException 403: Authorization error
    """
    product = db.get_product(product_id)
    
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID: {product_id} not found."
        )
    
    if not check_product_ownership(product, seller):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to perform this action on this product. You can only update your own products."
        )
    
    return {"product": product, "seller": seller}
