import unittest
from unittest.mock import patch, MagicMock
from flask import json
from app import create_app
from models import Destination

class DestinationServiceTests(unittest.TestCase):

    def setUp(self):
        """Set up test client."""
        app = create_app()
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_get_destinations(self):
        """Test getting all destinations."""
        mock_destinations = [
            {
                "id": 1,
                "name": "Berlin",
                "description": "Capital of Germany",
                "location": "Germany"
            },
            {
                "id": 2,
                "name": "Paris",
                "description": "City of Lights",
                "location": "France"
            }
        ]
        
        with patch('models.Destination.get_all_destinations', return_value=mock_destinations):
            response = self.app.get('api/destinations')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.data), mock_destinations)

    def test_add_destination_success(self):
        """Test adding a new destination with admin role."""
        mock_token_response = MagicMock()
        mock_token_response.status_code = 200
        mock_token_response.json.return_value = {"role": "admin"}
        
        new_destination = {
            "name": "Tokyo",
            "description": "Capital of Japan",
            "location": "Japan"
        }
        
        expected_response = {
            "id": 3,
            **new_destination
        }
        
        with patch('requests.post', return_value=mock_token_response), \
             patch('models.Destination.add_destination', return_value=expected_response):
            
            response = self.app.post(
                'api/destinations',
                data=json.dumps(new_destination),
                content_type='application/json',
                headers={'Authorization': 'Bearer fake-token'}
            )
            
            self.assertEqual(response.status_code, 201)
            response_data = json.loads(response.data)
            self.assertIn("destination", response_data)
            self.assertEqual(response_data["destination"], expected_response)

    def test_add_destination_missing_auth(self):
        """Test adding a destination without authentication header."""
        response = self.app.post(
            'api/destinations',
            data=json.dumps({
                "name": "Tokyo",
                "description": "Capital of Japan",
                "location": "Japan"
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn(b"Missing Authorization header", response.data)

    def test_add_destination_non_admin(self):
        """Test adding a destination with non-admin role."""
        mock_token_response = MagicMock()
        mock_token_response.status_code = 200
        mock_token_response.json.return_value = {"role": "user"}
        
        with patch('requests.post', return_value=mock_token_response):
            response = self.app.post(
                'api/destinations',
                data=json.dumps({
                    "name": "Tokyo",
                    "description": "Capital of Japan",
                    "location": "Japan"
                }),
                content_type='application/json',
                headers={'Authorization': 'Bearer fake-token'}
            )
            self.assertEqual(response.status_code, 403)
            self.assertIn(b"Unauthorized access. Admin role required.", response.data)

    def test_add_destination_missing_fields(self):
        """Test adding a destination with missing required fields."""
        mock_token_response = MagicMock()
        mock_token_response.status_code = 200
        mock_token_response.json.return_value = {"role": "admin"}
        
        with patch('requests.post', return_value=mock_token_response):
            response = self.app.post(
                'api/destinations',
                data=json.dumps({"name": "Tokyo"}),
                content_type='application/json',
                headers={'Authorization': 'Bearer fake-token'}
            )
            self.assertEqual(response.status_code, 400)
            self.assertIn(b"All fields (name, description, location) are required", response.data)

    def test_update_destination_success(self):
        """Test updating an existing destination with admin role."""
        mock_token_response = MagicMock()
        mock_token_response.status_code = 200
        mock_token_response.json.return_value = {"role": "admin"}
        
        update_data = {
            "name": "Updated Berlin",
            "description": "Updated description",
            "location": "Germany"
        }
        
        expected_response = {
            "id": 1,
            **update_data
        }
        
        with patch('requests.post', return_value=mock_token_response), \
             patch('models.Destination.update_destination', return_value=expected_response):
            
            response = self.app.put(
                'api/destinations/1',
                data=json.dumps(update_data),
                content_type='application/json',
                headers={'Authorization': 'Bearer fake-token'}
            )
            
            self.assertEqual(response.status_code, 200)
            response_data = json.loads(response.data)
            self.assertIn("destination", response_data)
            self.assertEqual(response_data["destination"], expected_response)

    def test_update_nonexistent_destination(self):
        """Test updating a non-existent destination."""
        mock_token_response = MagicMock()
        mock_token_response.status_code = 200
        mock_token_response.json.return_value = {"role": "admin"}
        
        with patch('requests.post', return_value=mock_token_response), \
             patch('models.Destination.update_destination', return_value=None):
            
            response = self.app.put(
                'api/destinations/999',
                data=json.dumps({"name": "Test"}),
                content_type='application/json',
                headers={'Authorization': 'Bearer fake-token'}
            )
            
            self.assertEqual(response.status_code, 404)
            self.assertIn(b"Destination not found", response.data)

    def test_delete_destination_success(self):
        """Test deleting an existing destination with admin role."""
        mock_token_response = MagicMock()
        mock_token_response.status_code = 200
        mock_token_response.json.return_value = {"role": "admin"}
        
        with patch('requests.post', return_value=mock_token_response), \
             patch('models.Destination.delete_destination', return_value=True):
            
            response = self.app.delete(
                'api/destinations/1',
                headers={'Authorization': 'Bearer fake-token'}
            )
            
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Destination deleted successfully", response.data)

    def test_delete_nonexistent_destination(self):
        """Test deleting a non-existent destination."""
        mock_token_response = MagicMock()
        mock_token_response.status_code = 200
        mock_token_response.json.return_value = {"role": "admin"}
        
        with patch('requests.post', return_value=mock_token_response), \
             patch('models.Destination.delete_destination', return_value=False):
            
            response = self.app.delete(
                'api/destinations/999',
                headers={'Authorization': 'Bearer fake-token'}
            )
            
            self.assertEqual(response.status_code, 404)
            self.assertIn(b"Destination not found", response.data)

    def test_invalid_token(self):
        """Test accessing protected endpoints with invalid token."""
        mock_token_response = MagicMock()
        mock_token_response.status_code = 401
        
        with patch('requests.post', return_value=mock_token_response):
            response = self.app.post(
                'api/destinations',
                data=json.dumps({"name": "Test"}),
                content_type='application/json',
                headers={'Authorization': 'Bearer invalid-token'}
            )
            self.assertEqual(response.status_code, 401)
            self.assertIn(b"Invalid or expired token", response.data)

if __name__ == '__main__':
    unittest.main()