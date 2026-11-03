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


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_ancient_text.py <file>")
        return
    filename = sys.argv[1]
    print("=== Cyber Archives Recovery ===")
    print(f"Accessing file '{filename}'")
    read_archive(filename)


if __name__ == "__main__":
    main()

# print("=== CYBER ARCHIVES - DATA RECOVERY SYSTEM ===\n")
# filename = "ancient_fragment.txt"
# print(f"Accessing Storage Vault: {filename}")
# try:
#     f = open(filename, "r")
#     print("Connection established...\n")
#     print("RECOVERED DATA:")
#     content = f.read()
#     print(content)
#     print("\nData recovery complete. Storage unit disconnected.")
# except FileNotFoundError:
#     print("ERROR: Storage vault not found. Run data generator first.")
# finally:
#     if f:
#         f.close()
