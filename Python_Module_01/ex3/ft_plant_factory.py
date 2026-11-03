#!/usr/bin/env python3.10


class Plant:
    def __init__(self, name: str, height: float, age: int,
                 growth_rate: float = 1.0) -> None:
        self.name = name
        self.height = height
        self.days_old = age
        self.growth_rate = growth_rate

    def grow(self) -> None:
        self.height += self.growth_rate

    def age(self, days: int = 1) -> None:
        self.days_old += days

    def show(self) -> None:
        print(f"{self.name}: {self.height:.1f}cm, {self.days_old} days old")


if __name__ == "__main__":
    plants: list[Plant] = [Plant("Rose", 25.0, 30, 0.8),
                           Plant("Oak", 200.0, 365, 0.2),
                           Plant("Cactus", 5.0, 90, 0.1),
                           Plant("Sunflower", 80.0, 45, 3.0),
                           Plant("Fern", 15.0, 120, 0.5)]
    print("=== Plant Factory Output ===")
    for plant in plants:
        print("Created:", end=" ")
        plant.show()

# class Plant:
#     def __init__(self, name, height, age):
#         self.name = name.capitalize()
#         self.height = height
#         self.age = age

#     def display(self):
#         print(f"Created: {self.name} ({self.height}cm, {self.age} days)")


# if __name__ == "__main__":
#     plants = [Plant("Rose", 25, 30),
#               Plant("Oak", 200, 365),
#               Plant("Cactus", 5, 90),
#               Plant("Sunflower", 80, 45),
#               Plant("Fern", 15, 120)]
#     print("=== Plant Factory Output ===")
#     count = 0
#     for plant in plants:
#         plant.display()
#         count += 1
#     print(f"\nTotal plants created: {count}")
