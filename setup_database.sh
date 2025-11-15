#!/bin/bash

# PostgreSQL Database Setup Script for Marketplace Application

echo "=========================================="
echo "PostgreSQL Database Setup"
echo "=========================================="
echo ""

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "PostgreSQL is not installed. Installing..."
    sudo apt update
    sudo apt install -y postgresql postgresql-contrib
    echo "PostgreSQL installed successfully!"
else
    echo "PostgreSQL is already installed."
fi

echo ""
echo "Starting PostgreSQL service..."
sudo systemctl start postgresql
sudo systemctl enable postgresql

echo ""
echo "Checking PostgreSQL status..."
sudo systemctl status postgresql --no-pager

echo ""
echo "=========================================="
echo "Creating Database and User"
echo "=========================================="
echo ""

# Create database and set password
echo "Creating database 'catalogmenuwithusers'..."
sudo -u postgres psql -c "CREATE DATABASE catalogmenuwithusers;" 2>/dev/null || echo "Database already exists."

echo "Setting password for postgres user..."
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'admin';"

echo ""
echo "=========================================="
echo "Database Setup Complete!"
echo "=========================================="
echo ""
echo "Database Details:"
echo "  Host: localhost"
echo "  Port: 5432"
echo "  Database: catalogmenuwithusers"
echo "  User: postgres"
echo "  Password: admin"
echo ""
echo "Connection String:"
echo "  postgresql://postgres:admin@localhost:5432/catalogmenuwithusers"
echo ""
echo "Next Steps:"
echo "  1. Run migrations: python3 migrations/migrate_db.py"
echo "  2. Seed data (optional): python3 migrations/seed_data.py"
echo "  3. Restart your application"
echo ""
