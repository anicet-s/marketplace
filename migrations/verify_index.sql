-- SQL script to verify the category index exists and test query performance
-- Run with: psql -U postgres -d catalogmenuwithusers -f migrations/verify_index.sql

\echo '============================================================'
\echo 'Database Index Verification and Performance Test'
\echo '============================================================'
\echo ''

-- Check if the index exists
\echo 'Checking for idx_item_category index...'
\echo ''
SELECT 
    indexname, 
    indexdef 
FROM pg_indexes 
WHERE tablename = 'item' 
AND indexname = 'idx_item_category';

\echo ''
\echo '------------------------------------------------------------'
\echo 'Query Performance Test'
\echo '------------------------------------------------------------'
\echo ''

-- Get total item count
\echo 'Total items in database:'
SELECT COUNT(*) as total_items FROM item;

\echo ''
\echo 'Items per category:'
SELECT category, COUNT(*) as count 
FROM item 
GROUP BY category 
ORDER BY category;

\echo ''
\echo '------------------------------------------------------------'
\echo 'Query Execution Plan (EXPLAIN ANALYZE)'
\echo '------------------------------------------------------------'
\echo ''

-- Show execution plan for furniture query
\echo 'Execution plan for: SELECT * FROM item WHERE category = ''furniture'''
EXPLAIN (ANALYZE, BUFFERS) 
SELECT * FROM item WHERE category = 'furniture';

\echo ''
\echo '------------------------------------------------------------'
\echo 'Execution plan for: SELECT * FROM item WHERE category = ''cars'''
EXPLAIN (ANALYZE, BUFFERS) 
SELECT * FROM item WHERE category = 'cars';

\echo ''
\echo '------------------------------------------------------------'
\echo 'Execution plan for: SELECT * FROM item WHERE category = ''houses'''
EXPLAIN (ANALYZE, BUFFERS) 
SELECT * FROM item WHERE category = 'houses';

\echo ''
\echo '============================================================'
\echo 'Verification Complete!'
\echo '============================================================'
