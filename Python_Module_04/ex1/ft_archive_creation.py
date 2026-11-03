#!/usr/bin/python3.10

import sys
import typing


def read_archive(filename: str) -> str | None:
    try:
        f: typing.IO[str] = open(filename, "r")
    except OSError as e:
        print(f"Error opening file '{filename}': {e}")
        return None
    try:
        content = f.read()
    except (OSError, ValueError) as e:
        print(f"Error reading file '{filename}': {e}")
        return None
    finally:
        f.close()
    print("---\n")
    print(content.rstrip("\n"))
    print("\n---")
    print(f"File '{filename}' closed.")
    return content


def transform_archive(content: str) -> str:
    lines = [line + "#" for line in content.splitlines()]
    new_content = "\n".join(lines) + "\n"
    print("\nTransform data:")
    print("---\n")
    print(new_content.rstrip("\n"))
    print("\n---")
    return new_content


def save_archive(filename: str, content: str) -> None:
    print(f"Saving data to '{filename}'")
    try:
        f: typing.IO[str] = open(filename, "w")
    except OSError as e:
        print(f"Error opening file '{filename}': {e}")
        print("Data not saved.")
        return
    try:
        f.write(content)
    except OSError as e:
        print(f"Error writing file '{filename}': {e}")
        print("Data not saved.")
        return
    finally:
        f.close()
    print(f"Data saved in file '{filename}'.")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_archive_creation.py <file>")
        return
    filename = sys.argv[1]
    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Accessing file '{filename}'")
    content = read_archive(filename)
    if content is None:
        return
    new_content = transform_archive(content)
    try:
        new_file = input("Enter new file name (or empty): ").strip()
    except EOFError:
        print()
        new_file = ""
    if new_file:
        save_archive(new_file, new_content)
    else:
        print("Not saving data.")


if __name__ == "__main__":
    main()

# print("=== CYBER ARCHIVES - PRESERVATION SYSTEM ===\n")
# newfile = "new_discovery.txt"
# print(f"Initializing new storage unit: {newfile}")
# try:
#     f = open(newfile, "w")
#     print("Storage unit created successfully...\n")
#     print("Inscribing preservation data...")
#     content = ("[ENTRY 001] New quantum algorithm discovered\n" +
#                "[ENTRY 002] Efficiency increased by 347%\n" +
#                "[ENTRY 003] Archived by Data Archivist trainee")
#     f.write(content)
#     print(content)
#     print("\nData inscription complete. Storage unit sealed.")
#     print(f"Archive '{newfile}' ready for long-term preservation.")
# except Exception as e:
#     print(e)
# finally:
#     if f:
#         f.close()
