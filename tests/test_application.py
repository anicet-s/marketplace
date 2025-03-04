import unittest
from application import application, db, Item
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

if __name__ == '__main__':
    unittest.main()