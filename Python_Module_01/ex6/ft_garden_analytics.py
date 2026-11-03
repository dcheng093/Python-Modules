#!/usr/bin/env python3.10

class Plant:
    class _Stats:
        def __init__(self) -> None:
            self._grow = 0
            self._age = 0
            self._show = 0

        def add_grow(self) -> None:
            self._grow += 1

        def add_age(self) -> None:
            self._age += 1

        def add_show(self) -> None:
            self._show += 1

        def display(self) -> None:
            print(f"Stats: {self._grow} grow, {self._age} age, "
                  f"{self._show} show")

    def __init__(self, name: str, height: float, age: int,
                 growth_rate: float = 1.0) -> None:
        self.name = name
        self._height = 0.0
        self._age = 0
        self._growth_rate = growth_rate
        self._stats = Plant._Stats()
        if self._is_valid(height, "height"):
            self._height = height
        if self._is_valid(age, "age"):
            self._age = age

    @staticmethod
    def is_older_than_year(days: int) -> bool:
        return days > 365

    @classmethod
    def anonymous(cls) -> "Plant":
        return cls("Unknown plant", 0.0, 0)

    def _is_valid(self, value: float, field: str) -> bool:
        if value < 0:
            print(f"{self.name}: Error, {field} can't be negative")
            return False
        return True

    def get_stats(self) -> "Plant._Stats":
        return self._stats

    def get_height(self) -> float:
        return self._height

    def set_height(self, height: float) -> None:
        if self._is_valid(height, "height"):
            self._height = height
            print(f"Height updated: {height}cm")
        else:
            print("Height update rejected")

    def get_age(self) -> int:
        return self._age

    def set_age(self, age: int) -> None:
        if self._is_valid(age, "age"):
            self._age = age
            print(f"Age updated: {age} days")
        else:
            print("Age update rejected")

    def grow(self) -> None:
        self._height += self._growth_rate
        self._stats.add_grow()

    def age(self, days: int = 1) -> None:
        self._age += days
        self._stats.add_age()

    def show(self) -> None:
        self._stats.add_show()
        print(f"{self.name}: {self._height:.1f}cm, {self._age} days old")


class Flower(Plant):
    def __init__(self, name: str, height: float, age: int, color: str,
                 growth_rate: float = 1.0) -> None:
        super().__init__(name, height, age, growth_rate)
        self.color = color
        self.bloomed = False

    def bloom(self) -> None:
        self.bloomed = True

    def show(self) -> None:
        super().show()
        print(f"Color: {self.color}")
        if self.bloomed:
            print(f"{self.name} is blooming beautifully!")
        else:
            print(f"{self.name} has not bloomed yet")


class Tree(Plant):
    class _Stats(Plant._Stats):
        def __init__(self) -> None:
            super().__init__()
            self._shade = 0

        def add_shade(self) -> None:
            self._shade += 1

        def display(self) -> None:
            super().display()
            print(f"{self._shade} shade")

    def __init__(self, name: str, height: float, age: int,
                 trunk_diameter: float, growth_rate: float = 1.0) -> None:
        super().__init__(name, height, age, growth_rate)
        self.trunk_diameter = trunk_diameter
        self._tree_stats = Tree._Stats()
        self._stats = self._tree_stats

    def produce_shade(self) -> None:
        self._tree_stats.add_shade()
        print(f"Tree {self.name} now produces a shade of "
              f"{self.get_height():.1f}cm long and "
              f"{self.trunk_diameter:.1f}cm wide.")

    def show(self) -> None:
        super().show()
        print(f"Trunk diameter: {self.trunk_diameter:.1f}cm")


class Vegetable(Plant):
    def __init__(self, name: str, height: float, age: int,
                 harvest_season: str, growth_rate: float = 1.0) -> None:
        super().__init__(name, height, age, growth_rate)
        self.harvest_season = harvest_season
        self.nutritional_value = 0.0

    def grow(self) -> None:
        super().grow()
        self.nutritional_value += 0.5

    def age(self, days: int = 1) -> None:
        super().age(days)
        self.nutritional_value += 0.5 * days

    def show(self) -> None:
        super().show()
        print(f"Harvest season: {self.harvest_season}")
        print(f"Nutritional value: {round(self.nutritional_value)}")


class Seed(Flower):
    def __init__(self, name: str, height: float, age: int, color: str,
                 growth_rate: float = 1.0) -> None:
        super().__init__(name, height, age, color, growth_rate)
        self.seeds = 0

    def bloom(self) -> None:
        super().bloom()
        self.seeds = 42

    def show(self) -> None:
        super().show()
        print(f"Seeds: {self.seeds}")


def show_stats(plant: Plant) -> None:
    print(f"[statistics for {plant.name}]")
    plant.get_stats().display()


if __name__ == "__main__":
    print("=== Garden statistics ===")

    print("=== Check year-old")
    print("Is 30 days more than a year? -> "
          f"{Plant.is_older_than_year(30)}")
    print("Is 400 days more than a year? -> "
          f"{Plant.is_older_than_year(400)}")

    print("\n=== Flower")
    rose = Flower("Rose", 15.0, 10, "red", growth_rate=8.0)
    rose.show()
    show_stats(rose)
    print("[asking the rose to grow and bloom]")
    rose.grow()
    rose.bloom()
    rose.show()
    show_stats(rose)

    print("\n=== Tree")
    oak = Tree("Oak", 200.0, 365, 5.0)
    oak.show()
    show_stats(oak)
    print("[asking the oak to produce shade]")
    oak.produce_shade()
    show_stats(oak)

    print("\n=== Seed")
    sunflower = Seed("Sunflower", 80.0, 45, "yellow", growth_rate=30.0)
    sunflower.show()
    print("[make sunflower grow, age and bloom]")
    sunflower.grow()
    sunflower.age(20)
    sunflower.bloom()
    sunflower.show()
    show_stats(sunflower)

    print("\n=== Anonymous")
    unknown = Plant.anonymous()
    unknown.show()
    show_stats(unknown)

# class Plant:
#     def __init__(self, name: str, height: int):
#         self.name = name.capitalize()
#         self.height = height

#     def grow(self):
#         self.height = self.height + 1
#         print(f"{self.name} grew 1cm")

#     def display(self):
#         print(f"- {self.name}: {self.height}cm")


# class FloweringPlant(Plant):
#     def __init__(self, name: str, height: int, color: str):
#         super().__init__(name, height)
#         self.color = color

#     def display(self):
#         print(f"- {self.name}: {self.height}cm, "
#               f"{self.color} flowers (blooming)")


# class PrizeFlower(FloweringPlant):
#     def __init__(self, name: str, height: int, color: str, points: int):
#         super().__init__(name, height, color)
#         self.points = points

#     def display(self):
#         print(f"- {self.name}: {self.height}cm, "
#               f"{self.color} flowers (blooming), "
#               f"Prize points: {self.points}")


# class Garden:
#     def __init__(self, owner: str):
#         self.owner = owner
#         self.plants = []

#     def add_plant(self, plant, announce=True):
#         self.plants = self.plants + [plant]
#         if announce:
#             print(f"Added {plant.name} to {self.owner}'s garden")

#     def grow_all(self):
#         print(f"{self.owner} is helping all plants grow...")
#         for plant in self.plants:
#             plant.grow()

#     def display(self):
#         print(f"=== {self.owner}'s Garden Report ===")
#         print("Plants in garden:")
#         for plant in self.plants:
#             plant.display()


# class GardenManager:
#     total_gardens = 0

#     class GardenStats:
#         @staticmethod
#         def total_growth(plants):
#             return len(plants)

#         @staticmethod
#         def plant_types(plants):
#             regular = flowering = prize = 0
#             for plant in plants:
#                 if isinstance(plant, PrizeFlower):
#                     prize += 1
#                 elif isinstance(plant, FloweringPlant):
#                     flowering += 1
#                 else:
#                     regular += 1
#             return regular, flowering, prize

#     @staticmethod
#     def calculate_garden_score(garden: Garden):
#         score = 0
#         for plant in garden.plants:
#             score += plant.height
#             if isinstance(plant, PrizeFlower):
#                 score += plant.points * 4
#         return score

#     def __init__(self):
#         self.gardens = {}

#     def add_garden(self, garden: Garden):
#         self.gardens[garden.owner] = garden
#         GardenManager.total_gardens += 1

#     @classmethod
#     def total_managed(cls):
#         return cls.total_gardens

#     @staticmethod
#     def validate_height(height):
#         return height > 0

#     @classmethod
#     def create_garden_network(cls):
#         return cls()


# if __name__ == "__main__":
#     print("=== Garden Management System Demo ===\n")
#     manager = GardenManager.create_garden_network()
#     alice = Garden("Alice")
#     bob = Garden("Bob")
#     bob.add_plant(Plant("cactus", 92), announce=False)
#     manager.add_garden(alice)
#     manager.add_garden(bob)
#     alice.add_plant(Plant("oak tree", 100))
#     alice.add_plant(FloweringPlant("rose", 25, "red"))
#     alice.add_plant(PrizeFlower("sunflower", 50, "yellow", 10))
#     print(" ")
#     alice.grow_all()
#     print(" ")
#     alice.display()
#     print(" ")
#     alice_score = GardenManager.calculate_garden_score(alice)
#     bob_score = GardenManager.calculate_garden_score(bob)
#     regular, flowering, prize = (
#         GardenManager.GardenStats.plant_types(alice.plants))
#     total_growth = GardenManager.GardenStats.total_growth(alice.plants)
#   print(f"Plants added: {len(alice.plants)}, Total growth: {total_growth}cm")
#     print(f"Plant types: {regular} regular, {flowering} flowering, {prize} "
#           "prize flowers")
#     print(" ")
#     print("Height validation test:", GardenManager.validate_height(10))
#     print(f"Garden scores - Alice: {alice_score}, Bob: {bob_score}")
#     print("Total gardens managed:", GardenManager.total_managed())
