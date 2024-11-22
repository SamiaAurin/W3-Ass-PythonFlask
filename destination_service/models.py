class Destination:
    # Sample destinations (you would typically use a database instead)
    destinations_db = [
        {"id": 1, "name": "Paris", "description": "The City of Light", "location": "France"},
        {"id": 2, "name": "Tokyo", "description": "The Capital of Japan", "location": "Japan"},
        {"id": 3, "name": "New York", "description": "The Big Apple", "location": "USA"}
    ]

    @classmethod
    def get_all_destinations(cls):
        """
        Retrieves all destinations.
        """
        return cls.destinations_db

    @classmethod
    def get_destination_by_id(cls, destination_id):
        """
        Retrieves a destination by its ID.
        """
        return next((destination for destination in cls.destinations_db if destination['id'] == destination_id), None)

    @classmethod
    def add_destination(cls, name, description, location):
        """
        Adds a new destination to the list of destinations.
        """
        new_id = max(destination['id'] for destination in cls.destinations_db) + 1
        new_destination = {
            "id": new_id,
            "name": name,
            "description": description,
            "location": location
        }
        cls.destinations_db.append(new_destination)
        return new_destination

    @classmethod
    def update_destination(cls, destination_id, name=None, description=None, location=None):
        """
        Updates an existing destination. Only non-None fields will be updated.
        """
        destination = cls.get_destination_by_id(destination_id)
        if not destination:
            return None  # Destination not found

        if name:
            destination['name'] = name
        if description:
            destination['description'] = description
        if location:
            destination['location'] = location
        
        return destination

    @classmethod
    def delete_destination(cls, destination_id):
        """
        Deletes a destination by its ID.
        """
        destination = cls.get_destination_by_id(destination_id)
        if destination:
            cls.destinations_db.remove(destination)
            return True
        return False
