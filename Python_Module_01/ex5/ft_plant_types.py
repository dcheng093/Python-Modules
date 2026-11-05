#!/usr/bin/env python3

class Plant:
    def __init__(self, name: str, height: float, age: int,
                 growth_rate: float = 1.0) -> None:
        self.name = name
        self._height = 0.0
        self._age = 0
        self._growth_rate = growth_rate
        if self._is_valid(height, "height"):
            self._height = height
        if self._is_valid(age, "age"):
            self._age = age

    def _is_valid(self, value: float, field: str) -> bool:
        if value < 0:
            print(f"{self.name}: Error, {field} can't be negative")
            return False
        return True

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

    def age(self, days: int = 1) -> None:
        self._age += days

    def show(self) -> None:
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
    def __init__(self, name: str, height: float, age: int,
                 trunk_diameter: float, growth_rate: float = 1.0) -> None:
        super().__init__(name, height, age, growth_rate)
        self.trunk_diameter = trunk_diameter

    def produce_shade(self) -> None:
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


if __name__ == "__main__":
    print("=== Garden Plant Types ===")

    print("=== Flower")
    rose = Flower("Rose", 15.0, 10, "red")
    rose.show()
    print("[asking the rose to bloom]")
    rose.bloom()
    rose.show()

    print("\n=== Tree")
    oak = Tree("Oak", 200.0, 365, 5.0)
    oak.show()
    print("[asking the oak to produce shade]")
    oak.produce_shade()

    print("\n=== Vegetable")
    tomato = Vegetable("Tomato", 5.0, 10, "April", growth_rate=2.1)
    tomato.show()
    print("[make tomato grow and age for 20 days]")
    for _ in range(20):
        tomato.grow()
        tomato.age()
    tomato.show()

# class Plant:
#     def __init__(self, name, height, age):
#         self.name = name.capitalize()
#         self.height = height
#         self.age = age

#     def display(self):
#         print(f"{self.name} ({self.__class__.__name__}):", end=" ")
#         print(f"{self.height}cm, {self.age} days", end="")


# class Flower(Plant):
#     def __init__(self, name, height, age, color):
#         super().__init__(name, height, age)
#         self.color = color

#     def display(self):
#         super().display()
#         print(f", {self.color} color")

#     def bloom(self):
#         print(f"{self.name} is blooming beautifully!\n")


# class Tree(Plant):
#     def __init__(self, name, height, age, diameter):
#         super().__init__(name, height, age)
#         self.diameter = diameter

#     def display(self):
#         super().display()
#         print(f", {self.diameter} diameter")

#     def produce_shade(self):
#         shade = int(self.diameter * 3.14 / 2)
#         print(f"{self.name} provides {shade}", end=" ")
#         print("square meters of shade\n")


# class Vegetable(Plant):
#     def __init__(self, name, height, age, harvest_season, nutritional_value):
#         super().__init__(name, height, age)
#         self.harvest_season = harvest_season
#         self.nutritional_value = nutritional_value

#     def display(self):
#         super().display()
#         print(f", {self.harvest_season} harvest")
#         print(f"{self.name} is rich in vitamin {self.nutritional_value}")


# print("=== Garden Plant Types ===\n")
# flower = Flower("Rose", 25, 30, "red")
# flower.display()
# flower.bloom()
# tree = Tree("Oak", 500, 1825, 50)
# tree.display()
# tree.produce_shade()
# vegetable = Vegetable("Tomato", 80, 90, "summer", "C")
# vegetable.display()
