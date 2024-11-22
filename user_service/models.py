import re
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List, Dict
from data import load_users  # Import the function to load user data from the file

# Load users data into the memory when the app starts
users_db = load_users()

class User:
    def __init__(self, name: str, email: str, password: str, role: str):
        """Initialize a new user with hashed password."""
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role

    def to_dict(self):
        """Return the user as a dictionary."""
        return {
            'name': self.name,
            'email': self.email,
            'password': self.password,  # Store the hashed password
            'role': self.role
        }

    @staticmethod
    def find_by_email(email: str) -> Dict:
        """Find a user by their email."""
        for user in users_db:
            if user['email'] == email:
                return user
        return None

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validate the email format using regex."""
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(regex, email) is not None

    @staticmethod
    def is_valid_password(password: str) -> bool:
        """Check if the password meets the minimum length requirement."""
        return len(password) >= 5

    @staticmethod
    def authenticate(email: str, password: str) -> Dict:
        """Authenticate a user based on email and password."""
        for user in users_db:
            if user['email'] == email and check_password_hash(user['password'], password):
                return user
        return None
