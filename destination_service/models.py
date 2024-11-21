class Destination:
    destinations_db = [
        {"id": 1, "name": "Paris", "description": "The City of Light", "location": "France"},
        {"id": 2, "name": "Tokyo", "description": "The Capital of Japan", "location": "Japan"},
        {"id": 3, "name": "New York", "description": "The Big Apple", "location": "USA"}
    ]

    @classmethod
    def get_all_destinations(cls):
        return cls.destinations_db

    @classmethod
    def get_destination_by_id(cls, destination_id):
        return next((destination for destination in cls.destinations_db if destination['id'] == destination_id), None)

    @classmethod
    def delete_destination(cls, destination_id):
        destination = cls.get_destination_by_id(destination_id)
        if destination:
            cls.destinations_db.remove(destination)
            return True
        return False
