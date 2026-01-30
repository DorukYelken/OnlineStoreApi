"""
Mock Online Store API
=====================
Main FastAPI application file.

This file:
- Creates the FastAPI application
- Registers routers
- Customizes Swagger UI
- Loads seed data on startup
- Configures CORS settings

Run:
    uvicorn app.main:app --reload --port 8000

Swagger UI:
    http://localhost:8000/docs

ReDoc:
    http://localhost:8000/redoc
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from .config import (
    API_TITLE,
    API_DESCRIPTION,
    API_VERSION,
    TAGS_METADATA
)
from .routers import (
    products_router,
    reviews_router,
    recommendations_router,
    categories_router
)
from .database.seed_data import seed_database
from .database import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifecycle manager.
    
    Loads seed data on startup.
    Cleanup operations can be performed on shutdown.
    """
    # Startup
    print("🚀 Starting Mock Online Store API...")
    seed_database()
    print("✅ Application ready!")
    
    yield
    
    # Shutdown
    print("👋 Shutting down application...")


# Create FastAPI application
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    openapi_tags=TAGS_METADATA,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": 0,
        "docExpansion": "list",
        "filter": True,
        "showExtensions": True,
        "showCommonExtensions": True,
        "syntaxHighlight.theme": "monokai"
    }
)

# CORS settings - For frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specify specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(products_router)
app.include_router(reviews_router)
app.include_router(recommendations_router)
app.include_router(categories_router)


# ==================== GENERAL ENDPOINTS ====================

@app.get(
    "/",
    tags=["General"],
    summary="API Status",
    description="""
## API Status

Checks if the API is running.

### Response

```json
{
    "status": "online",
    "message": "Mock Online Store API is running!",
    "version": "1.0.0",
    "docs": "/docs"
}
```
"""
)
async def root():
    """API status check"""
    return {
        "status": "online",
        "message": "Mock Online Store API is running!",
        "version": API_VERSION,
        "docs": "/docs"
    }


@app.get(
    "/health",
    tags=["General"],
    summary="Health Check",
    description="""
## Health Check

Returns the API health status and database statistics.

### Response

```json
{
    "status": "healthy",
    "database": {
        "total_products": 25,
        "total_reviews": 52,
        "total_users": 10,
        "total_sellers": 5,
        "total_categories": 5
    }
}
```
"""
)
async def health_check():
    """Health check and database statistics"""
    return {
        "status": "healthy",
        "database": db.get_stats()
    }


@app.get(
    "/api-keys",
    tags=["General"],
    summary="Test API Keys",
    description="""
## Test API Keys

List of API keys available for development and testing.

**IMPORTANT:** This endpoint is only active in development environment.
Should be disabled in production.

### Usage

Add to header:
```
X-API-Key: seller_key_001
```
"""
)
async def get_api_keys():
    """List of API keys available for testing"""
    return {
        "info": "You can use these API keys for testing.",
        "header_name": "X-API-Key",
        "keys": [
            {"key": "seller_key_001", "seller": "TechStore", "description": "Electronics seller"},
            {"key": "seller_key_002", "seller": "FashionHub", "description": "Fashion products seller"},
            {"key": "seller_key_003", "seller": "HomeDecor", "description": "Home & Living products seller"},
            {"key": "seller_key_004", "seller": "SportZone", "description": "Sports products seller"},
            {"key": "seller_key_005", "seller": "BookWorld", "description": "Books & Hobbies seller"}
        ],
        "example_usage": {
            "curl": 'curl -X POST "http://localhost:8000/products" -H "X-API-Key: seller_key_001" -H "Content-Type: application/json" -d \'{"name": "Test", "description": "Test product", "category_id": 1, "price": 100}\'',
            "python": """
import requests

headers = {"X-API-Key": "seller_key_001"}
data = {"name": "Test", "description": "Test product", "category_id": 1, "price": 100}
response = requests.post("http://localhost:8000/products", headers=headers, json=data)
"""
        }
    }


# Frontend static files
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")
    
    @app.get("/app", include_in_schema=False)
    async def serve_frontend():
        """Serve the frontend application"""
        return FileResponse(os.path.join(frontend_path, "index.html"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
