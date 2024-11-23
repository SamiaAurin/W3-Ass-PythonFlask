import os
import importlib

# Path to the Python file where destinations will be stored
DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), 'destinationdata.py')

class DestinationData:
    @staticmethod
    def load_destinations():
        """
        Load destinations from the Python file. If the file doesn't exist, create it with an empty list.
        """
        if not os.path.exists(DATA_FILE_PATH):
            # Create the file with an empty list if it doesn't exist
            with open(DATA_FILE_PATH, 'w') as file:
                file.write("destinations = []\n")

        # Import the destinations list dynamically from the Python file
        spec = importlib.util.spec_from_file_location("destinationdata", DATA_FILE_PATH)
        destinationdata = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(destinationdata)
        return getattr(destinationdata, "destinations", [])

    @staticmethod
    def save_destinations(destinations):
        """
        Save destinations to the Python file.
        """
        with open(DATA_FILE_PATH, 'w') as file:
            file.write(f"destinations = {repr(destinations)}\n")

    @staticmethod
    def get_next_id(destinations):
        """
        Generate the next destination ID based on the current destinations.
        """
        if not destinations:
            return 1
        return max(destination["id"] for destination in destinations) + 1
