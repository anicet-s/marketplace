# Database Index Documentation

## Overview

This document describes the database index created for the Item table's category column to optimize query performance for category-based filtering.

## Index Details

**Index Name:** `idx_item_category`

**Table:** `item`

**Column:** `category`

**Type:** B-tree index (PostgreSQL default)

## Purpose

The index was created to improve query performance for the following operations:

1. **Furniture listings:** `SELECT * FROM item WHERE category = 'furniture'`
2. **Car listings:** `SELECT * FROM item WHERE category = 'cars'`
3. **House listings:** `SELECT * FROM item WHERE category = 'houses'`

These queries are executed frequently in the marketplace application on the following routes:
- `/furniture` - Displays all furniture items
- `/cars` - Displays all car items
- `/houses` - Displays all house items

## Implementation

The index was created as part of the database migration in the following files:

1. **migrations/add_icon_and_specifications.sql**
   ```sql
   CREATE INDEX IF NOT EXISTS idx_item_category ON item(category);
   ```

2. **migrations/migrate_db.py**
   ```python
   db.session.execute(text(
       "CREATE INDEX IF NOT EXISTS idx_item_category ON item(category)"
   ))
   ```

## Performance Benefits

### Without Index
- **Query Type:** Sequential Scan
- **Performance:** O(n) - scans all rows in the table
- **Impact:** Slower as table grows

### With Index
- **Query Type:** Index Scan
- **Performance:** O(log n) - uses B-tree index for fast lookups
- **Impact:** Consistent fast performance even as table grows

### Expected Improvements

For a table with 10,000 items distributed across 3 categories:

| Operation | Without Index | With Index | Improvement |
|-----------|--------------|------------|-------------|
| Category Filter | ~50-100ms | ~1-5ms | 10-100x faster |
| Full Table Scan | Required | Not Required | Significant |

## Verification

### Check if Index Exists

**SQL Query:**
```sql
SELECT indexname, indexdef 
FROM pg_indexes 
WHERE tablename = 'item' 
AND indexname = 'idx_item_category';
```

**Expected Output:**
```
     indexname      |                    indexdef                     
--------------------+-------------------------------------------------
 idx_item_category  | CREATE INDEX idx_item_category ON item USING btree (category)
```

### Test Query Performance

**SQL Query with EXPLAIN:**
```sql
EXPLAIN (ANALYZE, BUFFERS) 
SELECT * FROM item WHERE category = 'furniture';
```

**Expected Output (with index):**
```
Index Scan using idx_item_category on item  (cost=0.15..8.17 rows=1 width=...)
  Index Cond: ((category)::text = 'furniture'::text)
  Planning Time: 0.123 ms
  Execution Time: 0.045 ms
```

### Automated Verification Scripts

1. **Python Script:** `migrations/verify_index.py`
   - Checks if index exists
   - Tests query performance for all categories
   - Shows execution plans

2. **SQL Script:** `migrations/verify_index.sql`
   - Direct SQL verification
   - Performance analysis
   - Execution plan display

**Run Python verification:**
```bash
python3 migrations/verify_index.py
```

**Run SQL verification:**
```bash
psql -U postgres -d catalogmenuwithusers -f migrations/verify_index.sql
```

## Testing

Unit tests have been added to verify the index functionality:

**Test File:** `tests/test_application.py`

**Test Cases:**
1. `test_category_index_exists()` - Verifies category filtering works correctly
2. `test_category_query_performance()` - Tests query performance with indexed column

**Run tests:**
```bash
python3 -m pytest tests/test_application.py::TestApplication::test_category_index_exists -v
python3 -m pytest tests/test_application.py::TestApplication::test_category_query_performance -v
```

## Maintenance

### Index Statistics

Monitor index usage with:
```sql
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan as index_scans,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_fetched
FROM pg_stat_user_indexes
WHERE indexname = 'idx_item_category';
```

### Rebuild Index (if needed)

If index becomes fragmented over time:
```sql
REINDEX INDEX idx_item_category;
```

### Drop Index (rollback)

To remove the index:
```sql
DROP INDEX IF EXISTS idx_item_category;
```

## Requirements Satisfied

This implementation satisfies the following requirements from the specification:

- **Requirement 3.1:** Faster furniture category page loading
- **Requirement 4.1:** Faster cars category page loading  
- **Requirement 5.1:** Faster houses category page loading

## Related Files

- `migrations/add_icon_and_specifications.sql` - SQL migration with index creation
- `migrations/migrate_db.py` - Python migration script with index creation
- `migrations/verify_index.py` - Python verification script
- `migrations/verify_index.sql` - SQL verification script
- `tests/test_application.py` - Unit tests for index functionality
- `application.py` - Application routes that benefit from the index

## Notes

- The index uses PostgreSQL's default B-tree structure, which is optimal for equality and range queries
- The `IF NOT EXISTS` clause ensures the migration is idempotent and can be run multiple times safely
- The index is automatically maintained by PostgreSQL when items are inserted, updated, or deleted
- No application code changes are required - the index is transparent to the application layer
