#!/usr/bin/env python3.10

class Plant:
    def __init__(self, name, height, age):
        self.name = name
        self.height = height
        self.age = age

    def display(self):
        print(f"Created: {self.name} ({self.height}cm, {self.age} days)")


if __name__ == "__main__":
    plants = [Plant("Rose", 25, 30),
              Plant("Oak", 200, 365),
              Plant("Cactus", 5, 90),
              Plant("Sunflower", 80, 45),
              Plant("Fern", 15, 120)]
    print("=== Plant Factory Output ===")
    count = 0
    for plant in plants:
        plant.display()
        count += 1
    print(f"\nTotal plants created: {count}")
