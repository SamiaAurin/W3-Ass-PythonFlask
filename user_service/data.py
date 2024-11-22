import os

# Path to the Python file where users will be stored
DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), 'userdata.py')  # Save as .py file

# Function to save users data to the file
def save_users(users_db):
    """Save the users data to a Python file."""
    with open(DATA_FILE_PATH, 'w') as file:
        file.write(f"users_db = {users_db}")  # Save the users data as a Python variable

# Function to load users data from the file
def load_users():
    """Load users data from the Python file."""
    if not os.path.exists(DATA_FILE_PATH):
        return []  # Return an empty list if the file doesn't exist
    try:
        # Initialize the users_db variable in case the file is empty or corrupted
        users_db = []
        
        with open(DATA_FILE_PATH, 'r') as file:
            # Read the Python file as code and execute it
            exec(file.read())  # This will define the 'users_db' variable in the current scope
            
        return users_db  # Return the loaded users data
    except Exception as e:
        return []  # Return an empty list if there is an error (e.g., file corruption)
