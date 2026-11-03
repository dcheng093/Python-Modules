#!/usr/bin/python3.10

import math


def distance_between(pos1: tuple[float, float, float],
                     pos2: tuple[float, float, float]) -> float:
    x1, y1, z1 = pos1
    x2, y2, z2 = pos2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)


def get_player_pos() -> tuple[float, float, float]:
    while True:
        raw = input("Enter new coordinates as floats in format 'x,y,z': ")
        try:
            x_str, y_str, z_str = raw.split(",")
        except ValueError:
            print("Invalid syntax")
            continue
        current = x_str
        try:
            x = float(x_str)
            current = y_str
            y = float(y_str)
            current = z_str
            z = float(z_str)
        except ValueError as e:
            print(f"Error on parameter '{current.strip()}': {e}")
            continue
        return (x, y, z)


if __name__ == "__main__":
    print("=== Game Coordinate System ===")
    try:
        print("\nGet a first set of coordinates")
        pos1 = get_player_pos()
        print(f"Got a first tuple: {pos1}")
        print(f"It includes: X={pos1[0]}, Y={pos1[1]}, Z={pos1[2]}")
        center = (0.0, 0.0, 0.0)
        print("Distance to center: "
              f"{round(distance_between(center, pos1), 4)}")
        print("\nGet a second set of coordinates")
        pos2 = get_player_pos()
        print("Distance between the 2 sets of coordinates: "
              f"{round(distance_between(pos1, pos2), 4)}")
    except EOFError:
        print("\nInput closed - leaving the coordinate system.")

# def parse_coords(coord_str):
#     try:
#         x_str, y_str, z_str = coord_str.split(',')
#         return (int(x_str), int(y_str), int(z_str))
#     except Exception as e:
#         print(f"Error parsing coordinates: {e}")
#         print(f"Error details - Type: {type(e).__name__}, Args: {e.args}")
#         return None


# def show_unpacking(position):
#     x, y, z = position
#     print(f"Player at x={x}, y={y}, z={z}")
#     print(f"Coordinates: X={x}, Y={y}, Z={z}")


# if __name__ == "__main__":
#     print("=== Game Coordinate System ===\n")
    # pos1 = (10, 20, 5)
    # origin = (0, 0, 0)
    # print(f"Position created: {pos1}")
    # print(f"Distance between {origin} and {pos1}: "
    #       f"{distance_between(origin, pos1):.2f}\n")
    # parsed = "3,4,0"
    # print(f'Parsing coordinates: "{parsed}"')
    # print(f"Parsed position: {parse_coords(parsed)}")
    # print(f"Distance between {origin} and {parse_coords(parsed)}: "
    #       f"{distance_between(origin, parse_coords(parsed))}\n")
    # invalid = "abc,def,ghi"
    # print(f'Parsing invalid coordinates: "{invalid}"')
    # parse_coords(invalid)
    # print("\nUnpacking demonstration:")
    # parsed_pos = parse_coords(parsed)
    # show_unpacking(parsed_pos)
