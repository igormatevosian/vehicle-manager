from typing import Any
from dataclasses import dataclass
from math import sin, cos, sqrt, asin, radians

import requests

# The radius of earth in metres.
R_M = 6371000


@dataclass
class Vehicle:
    name: str
    model: str
    year: int
    color: str
    price: float
    latitude: float
    longitude: float
    id: int | None = None

    def __str__(self):
        return f"<Vehicle: {self.name} {self.model} {self.year} {self.color} {self.price}>"

    def __repr__(self) -> str:
        return self.__str__()


@dataclass
class Coordinates:
    """A class representing geographic coordinates.

    Attributes:
        latitude (float): The latitude coordinate.
        longitude (float): The longitude coordinate.
    """
    latitude: float
    longitude: float


class VehicleManager:
    """A class for managing vehicles via an API."""

    def __init__(self, url):
        """Initialize the VehicleManager with the API URL.

        Args:
            url (str): The URL of the API.
        """
        self.url = url

    def get_vehicles(self) -> list[Vehicle]:
        """Get a list of vehicles from the API.

        Returns:
            list[Vehicle]: A list of Vehicle objects.
        """
        response = requests.get(f"{self.url}/vehicles")
        vehicles_data = response.json()
        vehicles = []
        for vehicle_data in vehicles_data:
            vehicles.append(Vehicle(**vehicle_data))
        return vehicles

    def filter_vehicles(self, params: dict[str, Any]) -> list[Vehicle]:
        """Filter vehicles based on the provided parameters.

        Args:
            params (dict): A dictionary of filtering parameters.

        Returns:
            list[Vehicle]: A list of Vehicle objects that match the filter.
        """
        response = requests.get(f"{self.url}/vehicles")
        vehicles_data = response.json()
        vehicles = []
        for vehicle_data in vehicles_data:
            for key, value in params.items():
                if key in vehicle_data and vehicle_data[key] == value:
                    vehicles.append(Vehicle(**vehicle_data))
        return vehicles

    def get_vehicle(self, id: int) -> Vehicle:
        """Get a vehicle by its ID from the API.

        Args:
            vehicle_id: The ID of the vehicle.

        Returns:
            Vehicle: The Vehicle object corresponding to the ID.
        """
        response = requests.get(f"{self.url}/vehicles/{id}")
        vehicle_data = response.json()
        return Vehicle(**vehicle_data)

    def add_vehicle(self, vehicle: Vehicle) -> Vehicle:
        """Add a new vehicle to the API.

        Args:
            vehicle (Vehicle): The Vehicle object to add.

        Returns:
            Vehicle: The added Vehicle object.
        """
        data = vars(vehicle)
        data['id'] = max(
            vehicle.id for vehicle in self.get_vehicles() if vehicle.id) + 1
        response = requests.post(f"{self.url}/vehicles", json=data)
        print(response.text)
        return Vehicle(**response.json())

    def update_vehicle(self, vehicle: Vehicle) -> Vehicle:
        """Update an existing vehicle in the API.

        Args:
            vehicle: The updated Vehicle object.

        Returns:
            Vehicle: The updated Vehicle object.
        """
        data = vars(vehicle)
        response = requests.put(f"{self.url}/vehicles/{vehicle.id}", json=data)
        return Vehicle(**response.json())

    def delete_vehicle(self, id: int) -> None:
        """Delete a vehicle from the API.

        Args:
            id: The ID of the vehicle to delete.
        """
        requests.delete(f"{self.url}/vehicles/{id}")

    def get_distance(self, id1: int, id2: int):
        """Calculate the distance between two vehicles.

        Args:
            id1 (int): The ID of the first vehicle.
            id2 (int): The ID of the second vehicle.

        Returns:
            float: The distance between the vehicles in meters.
        """
        vehicle1 = self.get_vehicle(id1)
        vehicle2 = self.get_vehicle(id2)
        coord1 = Coordinates(vehicle1.latitude, vehicle1.longitude)
        coord2 = Coordinates(vehicle2.latitude, vehicle2.longitude)
        return self._get_distance(coord1, coord2)

    def get_nearest_vehicle(self, id: int):
        """Find the nearest vehicle to a given vehicle.

        Args:
            id: The ID of the reference vehicle.

        Returns:
            Vehicle: The nearest Vehicle object.
        """
        vehicles = self.get_vehicles()
        vehicle = self.get_vehicle(id)
        coord1 = Coordinates(vehicle.latitude, vehicle.longitude)
        min_distance = float('inf')
        nearest_vehicle = None
        for v in vehicles:
            if v.id != id:
                coord2 = Coordinates(v.latitude, v.longitude)
                distance = self._get_distance(coord1, coord2)
                if distance < min_distance:
                    min_distance = distance
                    nearest_vehicle = v
        return nearest_vehicle

    def _get_distance(self, coord1: Coordinates, coord2: Coordinates) -> float:
        """Calculate the distance between two sets of coordinates.

        Args:
            coord1 (Coordinates): The first set of coordinates.
            coord2 (Coordinates): The second set of coordinates.

        Returns:
            float: The distance between the coordinates in meters.
        """
        lo1 = radians(coord1.longitude)
        lo2 = radians(coord2.longitude)
        la1 = radians(coord1.latitude)
        la2 = radians(coord2.latitude)

        # Using the "Haversine formula"
        d_lo = lo2 - lo1
        d_la = la2 - la1
        P = sin(d_la / 2)**2 + cos(la1) * cos(la2) * sin(d_lo / 2)**2

        Q = 2 * asin(sqrt(P))

        return (Q * R_M)
