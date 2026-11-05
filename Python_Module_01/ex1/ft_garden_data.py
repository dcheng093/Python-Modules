#!/usr/bin/env python3


class Plant:
    def __init__(self, name: str, height: int, age: int) -> None:
        self.name = name.capitalize()
        self.height = height
        self.age = age

    def show(self) -> None:
        print(f"{self.name}: {self.height}cm, {self.age} days old")


if __name__ == "__main__":
    plant1 = Plant("rose", 25, 30)
    plant2 = Plant("sunflower", 80, 45)
    plant3 = Plant("cactus", 15, 120)
    print("=== Garden Plant Registry ===")
    plant1.show()
    plant2.show()
    plant3.show()

# class Plant:
#     def __init__(self, name, height, age):
#         self.name = name.capitalize()
#         self.height = height
#         self.age = age


# if __name__ == "__main__":
#     plant1 = Plant("rose", 25, 30)
#     plant2 = Plant("sunflower", 80, 45)
#     plant3 = Plant("cactus", 15, 120)
#     garden = [plant1, plant2, plant3]
#     print("=== Garden Plant Registry ===")
#     for plant in garden:
#         print(f"{plant.name}: {plant.height}cm, {plant.age} days old")
