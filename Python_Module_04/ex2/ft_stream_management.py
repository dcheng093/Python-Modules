#!/usr/bin/python3.10

import sys
import typing


def read_archive(filename: str) -> str | None:
    try:
        f: typing.IO[str] = open(filename, "r")
    except OSError as e:
        print(f"[STDERR] Error opening file '{filename}': {e}",
              file=sys.stderr)
        return None
    try:
        content = f.read()
    except (OSError, ValueError) as e:
        print(f"[STDERR] Error reading file '{filename}': {e}",
              file=sys.stderr)
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
        print(f"[STDERR] Error opening file '{filename}': {e}",
              file=sys.stderr)
        print("Data not saved.")
        return
    try:
        f.write(content)
    except OSError as e:
        print(f"[STDERR] Error writing file '{filename}': {e}",
              file=sys.stderr)
        print("Data not saved.")
        return
    finally:
        f.close()
    print(f"Data saved in file '{filename}'.")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_stream_management.py <file>", file=sys.stderr)
        return
    filename = sys.argv[1]
    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Accessing file '{filename}'")
    content = read_archive(filename)
    if content is None:
        return
    new_content = transform_archive(content)
    sys.stdout.write("Enter new file name (or empty): ")
    sys.stdout.flush()
    new_file = sys.stdin.readline().strip()
    if new_file:
        save_archive(new_file, new_content)
    else:
        print("Not saving data.")


if __name__ == "__main__":
    main()

# print("=== CYBER ARCHIVES - COMMUNICATION SYSTEM ===\n")
# id = input("Input Stream active. Enter archivist ID: ")
# stat_rep = input("Input Stream active. Enter status report: ")
# print("")
# print("{[}STANDARD{]} Archive status "
#       f"from {id}: {stat_rep}", file=sys.stdout)
# print("{[}ALERT{]} System diagnostic: Communication channels verified",
#       file=sys.stderr)
# print("{[}STANDARD{]} Data transmission complete\n")
# print("Three-channel communication test successful.")
