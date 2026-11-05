#!/usr/bin/env python3

class GardenError(Exception):
    def __init__(self, message: str = "Unknown garden error") -> None:
        super().__init__(message)


class PlantError(GardenError):
    def __init__(self, message: str = "Unknown plant error") -> None:
        super().__init__(message)


class WaterError(GardenError):
    def __init__(self, message: str = "Unknown watering error") -> None:
        super().__init__(message)


def test_plant_error() -> None:
    print("\nTesting PlantError...")
    try:
        raise PlantError("The tomato plant is wilting!")
    except PlantError as e:
        print(f"Caught PlantError: {e}")


def test_water_error() -> None:
    print("\nTesting WaterError...")
    try:
        raise WaterError("Not enough water in the tank!")
    except WaterError as e:
        print(f"Caught WaterError: {e}")


def test_garden_error() -> None:
    print("\nTesting catching all garden errors...")

    try:
        raise PlantError("The tomato plant is wilting!")
    except GardenError as e:
        print(f"Caught GardenError: {e}")

    try:
        raise WaterError("Not enough water in the tank!")
    except GardenError as e:
        print(f"Caught GardenError: {e}")


if __name__ == "__main__":
    print("=== Custom Garden Errors Demo ===")

    test_plant_error()
    test_water_error()
    test_garden_error()

    print("\nAll custom error types work correctly!")

# class GardenError(Exception):
#     def __init__(self, message: str):
#         self.message = message

#     def __str__(self):
#         return f"Caught a garden error: {self.message}"


# class PlantError(GardenError):
#     def __str__(self):
#         return f"Caught PlantError: {self.message}"


# class WaterError(GardenError):
#     def __str__(self):
#         return f"Caught WaterError: {self.message}"


# def plant_error(plant: str):
#     print("Testing PlantError...")
#     try:
#         raise PlantError(f"The {plant} plant is wilting!")
#     except PlantError as e:
#         print(e)
#     print("")


# def water_error():
#     print("Testing WaterError...")
#     try:
#         raise WaterError("Not enough water in the tank!")
#     except WaterError as e:
#         print(e)
#     print("")


# def garden_error(plant: str):
#     print("Testing catching all garden errors...")
#     try:
#         raise GardenError(f"The {plant} plant is wilting!")
#     except GardenError as e:
#         print(e)
#     try:
#         raise GardenError("Not enough water in the tank!")
#     except GardenError as e:
#         print(e)
#     print("")


# if __name__ == "__main__":
#     print("=== Custom Garden Errors Demo ===\n")
#     plant_error("tomato")
#     water_error()
#     garden_error("tomato")
#     print("All custom error types work correctly!")
