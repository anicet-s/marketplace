# Database Migrations

This directory contains database migration scripts for the marketplace application.

## Migration: Add Icon and Specifications Support

**Date:** 2025-11-09

**Purpose:** Extends the Item model to support product icons and category-specific specifications.

### Changes

- Adds `icon_url` column (VARCHAR(500), nullable) to store image URLs or file paths
- Adds `specifications` column (JSONB, nullable) to store category-specific product details
- Creates index on `category` column for improved query performance

### Running the Migration

#### Option 1: Python Script (Recommended)

```bash
python migrations/migrate_db.py
```

To rollback:
```bash
python migrations/migrate_db.py rollback
```

#### Option 2: SQL Script

```bash
psql -U postgres -d catalogmenuwithusers -f migrations/add_icon_and_specifications.sql
```

### Specification Schema Examples

**Furniture:**
```json
{
  "material": "Oak Wood",
  "dimensions": "72x36x30 inches",
  "condition": "new"
}
```

**Cars:**
```json
{
  "year": 2022,
  "make": "Toyota",
  "model": "Camry",
  "mileage": 15000,
  "condition": "used"
}
```

**Houses:**
```json
{
  "bedrooms": 3,
  "bathrooms": 2.5,
  "square_footage": 2100,
  "location": "Austin, TX"
}
```

### Notes

- Both columns are nullable to maintain compatibility with existing data
- The migration scripts use `IF NOT EXISTS` / `IF EXISTS` clauses for idempotency
- The Python script requires the application to be properly configured with database credentials
