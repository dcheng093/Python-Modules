import os
import site
import sys


def package_paths() -> list[str]:
    try:
        return site.getsitepackages()
    except AttributeError:
        return []


def global_package_path() -> str:
    version = f"python{sys.version_info.major}.{sys.version_info.minor}"
    return os.path.join(sys.base_prefix, "lib", version, "site-packages")


def inside_construct() -> None:
    venv_path = sys.prefix
    print("\nMATRIX STATUS: Welcome to the construct\n")
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {os.path.basename(venv_path)}")
    print(f"Environment Path: {venv_path}\n")
    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting")
    print("the global system.\n")
    print("Package installation path:")
    for path in package_paths():
        print(path)
    print("\nGlobal package location (untouched while you are here):")
    print(global_package_path())


def outside_construct() -> None:
    print("\nMATRIX STATUS: You're still plugged in\n")
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected\n")
    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.\n")
    print("Global package locations (shared by the whole system):")
    for path in package_paths():
        print(path)
    print("\nTo enter the construct, run:")
    print("python -m venv matrix_env")
    print("source matrix_env/bin/activate  # On Unix")
    print(r"matrix_env\Scripts\activate     # On Windows")
    print("\nThen run this program again.")


def main() -> None:
    if sys.prefix != sys.base_prefix:
        inside_construct()
    else:
        outside_construct()


if __name__ == "__main__":
    main()
