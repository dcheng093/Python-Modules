#!/usr/bin/python3.10


class SecurePlant:
    def __init__(self, name: str, height: int, age: int) -> None:
        self._name = name.capitalize()
        self._height = height
        self._age = age
        print(f"Plant created: {self._name}: {float(self._height)}cm, "
              f"{self._age} days old\n")

    def get_height(self):
        return self._height

    def set_height(self, value: int):
        if value >= 0:
            self._height = value
            print(f"Height updated: {value}cm")
        else:
            print(f"{self._name}: Error, height can't be negative\n"
                  "Height update rejected")

    def get_age(self):
        return self._age

    def set_age(self, value: int):
        if value >= 0:
            self._age = value
            print(f"Age updated: {value} days\n")
        else:
            print(f"{self._name}: Error, age can't be negative\n"
                  "Age update rejected")

    def show(self):
        print(
            f"\nCurrent state: {self._name}: "
            f"{float(self._height)}cm, {self._age} days")


if __name__ == "__main__":
    print("=== Garden Security System ===")
    plant = SecurePlant("Rose", 15, 10)
    plant.set_height(25)
    plant.set_age(30)
    plant.set_height(-10000000000)
    plant.set_age(-10000000000)
    plant.show()

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
