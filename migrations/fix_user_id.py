#!/usr/bin/env python3
"""
Migration to fix User ID column from BIGINT to VARCHAR.
This fixes the issue with Google IDs being too large for BIGINT.

Usage:
    python3 migrations/fix_user_id.py
"""

import sys
import os

# Add parent directory to path to import application modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from application import db, application
from sqlalchemy import text


def fix_user_id():
    """Change User ID from BIGINT to VARCHAR."""
    with application.app_context():
        try:
            print("========================================")
            print("Fixing User ID Column Type")
            print("========================================")
            print("")
            
            # Drop the user table and recreate it
            print("Dropping existing user table...")
            db.session.execute(text("DROP TABLE IF EXISTS \"user\" CASCADE"))
            
            print("Creating user table with VARCHAR ID...")
            db.session.execute(text("""
                CREATE TABLE "user" (
                    id VARCHAR(255) PRIMARY KEY,
                    email VARCHAR(100) UNIQUE,
                    name VARCHAR(100)
                )
            """))
            
            db.session.commit()
            
            print("")
            print("========================================")
            print("✓ User table fixed successfully!")
            print("========================================")
            print("")
            print("User ID is now VARCHAR(255) to support large Google IDs")
            print("")
            
        except Exception as e:
            print(f"Migration failed: {e}")
            db.session.rollback()
            raise


if __name__ == "__main__":
    fix_user_id()
