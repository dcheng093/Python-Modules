import importlib
import sys

REQUIRED: dict[str, tuple[str, str]] = {
    "pandas": (">=2.1.0", "Data manipulation ready"),
    "numpy": (">=1.25.0", "Numerical computation ready"),
    "matplotlib": (">=3.7.2", "Visualization ready"),
}
OUTPUT_FILE = "matrix_analysis.png"
DATA_POINTS = 1000


def load(name: str) -> object | None:
    try:
        return importlib.import_module(name)
    except ImportError:
        return None


def check_dependencies() -> list[str]:
    print("Checking dependencies:")
    missing: list[str] = []
    for name, (_, message) in REQUIRED.items():
        module = load(name)
        if module is None:
            print(f"[MISSING] {name} - not installed")
            missing.append(name)
        else:
            version = getattr(module, "__version__", "unknown version")
            print(f"[OK] {name} ({version}) - {message}")
    return missing


def compare_versions() -> None:
    print("\nInstalled versions vs declared constraints:")
    for name, (constraint, _) in REQUIRED.items():
        module = load(name)
        installed = ("not installed" if module is None
                     else getattr(module, "__version__", "unknown"))
        print(f"  {name:<11} declared {constraint:<9} installed {installed}")


def explain_managers() -> None:
    poetry = "pypoetry" in sys.prefix
    manager = "Poetry" if poetry else "pip (or no manager)"
    print(f"\nRunning with: {manager}  [{sys.prefix}]")
    print("pip vs Poetry:")
    print("  pip    reads requirements.txt and resolves versions at install "
          "time;")
    print("         two installs on different days may get different "
          "versions.")
    print("  Poetry reads pyproject.toml, resolves once and pins everything "
          "in")
    print("         poetry.lock, and creates/manages the virtual environment "
          "itself.")


def install_help(missing: list[str]) -> None:
    print(f"\nMissing dependencies: {', '.join(missing)}")
    print("Install them with pip:")
    print("  pip install -r requirements.txt")
    print("Or with Poetry:")
    print("  poetry install")
    print("  poetry run python loading.py")


def run_analysis() -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    print("\nAnalyzing Matrix data...")
    print(f"Processing {DATA_POINTS} data points...")
    rng = np.random.default_rng()
    df = pd.DataFrame({"signal": rng.normal(0.0, 1.0, DATA_POINTS)})
    df["trend"] = df["signal"].rolling(window=50, min_periods=1).mean()
    anomalies = int((df["signal"].abs() > 2.5).sum())
    print(f"Mean {df['signal'].mean():.3f}, std {df['signal'].std():.3f}, "
          f"{anomalies} anomalies beyond 2.5 sigma")

    print("Generating visualization...")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df.index, df["signal"], linewidth=0.6, label="signal")
    ax.plot(df.index, df["trend"], linewidth=1.5, label="rolling mean (50)")
    ax.set_title("Matrix Signal Analysis")
    ax.set_xlabel("Sample")
    ax.set_ylabel("Signal value")
    ax.legend()
    fig.savefig(OUTPUT_FILE)
    plt.close(fig)
    print("\nAnalysis complete!")
    print(f"Results saved to: {OUTPUT_FILE}")


def main() -> None:
    print("\nLOADING STATUS: Loading programs...\n")
    missing = check_dependencies()
    compare_versions()
    explain_managers()
    if missing:
        install_help(missing)
        sys.exit(1)
    try:
        run_analysis()
    except (OSError, ValueError) as e:
        print(f"Analysis failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
