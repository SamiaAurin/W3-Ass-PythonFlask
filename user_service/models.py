import json
import re
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List, Dict

# File to store user data
USERS_FILE = 'users.json'

# Load users from the JSON file
def load_users() -> List[Dict]:
    try:
        with open(USERS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save users to the JSON file
def save_users(users: List[Dict]):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)

# Load users into memory
users_db = load_users()

class User:
    def __init__(self, name: str, email: str, password: str, role: str):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'password': self.password,  # Store the hashed password
            'role': self.role
        }

    @staticmethod
    def authenticate(email: str, password: str):
        for user in users_db:
            if user['email'] == email and check_password_hash(user['password'], password):
                return user
        return None

    @staticmethod
    def find_by_email(email: str):
        for user in users_db:
            if user['email'] == email:
                return user
        return None

    @staticmethod
    def is_valid_email(email: str) -> bool:
        # Regex for validating an email
        regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.match(regex, email) is not None

    @staticmethod
    def is_valid_password(password: str) -> bool:
        # Check if the password length is at least 5 characters
        return len(password) >= 5
