#!/usr/bin/python3.10

class SecurePlant:
    def __init__(self, name, height, age):
        self.__name = name
        self.__height = height
        self.__age = age
        print(f"Plant created: {self.__name}")
        print(f"Height updated: {self.__height}cm [OK]")
        print(f"Age updated: {self.__age} days [OK]\n")

    def get_height(self):
        return self.__height

    def set_height(self, value: int):
        if value >= 0:
            self.__height = value
            print(f"Height updated: {value}cm [OK]")
        else:
            print(f"Invalid operation attempted: height {value}cm [REJECTED]")
            print("Security: Negative height rejected\n")

    def get_age(self):
        return self.__age

    def set_age(self, value: int):
        if value >= 0:
            self.__age = value
            print(f"Age updated: {value} days [OK]")
        else:
            print(f"Invalid operation attempted: age {value} days [REJECTED]")
            print("Security: Negative age rejected\n")

    def display(self):
        print(
            f"Current plant: {self.__name} "
            f"({self.__height}cm, {self.__age} days)")


if __name__ == "__main__":
    print("=== Garden Security System ===")
    plant = SecurePlant("Rose", 25, 30)
    plant.set_height(-5)
    plant.set_age(-42)
    plant.display()
