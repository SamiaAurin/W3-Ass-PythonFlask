from data import DestinationData

class Destination:
    @staticmethod
    def get_all_destinations():
        """
        Retrieves all destinations.
        """
        return DestinationData.load_destinations()

    @staticmethod
    def get_destination_by_id(destination_id):
        """
        Retrieves a destination by its ID.
        """
        destinations = DestinationData.load_destinations()
        return next((destination for destination in destinations if destination["id"] == destination_id), None)

    @staticmethod
    def add_destination(name, description, location):
        """
        Adds a new destination to the list of destinations.
        """
        destinations = DestinationData.load_destinations()
        new_id = DestinationData.get_next_id(destinations)
        new_destination = {
            "id": new_id,
            "name": name,
            "description": description,
            "location": location
        }
        destinations.append(new_destination)
        DestinationData.save_destinations(destinations)
        return new_destination

    @staticmethod
    def update_destination(destination_id, name=None, description=None, location=None):
        """
        Updates an existing destination. Only non-None fields will be updated.
        """
        destinations = DestinationData.load_destinations()
        destination = next((dest for dest in destinations if dest["id"] == destination_id), None)
        if not destination:
            return None

        if name:
            destination["name"] = name
        if description:
            destination["description"] = description
        if location:
            destination["location"] = location

        DestinationData.save_destinations(destinations)
        return destination

    @staticmethod
    def delete_destination(destination_id):
        """
        Deletes a destination by its ID.
        """
        destinations = DestinationData.load_destinations()
        destination = next((dest for dest in destinations if dest["id"] == destination_id), None)
        if destination:
            destinations.remove(destination)
            DestinationData.save_destinations(destinations)
            return True
        return False