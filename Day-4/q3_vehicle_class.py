from datetime import datetime, timedelta

# -------- Maintenance Record --------
class MaintenanceRecord:
    def __init__(self):
        self.last_service_date = datetime.now()
        self.issues_reported = []

    def report_issue(self, issue):
        self.issues_reported.append(issue)

    def service(self):
        self.last_service_date = datetime.now()
        self.issues_reported = []

# -------- Base Class: Vehicle --------
class Vehicle(MaintenanceRecord):
    def __init__(self, vehicle_id, make, model, year, daily_rate, mileage, fuel_type):
        super().__init__()
        self.vehicle_id = vehicle_id
        self.make = make
        self.model = model
        self.year = year
        self.daily_rate = daily_rate
        self.is_available = True
        self.mileage = mileage
        self.fuel_type = fuel_type

    def rent(self):
        if self.is_available:
            self.is_available = False
            return "Rented successfully!"
        return "Vehicle not available"

    def return_vehicle(self):
        self.is_available = True
        return "Returned successfully!"

    def calculate_rental_cost(self, days):
        return self.daily_rate * days

    def get_vehicle_info(self):
        return {
            "vehicle_id": self.vehicle_id,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "daily_rate": self.daily_rate,
            "is_available": self.is_available,
            "mileage": self.mileage,
            "fuel_type": self.fuel_type
        }

    def get_fuel_efficiency(self):
        return {
            "city_mpg": 20,
            "highway_mpg": 25
        }

# -------- Derived Class: Car --------
class Car(Vehicle):
    def __init__(self, vehicle_id, make, model, year, daily_rate, mileage, seating_capacity, transmission_type, has_gps):
        super().__init__(vehicle_id, make, model, year, daily_rate, mileage, "Petrol")
        self.seating_capacity = seating_capacity
        self.transmission_type = transmission_type
        self.has_gps = has_gps

    def calculate_rental_cost(self, days):
        return self.daily_rate * days

    def get_vehicle_info(self):
        info = super().get_vehicle_info()
        info.update({
            "seating_capacity": self.seating_capacity,
            "transmission_type": self.transmission_type,
            "has_gps": self.has_gps
        })
        return info

    def get_fuel_efficiency(self):
        return {
            "city_mpg": 28,
            "highway_mpg": 35
        }

# -------- Derived Class: Motorcycle --------
class Motorcycle(Vehicle):
    def __init__(self, vehicle_id, make, model, year, daily_rate, mileage, engine_cc, bike_type):
        super().__init__(vehicle_id, make, model, year, daily_rate, mileage, "Petrol")
        self.engine_cc = engine_cc
        self.bike_type = bike_type

    def calculate_rental_cost(self, days):
        cost = self.daily_rate * days
        if days <= 7:
            cost *= 0.8  # 20% discount
        return cost

    def get_vehicle_info(self):
        info = super().get_vehicle_info()
        info.update({
            "engine_cc": self.engine_cc,
            "bike_type": self.bike_type
        })
        return info

    def get_fuel_efficiency(self):
        return 48.0

# -------- Derived Class: Truck --------
class Truck(Vehicle):
    def __init__(self, vehicle_id, make, model, year, daily_rate, mileage, cargo_capacity, license_required, max_weight):
        super().__init__(vehicle_id, make, model, year, daily_rate, mileage, "Diesel")
        self.cargo_capacity = cargo_capacity
        self.license_required = license_required
        self.max_weight = max_weight

    def calculate_rental_cost(self, days):
        base_cost = self.daily_rate * days
        return base_cost + (base_cost * 0.5)

    def get_vehicle_info(self):
        info = super().get_vehicle_info()
        info.update({
            "cargo_capacity": self.cargo_capacity,
            "license_required": self.license_required,
            "max_weight": self.max_weight
        })
        return info

    def get_fuel_efficiency(self):
        return {
            "city_mpg": 10,
            "highway_mpg": 15,
            "empty_mpg": 18,
            "loaded_mpg": 12
        }


car = Car("CAR001", "Toyota", "Camry", 2023, 45.0, 5, 5, "Automatic", True)
motorcycle = Motorcycle("BIKE001", "Harley", "Street 750", 2022, 35.0, 75, 750, "Cruiser")
truck = Truck("TRUCK001", "Ford", "F-150", 2023, 85.0, 15000, 1200, "CDL-A", 5000)

# Test Case 1
assert car.seating_capacity == 5
assert motorcycle.engine_cc == 750
assert truck.cargo_capacity == 1200

# Test Case 2
assert car.is_available == True
rental_result = car.rent()
assert car.is_available == False
assert "rented successfully" in rental_result.lower()

return_result = car.return_vehicle()
assert car.is_available == True

# Test Case 3: Type-specific rental cost
car_cost = car.calculate_rental_cost(3)
assert car_cost == 45.0 * 3

bike_cost = motorcycle.calculate_rental_cost(2)
expected_bike = 35.0 * 2 * 0.8
assert abs(bike_cost - expected_bike) < 0.01

truck_cost = truck.calculate_rental_cost(2)
expected_truck = 85.0 * 2 * 1.5
assert abs(truck_cost - expected_truck) < 0.01

# Test Case 4: Polymorphism
vehicles = [car, motorcycle, truck]
total_fleet_value = 0
for vehicle in vehicles:
    info = vehicle.get_vehicle_info()
    assert info["make"] == vehicle.make
    if hasattr(vehicle, "seating_capacity"):
        assert str(vehicle.seating_capacity) in info.values() or str(vehicle.seating_capacity) in str(info)
    elif hasattr(vehicle, "engine_cc"):
        assert str(vehicle.engine_cc) in info.values() or str(vehicle.engine_cc) in str(info)

# Test Case 5: Fuel efficiency
car_efficiency = car.get_fuel_efficiency()
assert isinstance(car_efficiency, dict)
assert "city_mpg" in car_efficiency
assert "highway_mpg" in car_efficiency

bike_efficiency = motorcycle.get_fuel_efficiency()
assert isinstance(bike_efficiency, float)
assert bike_efficiency > 40

truck_efficiency = truck.get_fuel_efficiency()
assert isinstance(truck_efficiency, dict)
assert "empty_mpg" in truck_efficiency
assert "loaded_mpg" in truck_efficiency

print("✅ All tests passed!")