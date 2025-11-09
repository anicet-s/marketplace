# Implementation Plan

- [x] 1. Extend database models to support product icons and specifications
  - Add `icon_url` column to Item model as String(500), nullable
  - Add `specifications` column to Item model as JSON type, nullable
  - Create database migration script to add new columns to existing schema
  - _Requirements: 2.2, 3.2, 4.2, 5.2_

- [x] 2. Enhance Google OAuth authentication flow
  - [x] 2.1 Update login route to ensure proper nonce generation and session storage
    - Verify nonce is generated using secure random method
    - Ensure nonce is stored in session before OAuth redirect
    - _Requirements: 1.1, 1.2_
  
  - [x] 2.2 Improve auth callback route with error handling
    - Add try-except blocks around token exchange
    - Add error handling for user info retrieval
    - Add database transaction error handling for user creation
    - Log authentication errors for debugging
    - _Requirements: 1.3, 1.4, 1.5_
  
  - [x] 2.3 Verify session persistence configuration
    - Confirm PERMANENT_SESSION_LIFETIME is set to 7 days
    - Ensure SESSION_PERMANENT is True in app config
    - _Requirements: 6.1, 6.2, 6.4_
  
  - [x] 2.4 Update logout route to properly clear session
    - Use Flask-Login's logout_user() function
    - Clear any additional session data
    - Redirect to login page after logout
    - _Requirements: 6.3_

- [x] 3. Create template macros for product card display
  - [x] 3.1 Create product card macro in templates/macros.html
    - Define macro that accepts item object and category
    - Implement icon display with fallback to placeholder
    - Implement dynamic specification rendering based on category
    - Implement price formatting with 2 decimal places
    - Apply Tailwind CSS classes for consistent styling
    - _Requirements: 2.1, 2.3, 2.4, 3.1, 3.4, 4.1, 4.4, 5.1, 5.4_
  
  - [x] 3.2 Create placeholder image handling logic
    - Define default placeholder URLs for each category
    - Implement Jinja2 filter or logic to select appropriate placeholder
    - _Requirements: 2.3_

- [x] 4. Update furniture template with enhanced product display
  - Import product card macro from macros.html
  - Update template to use macro for each furniture item
  - Pass furniture-specific specification labels (material, dimensions, condition)
  - Ensure grid layout remains responsive
  - _Requirements: 3.1, 3.3, 3.4_

- [x] 5. Update cars template with enhanced product display
  - Import product card macro from macros.html
  - Update template to use macro for each car item
  - Pass car-specific specification labels (year, make, model, mileage, condition)
  - Ensure grid layout remains responsive
  - _Requirements: 4.1, 4.3, 4.4_

- [x] 6. Update houses template with enhanced product display
  - Import product card macro from macros.html
  - Update template to use macro for each house item
  - Pass house-specific specification labels (bedrooms, bathrooms, square footage, location)
  - Ensure grid layout remains responsive
  - _Requirements: 5.1, 5.3, 5.4_

- [x] 7. Update login template with improved Google sign-in button
  - Ensure "Sign in with Google" button is prominently displayed
  - Apply appropriate styling with Tailwind CSS
  - Add Google branding if appropriate
  - _Requirements: 1.1_

- [x] 8. Create database migration and seed data
  - [x] 8.1 Write Alembic migration or manual SQL script
    - Create migration to add icon_url and specifications columns
    - Ensure migration is reversible
    - _Requirements: 2.2, 3.2, 4.2, 5.2_
  
  - [x] 8.2 Create seed data script with sample items
    - Create sample furniture items with specifications and icon URLs
    - Create sample car items with specifications and icon URLs
    - Create sample house items with specifications and icon URLs
    - Include mix of items with and without icons to test placeholders
    - _Requirements: 2.1, 2.2, 3.1, 3.2, 4.1, 4.2, 5.1, 5.2_

- [x] 9. Write automated tests for new functionality
  - [x] 9.1 Write unit tests for Item model with specifications
    - Test Item creation with valid specifications JSON
    - Test specification retrieval and default handling
    - _Requirements: 3.2, 4.2, 5.2_
  
  - [x] 9.2 Write integration tests for OAuth flow
    - Mock Google OAuth responses
    - Test successful authentication and user creation
    - Test authentication error handling
    - _Requirements: 1.2, 1.3, 1.4, 1.5_
  
  - [x] 9.3 Write template rendering tests
    - Test product card rendering with specifications
    - Test placeholder image fallback
    - Test price formatting
    - _Requirements: 2.1, 2.3, 2.4, 3.1, 4.1, 5.1_

- [x] 10. Add database index for performance optimization
  - Create index on Item.category column for faster filtering
  - Test query performance with indexed column
  - _Requirements: 3.1, 4.1, 5.1_
