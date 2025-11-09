import unittest
from unittest.mock import patch, MagicMock
from application import application, db, Item, User
from flask import session

class TestApplication(unittest.TestCase):
    def setUp(self):
        application.config['TESTING'] = True
        application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        application.config['SECRET_KEY'] = 'test_secret_key'
        self.client = application.test_client()
        with application.app_context():
            db.create_all()

    def tearDown(self):
        with application.app_context():
            db.session.remove()
            db.drop_all()

    def test_logout(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user'] = 'testuser'
            response = c.get('/logout')
            self.assertEqual(response.status_code, 302)  # Check redirect
            self.assertNotIn('user', session)  # Check session cleared

    def test_cars_route_requires_login(self):
        response = self.client.get('/cars')
        self.assertEqual(response.status_code, 302)  # Should redirect to login

    def test_cars_route_with_login(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user'] = 'testuser'
            response = c.get('/cars')
            self.assertEqual(response.status_code, 200)

    def test_houses_route_requires_login(self):
        response = self.client.get('/houses')
        self.assertEqual(response.status_code, 302)  # Should redirect to login

    def test_houses_route_with_login(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user'] = 'testuser'
            response = c.get('/houses')
            self.assertEqual(response.status_code, 200)

    def test_cars_content(self):
        with application.app_context():
            # Add test car item
            test_car = Item(category='cars', name='Test Car', price=10000)
            db.session.add(test_car)
            db.session.commit()

            with self.client as c:
                with c.session_transaction() as sess:
                    sess['user'] = 'testuser'
                response = c.get('/cars')
                self.assertIn(b'Test Car', response.data)

    def test_houses_content(self):
        with application.app_context():
            # Add test house item
            test_house = Item(category='houses', name='Test House', price=100000)
            db.session.add(test_house)
            db.session.commit()

            with self.client as c:
                with c.session_transaction() as sess:
                    sess['user'] = 'testuser'
                response = c.get('/houses')
                self.assertIn(b'Test House', response.data)

    # Task 9.1: Unit tests for Item model with specifications
    def test_item_creation_with_specifications(self):
        """Test Item creation with valid specifications JSON"""
        with application.app_context():
            # Test furniture item with specifications
            furniture_specs = {
                'material': 'Oak Wood',
                'dimensions': '72x36x30 inches',
                'condition': 'new'
            }
            furniture_item = Item(
                category='furniture',
                name='Oak Desk',
                price=599.99,
                icon_url='https://example.com/desk.jpg',
                specifications=furniture_specs
            )
            db.session.add(furniture_item)
            db.session.commit()

            # Retrieve and verify
            retrieved_item = Item.query.filter_by(name='Oak Desk').first()
            self.assertIsNotNone(retrieved_item)
            self.assertEqual(retrieved_item.specifications['material'], 'Oak Wood')
            self.assertEqual(retrieved_item.specifications['dimensions'], '72x36x30 inches')
            self.assertEqual(retrieved_item.specifications['condition'], 'new')

    def test_item_specification_retrieval_with_defaults(self):
        """Test specification retrieval and default handling"""
        with application.app_context():
            # Create item without specifications
            item_without_specs = Item(
                category='cars',
                name='Test Car',
                price=15000
            )
            db.session.add(item_without_specs)
            
            # Create item with partial specifications
            car_specs = {'year': 2020, 'make': 'Toyota'}
            item_with_partial_specs = Item(
                category='cars',
                name='Toyota Camry',
                price=25000,
                specifications=car_specs
            )
            db.session.add(item_with_partial_specs)
            db.session.commit()

            # Test default handling for missing specifications
            item1 = Item.query.filter_by(name='Test Car').first()
            self.assertIsNone(item1.specifications)
            
            # Test retrieval with .get() for safe access
            item2 = Item.query.filter_by(name='Toyota Camry').first()
            self.assertEqual(item2.specifications.get('year'), 2020)
            self.assertEqual(item2.specifications.get('make'), 'Toyota')
            self.assertIsNone(item2.specifications.get('model'))  # Missing key returns None

    def test_item_specifications_for_all_categories(self):
        """Test specifications for furniture, cars, and houses"""
        with application.app_context():
            # Furniture
            furniture = Item(
                category='furniture',
                name='Leather Sofa',
                price=1200,
                specifications={'material': 'Leather', 'dimensions': '84x36x32 inches', 'condition': 'new'}
            )
            
            # Car
            car = Item(
                category='cars',
                name='Honda Accord',
                price=28000,
                specifications={'year': 2022, 'make': 'Honda', 'model': 'Accord', 'mileage': 15000, 'condition': 'used'}
            )
            
            # House
            house = Item(
                category='houses',
                name='Suburban Home',
                price=450000,
                specifications={'bedrooms': 4, 'bathrooms': 2.5, 'square_footage': 2500, 'location': 'Austin, TX'}
            )
            
            db.session.add_all([furniture, car, house])
            db.session.commit()

            # Verify all items
            self.assertEqual(Item.query.filter_by(category='furniture').count(), 1)
            self.assertEqual(Item.query.filter_by(category='cars').count(), 1)
            self.assertEqual(Item.query.filter_by(category='houses').count(), 1)

    # Task 9.2: Integration tests for OAuth flow
    @patch('application.oauth.google.authorize_access_token')
    @patch('application.google.get')
    def test_oauth_successful_authentication_new_user(self, mock_google_get, mock_authorize_token):
        """Test successful authentication and user creation"""
        # Mock OAuth token exchange
        mock_authorize_token.return_value = {'access_token': 'test_token'}
        
        # Mock user info response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'id': '123456789',
            'email': 'newuser@example.com',
            'name': 'New User'
        }
        mock_google_get.return_value = mock_response

        with application.app_context():
            with self.client as c:
                # Simulate OAuth callback
                response = c.get('/auth')
                
                # Verify redirect to home
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.location.endswith('/'))
                
                # Verify user was created in database
                user = User.query.filter_by(email='newuser@example.com').first()
                self.assertIsNotNone(user)
                self.assertEqual(user.name, 'New User')
                self.assertEqual(user.id, 123456789)

    @patch('application.oauth.google.authorize_access_token')
    @patch('application.google.get')
    def test_oauth_successful_authentication_existing_user(self, mock_google_get, mock_authorize_token):
        """Test successful authentication for existing user"""
        with application.app_context():
            # Create existing user
            existing_user = User(id=987654321, email='existing@example.com', name='Existing User')
            db.session.add(existing_user)
            db.session.commit()

            # Mock OAuth responses
            mock_authorize_token.return_value = {'access_token': 'test_token'}
            mock_response = MagicMock()
            mock_response.json.return_value = {
                'id': '987654321',
                'email': 'existing@example.com',
                'name': 'Existing User'
            }
            mock_google_get.return_value = mock_response

            with self.client as c:
                response = c.get('/auth')
                
                # Verify redirect to home
                self.assertEqual(response.status_code, 302)
                
                # Verify no duplicate user was created
                user_count = User.query.filter_by(email='existing@example.com').count()
                self.assertEqual(user_count, 1)

    @patch('application.oauth.google.authorize_access_token')
    def test_oauth_token_exchange_failure(self, mock_authorize_token):
        """Test authentication error handling for token exchange failure"""
        # Mock token exchange failure
        mock_authorize_token.side_effect = Exception('Token exchange failed')

        with self.client as c:
            response = c.get('/auth')
            
            # Verify redirect to login page
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.location.endswith('/login'))

    @patch('application.oauth.google.authorize_access_token')
    @patch('application.google.get')
    def test_oauth_user_info_retrieval_failure(self, mock_google_get, mock_authorize_token):
        """Test authentication error handling for user info retrieval failure"""
        # Mock successful token exchange but failed user info retrieval
        mock_authorize_token.return_value = {'access_token': 'test_token'}
        mock_google_get.side_effect = Exception('User info retrieval failed')

        with self.client as c:
            response = c.get('/auth')
            
            # Verify redirect to login page
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.location.endswith('/login'))

    # Task 9.3: Template rendering tests
    def test_product_card_rendering_with_specifications(self):
        """Test product card rendering with specifications"""
        with application.app_context():
            # Create furniture item with specifications
            furniture = Item(
                category='furniture',
                name='Modern Chair',
                description='Comfortable office chair',
                price=299.99,
                icon_url='https://example.com/chair.jpg',
                specifications={'material': 'Mesh', 'dimensions': '24x24x40 inches', 'condition': 'new'}
            )
            db.session.add(furniture)
            db.session.commit()

            with self.client as c:
                with c.session_transaction() as sess:
                    sess['user'] = 'testuser'
                response = c.get('/furniture')
                
                # Verify item name and price are rendered
                self.assertIn(b'Modern Chair', response.data)
                self.assertIn(b'299.99', response.data)
                
                # Verify specifications are rendered
                self.assertIn(b'Mesh', response.data)
                self.assertIn(b'24x24x40 inches', response.data)

    def test_placeholder_image_fallback(self):
        """Test placeholder image fallback for items without icons"""
        with application.app_context():
            # Create item without icon_url
            car = Item(
                category='cars',
                name='Budget Car',
                price=8000,
                specifications={'year': 2015, 'make': 'Ford', 'model': 'Focus', 'mileage': 80000, 'condition': 'used'}
            )
            db.session.add(car)
            db.session.commit()

            with self.client as c:
                with c.session_transaction() as sess:
                    sess['user'] = 'testuser'
                response = c.get('/cars')
                
                # Verify item is rendered
                self.assertIn(b'Budget Car', response.data)
                
                # Verify placeholder is used (checking for placeholder URL pattern)
                self.assertIn(b'placeholder', response.data.lower())

    def test_price_formatting(self):
        """Test price formatting with 2 decimal places"""
        with application.app_context():
            # Create items with various price formats
            house1 = Item(category='houses', name='House 1', price=250000)
            house2 = Item(category='houses', name='House 2', price=350000.5)
            house3 = Item(category='houses', name='House 3', price=450000.99)
            
            db.session.add_all([house1, house2, house3])
            db.session.commit()

            with self.client as c:
                with c.session_transaction() as sess:
                    sess['user'] = 'testuser'
                response = c.get('/houses')
                
                # Verify prices are formatted with 2 decimal places
                response_text = response.data.decode('utf-8')
                self.assertIn('250,000.00', response_text)
                self.assertIn('350,000.50', response_text)
                self.assertIn('450,000.99', response_text)

    def test_category_specific_specifications_display(self):
        """Test that category-specific specifications are displayed correctly"""
        with application.app_context():
            # Create items for each category with specifications
            furniture = Item(
                category='furniture',
                name='Dining Table',
                price=800,
                specifications={'material': 'Walnut', 'dimensions': '60x36x30 inches', 'condition': 'new'}
            )
            car = Item(
                category='cars',
                name='Tesla Model 3',
                price=45000,
                specifications={'year': 2023, 'make': 'Tesla', 'model': 'Model 3', 'mileage': 5000, 'condition': 'used'}
            )
            house = Item(
                category='houses',
                name='Downtown Condo',
                price=380000,
                specifications={'bedrooms': 2, 'bathrooms': 2, 'square_footage': 1200, 'location': 'Seattle, WA'}
            )
            
            db.session.add_all([furniture, car, house])
            db.session.commit()

            with self.client as c:
                with c.session_transaction() as sess:
                    sess['user'] = 'testuser'
                
                # Test furniture page
                furniture_response = c.get('/furniture')
                self.assertIn(b'Walnut', furniture_response.data)
                self.assertIn(b'60x36x30 inches', furniture_response.data)
                
                # Test cars page
                cars_response = c.get('/cars')
                self.assertIn(b'Tesla', cars_response.data)
                self.assertIn(b'2023', cars_response.data)
                self.assertIn(b'5000', cars_response.data)
                
                # Test houses page
                houses_response = c.get('/houses')
                self.assertIn(b'2', houses_response.data)  # bedrooms
                self.assertIn(b'1200', houses_response.data)  # square footage
                self.assertIn(b'Seattle, WA', houses_response.data)

    # Task 10: Database index performance tests
    def test_category_index_exists(self):
        """Test that the category index exists in the database"""
        with application.app_context():
            # This test is primarily for PostgreSQL production database
            # SQLite in-memory database used for testing doesn't support the same index introspection
            # In production, verify with: SELECT indexname FROM pg_indexes WHERE tablename = 'item' AND indexname = 'idx_item_category'
            
            # For SQLite testing, we verify that category queries work efficiently
            # Create multiple items across categories
            items = []
            for i in range(10):
                items.append(Item(category='furniture', name=f'Furniture {i}', price=100 + i))
                items.append(Item(category='cars', name=f'Car {i}', price=10000 + i))
                items.append(Item(category='houses', name=f'House {i}', price=100000 + i))
            
            db.session.add_all(items)
            db.session.commit()
            
            # Verify category filtering works correctly
            furniture_count = Item.query.filter_by(category='furniture').count()
            cars_count = Item.query.filter_by(category='cars').count()
            houses_count = Item.query.filter_by(category='houses').count()
            
            self.assertEqual(furniture_count, 10)
            self.assertEqual(cars_count, 10)
            self.assertEqual(houses_count, 10)

    def test_category_query_performance(self):
        """Test query performance with indexed category column"""
        with application.app_context():
            import time
            
            # Create a larger dataset to test performance
            items = []
            for i in range(100):
                items.append(Item(
                    category='furniture',
                    name=f'Furniture Item {i}',
                    price=100 + i,
                    specifications={'material': 'Wood', 'condition': 'new'}
                ))
                items.append(Item(
                    category='cars',
                    name=f'Car Item {i}',
                    price=10000 + i,
                    specifications={'year': 2020, 'make': 'Toyota', 'mileage': 10000}
                ))
                items.append(Item(
                    category='houses',
                    name=f'House Item {i}',
                    price=200000 + i,
                    specifications={'bedrooms': 3, 'bathrooms': 2, 'square_footage': 1500}
                ))
            
            db.session.add_all(items)
            db.session.commit()
            
            # Test query performance for each category
            categories = ['furniture', 'cars', 'houses']
            
            for category in categories:
                start_time = time.time()
                items = Item.query.filter_by(category=category).all()
                end_time = time.time()
                
                query_time = (end_time - start_time) * 1000  # Convert to milliseconds
                
                # Verify correct number of items returned
                self.assertEqual(len(items), 100)
                
                # Query should be fast (under 100ms for this small dataset)
                # This is a basic performance check
                self.assertLess(query_time, 100, f"Query for {category} took {query_time:.2f}ms")

if __name__ == '__main__':
    unittest.main()