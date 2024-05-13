import pytest
from vehicle_manager import VehicleManager, Vehicle


@pytest.fixture
def manager() -> VehicleManager:
    return VehicleManager(url="https://test.tspb.su/test-task")


def test_get_vehicles(manager: VehicleManager):
    vehicles = manager.get_vehicles()
    assert len(vehicles) > 0
    assert isinstance(vehicles[0], Vehicle)


def test_filter_vehicles(manager: VehicleManager):
    vehicles = manager.filter_vehicles(params={"name": "Toyota"})
    assert len(vehicles) > 0
    for vehicle in vehicles:
        assert vehicle.name == "Toyota"


def test_get_vehicle(manager: VehicleManager):
    vehicle = manager.get_vehicle(id=1)
    assert vehicle.id == 1


def test_add_vehicle(manager: VehicleManager):
    new_vehicle = Vehicle(
        name='Toyota',
        model='Camry',
        year=2021,
        color='red',
        price=21000,
        latitude=55.753215,
        longitude=37.620393
    )
    added_vehicle = manager.add_vehicle(vehicle=new_vehicle)
    assert added_vehicle.name == new_vehicle.name


def test_update_vehicle(manager: VehicleManager):
    vehicle = Vehicle(
        id=1,
        name='Toyota',
        model='Camry',
        year=2021,
        color='red',
        price=21000,
        latitude=55.753215,
        longitude=37.620393
    )
    updated_vehicle = manager.update_vehicle(vehicle=vehicle)
    assert updated_vehicle == vehicle


def test_delete_vehicle(manager: VehicleManager):
    manager.delete_vehicle(id=1)


def test_get_distance(manager: VehicleManager):
    distance = manager.get_distance(id1=1, id2=2)
    assert isinstance(distance, float)


def test_get_nearest_vehicle(manager: VehicleManager):
    nearest_vehicle = manager.get_nearest_vehicle(id=1)
    assert isinstance(nearest_vehicle, Vehicle)
