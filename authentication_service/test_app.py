import unittest
from unittest.mock import patch, MagicMock
from flask import json
from app import app  

class AuthenticationServiceTests(unittest.TestCase):

    def setUp(self):
        """Set up test client."""
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_validate_admin_code_success(self):
        """Test validating admin code with correct code."""
        with patch('os.getenv', return_value="Syeda_Samia_Sultana"):
            response = self.app.post(
                '/api/auth/validate_admin_code',
                data=json.dumps({"admin_code": "Syeda_Samia_Sultana"}),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Admin code valid, proceed with registration", response.data)

    def test_validate_admin_code_failure(self):
        """Test validating admin code with incorrect code."""
        with patch('os.getenv', return_value="Syeda_Samia_Sultana"):
            response = self.app.post(
                '/api/auth/validate_admin_code',
                data=json.dumps({"admin_code": "wrong_code"}),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 403)
            self.assertIn(b"Invalid admin code", response.data)

    def test_validate_admin_code_missing(self):
        """Test validating admin code with missing admin_code field."""
        response = self.app.post(
            '/api/auth/validate_admin_code',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Admin code is required", response.data)


    def test_decode_token_missing(self):
        """Test decoding token with no token provided."""
        response = self.app.post(
            '/api/auth/decode_token',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Token is required.", response.data)

    def test_decode_token_invalid(self):
        """Test decoding an invalid token."""
        with patch('flask_jwt_extended.decode_token', side_effect=Exception("Invalid token")):
            response = self.app.post(
                '/api/auth/decode_token',
                data=json.dumps({"token": "invalid_token"}),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
