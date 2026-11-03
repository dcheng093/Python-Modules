#!/usr/bin/python3.10

def garden_operations(operation_number: int) -> None:
    if operation_number == 0:
        int("abc")
    elif operation_number == 1:
        1 / 0
    elif operation_number == 2:
        open("/non/existent/file")
    elif operation_number == 3:
        "hello" + 5
    else:
        return


def test_error_types() -> None:
    print("=== Garden Error Types Demo ===")
    for i in range(5):
        print(f"Testing operation {i}...")
        try:
            garden_operations(i)
            print("Operation completed successfully")
        except (ValueError, ZeroDivisionError,
                FileNotFoundError, TypeError) as e:
            print(f"Caught {e.__class__.__name__}: {e}")
    print("\nAll error types tested successfully!")


if __name__ == "__main__":
    test_error_types()

# def garden_operations():
#     try:
#         print("Testing ValueError...")
#         int("abc")
#     except ValueError:
#         print("Caught ValueError: invalid literal for int()\n")
#     try:
#         print("Testing ZeroDivisionError...")
#         1 / 0
#     except ZeroDivisionError:
#         print("Caught ZeroDivisionError: division by zero\n")
#     try:
#         print("Testing FileNotFoundError...")
#         open("missing.txt")
#     except FileNotFoundError:
#         print("Caught FileNotFoundError: No such file 'missing.txt'\n")
#     try:
#         print("Testing KeyError...")
#         missing = {"flowers": 5}
#         print(missing["plant"])
#     except KeyError:
#         print("Caught KeyError: 'missing\\_plant'\n")
#     try:
#         print("Testing multiple errors together...")
#         int("abc")
#     except (ValueError, ZeroDivisionError, FileNotFoundError, KeyError):
#         print("Caught an error, but program continues!\n")

#     print("All error types tested successfully!")


# def test_error_types():
#     print("=== Garden Error Types Demo ===\n")
#     garden_operations()


# if __name__ == "__main__":
#     test_error_types()
