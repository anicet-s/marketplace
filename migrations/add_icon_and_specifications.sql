-- Migration: Add icon_url and specifications columns to Item table
-- Date: 2025-11-09
-- Description: Extends the Item model to support product icons and category-specific specifications

-- Add icon_url column
ALTER TABLE item ADD COLUMN IF NOT EXISTS icon_url VARCHAR(500);

-- Add specifications column (JSONB for PostgreSQL)
ALTER TABLE item ADD COLUMN IF NOT EXISTS specifications JSONB;

-- Create index on category column for better query performance
CREATE INDEX IF NOT EXISTS idx_item_category ON item(category);

-- Rollback script (commented out, uncomment to revert):
-- ALTER TABLE item DROP COLUMN IF EXISTS icon_url;
-- ALTER TABLE item DROP COLUMN IF EXISTS specifications;
-- DROP INDEX IF EXISTS idx_item_category;
