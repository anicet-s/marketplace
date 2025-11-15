# Database Setup Guide

This guide walks you through setting up PostgreSQL for the marketplace application.

## Step 1: Install and Configure PostgreSQL

Run the setup script:

```bash
./setup_database.sh
```

This will:
- Install PostgreSQL if not already installed
- Start the PostgreSQL service
- Create the `catalogmenuwithusers` database
- Set the postgres user password to `admin`

## Step 2: Initialize Database Tables

Create the base tables (User and Item):

```bash
python3 migrations/init_db.py
```

This creates:
- **User table**: Stores user authentication data (id, email, name)
- **Item table**: Stores marketplace items (id, name, description, price, category)

## Step 3: Run Migrations

Add additional columns and indexes:

```bash
python3 migrations/migrate_db.py
```

This adds:
- **icon_url column**: For product images
- **specifications column**: For category-specific details (JSON)
- **idx_item_category index**: For faster category filtering (Task 10)

## Step 4: Seed Test Data (Optional)

Populate the database with sample items:

```bash
python3 migrations/seed_data.py
```

This adds sample data for:
- Furniture items
- Car items
- House items

## Step 5: Restart the Application

After database setup, restart your Flask application:

```bash
# Stop the current process (Ctrl+C if running in terminal)
# Then start again:
./venv/bin/python application.py
```

## Complete Setup Commands

For a fresh setup, run these commands in order:

```bash
# 1. Setup PostgreSQL
./setup_database.sh

# 2. Initialize tables
python3 migrations/init_db.py

# 3. Run migrations
python3 migrations/migrate_db.py

# 4. Seed data (optional)
python3 migrations/seed_data.py

# 5. Restart application
./venv/bin/python application.py
```

## Verification

After setup, you can verify the database:

```bash
# Check if tables exist
sudo -u postgres psql -d catalogmenuwithusers -c "\dt"

# Check User table structure
sudo -u postgres psql -d catalogmenuwithusers -c "\d user"

# Check Item table structure
sudo -u postgres psql -d catalogmenuwithusers -c "\d item"

# Check indexes
sudo -u postgres psql -d catalogmenuwithusers -c "\di"

# Count items
sudo -u postgres psql -d catalogmenuwithusers -c "SELECT category, COUNT(*) FROM item GROUP BY category;"
```

## Troubleshooting

### Connection Refused Error

If you see "connection refused" errors:

```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Start PostgreSQL if not running
sudo systemctl start postgresql
```

### Authentication Failed

If you get authentication errors:

```bash
# Reset postgres password
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'admin';"
```

### Database Already Exists

If the database already exists:

```bash
# Drop and recreate (WARNING: deletes all data)
sudo -u postgres psql -c "DROP DATABASE catalogmenuwithusers;"
sudo -u postgres psql -c "CREATE DATABASE catalogmenuwithusers;"
```

### Table Already Exists

If tables already exist, you can:

```bash
# Drop all tables and start fresh
python3 migrations/init_db.py drop

# Then reinitialize
python3 migrations/init_db.py
```

## Database Schema

### User Table
```sql
CREATE TABLE "user" (
    id BIGINT PRIMARY KEY,
    email VARCHAR(100) UNIQUE,
    name VARCHAR(100)
);
```

### Item Table
```sql
CREATE TABLE item (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    price FLOAT,
    category VARCHAR(50),
    icon_url VARCHAR(500),
    specifications JSONB
);

CREATE INDEX idx_item_category ON item(category);
```

## Connection Details

- **Host**: localhost
- **Port**: 5432
- **Database**: catalogmenuwithusers
- **User**: postgres
- **Password**: admin
- **Connection String**: `postgresql://postgres:admin@localhost:5432/catalogmenuwithusers`
