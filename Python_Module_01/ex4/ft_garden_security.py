#!/usr/bin/python3.10


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


if __name__ == "__main__":
    print("=== Garden Security System ===")
    rose = Plant("Rose", 15.0, 10)
    print("Plant created:", end=" ")
    rose.show()
    print()
    rose.set_height(25)
    rose.set_age(30)
    print()
    rose.set_height(-5)
    rose.set_age(-3)
    print()
    print("Current state:", end=" ")
    rose.show()

# class SecurePlant:
#    def __init__(self, name, height, age):
#        self.__name = name.capitalize()
#        self.__height = height
#        self.__age = age
#        print(f"Plant created: {self.__name}")
#        print(f"Height updated: {self.__height}cm [OK]")
#        print(f"Age updated: {self.__age} days [OK]\n")

#    def get_height(self):
#        return self.__height

#    def set_height(self, value: int):
#        if value >= 0:
#            self.__height = value
#            print(f"Height updated: {value}cm [OK]")
#        else:
#           print(f"Invalid operation attempted: height {value}cm [REJECTED]")
#           print("Security: Negative height rejected\n")

#    def get_age(self):
#         return self.__age

#    def set_age(self, value: int):
#        if value >= 0:
#            self.__age = value
#            print(f"Age updated: {value} days [OK]")
#        else:
#            print(f"Invalid operation attempted: age {value} days [REJECTED]")
#            print("Security: Negative age rejected\n")

#    def display(self):
#        print(
#            f"Current plant: {self.__name} "
#            f"({self.__height}cm, {self.__age} days)")


# if __name__ == "__main__":
#     print("=== Garden Security System ===")
#     plant = SecurePlant("Rose", 25, 30)
#     plant.set_height(-5)
#     plant.set_age(-42)
#     plant.display()
