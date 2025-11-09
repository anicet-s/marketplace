#!/usr/bin/env python3
"""
Seed data script to populate the database with sample items.
This script creates sample furniture, cars, and houses with specifications and icons.

Usage:
    python migrations/seed_data.py
"""

import sys
import os

# Add parent directory to path to import application modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from application import db, application, Item


def clear_existing_items():
    """Remove all existing items from the database."""
    with application.app_context():
        try:
            print("Clearing existing items...")
            Item.query.delete()
            db.session.commit()
            print("Existing items cleared successfully!")
        except Exception as e:
            print(f"Failed to clear existing items: {e}")
            db.session.rollback()
            raise


def seed_furniture():
    """Create sample furniture items."""
    furniture_items = [
        {
            'name': 'Modern Leather Sofa',
            'description': 'Comfortable 3-seater leather sofa in excellent condition',
            'price': 899.99,
            'category': 'furniture',
            'icon_url': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc',
            'specifications': {
                'material': 'Genuine Leather',
                'dimensions': '84x36x32 inches',
                'condition': 'new'
            }
        },
        {
            'name': 'Oak Dining Table',
            'description': 'Solid oak dining table with 6 chairs',
            'price': 1299.50,
            'category': 'furniture',
            'icon_url': 'https://images.unsplash.com/photo-1617806118233-18e1de247200',
            'specifications': {
                'material': 'Solid Oak',
                'dimensions': '72x42x30 inches',
                'condition': 'used'
            }
        },
        {
            'name': 'Queen Size Bed Frame',
            'description': 'Elegant wooden bed frame with headboard',
            'price': 549.00,
            'category': 'furniture',
            'icon_url': None,  # Test placeholder
            'specifications': {
                'material': 'Pine Wood',
                'dimensions': '80x60x48 inches',
                'condition': 'refurbished'
            }
        },
        {
            'name': 'Office Desk with Drawers',
            'description': 'Spacious desk perfect for home office',
            'price': 349.99,
            'category': 'furniture',
            'icon_url': 'https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd',
            'specifications': {
                'material': 'Engineered Wood',
                'dimensions': '60x30x29 inches',
                'condition': 'new'
            }
        },
        {
            'name': 'Vintage Bookshelf',
            'description': '5-tier bookshelf with classic design',
            'price': 199.00,
            'category': 'furniture',
            'icon_url': None,  # Test placeholder
            'specifications': {
                'material': 'Reclaimed Wood',
                'dimensions': '36x12x72 inches',
                'condition': 'used'
            }
        }
    ]
    
    print(f"Creating {len(furniture_items)} furniture items...")
    for item_data in furniture_items:
        item = Item(**item_data)
        db.session.add(item)
    print("Furniture items created!")


def seed_cars():
    """Create sample car items."""
    car_items = [
        {
            'name': '2022 Toyota Camry',
            'description': 'Reliable sedan with excellent fuel economy',
            'price': 24999.00,
            'category': 'cars',
            'icon_url': 'https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb',
            'specifications': {
                'year': 2022,
                'make': 'Toyota',
                'model': 'Camry',
                'mileage': 15000,
                'condition': 'used'
            }
        },
        {
            'name': '2023 Honda Civic',
            'description': 'Sporty compact car with modern features',
            'price': 27500.00,
            'category': 'cars',
            'icon_url': 'https://images.unsplash.com/photo-1590362891991-f776e747a588',
            'specifications': {
                'year': 2023,
                'make': 'Honda',
                'model': 'Civic',
                'mileage': 8500,
                'condition': 'certified'
            }
        },
        {
            'name': '2021 Ford F-150',
            'description': 'Powerful pickup truck for work and play',
            'price': 35999.99,
            'category': 'cars',
            'icon_url': None,  # Test placeholder
            'specifications': {
                'year': 2021,
                'make': 'Ford',
                'model': 'F-150',
                'mileage': 32000,
                'condition': 'used'
            }
        },
        {
            'name': '2024 Tesla Model 3',
            'description': 'Electric sedan with autopilot features',
            'price': 42000.00,
            'category': 'cars',
            'icon_url': 'https://images.unsplash.com/photo-1560958089-b8a1929cea89',
            'specifications': {
                'year': 2024,
                'make': 'Tesla',
                'model': 'Model 3',
                'mileage': 2000,
                'condition': 'new'
            }
        },
        {
            'name': '2020 Jeep Wrangler',
            'description': 'Adventure-ready SUV with 4WD',
            'price': 31500.00,
            'category': 'cars',
            'icon_url': None,  # Test placeholder
            'specifications': {
                'year': 2020,
                'make': 'Jeep',
                'model': 'Wrangler',
                'mileage': 45000,
                'condition': 'used'
            }
        }
    ]
    
    print(f"Creating {len(car_items)} car items...")
    for item_data in car_items:
        item = Item(**item_data)
        db.session.add(item)
    print("Car items created!")


def seed_houses():
    """Create sample house items."""
    house_items = [
        {
            'name': 'Modern Downtown Condo',
            'description': 'Luxury condo in the heart of the city',
            'price': 450000.00,
            'category': 'houses',
            'icon_url': 'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00',
            'specifications': {
                'bedrooms': 2,
                'bathrooms': 2.0,
                'square_footage': 1200,
                'location': 'Seattle, WA'
            }
        },
        {
            'name': 'Suburban Family Home',
            'description': 'Spacious home with large backyard',
            'price': 625000.00,
            'category': 'houses',
            'icon_url': 'https://images.unsplash.com/photo-1568605114967-8130f3a36994',
            'specifications': {
                'bedrooms': 4,
                'bathrooms': 3.5,
                'square_footage': 2800,
                'location': 'Portland, OR'
            }
        },
        {
            'name': 'Cozy Starter Home',
            'description': 'Perfect first home with updated kitchen',
            'price': 285000.00,
            'category': 'houses',
            'icon_url': None,  # Test placeholder
            'specifications': {
                'bedrooms': 3,
                'bathrooms': 2.0,
                'square_footage': 1500,
                'location': 'Boise, ID'
            }
        },
        {
            'name': 'Luxury Estate',
            'description': 'Stunning estate with pool and guest house',
            'price': 1250000.00,
            'category': 'houses',
            'icon_url': 'https://images.unsplash.com/photo-1613490493576-7fde63acd811',
            'specifications': {
                'bedrooms': 5,
                'bathrooms': 4.5,
                'square_footage': 4500,
                'location': 'San Francisco, CA'
            }
        },
        {
            'name': 'Mountain Cabin Retreat',
            'description': 'Rustic cabin with mountain views',
            'price': 375000.00,
            'category': 'houses',
            'icon_url': None,  # Test placeholder
            'specifications': {
                'bedrooms': 2,
                'bathrooms': 1.5,
                'square_footage': 1100,
                'location': 'Aspen, CO'
            }
        },
        {
            'name': 'Beachfront Bungalow',
            'description': 'Charming beach house with ocean access',
            'price': 895000.00,
            'category': 'houses',
            'icon_url': 'https://images.unsplash.com/photo-1499793983690-e29da59ef1c2',
            'specifications': {
                'bedrooms': 3,
                'bathrooms': 2.5,
                'square_footage': 1800,
                'location': 'San Diego, CA'
            }
        }
    ]
    
    print(f"Creating {len(house_items)} house items...")
    for item_data in house_items:
        item = Item(**item_data)
        db.session.add(item)
    print("House items created!")


def seed_all():
    """Seed all categories of items."""
    with application.app_context():
        try:
            print("Starting database seeding...")
            
            # Seed each category
            seed_furniture()
            seed_cars()
            seed_houses()
            
            # Commit all changes
            db.session.commit()
            print("\nDatabase seeding completed successfully!")
            print("Summary:")
            print(f"  - Furniture items: {Item.query.filter_by(category='furniture').count()}")
            print(f"  - Car items: {Item.query.filter_by(category='cars').count()}")
            print(f"  - House items: {Item.query.filter_by(category='houses').count()}")
            print(f"  - Total items: {Item.query.count()}")
            
        except Exception as e:
            print(f"Seeding failed: {e}")
            db.session.rollback()
            raise


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "clear":
        clear_existing_items()
    else:
        seed_all()
