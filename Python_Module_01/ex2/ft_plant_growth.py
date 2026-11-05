#!/usr/bin/env python3


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
    rose = Plant("Rose", 25.0, 30, growth_rate=0.8)
    start_height = rose.height
    print("=== Garden Plant Growth ===")
    rose.show()
    for day in range(1, 8):
        print(f"=== Day {day} ===")
        rose.grow()
        rose.age()
        rose.show()
    print(f"Growth this week: {round(rose.height - start_height, 1)}cm")

# class Plant:
#     def __init__(self, name, height, age):
#         self.name = name.capitalize()
#         self.height = height
#         self.age = age

#     def grow(self, cm):
#         self.height += cm

#     def age_by(self, days):
#         self.age += days

#     def get_info(self):
#         return (f"{self.name}: {self.height}cm, {self.age} days old")


# if __name__ == "__main__":
#     plant1 = Plant("Rose", 25, 30)
#     plant2 = Plant("Sunflower", 80, 45)
#     plant3 = Plant("Cactus", 15, 120)
#     garden = [plant1, plant2, plant3]

#     print("=== Day 1 ===")
#     for plant in garden:
#         print(plant.get_info())
#     days = 6
#     growth_per_plant = {"Rose": 6, "Sunflower": 200, "Cactus": 2}
#     for plant in garden:
#         plant.age_by(days)
#         plant.grow(growth_per_plant[plant.name])

#     print("\n=== Day 7 ===")
#     for plant in garden:
#         print(plant.get_info())
#         print(f"Growth this week: +{growth_per_plant[plant.name]}cm")
