#!/usr/bin/env python3.10

class Plant:
    class _Stats:
        def __init__(self):
            self.grow_calls = 0
            self.age_calls = 0
            self.show_calls = 0

        def display(self):
            print(f"Stats: {self.grow_calls} grow, "
                  f"{self.age_calls} age, {self.show_calls} show")

    def __init__(self, name: str, height: int, age: int):
        self.name = name.capitalize()
        self.height = height
        self.age = age
        self._stats = self._Stats()

    @staticmethod
    def is_older_than_year(days: int) -> bool:
        return days > 365

# @classmethod exists comes down to clean object-oriented design
# Create objects in different formats or track global class data.

    @classmethod
    def anonymous(cls):
        return cls("Unknown plant", 0, 0)

    def grow(self, cm):
        self.height += cm
        self._stats.grow_calls += 1

    def age_by(self, days):
        self.age += days
        self._stats.age_calls += 1

    def show(self):
        self._stats.show_calls += 1
        print(f"{self.name}: {float(self.height)}cm, {self.age} days old")


class Flower(Plant):
    def __init__(self, name, height, age, color):
        super().__init__(name, height, age)
        self.color = color
        self.bloomed = False

    def show(self):
        super().show()
        print(f" Color: {self.color}")
        if not self.bloomed:
            print(f" {self.name} has not bloomed yet")
        else:
            print(f" {self.name} is blooming beautifully!")

    def bloom(self):
        self.bloomed = True


class Tree(Plant):
    def __init__(self, name, height, age, trunk_diameter):
        super().__init__(name, height, age)
        self.diameter = trunk_diameter
        self._shade_calls = 0

    def show(self):
        super().show()
        print(f" Trunk diameter: {float(self.diameter)}cm")

    def produce_shade(self):
        self._shade_calls += 1
        print(f"{self.__class__.__name__} {self.name} now produces a shade of "
              f"{float(self.height)}cm long and "
              f"{float(self.diameter)}cm wide.")


class Vegetable(Plant):
    def __init__(self, name, height, age, harvest_season, nutritional_value):
        super().__init__(name, height, age)
        self.harvest_season = harvest_season
        self.nutritional_value = nutritional_value

    def show(self):
        super().show()
        print(f"Harvest season: {self.harvest_season}")
        print(f"Nutritional value: {self.nutritional_value}")


class Seed(Flower):
    def __init__(self, name, height, age, color):
        super().__init__(name, height, age, color)
        self.seeds = 0

    def show(self):
        super().show()
        print(f" Seeds: {self.seeds}")

    def bloom(self):
        super().bloom()
        self.seeds = 42  # example value


# global function
def show_stats(plant):
    print(f"[statistics for {plant.name.capitalize()}]")
    plant._stats.display()
    if hasattr(plant, "_shade_calls"):
        print(f" {plant._shade_calls} shade")


if __name__ == "__main__":
    print("=== Garden statistics ===")

    # static method
    print("=== Check year-old")
    print(f"Is 30 days more than a year? -> "
          f"{Plant.is_older_than_year(30)}")
    print(f"Is 400 days more than a year? -> "
          f"{Plant.is_older_than_year(400)}")

    # flour
    print("\n=== Flower")
    flower = Flower("Rose", 15, 10, "red")
    flower.show()
    show_stats(flower)
    print(f"[asking the {flower.name.lower()} to grow and bloom]")
    flower.grow(8)
    flower.bloom()
    flower.show()
    show_stats(flower)

    # three
    print("\n=== Tree")
    tree = Tree("Oak", 200, 365, 5)
    tree.show()
    show_stats(tree)
    print(f"[asking the {tree.name.lower()} to produce shade]")
    tree.produce_shade()
    show_stats(tree)

    # sad
    print("\n=== Seed")
    seed = Seed("Sunflower", 80, 45, "yellow")
    seed.show()
    print(f"[make {seed.name.lower()} grow, age and bloom]")
    seed.grow(30)
    seed.age_by(20)
    seed.bloom()
    seed.show()
    show_stats(seed)

    # 4chan
    print("\n=== Anonymous")
    anon = Plant.anonymous()
    anon.show()
    show_stats(anon)


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
