import importlib

REAGENTS: dict[str, str] = {
    "pandas": "Data manipulation ready",
    "numpy": "Numerical computation ready",
}


def check_reagent(name: str) -> str | None:
    """Return the installed version of a reagent, or None if missing."""
    try:
        module = importlib.import_module(name)
    except ImportError:
        return None
    return str(getattr(module, "__version__", "unknown version"))


def explain_tools() -> None:
    print("\npip vs Poetry:")
    print("requirements.txt declares what to install; "
          "pip resolves it at install time.")
    print("pyproject.toml declares the same constraints, and Poetry pins "
          "the resolved")
    print("versions in poetry.lock so every install is identical.")


def main() -> None:
    print("\nREAGENT STATUS: Loading reagents...\n")
    print("Checking dependencies:")
    missing: list[str] = []
    for name, message in REAGENTS.items():
        version = check_reagent(name)
        if version is None:
            print(f"[MISSING] {name} - not installed")
            missing.append(name)
        else:
            print(f"[OK] {name} ({version}) - {message}")

    explain_tools()

    if missing:
        names = " ".join(missing)
        print(f"\nMissing reagents: {', '.join(missing)}")
        print("Install them with pip:")
        print(f"  pip install {names}")
        print("  # or all declared reagents: "
              "pip install -r ex0/requirements.txt")
        print("Or with Poetry (from inside ex0/):")
        print(f"  poetry add {names}")
        print("  # or everything declared: poetry install")
        print("  poetry run python loading.py")
    else:
        print("\nAll reagents present and accounted for.")


if __name__ == "__main__":
    main()
