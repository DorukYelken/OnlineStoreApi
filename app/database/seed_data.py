"""
Mock Data (Seed Data)
=====================
Sample data loaded on application startup.

This module contains a rich mock dataset for development and testing:
- 5 Categories
- 5 Sellers
- 10 Users
- 25+ Products
- 50+ Reviews

All data is in English with USD pricing for a realistic e-commerce simulation.
"""

from ..database.memory_db import db


def seed_database():
    """
    Populates the database with mock data.
    Called on application startup.
    """
    
    # ==================== CATEGORIES ====================
    categories = [
        {
            "name": "Electronics",
            "description": "Phones, computers, tablets, headphones and other electronic devices",
            "icon": "📱",
            "image_url": "https://images.unsplash.com/photo-1498049794561-7780e7231661?w=400",
            "parent_id": None
        },
        {
            "name": "Fashion",
            "description": "Men's, women's and children's clothing, shoes, bags and accessories",
            "icon": "👔",
            "image_url": "https://images.unsplash.com/photo-1445205170230-053b83016050?w=400",
            "parent_id": None
        },
        {
            "name": "Home & Living",
            "description": "Furniture, decoration, kitchen supplies and home textiles",
            "icon": "🏠",
            "image_url": "https://images.unsplash.com/photo-1484101403633-562f891dc89a?w=400",
            "parent_id": None
        },
        {
            "name": "Sports & Outdoor",
            "description": "Sports equipment, outdoor clothing, fitness products and bicycles",
            "icon": "⚽",
            "image_url": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400",
            "parent_id": None
        },
        {
            "name": "Books & Hobbies",
            "description": "Books, e-books, musical instruments and hobby supplies",
            "icon": "📚",
            "image_url": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400",
            "parent_id": None
        }
    ]
    
    for cat in categories:
        db.create_category(cat)
    
    # ==================== SELLERS ====================
    sellers = [
        {
            "name": "TechStore",
            "description": "Your trusted technology store. Leading in electronics for 10 years.",
            "logo_url": "https://ui-avatars.com/api/?name=Tech+Store&background=0D8ABC&color=fff",
            "contact_email": "info@techstore.com",
            "contact_phone": "+1 555-0101",
            "is_verified": True,
            "product_count": 0,
            "average_rating": 4.7
        },
        {
            "name": "FashionHub",
            "description": "Online store offering the latest fashion trends at affordable prices.",
            "logo_url": "https://ui-avatars.com/api/?name=Fashion+Hub&background=E91E63&color=fff",
            "contact_email": "info@fashionhub.com",
            "contact_phone": "+1 555-0102",
            "is_verified": True,
            "product_count": 0,
            "average_rating": 4.5
        },
        {
            "name": "HomeDecor",
            "description": "Beautify your home! Decoration and furniture specialist.",
            "logo_url": "https://ui-avatars.com/api/?name=Home+Decor&background=4CAF50&color=fff",
            "contact_email": "info@homedecor.com",
            "contact_phone": "+1 555-0103",
            "is_verified": True,
            "product_count": 0,
            "average_rating": 4.3
        },
        {
            "name": "SportZone",
            "description": "Everything for sports enthusiasts! From fitness to outdoor equipment.",
            "logo_url": "https://ui-avatars.com/api/?name=Sport+Zone&background=FF5722&color=fff",
            "contact_email": "info@sportzone.com",
            "contact_phone": "+1 555-0104",
            "is_verified": True,
            "product_count": 0,
            "average_rating": 4.6
        },
        {
            "name": "BookWorld",
            "description": "Paradise for book lovers! Over 100,000 book varieties.",
            "logo_url": "https://ui-avatars.com/api/?name=Book+World&background=9C27B0&color=fff",
            "contact_email": "info@bookworld.com",
            "contact_phone": "+1 555-0105",
            "is_verified": True,
            "product_count": 0,
            "average_rating": 4.8
        }
    ]
    
    api_keys = [
        "seller_key_001",
        "seller_key_002",
        "seller_key_003",
        "seller_key_004",
        "seller_key_005"
    ]
    
    for seller, api_key in zip(sellers, api_keys):
        db.create_seller(seller, api_key)
    
    # ==================== USERS ====================
    users = [
        {"name": "John Smith", "email": "john@example.com", "avatar_url": "https://ui-avatars.com/api/?name=John+Smith"},
        {"name": "Emily Johnson", "email": "emily@example.com", "avatar_url": "https://ui-avatars.com/api/?name=Emily+Johnson"},
        {"name": "Michael Brown", "email": "michael@example.com", "avatar_url": "https://ui-avatars.com/api/?name=Michael+Brown"},
        {"name": "Sarah Davis", "email": "sarah@example.com", "avatar_url": "https://ui-avatars.com/api/?name=Sarah+Davis"},
        {"name": "David Wilson", "email": "david@example.com", "avatar_url": "https://ui-avatars.com/api/?name=David+Wilson"},
        {"name": "Jessica Martinez", "email": "jessica@example.com", "avatar_url": "https://ui-avatars.com/api/?name=Jessica+Martinez"},
        {"name": "Chris Anderson", "email": "chris@example.com", "avatar_url": "https://ui-avatars.com/api/?name=Chris+Anderson"},
        {"name": "Amanda Taylor", "email": "amanda@example.com", "avatar_url": "https://ui-avatars.com/api/?name=Amanda+Taylor"},
        {"name": "James Thomas", "email": "james@example.com", "avatar_url": "https://ui-avatars.com/api/?name=James+Thomas"},
        {"name": "Ashley Garcia", "email": "ashley@example.com", "avatar_url": "https://ui-avatars.com/api/?name=Ashley+Garcia"}
    ]
    
    for user in users:
        db.create_user(user)
    
    # ==================== PRODUCTS ====================
    products = [
        # Electronics - TechStore (seller_id: 1)
        {
            "name": "Apple iPhone 15 Pro 256GB",
            "description": "Apple's newest flagship phone. Unmatched performance with A17 Pro chip, professional photos with 48MP main camera, premium look with titanium design. USB-C port and Action Button innovations.",
            "category_id": 1,
            "seller_id": 1,
            "price": 1199.99,
            "discount_percentage": 8,
            "stock_status": "in_stock",
            "features": {
                "Display": "6.1 inch Super Retina XDR OLED",
                "Processor": "A17 Pro (3nm)",
                "RAM": "8GB",
                "Storage": "256GB",
                "Camera": "48MP + 12MP + 12MP",
                "Battery": "3274 mAh",
                "OS": "iOS 17",
                "Color": "Titanium Blue"
            },
            "images": [
                "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=400",
                "https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?w=400"
            ]
        },
        {
            "name": "Samsung Galaxy S24 Ultra 512GB",
            "description": "Samsung's most powerful phone. Snapdragon 8 Gen 3 processor, 200MP camera system, Galaxy AI features and built-in S Pen. Cinema experience with 6.8 inch Dynamic AMOLED display.",
            "category_id": 1,
            "seller_id": 1,
            "price": 1399.99,
            "discount_percentage": 12,
            "stock_status": "in_stock",
            "features": {
                "Display": "6.8 inch Dynamic AMOLED 2X",
                "Processor": "Snapdragon 8 Gen 3",
                "RAM": "12GB",
                "Storage": "512GB",
                "Camera": "200MP + 12MP + 50MP + 10MP",
                "Battery": "5000 mAh",
                "OS": "Android 14 / One UI 6.1",
                "Feature": "S Pen included"
            },
            "images": [
                "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=400"
            ]
        },
        {
            "name": "MacBook Pro 14\" M3 Pro",
            "description": "Professional performance with Apple M3 Pro chip. 14.2 inch Liquid Retina XDR display, 18 hours battery life. Ideal for software developers, video editors and professionals.",
            "category_id": 1,
            "seller_id": 1,
            "price": 1999.99,
            "discount_percentage": 5,
            "stock_status": "in_stock",
            "features": {
                "Display": "14.2 inch Liquid Retina XDR",
                "Processor": "Apple M3 Pro (11-core CPU)",
                "RAM": "18GB Unified Memory",
                "Storage": "512GB SSD",
                "GPU": "14-core GPU",
                "Battery": "17 hours video playback",
                "Ports": "3x Thunderbolt 4, HDMI, SD card",
                "Color": "Space Black"
            },
            "images": [
                "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400"
            ]
        },
        {
            "name": "Sony WH-1000XM5 Headphones",
            "description": "World's best noise cancelling headphones. 30 hours battery life, LDAC support, multi-device connection. Premium sound experience and maximum comfort.",
            "category_id": 1,
            "seller_id": 1,
            "price": 399.99,
            "discount_percentage": 15,
            "stock_status": "in_stock",
            "features": {
                "Type": "Over-ear wireless",
                "Noise Cancelling": "Active (Industry Leading)",
                "Battery Life": "30 hours",
                "Quick Charge": "3 minutes for 3 hours",
                "Codec": "LDAC, AAC, SBC",
                "Microphone": "8 pcs (Beam Forming)",
                "Weight": "250g",
                "Color": "Black"
            },
            "images": [
                "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=400"
            ]
        },
        {
            "name": "iPad Pro 12.9\" M2 256GB",
            "description": "The most powerful iPad. M2 chip, Liquid Retina XDR display, Apple Pencil hover support. Desktop-class performance for creative professionals.",
            "category_id": 1,
            "seller_id": 1,
            "price": 1099.99,
            "discount_percentage": 10,
            "stock_status": "low_stock",
            "features": {
                "Display": "12.9 inch Liquid Retina XDR",
                "Processor": "Apple M2",
                "RAM": "8GB",
                "Storage": "256GB",
                "Camera": "12MP + 10MP + LiDAR",
                "Connectivity": "WiFi 6E, 5G (optional)",
                "Face ID": "Yes",
                "Apple Pencil": "2nd generation compatible"
            },
            "images": [
                "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400"
            ]
        },
        {
            "name": "DJI Mini 4 Pro Drone",
            "description": "Professional drone under 249g. 4K/60fps video, 48MP photos, 34 minutes flight time. Obstacle sensing and ActiveTrack 360°.",
            "category_id": 1,
            "seller_id": 1,
            "price": 759.99,
            "discount_percentage": 0,
            "stock_status": "in_stock",
            "features": {
                "Weight": "249g",
                "Video": "4K/60fps HDR",
                "Photo": "48MP",
                "Flight Time": "34 minutes",
                "Range": "12 miles",
                "Obstacle Sensing": "Omnidirectional",
                "Smart Features": "ActiveTrack 360°, MasterShots"
            },
            "images": [
                "https://images.unsplash.com/photo-1473968512647-3e447244af8f?w=400"
            ]
        },
        
        # Fashion - FashionHub (seller_id: 2)
        {
            "name": "Men's Premium Leather Jacket",
            "description": "Genuine lamb leather, handcrafted Italian workmanship. Timeless design, lined interior, four pockets. Stylish look for every season.",
            "category_id": 2,
            "seller_id": 2,
            "price": 299.99,
            "discount_percentage": 20,
            "stock_status": "in_stock",
            "features": {
                "Material": "Genuine Lamb Leather",
                "Lining": "Polyester",
                "Collar": "Classic Collar",
                "Pockets": "4 pcs (2 interior, 2 exterior)",
                "Sizes": "S, M, L, XL, XXL",
                "Color": "Black",
                "Origin": "Italy"
            },
            "images": [
                "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400"
            ]
        },
        {
            "name": "Women's Classic Beige Trench Coat",
            "description": "British style classic trench coat. Water resistant fabric, double button detail, elegant silhouette with belt. Fall-spring favorite.",
            "category_id": 2,
            "seller_id": 2,
            "price": 179.99,
            "discount_percentage": 25,
            "stock_status": "in_stock",
            "features": {
                "Material": "Cotton-Polyester blend",
                "Water Resistant": "Yes",
                "Lining": "Polyester",
                "Belt": "Fabric belt included",
                "Sizes": "XS, S, M, L, XL",
                "Color": "Beige",
                "Length": "Above knee"
            },
            "images": [
                "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=400"
            ]
        },
        {
            "name": "Nike Air Max 270 Men's",
            "description": "Legendary Air Max comfort meets modern design. Maximum cushioning with 270 degree Air unit. Ideal for everyday use.",
            "category_id": 2,
            "seller_id": 2,
            "price": 149.99,
            "discount_percentage": 18,
            "stock_status": "in_stock",
            "features": {
                "Sole": "270 degree Air unit",
                "Upper": "Mesh and synthetic",
                "Closure": "Classic lace-up",
                "Sizes": "7-12",
                "Color": "Black/White",
                "Use": "Daily/Lifestyle"
            },
            "images": [
                "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400"
            ]
        },
        {
            "name": "Michael Kors Jet Set Bag",
            "description": "Timeless design, premium leather. Medium size, zippered main compartment, interior pockets. Stylish and practical everyday bag.",
            "category_id": 2,
            "seller_id": 2,
            "price": 298.99,
            "discount_percentage": 30,
            "stock_status": "low_stock",
            "features": {
                "Material": "Saffiano Leather",
                "Dimensions": "12.5x10x5 inches",
                "Closure": "Zippered",
                "Pockets": "1 zippered, 2 open interior",
                "Strap": "Adjustable shoulder strap",
                "Color": "Black",
                "Logo": "MK metal logo"
            },
            "images": [
                "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=400"
            ]
        },
        {
            "name": "Ray-Ban Aviator Sunglasses",
            "description": "Icon since 1937. Original Aviator design, glass lens, metal frame. Timeless model suitable for all face types.",
            "category_id": 2,
            "seller_id": 2,
            "price": 169.99,
            "discount_percentage": 15,
            "stock_status": "in_stock",
            "features": {
                "Lens": "G-15 glass (green)",
                "UV Protection": "UV400",
                "Frame": "Metal (gold tone)",
                "Bridge": "Double bridge",
                "Lens Width": "58mm",
                "Case": "Original case included",
                "Certificate": "Authenticity certificate"
            },
            "images": [
                "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400"
            ]
        },
        
        # Home & Living - HomeDecor (seller_id: 3)
        {
            "name": "IKEA KALLAX Bookshelf 4x4",
            "description": "Modular storage solution. 16 compartments, each 13x13 inches. Can be used with books, decoration or boxes.",
            "category_id": 3,
            "seller_id": 3,
            "price": 179.99,
            "discount_percentage": 10,
            "stock_status": "in_stock",
            "features": {
                "Dimensions": "58x58x15 inches",
                "Material": "Particleboard, foil coating",
                "Compartments": "16 pcs (13x13 inches)",
                "Max Load": "29 lbs per compartment",
                "Color": "White",
                "Assembly": "Assembly required",
                "Wall Mount": "Included"
            },
            "images": [
                "https://images.unsplash.com/photo-1594620302200-9a762244a156?w=400"
            ]
        },
        {
            "name": "Dyson V15 Detect Vacuum",
            "description": "See invisible dust with laser technology. Most powerful Dyson vacuum, LCD screen with particle count. Smart cleaning experience.",
            "category_id": 3,
            "seller_id": 3,
            "price": 749.99,
            "discount_percentage": 8,
            "stock_status": "in_stock",
            "features": {
                "Motor": "Dyson Hyperdymium (125,000 RPM)",
                "Suction Power": "230 AW",
                "Battery": "60 minutes (Eco mode)",
                "Bin": "0.2 gallon",
                "Laser": "Green laser dust detection",
                "Display": "LCD piezo sensor",
                "Attachments": "5 included",
                "Filtration": "HEPA"
            },
            "images": [
                "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=400"
            ]
        },
        {
            "name": "Philips Airfryer XXL",
            "description": "Oil-free frying technology. Family size 3 lb capacity, 7 preset programs, washable parts. Healthy and delicious meals.",
            "category_id": 3,
            "seller_id": 3,
            "price": 249.99,
            "discount_percentage": 22,
            "stock_status": "in_stock",
            "features": {
                "Capacity": "3 lbs (1.9 gallon)",
                "Power": "2225W",
                "Programs": "7 presets",
                "Technology": "Twin TurboStar",
                "Display": "Digital touchscreen",
                "Cleaning": "Dishwasher safe",
                "Accessories": "Grill tray included"
            },
            "images": [
                "https://images.unsplash.com/photo-1585515320310-259814833e62?w=400"
            ]
        },
        {
            "name": "Nespresso Vertuo Next Coffee Machine",
            "description": "Perfect crema with Centrifusion technology. 5 different cup sizes, one-touch operation. Premium experience for coffee lovers.",
            "category_id": 3,
            "seller_id": 3,
            "price": 179.99,
            "discount_percentage": 18,
            "stock_status": "in_stock",
            "features": {
                "Technology": "Centrifusion",
                "Pressure": "19 bar",
                "Water Tank": "1.1 liters",
                "Cup Sizes": "5 (Espresso - Carafe)",
                "Heat-up": "15 seconds",
                "Energy": "A++ energy saving mode",
                "Color": "Matte Black",
                "Capsules": "Vertuo capsules"
            },
            "images": [
                "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=400"
            ]
        },
        {
            "name": "Simmons Mattress Topper 60x80",
            "description": "Memory foam cushioned, orthopedic support. 7-zone ergonomic structure, breathable fabric. Ideal for healthy sleep.",
            "category_id": 3,
            "seller_id": 3,
            "price": 299.99,
            "discount_percentage": 35,
            "stock_status": "in_stock",
            "features": {
                "Size": "60x80 inches (Queen)",
                "Height": "3 inches",
                "Fill": "Memory foam",
                "Fabric": "Antibacterial, breathable",
                "Density": "3.1 lbs/ft³",
                "Zones": "7-zone ergonomic",
                "Warranty": "10 years"
            },
            "images": [
                "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=400"
            ]
        },
        
        # Sports & Outdoor - SportZone (seller_id: 4)
        {
            "name": "Garmin Fenix 7X Pro Solar",
            "description": "Ultimate outdoor smartwatch. Solar charging, AMOLED display, multi-band GPS. For mountaineering, running, swimming - every activity.",
            "category_id": 4,
            "seller_id": 4,
            "price": 899.99,
            "discount_percentage": 5,
            "stock_status": "in_stock",
            "features": {
                "Display": "1.4 inch AMOLED",
                "GPS": "Multi-band (L1 + L5)",
                "Battery": "37 days (with solar)",
                "Water Resistance": "10 ATM",
                "Maps": "TopoActive maps",
                "Music": "32GB storage",
                "Payment": "Garmin Pay",
                "Material": "Titanium bezel"
            },
            "images": [
                "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400"
            ]
        },
        {
            "name": "Decathlon Trekking Tent 3-Person",
            "description": "4-season trekking tent. 3000mm water column, dual cabin, easy setup. Reliable shelter for nature enthusiasts.",
            "category_id": 4,
            "seller_id": 4,
            "price": 199.99,
            "discount_percentage": 15,
            "stock_status": "in_stock",
            "features": {
                "Capacity": "3 person",
                "Weight": "9.2 lbs",
                "Water Column": "3000mm",
                "Poles": "Aluminum (7001 T6)",
                "Interior Height": "47 inches",
                "Setup": "Clip-on (5 minutes)",
                "Ventilation": "2 vents",
                "Season": "4 season"
            },
            "images": [
                "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=400"
            ]
        },
        {
            "name": "Kettler Exercise Bike",
            "description": "Professional home exercise bike. 32 resistance levels, heart rate monitor, tablet holder. Silent magnetic resistance system.",
            "category_id": 4,
            "seller_id": 4,
            "price": 599.99,
            "discount_percentage": 12,
            "stock_status": "in_stock",
            "features": {
                "Resistance": "32 levels (magnetic)",
                "Flywheel": "26 lbs",
                "Max User": "330 lbs",
                "Display": "LCD (calories, speed, distance)",
                "Heart Rate": "Hand sensor + chest strap compatible",
                "Programs": "12 preset programs",
                "Seat": "Horizontal/vertical adjustable",
                "Dimensions": "43x22x55 inches"
            },
            "images": [
                "https://images.unsplash.com/photo-1520877880798-5ee004e3f11e?w=400"
            ]
        },
        {
            "name": "Wilson Pro Staff Tennis Racket",
            "description": "Roger Federer's choice. 97 sq in head, 11.1oz weight, control-focused performance. For advanced players.",
            "category_id": 4,
            "seller_id": 4,
            "price": 269.99,
            "discount_percentage": 10,
            "stock_status": "low_stock",
            "features": {
                "Head": "97 sq inches",
                "Weight": "11.1oz (unstrung)",
                "Balance": "12.2 inches",
                "Stiffness": "62 RA",
                "Pattern": "16x19",
                "Beam": "21.5 mm",
                "Material": "Graphite + Kevlar",
                "Grip": "4 3/8"
            },
            "images": [
                "https://images.unsplash.com/photo-1617083934555-ac8c5f1d3d14?w=400"
            ]
        },
        {
            "name": "Adidas Predator Elite FG Cleats",
            "description": "Control-focused professional football boots. Controlskin upper, Facet Frame sole, AG/FG compatible. Dominate the field.",
            "category_id": 4,
            "seller_id": 4,
            "price": 299.99,
            "discount_percentage": 20,
            "stock_status": "in_stock",
            "features": {
                "Upper": "Controlskin (textured)",
                "Sole": "Facet Frame FG",
                "Closure": "Asymmetric lacing",
                "Collar": "Laceless collar",
                "Ground": "Firm Ground (grass)",
                "Sizes": "6-12",
                "Color": "Core Black / Solar Red",
                "Weight": "7.4oz (size 9)"
            },
            "images": [
                "https://images.unsplash.com/photo-1511886929837-354d827aae26?w=400"
            ]
        },
        
        # Books & Hobbies - BookWorld (seller_id: 5)
        {
            "name": "Kindle Paperwhite 11th Gen",
            "description": "6.8 inch display, adjustable warm light, waterproof. 10 weeks battery life, eye-friendly e-ink technology. Perfect for book lovers.",
            "category_id": 5,
            "seller_id": 5,
            "price": 149.99,
            "discount_percentage": 10,
            "stock_status": "in_stock",
            "features": {
                "Display": "6.8 inch E-ink Paperwhite",
                "Resolution": "300 ppi",
                "Storage": "16GB",
                "Lighting": "17 LED + warm light",
                "Water Resistance": "IPX8 (6.5ft, 60 min)",
                "Battery": "10 weeks",
                "Connectivity": "WiFi + Bluetooth",
                "Weight": "7.2oz"
            },
            "images": [
                "https://images.unsplash.com/photo-1592496001020-d31bd830651f?w=400"
            ]
        },
        {
            "name": "Atomic Habits - James Clear",
            "description": "New York Times bestseller. Discover how small habits create big results. The most read personal development book.",
            "category_id": 5,
            "seller_id": 5,
            "price": 18.99,
            "discount_percentage": 25,
            "stock_status": "in_stock",
            "features": {
                "Author": "James Clear",
                "Publisher": "Penguin Random House",
                "Pages": "320",
                "Language": "English",
                "Cover": "Paperback",
                "ISBN": "978-0735211292",
                "Edition": "1st Edition 2018",
                "Category": "Personal Development"
            },
            "images": [
                "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400"
            ]
        },
        {
            "name": "Yamaha PSR-E473 Keyboard",
            "description": "61-key professional keyboard. 820 voices, 290 rhythms, USB-MIDI connection. Ideal learning companion for beginners and intermediate players.",
            "category_id": 5,
            "seller_id": 5,
            "price": 349.99,
            "discount_percentage": 8,
            "stock_status": "in_stock",
            "features": {
                "Keys": "61 keys (touch sensitive)",
                "Voices": "820 Voice + Super Articulation",
                "Rhythms": "290 Styles",
                "Polyphony": "64 notes",
                "Effects": "DSP + Reverb + Chorus",
                "Recording": "USB Audio",
                "Connectivity": "USB-MIDI, Aux, Headphone",
                "Power": "Adapter / 6xAA batteries"
            },
            "images": [
                "https://images.unsplash.com/photo-1520523839897-bd0b52f945a0?w=400"
            ]
        },
        {
            "name": "LEGO Technic Ferrari 488 GTE",
            "description": "1:8 scale Ferrari model. 3841 pieces, working V8 engine, drivetrain. Premium set for collectors.",
            "category_id": 5,
            "seller_id": 5,
            "price": 449.99,
            "discount_percentage": 0,
            "stock_status": "low_stock",
            "features": {
                "Pieces": "3841 pcs",
                "Scale": "1:8",
                "Size": "20x8x5 inches",
                "Age": "18+",
                "Features": "Working engine, steering",
                "License": "Official Ferrari license",
                "Box": "Premium box + booklet",
                "Series": "Technic Ultimate"
            },
            "images": [
                "https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400"
            ]
        },
        {
            "name": "Winsor & Newton Professional Watercolor Set",
            "description": "24-color professional quality watercolors. High pigment density, excellent flow. For artists and hobbyists.",
            "category_id": 5,
            "seller_id": 5,
            "price": 89.99,
            "discount_percentage": 15,
            "stock_status": "in_stock",
            "features": {
                "Colors": "24 half pans",
                "Quality": "Professional grade",
                "Pigment": "High density",
                "Lightfastness": "Very Good - Excellent",
                "Case": "Metal case + mixing palette",
                "Brush": "Series 7 travel brush included",
                "Origin": "England",
                "Certification": "ASTM D-4236"
            },
            "images": [
                "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=400"
            ]
        }
    ]
    
    for product in products:
        db.create_product(product)
    
    # ==================== REVIEWS ====================
    reviews = [
        # iPhone reviews (product_id: 1)
        {"product_id": 1, "user_id": 1, "rating": 5, "title": "Amazing phone!", "comment": "A17 Pro processor is incredibly fast. Camera quality is professional level. Been using it for 2 months, battery life is also great.", "pros": ["Camera quality", "Processor performance", "Titanium design"], "cons": ["Price is very high"]},
        {"product_id": 1, "user_id": 2, "rating": 5, "title": "Worth every penny", "comment": "Upgraded from iPhone 12, night and day difference. USB-C switch makes so much sense. Love the Action button.", "pros": ["USB-C", "Action Button", "Display quality"], "cons": ["Charger not included"]},
        {"product_id": 1, "user_id": 3, "rating": 4, "title": "Very good but not perfect", "comment": "Overall satisfied but expected a bit more innovation at this price. Dynamic Island is nice but could be more.", "pros": ["Fast performance", "iOS ecosystem"], "cons": ["Lacks innovation", "Expensive"]},
        {"product_id": 1, "user_id": 4, "rating": 5, "title": "Best iPhone ever!", "comment": "Been using iPhones for years, this is the best. Photography with ProRAW is amazing. Cinematic mode in videos is stunning.", "pros": ["ProRAW", "Cinematic Mode", "Build quality"], "cons": ["A bit heavy"]},
        
        # Samsung S24 reviews (product_id: 2)
        {"product_id": 2, "user_id": 5, "rating": 5, "title": "Galaxy AI is incredible!", "comment": "AI features are really useful. Circle to Search is so practical. 200MP camera is a detail monster.", "pros": ["Galaxy AI", "Camera", "S Pen"], "cons": ["Price"]},
        {"product_id": 2, "user_id": 6, "rating": 4, "title": "Very powerful but...", "comment": "Performance is amazing, display is perfect. But there's some heating issue during heavy use. Love the S Pen.", "pros": ["Display", "Performance", "S Pen"], "cons": ["Heating", "Heavy"]},
        {"product_id": 2, "user_id": 7, "rating": 5, "title": "Best Android phone", "comment": "Been using Samsung since the Note series. This phone offers the best of everything. 100x zoom is surprising.", "pros": ["Zoom camera", "Large display", "Battery"], "cons": ["One-handed use difficult"]},
        
        # MacBook Pro reviews (product_id: 3)
        {"product_id": 3, "user_id": 8, "rating": 5, "title": "Perfect for developers", "comment": "With M3 Pro, Docker, multiple IDEs, simulators - can keep them all running. Fan noise is almost none.", "pros": ["Performance", "Silent operation", "Battery life"], "cons": ["Limited ports"]},
        {"product_id": 3, "user_id": 9, "rating": 5, "title": "Great for video editing", "comment": "4K video editing is butter smooth. No proxy needed in DaVinci Resolve. Display color accuracy is superb.", "pros": ["Video performance", "Display quality", "Build quality"], "cons": ["No RAM upgrade"]},
        {"product_id": 3, "user_id": 10, "rating": 4, "title": "Amazing but expensive", "comment": "Yes it's a great machine but the price is really high. Still, it pays for itself for professional work.", "pros": ["Productivity", "macOS", "Trackpad"], "cons": ["Price", "Not suitable for gaming"]},
        
        # Sony Headphones reviews (product_id: 4)
        {"product_id": 4, "user_id": 1, "rating": 5, "title": "Noise cancelling is amazing!", "comment": "Office, subway, airplane... Perfect silence everywhere. Sound quality is top notch. 30 hours battery is really true.", "pros": ["ANC", "Sound quality", "Battery life"], "cons": ["Ears get warm in summer"]},
        {"product_id": 4, "user_id": 2, "rating": 5, "title": "Upgraded from XM4", "comment": "XM4 was good but XM5's ANC is much better. Multipoint now works flawlessly. Miss the folding design though.", "pros": ["ANC improvement", "Multipoint", "Comfort"], "cons": ["Doesn't fold", "Large case"]},
        {"product_id": 4, "user_id": 3, "rating": 4, "title": "Great but the price...", "comment": "No complaints about sound quality and ANC. But at this price, expected a more premium box and accessories.", "pros": ["Sound", "ANC", "Comfort"], "cons": ["Price", "Limited accessories"]},
        
        # iPad Pro reviews (product_id: 5)
        {"product_id": 5, "user_id": 4, "rating": 5, "title": "Perfect for digital drawing", "comment": "Procreate + Apple Pencil 2 combo is unmatched. M2 chip handles heaviest brushes without lag. Hover feature is super.", "pros": ["Apple Pencil hover", "Performance", "Display"], "cons": ["iPadOS limitations"]},
        {"product_id": 5, "user_id": 5, "rating": 4, "title": "Great hardware, lacking software", "comment": "Hardware-wise it surpasses laptops but iPadOS still doesn't allow full productive use. Stage Manager needs improvement.", "pros": ["Hardware", "Display", "Face ID"], "cons": ["iPadOS limits", "Magic Keyboard expensive"]},
        
        # DJI Drone reviews (product_id: 6)
        {"product_id": 6, "user_id": 6, "rating": 5, "title": "Miracle under 249g!", "comment": "Didn't expect this image quality from such a small and light drone. ActiveTrack tracking works perfectly.", "pros": ["249g (no registration needed)", "4K quality", "Obstacle sensing"], "cons": ["Struggles a bit in wind"]},
        {"product_id": 6, "user_id": 7, "rating": 5, "title": "Perfect vacation drone", "comment": "So easy to carry while traveling. Despite being Mini, it has pro features. Fly More Combo is definitely worth it.", "pros": ["Portability", "Flight time", "Quality"], "cons": ["Single battery isn't enough"]},
        
        # Leather Jacket reviews (product_id: 7)
        {"product_id": 7, "user_id": 8, "rating": 5, "title": "Quality is evident", "comment": "Real leather smell, stitching is perfect. Italian craftsmanship really makes a difference. Using for 3 years, still like new.", "pros": ["Leather quality", "Craftsmanship", "Durability"], "cons": ["Price is high but worth it"]},
        {"product_id": 7, "user_id": 9, "rating": 4, "title": "Very stylish", "comment": "Exactly what I expected. Just a bit stiff initially, softens up after a few wears.", "pros": ["Design", "Quality", "Keeps warm"], "cons": ["Stiff at first"]},
        
        # Trench Coat reviews (product_id: 8)
        {"product_id": 8, "user_id": 10, "rating": 5, "title": "Classic and elegant", "comment": "Goes with every outfit. Doesn't let water through in rain. Fit is perfect, looks stylish with belt.", "pros": ["Water resistant", "Fit", "Color"], "cons": ["Pockets a bit small"]},
        {"product_id": 8, "user_id": 1, "rating": 5, "title": "My fall favorite", "comment": "Been wearing it every fall/spring for 2 years. Still like new. Easy to clean too.", "pros": ["Durability", "Elegance", "Easy care"], "cons": ["Not enough for winter"]},
        
        # Nike Air Max reviews (product_id: 9)
        {"product_id": 9, "user_id": 2, "rating": 5, "title": "So comfortable!", "comment": "Most comfortable Air Max ever. Stand all day, no fatigue. 270 air unit makes the difference.", "pros": ["Comfort", "Design", "Lightweight"], "cons": ["Hard to clean when dirty"]},
        {"product_id": 9, "user_id": 3, "rating": 4, "title": "Nice but narrow fit", "comment": "Very stylish shoe but recommend going half size up. Runs a bit narrow.", "pros": ["Look", "Comfort"], "cons": ["Narrow fit"]},
        
        # MK Bag reviews (product_id: 10)
        {"product_id": 10, "user_id": 4, "rating": 5, "title": "Stylish and practical", "comment": "Perfect size for everyday use. Leather quality is excellent, scratch-resistant Saffiano leather.", "pros": ["Leather quality", "Size", "Pocket layout"], "cons": ["Strap a bit thin"]},
        {"product_id": 10, "user_id": 5, "rating": 4, "title": "Great gift", "comment": "Got it for my wife, she loves it. Even the box is very elegant. Just wish it had a locked pocket.", "pros": ["Elegance", "Packaging", "Quality"], "cons": ["No locked pocket"]},
        
        # Ray-Ban reviews (product_id: 11)
        {"product_id": 11, "user_id": 6, "rating": 5, "title": "Classic model", "comment": "Aviator is always stylish. G-15 glass lens really makes a difference, incomparable to plastic lenses.", "pros": ["Glass lens", "Timeless design", "UV protection"], "cons": ["Can break if dropped"]},
        {"product_id": 11, "user_id": 7, "rating": 5, "title": "Nothing beats the original", "comment": "Used replicas before, original is completely different. Vision clarity, color accuracy is perfect.", "pros": ["Original quality", "Vision clarity"], "cons": ["Price"]},
        
        # IKEA Bookshelf reviews (product_id: 12)
        {"product_id": 12, "user_id": 8, "rating": 4, "title": "Assembly is a bit tedious", "comment": "Assembled alone in 2 hours. Result is nice but need to be careful during assembly. Wall mounting is essential.", "pros": ["Design", "Modularity", "Value for money"], "cons": ["Assembly difficulty"]},
        {"product_id": 12, "user_id": 9, "rating": 5, "title": "Exactly what I wanted", "comment": "Simple design fits any room. Turns into a storage monster with boxes inside. Bought 3 for different rooms.", "pros": ["Versatile use", "Design", "Price"], "cons": ["Heavy"]},
        
        # Dyson Vacuum reviews (product_id: 13)
        {"product_id": 13, "user_id": 10, "rating": 5, "title": "Laser technology is surprising", "comment": "Shocked when I turned on the laser in the dark and saw how much dust there was. LCD particle count is really motivating.", "pros": ["Laser", "Suction power", "Filtration"], "cons": ["Price is very high"]},
        {"product_id": 13, "user_id": 1, "rating": 5, "title": "Home cleaning is now fun", "comment": "Yes it's expensive but completely changed home cleaning. Perfect on carpet, hardwood, everywhere. HEPA filter great for my allergies.", "pros": ["Cleaning quality", "Ease of use", "Allergy friendly"], "cons": ["High price"]},
        
        # Airfryer reviews (product_id: 14)
        {"product_id": 14, "user_id": 2, "rating": 5, "title": "French fries never been this good", "comment": "Oil-free frying really works. Crispy outside, soft inside. Cleaning is so easy, everything goes in dishwasher.", "pros": ["Taste", "Healthy", "Easy cleaning"], "cons": ["Takes up space"]},
        {"product_id": 14, "user_id": 3, "rating": 4, "title": "Ideal for family", "comment": "XXL size is really big, enough for family of 4. Preset programs very useful. Just a bit noisy.", "pros": ["Large capacity", "Presets", "Results"], "cons": ["Noise"]},
        
        # Nespresso reviews (product_id: 15)
        {"product_id": 15, "user_id": 4, "rating": 5, "title": "Mornings are now better", "comment": "Perfect coffee with one touch. Crema thickness even better than Starbucks. Centrifusion technology really makes a difference.", "pros": ["Coffee quality", "Ease of use", "Crema"], "cons": ["Capsule cost"]},
        {"product_id": 15, "user_id": 5, "rating": 4, "title": "Fast and practical", "comment": "Heats up in 15 seconds, coffee ready in 1 minute. Perfect for morning rush. Vertuo capsules a bit pricier than Original.", "pros": ["Speed", "Convenience", "Design"], "cons": ["Capsule prices"]},
        
        # Garmin Fenix reviews (product_id: 17)
        {"product_id": 17, "user_id": 6, "rating": 5, "title": "King of outdoor", "comment": "Got it for mountaineering, maps are excellent. GPS accuracy is very high. No battery worries thanks to solar charging.", "pros": ["GPS accuracy", "Maps", "Solar charging", "Durability"], "cons": ["Can be considered heavy"]},
        {"product_id": 17, "user_id": 7, "rating": 5, "title": "Perfect for running", "comment": "Running dynamics, training status, recovery time... Every metric available. Charging every 2 weeks is enough.", "pros": ["Metrics", "Battery life", "Display"], "cons": ["Price is very high"]},
        
        # Tent reviews (product_id: 18)
        {"product_id": 18, "user_id": 8, "rating": 4, "title": "Very good for the price", "comment": "Used for 3 nights, didn't leak even in heavy rain. Easy to set up, 2 people can do it in 5 minutes.", "pros": ["Waterproof", "Easy setup", "Price"], "cons": ["Interior space a bit tight"]},
        {"product_id": 18, "user_id": 9, "rating": 5, "title": "Ideal for trekking", "comment": "9.2 lbs weight barely noticeable in backpack. Being 4-season usable is a big plus.", "pros": ["Weight", "4 season", "Durability"], "cons": ["Small vestibule"]},
        
        # Exercise Bike reviews (product_id: 19)
        {"product_id": 19, "user_id": 10, "rating": 5, "title": "Home gym experience", "comment": "Magnetic resistance system is very quiet, can use even at night. 32 levels suitable for every level.", "pros": ["Silent", "Resistance levels", "Sturdiness"], "cons": ["Heavy, hard to move"]},
        {"product_id": 19, "user_id": 1, "rating": 4, "title": "Gets the job done", "comment": "Got this instead of gym membership, paid for itself in 3 months. Heart rate monitor sometimes skips but no problem with chest strap.", "pros": ["Economic", "Quality build", "Programs"], "cons": ["Hand sensor not sensitive"]},
        
        # Kindle reviews (product_id: 22)
        {"product_id": 22, "user_id": 2, "rating": 5, "title": "Must-have for bookworms", "comment": "10 weeks battery is real. Reading on beach in sunlight is amazing, screen doesn't reflect at all. Warm light comfortable at night.", "pros": ["Battery life", "Sunlight readability", "Warm light"], "cons": ["Reading PDFs not comfortable"]},
        {"product_id": 22, "user_id": 3, "rating": 5, "title": "Reading habit increased", "comment": "Instead of carrying physical books, entire library in my pocket. Being waterproof is amazing for reading by the pool.", "pros": ["Lightweight", "Waterproof", "Book capacity"], "cons": ["No color content"]},
        
        # Atomic Habits reviews (product_id: 23)
        {"product_id": 23, "user_id": 4, "rating": 5, "title": "Changed my life", "comment": "Read it 3 times in 2 years. Learn something new every time. Habit tracking system really works.", "pros": ["Practical advice", "Science-based", "Easy to apply"], "cons": ["Some parts repetitive"]},
        {"product_id": 23, "user_id": 5, "rating": 5, "title": "Everyone should read", "comment": "Most concrete and applicable personal development book. Still applying the 1% rule.", "pros": ["Concrete examples", "Easy to read", "Motivating"], "cons": ["Some sections contain repetition"]},
        
        # Yamaha Keyboard reviews (product_id: 24)
        {"product_id": 24, "user_id": 6, "rating": 5, "title": "Perfect for students", "comment": "Got it for my son, 820 sounds offer so many options. Touch sensitive keys give real piano feel.", "pros": ["Sound variety", "Touch sensitive", "USB connection"], "cons": ["Stand not included"]},
        {"product_id": 24, "user_id": 7, "rating": 4, "title": "Ideal for beginners", "comment": "Started piano lessons, teacher recommended this model. Sound quality good for the price. Speakers are sufficient.", "pros": ["Value for money", "Sound quality", "Learning functions"], "cons": ["Not 88 keys"]},
        
        # LEGO Ferrari reviews (product_id: 25)
        {"product_id": 25, "user_id": 8, "rating": 5, "title": "Engineering marvel", "comment": "3841 pieces, took 12 hours but every minute was enjoyable. V8 engine actually works, steering turns. Display piece.", "pros": ["Details", "Working mechanics", "Build quality"], "cons": ["Price is very high"]},
        {"product_id": 25, "user_id": 9, "rating": 5, "title": "Pride of my collection", "comment": "Have a LEGO Technic collection, this is by far the best. Real Ferrari license, every detail thought through.", "pros": ["Licensed product", "Large size", "Detailed content"], "cons": ["Needs shelf space"]},
        
        # Watercolor Set reviews (product_id: 26)
        {"product_id": 26, "user_id": 10, "rating": 5, "title": "Professional quality", "comment": "Switched from student grade paints, difference is incredible. Pigment density, mixing ease is top level.", "pros": ["Pigment quality", "Color vibrancy", "Mixing"], "cons": ["Brush quality average"]},
        {"product_id": 26, "user_id": 1, "rating": 5, "title": "Winsor & Newton quality", "comment": "Been using this brand for years. Buying as a set is economical. Metal case very useful for travel.", "pros": ["Brand quality", "Set contents", "Metal case"], "cons": ["Half pans small, run out quickly"]}
    ]
    
    for review in reviews:
        db.create_review(review)
    
    print(f"✅ Seed data loaded: {db.get_stats()}")


def reset_and_seed():
    """Resets the database and seeds again."""
    db.clear_all()
    seed_database()
