#!/usr/bin/python3.10

class Plant:
    def __init__(self, name: str, height: int):
        self.name = name.capitalize()
        self.height = height

    def grow(self):
        self.height = self.height + 1
        print(f"{self.name} grew 1cm")

    def display(self):
        print(f"- {self.name}: {self.height}cm")


class FloweringPlant(Plant):
    def __init__(self, name: str, height: int, color: str):
        super().__init__(name, height)
        self.color = color

    def display(self):
        print(f"- {self.name}: {self.height}cm, "
              f"{self.color} flowers (blooming)")


class PrizeFlower(FloweringPlant):
    def __init__(self, name: str, height: int, color: str, points: int):
        super().__init__(name, height, color)
        self.points = points

    def display(self):
        print(f"- {self.name}: {self.height}cm, "
              f"{self.color} flowers (blooming), "
              f"Prize points: {self.points}")


class Garden:
    def __init__(self, owner: str):
        self.owner = owner
        self.plants = []

    def add_plant(self, plant, announce=True):
        self.plants.append(plant)
        if announce:
            print(f"Added {plant.name} to {self.owner}'s garden")

    def grow_all(self):
        print(f"{self.owner} is helping all plants grow...")
        for plant in self.plants:
            plant.grow()

    def display(self):
        print(f"=== {self.owner}'s Garden Report ===")
        print("Plants in garden:")
        for plant in self.plants:
            plant.display()


class GardenManager:
    total_gardens = 0

    class GardenStats:
        @staticmethod
        def total_growth(plants):
            return len(plants)

        @staticmethod
        def plant_types(plants):
            regular = flowering = prize = 0
            for p in plants:
                if isinstance(p, PrizeFlower):
                    prize += 1
                elif isinstance(p, FloweringPlant):
                    flowering += 1
                else:
                    regular += 1
            return regular, flowering, prize

    @staticmethod
    def calculate_garden_score(garden: Garden):
        score = 0
        for plant in garden.plants:
            score += plant.height
            if isinstance(plant, PrizeFlower):
                score += plant.points * 4
        return score

    def __init__(self):
        self.gardens = {}

    def add_garden(self, garden: Garden):
        self.gardens[garden.owner] = garden
        GardenManager.total_gardens += 1

    @classmethod
    def total_managed(cls):
        return cls.total_gardens

    @staticmethod
    def validate_height(height):
        return height > 0

    @classmethod
    def create_garden_network(cls):
        return cls()


if __name__ == "__main__":
    print("=== Garden Management System Demo ===\n")
    manager = GardenManager.create_garden_network()
    alice = Garden("Alice")
    bob = Garden("Bob")
    bob.add_plant(Plant("cactus", 92), announce=False)
    manager.add_garden(alice)
    manager.add_garden(bob)
    alice.add_plant(Plant("oak tree", 100))
    alice.add_plant(FloweringPlant("rose", 25, "red"))
    alice.add_plant(PrizeFlower("sunflower", 50, "yellow", 10))
    print(" ")
    alice.grow_all()
    print(" ")
    alice.display()
    print(" ")
    alice_score = GardenManager.calculate_garden_score(alice)
    bob_score = GardenManager.calculate_garden_score(bob)
    regular, flowering, prize = (
        GardenManager.GardenStats.plant_types(alice.plants))
    total_growth = GardenManager.GardenStats.total_growth(alice.plants)
    print(f"Plants added: {len(alice.plants)}, Total growth: {total_growth}cm")
    print(f"Plant types: {regular} regular, {flowering} flowering, {prize} "
          "prize flowers")
    print(" ")
    print("Height validation test:", GardenManager.validate_height(10))
    print(f"Garden scores - Alice: {alice_score}, Bob: {bob_score}")
    print("Total gardens managed:", GardenManager.total_managed())
