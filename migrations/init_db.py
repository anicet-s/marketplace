#!/usr/bin/env python3
"""
Database initialization script to create all tables from SQLAlchemy models.
This should be run BEFORE migrate_db.py on a fresh database.

Usage:
    python3 migrations/init_db.py
"""

import sys
import os

# Add parent directory to path to import application modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from application import db, application, User, Item


def init_database():
    """Initialize the database by creating all tables."""
    with application.app_context():
        try:
            print("========================================")
            print("Database Initialization")
            print("========================================")
            print("")
            
            # Create all tables defined in the models
            print("Creating database tables...")
            db.create_all()
            
            print("✓ User table created")
            print("✓ Item table created")
            
            print("")
            print("========================================")
            print("Database initialized successfully!")
            print("========================================")
            print("")
            print("Next steps:")
            print("  1. Run migrations: python3 migrations/migrate_db.py")
            print("  2. Seed data (optional): python3 migrations/seed_data.py")
            print("")
            
        except Exception as e:
            print(f"Database initialization failed: {e}")
            raise


def drop_all_tables():
    """Drop all tables (use with caution!)."""
    with application.app_context():
        try:
            print("WARNING: Dropping all tables...")
            response = input("Are you sure? This will delete all data! (yes/no): ")
            
            if response.lower() == 'yes':
                db.drop_all()
                print("All tables dropped successfully!")
            else:
                print("Operation cancelled.")
                
        except Exception as e:
            print(f"Failed to drop tables: {e}")
            raise


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "drop":
        drop_all_tables()
    else:
        init_database()
