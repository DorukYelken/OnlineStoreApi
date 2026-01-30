"""
In-Memory Database
==================
In-memory data storage and CRUD operations for the application.

This module provides data storage using Python dictionaries instead of
a real database. Data is reset when the application restarts
and reloaded with seed data.

Data Structures:
- products: Product information (id -> Product dict)
- reviews: User reviews (id -> Review dict)
- users: User information (id -> User dict)
- sellers: Seller information (id -> Seller dict)
- categories: Category information (id -> Category dict)
- api_keys: API key -> seller_id mappings
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import threading


class InMemoryDatabase:
    """
    Thread-safe in-memory database class.
    
    Provides a centralized structure for all CRUD operations.
    Thread-safety is guaranteed with a lock mechanism.
    """
    
    def __init__(self):
        self._lock = threading.Lock()
        self._products: Dict[int, Dict[str, Any]] = {}
        self._reviews: Dict[int, Dict[str, Any]] = {}
        self._users: Dict[int, Dict[str, Any]] = {}
        self._sellers: Dict[int, Dict[str, Any]] = {}
        self._categories: Dict[int, Dict[str, Any]] = {}
        self._api_keys: Dict[str, int] = {}  # api_key -> seller_id
        
        # Auto-increment counters
        self._product_counter = 0
        self._review_counter = 0
        self._user_counter = 0
        self._seller_counter = 0
        self._category_counter = 0
    
    # ==================== PRODUCTS ====================
    
    def get_all_products(self) -> List[Dict[str, Any]]:
        """Returns all products."""
        with self._lock:
            return list(self._products.values())
    
    def get_product(self, product_id: int) -> Optional[Dict[str, Any]]:
        """Returns a single product by ID."""
        with self._lock:
            return self._products.get(product_id)
    
    def get_products_by_category(self, category_id: int) -> List[Dict[str, Any]]:
        """Returns products in a specific category."""
        with self._lock:
            return [p for p in self._products.values() if p.get("category_id") == category_id]
    
    def get_products_by_seller(self, seller_id: int) -> List[Dict[str, Any]]:
        """Returns products of a specific seller."""
        with self._lock:
            return [p for p in self._products.values() if p.get("seller_id") == seller_id]
    
    def search_products(self, query: str) -> List[Dict[str, Any]]:
        """Searches in product name or description."""
        query_lower = query.lower()
        with self._lock:
            return [
                p for p in self._products.values()
                if query_lower in p.get("name", "").lower() 
                or query_lower in p.get("description", "").lower()
            ]
    
    def create_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new product."""
        with self._lock:
            self._product_counter += 1
            product_id = self._product_counter
            product = {
                "id": product_id,
                **product_data,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "average_rating": 0.0,
                "review_count": 0
            }
            # Calculate final price
            price = product.get("price", 0)
            discount = product.get("discount_percentage", 0)
            product["final_price"] = round(price * (1 - discount / 100), 2)
            
            self._products[product_id] = product
            return product
    
    def update_product(self, product_id: int, product_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Updates an existing product."""
        with self._lock:
            if product_id not in self._products:
                return None
            
            product = self._products[product_id]
            product.update(product_data)
            product["updated_at"] = datetime.now().isoformat()
            
            # Recalculate final price
            price = product.get("price", 0)
            discount = product.get("discount_percentage", 0)
            product["final_price"] = round(price * (1 - discount / 100), 2)
            
            return product
    
    def delete_product(self, product_id: int) -> bool:
        """Deletes a product."""
        with self._lock:
            if product_id in self._products:
                del self._products[product_id]
                # Also delete related reviews
                self._reviews = {
                    k: v for k, v in self._reviews.items() 
                    if v.get("product_id") != product_id
                }
                return True
            return False
    
    def update_product_rating(self, product_id: int):
        """Updates the product's average rating and review count."""
        with self._lock:
            if product_id not in self._products:
                return
            
            product_reviews = [
                r for r in self._reviews.values() 
                if r.get("product_id") == product_id
            ]
            
            if product_reviews:
                avg_rating = sum(r.get("rating", 0) for r in product_reviews) / len(product_reviews)
                self._products[product_id]["average_rating"] = round(avg_rating, 2)
                self._products[product_id]["review_count"] = len(product_reviews)
            else:
                self._products[product_id]["average_rating"] = 0.0
                self._products[product_id]["review_count"] = 0
    
    # ==================== REVIEWS ====================
    
    def get_all_reviews(self) -> List[Dict[str, Any]]:
        """Returns all reviews."""
        with self._lock:
            return list(self._reviews.values())
    
    def get_review(self, review_id: int) -> Optional[Dict[str, Any]]:
        """Returns a single review by ID."""
        with self._lock:
            return self._reviews.get(review_id)
    
    def get_reviews_by_product(self, product_id: int) -> List[Dict[str, Any]]:
        """Returns reviews for a specific product."""
        with self._lock:
            return [r for r in self._reviews.values() if r.get("product_id") == product_id]
    
    def get_reviews_by_user(self, user_id: int) -> List[Dict[str, Any]]:
        """Returns reviews by a specific user."""
        with self._lock:
            return [r for r in self._reviews.values() if r.get("user_id") == user_id]
    
    def create_review(self, review_data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new review."""
        with self._lock:
            self._review_counter += 1
            review_id = self._review_counter
            review = {
                "id": review_id,
                **review_data,
                "created_at": datetime.now().isoformat(),
                "helpful_count": 0
            }
            self._reviews[review_id] = review
        
        # Update product rating (outside lock)
        self.update_product_rating(review_data.get("product_id"))
        return review
    
    def increment_helpful(self, review_id: int) -> bool:
        """Increments a review's helpful count."""
        with self._lock:
            if review_id in self._reviews:
                self._reviews[review_id]["helpful_count"] += 1
                return True
            return False
    
    # ==================== USERS ====================
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Returns all users."""
        with self._lock:
            return list(self._users.values())
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Returns a single user by ID."""
        with self._lock:
            return self._users.get(user_id)
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new user."""
        with self._lock:
            self._user_counter += 1
            user_id = self._user_counter
            user = {
                "id": user_id,
                **user_data,
                "created_at": datetime.now().isoformat()
            }
            self._users[user_id] = user
            return user
    
    # ==================== SELLERS ====================
    
    def get_all_sellers(self) -> List[Dict[str, Any]]:
        """Returns all sellers."""
        with self._lock:
            return list(self._sellers.values())
    
    def get_seller(self, seller_id: int) -> Optional[Dict[str, Any]]:
        """Returns a single seller by ID."""
        with self._lock:
            return self._sellers.get(seller_id)
    
    def get_seller_by_api_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """Returns seller by API key."""
        with self._lock:
            seller_id = self._api_keys.get(api_key)
            if seller_id:
                return self._sellers.get(seller_id)
            return None
    
    def create_seller(self, seller_data: Dict[str, Any], api_key: str) -> Dict[str, Any]:
        """Creates a new seller."""
        with self._lock:
            self._seller_counter += 1
            seller_id = self._seller_counter
            seller = {
                "id": seller_id,
                **seller_data,
                "created_at": datetime.now().isoformat()
            }
            self._sellers[seller_id] = seller
            self._api_keys[api_key] = seller_id
            return seller
    
    def verify_api_key(self, api_key: str) -> bool:
        """Checks if the API key is valid."""
        with self._lock:
            return api_key in self._api_keys
    
    # ==================== CATEGORIES ====================
    
    def get_all_categories(self) -> List[Dict[str, Any]]:
        """Returns all categories."""
        with self._lock:
            return list(self._categories.values())
    
    def get_category(self, category_id: int) -> Optional[Dict[str, Any]]:
        """Returns a single category by ID."""
        with self._lock:
            return self._categories.get(category_id)
    
    def create_category(self, category_data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new category."""
        with self._lock:
            self._category_counter += 1
            category_id = self._category_counter
            category = {
                "id": category_id,
                **category_data
            }
            self._categories[category_id] = category
            return category
    
    def get_category_product_count(self, category_id: int) -> int:
        """Returns the number of products in a category."""
        with self._lock:
            return len([p for p in self._products.values() if p.get("category_id") == category_id])
    
    # ==================== UTILITY ====================
    
    def clear_all(self):
        """Clears all data (for testing)."""
        with self._lock:
            self._products.clear()
            self._reviews.clear()
            self._users.clear()
            self._sellers.clear()
            self._categories.clear()
            self._api_keys.clear()
            self._product_counter = 0
            self._review_counter = 0
            self._user_counter = 0
            self._seller_counter = 0
            self._category_counter = 0
    
    def get_stats(self) -> Dict[str, int]:
        """Returns database statistics."""
        with self._lock:
            return {
                "total_products": len(self._products),
                "total_reviews": len(self._reviews),
                "total_users": len(self._users),
                "total_sellers": len(self._sellers),
                "total_categories": len(self._categories)
            }


# Singleton instance
db = InMemoryDatabase()
