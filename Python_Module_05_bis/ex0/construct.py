import os
import site
import sys


def in_virtual_env() -> bool:
    return sys.prefix != sys.base_prefix


def site_packages() -> str:
    paths = site.getsitepackages()
    return paths[0] if paths else "unknown"


def sealed_report() -> None:
    venv_path = sys.prefix
    print("\nLABORATORY STATUS: The laboratory is sealed\n")
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {os.path.basename(venv_path)}")
    print(f"Environment Path: {venv_path}\n")
    print("SUCCESS: You are working in an isolated environment!")
    print("Safe to install reagents without affecting")
    print("the global system.\n")
    print("Reagent installation path:")
    print(site_packages())
    print("\nGlobal installation path (untouched):")
    print(f"{sys.base_prefix}")


def open_report() -> None:
    print("\nLABORATORY STATUS: You are working in the open\n")
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected\n")
    print("WARNING: You are in the global environment!")
    print("Every reagent you install here leaks into the whole system.\n")
    print("Global installation path:")
    print(site_packages())
    print("\nTo seal the laboratory, run:")
    print("python3 -m venv lab_env")
    print("source lab_env/bin/activate  # On Unix")
    print(r"lab_env\Scripts\activate     # On Windows")
    print("\nThen run this program again.")


def main() -> None:
    if in_virtual_env():
        sealed_report()
    else:
        open_report()


if __name__ == "__main__":
    main()
