#!/usr/bin/env python3
"""
Script to verify the category index exists and test query performance.
"""

import sys
import os
import time

# Add parent directory to path to import application modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from application import db, application, Item
from sqlalchemy import text


def verify_index_exists():
    """Check if the category index exists in the database."""
    with application.app_context():
        try:
            print("Checking for idx_item_category index...")
            
            # Query PostgreSQL system catalog to check for index
            result = db.session.execute(text("""
                SELECT indexname, indexdef 
                FROM pg_indexes 
                WHERE tablename = 'item' 
                AND indexname = 'idx_item_category'
            """))
            
            index_info = result.fetchone()
            
            if index_info:
                print(f"✓ Index found: {index_info[0]}")
                print(f"  Definition: {index_info[1]}")
                return True
            else:
                print("✗ Index not found")
                return False
                
        except Exception as e:
            print(f"Error checking index: {e}")
            return False


def test_query_performance():
    """Test query performance with the indexed category column."""
    with application.app_context():
        try:
            print("\nTesting query performance...")
            
            # Get total item count
            total_items = Item.query.count()
            print(f"Total items in database: {total_items}")
            
            if total_items == 0:
                print("No items in database to test. Run seed_data.py first.")
                return
            
            # Test queries for each category
            categories = ['furniture', 'cars', 'houses']
            
            for category in categories:
                # Warm up query
                Item.query.filter_by(category=category).first()
                
                # Time the query
                start_time = time.time()
                items = Item.query.filter_by(category=category).all()
                end_time = time.time()
                
                query_time = (end_time - start_time) * 1000  # Convert to milliseconds
                
                print(f"\nCategory: {category}")
                print(f"  Items found: {len(items)}")
                print(f"  Query time: {query_time:.2f}ms")
            
            # Show query execution plan
            print("\n" + "="*60)
            print("Query Execution Plan (EXPLAIN):")
            print("="*60)
            
            result = db.session.execute(text("""
                EXPLAIN (ANALYZE, BUFFERS) 
                SELECT * FROM item WHERE category = 'furniture'
            """))
            
            for row in result:
                print(row[0])
                
        except Exception as e:
            print(f"Error testing query performance: {e}")


if __name__ == "__main__":
    print("Database Index Verification and Performance Test")
    print("="*60)
    
    # Verify index exists
    index_exists = verify_index_exists()
    
    if index_exists:
        # Test query performance
        test_query_performance()
        print("\n" + "="*60)
        print("✓ Index verification and performance test completed!")
    else:
        print("\n" + "="*60)
        print("✗ Index not found. Run migrate_db.py to create the index.")
        sys.exit(1)
