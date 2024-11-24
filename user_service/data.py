import os

# Path to the Python file where users will be stored
DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), 'userdata.py')

# Function to save users data to the file
def save_users(new_users):
    """Append new user data to the existing users_db and save it."""
    # Load the current users from the file
    existing_users = load_users()

    # Combine existing and new users
    updated_users = existing_users + new_users
    

    # Write the updated users to the file
    with open(DATA_FILE_PATH, 'w+') as file:
        file.write(f"users_db = {repr(updated_users)}")  # Save the updated list

# Function to load users data from the file
def load_users():
    """Load users data from the Python file."""
    if not os.path.exists(DATA_FILE_PATH):
        return []  # Return an empty list if the file doesn't exist
    try:
        with open(DATA_FILE_PATH, 'r') as file:
            exec(file.read(), globals())  # Execute the Python code to load users_db
        return users_db
    except Exception as e:
        print(f"Error loading users: {e}")
        return []  # Return an empty list if there is an error
