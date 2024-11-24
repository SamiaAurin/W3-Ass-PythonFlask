import unittest
from app import create_app
from data import load_users, save_users
from models import User

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        """Set up a test client."""
        app = create_app()
        app.config['TESTING'] = True
        self.app = app.test_client()

   

    def test_register_user_with_invalid_email(self):
        """Test registering a user with an invalid email."""
        response = self.app.post('/api/users/register', json={
            "name": "Invalid Email User",
            "email": "invalid-email",
            "password": "password123",
            "role": "User"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], "Invalid email format!")

    def test_register_user_with_short_password(self):
        """Test registering a user with a password shorter than 5 characters."""
        response = self.app.post('/api/users/register', json={
            "name": "Short Password User",
            "email": "shortpass@example.com",
            "password": "1234",
            "role": "User"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], "Password must be at least 5 characters long!")

    def test_login_user(self):
        """Test logging in a user."""
        save_users([{
            "name": "Test Login User",
            "email": "loginuser@example.com",
            "password": User("Test Login User", "loginuser@example.com", "securepassword", "User").password,
            "role": "User"
        }])

        response = self.app.post('/api/users/login', json={
            "email": "loginuser@example.com",
            "password": "securepassword"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)

    def test_login_invalid_email(self):
        """Test logging in with an invalid email."""
        response = self.app.post('/api/users/login', json={
            "email": "nonexistentuser@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], "User not found")

    def test_login_invalid_password(self):
        """Test logging in with an incorrect password."""
        save_users([{
            "name": "Test Invalid Password User",
            "email": "invalidpassworduser@example.com",
            "password": User("Test Invalid Password User", "invalidpassworduser@example.com", "correctpassword", "User").password,
            "role": "User"
        }])

        response = self.app.post('/api/users/login', json={
            "email": "invalidpassworduser@example.com",
            "password": "wrongpassword"
        })

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['message'], "Invalid password")

    def test_profile(self):
        """Test viewing a user's profile."""
        self.app.post('/api/users/register', json={
            "name": "Profile User",
            "email": "profileuser@example.com",
            "password": "password123",
            "role": "User"
        })
        login_response = self.app.post('/api/users/login', json={
            "email": "profileuser@example.com",
            "password": "password123"
        })

        token = login_response.json['access_token']

        response = self.app.get('/api/users/profile', headers={
            "Authorization": f"Bearer {token}"
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['user']['email'], "profileuser@example.com")
        self.assertEqual(response.json['user']['name'], "Profile User")
        self.assertEqual(response.json['user']['role'], "User")

    def test_profile_unauthorized(self):
        """Test accessing the profile endpoint without a valid token."""
        response = self.app.get('/api/users/profile')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['message'], "Missing Authorization header")

    def test_profile_invalid_token(self):
        """Test accessing the profile endpoint with an invalid token."""
        response = self.app.get('/api/users/profile', headers={
            "Authorization": "Bearer invalidtoken"
        })
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['message'], "Invalid or expired token")

if __name__ == '__main__':
    unittest.main()
