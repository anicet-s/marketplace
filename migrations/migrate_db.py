#!/usr/bin/env python3
"""
Database migration script to add icon_url and specifications columns to Item table.
This script can be run independently or imported as a module.

Usage:
    python migrations/migrate_db.py
"""

import sys
import os

# Add parent directory to path to import application modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from application import db, application
from sqlalchemy import text


def run_migration():
    """Execute the database migration to add new columns."""
    with application.app_context():
        try:
            print("Starting database migration...")
            
            # Add icon_url column
            print("Adding icon_url column...")
            db.session.execute(text(
                "ALTER TABLE item ADD COLUMN IF NOT EXISTS icon_url VARCHAR(500)"
            ))
            
            # Add specifications column (JSONB for PostgreSQL)
            print("Adding specifications column...")
            db.session.execute(text(
                "ALTER TABLE item ADD COLUMN IF NOT EXISTS specifications JSONB"
            ))
            
            # Create index on category column for better query performance
            print("Creating index on category column...")
            db.session.execute(text(
                "CREATE INDEX IF NOT EXISTS idx_item_category ON item(category)"
            ))
            
            # Commit the changes
            db.session.commit()
            print("Migration completed successfully!")
            
        except Exception as e:
            print(f"Migration failed: {e}")
            db.session.rollback()
            raise


def rollback_migration():
    """Rollback the migration (remove added columns)."""
    with application.app_context():
        try:
            print("Starting migration rollback...")
            
            # Drop columns
            print("Dropping icon_url column...")
            db.session.execute(text(
                "ALTER TABLE item DROP COLUMN IF EXISTS icon_url"
            ))
            
            print("Dropping specifications column...")
            db.session.execute(text(
                "ALTER TABLE item DROP COLUMN IF EXISTS specifications"
            ))
            
            print("Dropping category index...")
            db.session.execute(text(
                "DROP INDEX IF EXISTS idx_item_category"
            ))
            
            # Commit the changes
            db.session.commit()
            print("Rollback completed successfully!")
            
        except Exception as e:
            print(f"Rollback failed: {e}")
            db.session.rollback()
            raise


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "rollback":
        rollback_migration()
    else:
        run_migration()
