from abc import ABC, abstractmethod

class Vehicle(ABC):
    def __init__(self, plate: str, owner: str):
        self.plate = plate
        self.owner = owner

    @abstractmethod
    def parking_rate(self) -> float:
        pass


class Car(Vehicle):
    def parking_rate(self) -> float:
        return 30.0


class Truck(Vehicle):
    def __init__(self, plate: str, owner: str, weight_tons: float):
        super().__init__(plate, owner)
        self.weight_tons = weight_tons

    def parking_rate(self) -> float:
        return 50 + self.weight_tons * 5


class ParkingLot:
    def __init__(self):
        self.__parked = {}  

    def park(self, vehicle, entry_hour: float):
        self.__parked[vehicle.plate] = (vehicle, entry_hour)
        print(f"{vehicle.plate} припарковано о {entry_hour} год.")

    def leave(self, plate: str, exit_hour: float) -> dict:
        if plate not in self.__parked:
            return {"error": "Автомобіль не знайдено"}

        vehicle, entry_hour = self.__parked.pop(plate)

        hours = exit_hour - entry_hour
        cost = hours * vehicle.parking_rate()

        return {
            "plate": plate,
            "owner": vehicle.owner,
            "hours": hours,
            "rate_per_hour": vehicle.parking_rate(),
            "total_cost": cost
        }

    def list_parked(self):
        if not self.__parked:
            print("Паркінг порожній")
            return

        print("Припарковані транспортні засоби:")
        for plate, (vehicle, entry_hour) in self.__parked.items():
            print(
                f"Номер: {plate}, Власник: {vehicle.owner}, "
                f"Час в'їзду: {entry_hour}"
            )


def calculate_parking_cost(
        vehicle_type: str,
        hours: float,
        weight_tons: float = 0
) -> dict:

    if vehicle_type.lower() == "car":
        vehicle = Car("TEMP001", "Тимчасовий власник")

    elif vehicle_type.lower() == "truck":
        vehicle = Truck(
            "TEMP002",
            "Тимчасовий власник",
            weight_tons
        )

    else:
        return {"error": "Невідомий тип транспорту"}

    rate = vehicle.parking_rate()
    cost = rate * hours

    return {
        "vehicle_type": vehicle_type,
        "hours": hours,
        "rate_per_hour": rate,
        "total_cost": cost
    }


parking = ParkingLot()

car1 = Car("AA1111AA", "Іван")
truck1 = Truck("BC2222BC", "Петро", 8)

parking.park(car1, 9.0)
parking.park(truck1, 10.0)

parking.list_parked()

print("\nВиїзд автомобіля:")
print(parking.leave("AA1111AA", 13.5))

print("\nВиїзд вантажівки:")
print(parking.leave("BC2222BC", 15.0))


print("\n=== AI-Агент ===")

print("Запит 1:")
print(calculate_parking_cost("car", 3))

print("\nЗапит 2:")
print(calculate_parking_cost("truck", 4, 5))

print("\nЗапит 3:")
print(calculate_parking_cost("truck", 2.5, 12))