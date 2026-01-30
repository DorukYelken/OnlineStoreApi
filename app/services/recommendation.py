"""
Recommendation Service
======================
Product recommendation algorithms.

This module contains various algorithms to provide product recommendations to users:
- Similar products (same category, similar price range)
- Top rated products
- Discounted products (deals)

Algorithms:
1. Category-based: Other products in the same category
2. Price-based: Products within ±30% price range
3. Rating-based: Products with 4+ rating prioritized
4. Popularity-based: Sorted by review count
"""

from typing import List, Dict, Any, Optional
from ..database import db


class RecommendationService:
    """
    Product Recommendation Service
    
    Service class that provides product recommendations based on different criteria.
    All methods are static and stateless.
    
    Usage:
        similar = RecommendationService.get_similar_products(product_id=1, limit=5)
        top_rated = RecommendationService.get_top_rated(category_id=1, limit=10)
        deals = RecommendationService.get_best_deals(limit=10)
    """
    
    @staticmethod
    def get_similar_products(
        product_id: int,
        limit: int = 5,
        include_same_seller: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Get Similar Products
        
        Returns products similar to the given product. Similarity criteria:
        1. Must be in the same category (required)
        2. Price within ±30% range (preferred)
        3. High rating (sorting criterion)
        
        Algorithm:
        - Filter products in the same category
        - Remove itself and (optionally) same seller's products
        - Score based on price similarity
        - Sort by average rating
        - Return first N products
        
        Args:
            product_id: Reference product ID
            limit: Maximum number of products to return
            include_same_seller: Include products from the same seller
        
        Returns:
            List[Dict]: Similar products list (sorted by score)
        
        Example Response:
            [
                {"id": 5, "name": "Samsung Galaxy S24", "price": 999.99, ...},
                {"id": 8, "name": "Google Pixel 8 Pro", "price": 899.99, ...}
            ]
        """
        # Get reference product
        product = db.get_product(product_id)
        if product is None:
            return []
        
        category_id = product.get("category_id")
        product_price = product.get("final_price", product.get("price", 0))
        seller_id = product.get("seller_id")
        
        # Get products in the same category
        candidates = db.get_products_by_category(category_id)
        
        # Remove itself
        candidates = [p for p in candidates if p.get("id") != product_id]
        
        # Remove same seller's products (optional)
        if not include_same_seller:
            candidates = [p for p in candidates if p.get("seller_id") != seller_id]
        
        # Score by price similarity and rating
        def calculate_score(p: Dict) -> float:
            p_price = p.get("final_price", p.get("price", 0))
            rating = p.get("average_rating", 0)
            
            # Price similarity score (bonus if within ±30%)
            if product_price > 0:
                price_diff_ratio = abs(p_price - product_price) / product_price
                price_score = max(0, 1 - price_diff_ratio) * 2  # 0-2 range
            else:
                price_score = 0
            
            # Total score = rating + price similarity
            return rating + price_score
        
        # Score and sort
        scored = [(p, calculate_score(p)) for p in candidates]
        scored.sort(key=lambda x: x[1], reverse=True)
        
        return [p for p, _ in scored[:limit]]
    
    @staticmethod
    def get_top_rated(
        category_id: Optional[int] = None,
        min_reviews: int = 3,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get Top Rated Products
        
        Returns products with the highest average rating.
        Provides reliable results with minimum review count filter.
        
        Algorithm:
        - Filter products meeting minimum review count
        - (Optional) Filter by category
        - Sort by average rating descending
        - Return first N products
        
        Args:
            category_id: Optional category filter
            min_reviews: Minimum review count (default: 3)
            limit: Maximum number of products to return
        
        Returns:
            List[Dict]: Top rated products (sorted by rating)
        
        Note:
            min_reviews parameter is used to filter out
            misleading high ratings from products with few reviews.
        """
        # Get all products or filter by category
        if category_id:
            products = db.get_products_by_category(category_id)
        else:
            products = db.get_all_products()
        
        # Minimum review count filter
        products = [p for p in products if p.get("review_count", 0) >= min_reviews]
        
        # Sort by rating
        products.sort(key=lambda p: p.get("average_rating", 0), reverse=True)
        
        return products[:limit]
    
    @staticmethod
    def get_best_deals(
        category_id: Optional[int] = None,
        min_discount: float = 5.0,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get Best Deals
        
        Returns products with the highest discount percentage.
        
        Algorithm:
        - Filter products meeting minimum discount percentage
        - (Optional) Filter by category
        - Sort by discount percentage descending
        - Return first N products
        
        Args:
            category_id: Optional category filter
            min_discount: Minimum discount percentage (default: 5%)
            limit: Maximum number of products to return
        
        Returns:
            List[Dict]: Discounted products (sorted by discount)
        
        Example Response:
            [
                {"id": 3, "name": "...", "discount_percentage": 25, ...},
                {"id": 7, "name": "...", "discount_percentage": 20, ...}
            ]
        """
        # Get all products or filter by category
        if category_id:
            products = db.get_products_by_category(category_id)
        else:
            products = db.get_all_products()
        
        # Minimum discount filter
        products = [
            p for p in products 
            if p.get("discount_percentage", 0) >= min_discount
        ]
        
        # Sort by discount percentage
        products.sort(key=lambda p: p.get("discount_percentage", 0), reverse=True)
        
        return products[:limit]
    
    @staticmethod
    def get_popular_products(
        category_id: Optional[int] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get Popular Products
        
        Returns products with the most reviews (most popular).
        
        Args:
            category_id: Optional category filter
            limit: Maximum number of products to return
        
        Returns:
            List[Dict]: Popular products (sorted by review count)
        """
        if category_id:
            products = db.get_products_by_category(category_id)
        else:
            products = db.get_all_products()
        
        # Sort by review count
        products.sort(key=lambda p: p.get("review_count", 0), reverse=True)
        
        return products[:limit]
    
    @staticmethod
    def get_price_range_products(
        min_price: float,
        max_price: float,
        category_id: Optional[int] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get Products in Price Range
        
        Returns products within a specific price range.
        
        Args:
            min_price: Minimum price (inclusive)
            max_price: Maximum price (inclusive)
            category_id: Optional category filter
            limit: Maximum number of products to return
        
        Returns:
            List[Dict]: Products in price range (sorted by rating)
        """
        if category_id:
            products = db.get_products_by_category(category_id)
        else:
            products = db.get_all_products()
        
        # Price filter (use final_price)
        products = [
            p for p in products
            if min_price <= p.get("final_price", p.get("price", 0)) <= max_price
        ]
        
        # Sort by rating
        products.sort(key=lambda p: p.get("average_rating", 0), reverse=True)
        
        return products[:limit]
    
    @staticmethod
    def get_new_arrivals(
        category_id: Optional[int] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get New Arrivals
        
        Returns most recently added products.
        
        Args:
            category_id: Optional category filter
            limit: Maximum number of products to return
        
        Returns:
            List[Dict]: New products (sorted by date added)
        """
        if category_id:
            products = db.get_products_by_category(category_id)
        else:
            products = db.get_all_products()
        
        # Sort by date (newest first)
        products.sort(key=lambda p: p.get("created_at", ""), reverse=True)
        
        return products[:limit]
