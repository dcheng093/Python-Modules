import os
import sys

try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(BASE_DIR, ".env")
GITIGNORE_FILE = os.path.join(BASE_DIR, ".gitignore")

KEYS: list[str] = [
    "MATRIX_MODE",
    "DATABASE_URL",
    "API_KEY",
    "LOG_LEVEL",
    "ZION_ENDPOINT",
]

# Safe defaults only: never a default for a secret.
DEFAULTS: dict[str, str] = {
    "MATRIX_MODE": "development",
    "DATABASE_URL": "sqlite:///local.db",
    "LOG_LEVEL": "DEBUG",
}

SECRETS: list[str] = ["API_KEY", "DATABASE_URL"]
PLACEHOLDER = "your_api_key_here"


def load_configuration() -> tuple[dict[str, str | None], dict[str, str]]:
    """Return (config, source) where source says where each value came from.

    Precedence: real environment > .env file > safe default.
    """
    from_env = {k for k in KEYS if k in os.environ}
    if DOTENV_AVAILABLE and os.path.isfile(ENV_FILE):
        # override=False: variables already in the environment win.
        load_dotenv(ENV_FILE, override=False)

    config: dict[str, str | None] = {}
    source: dict[str, str] = {}
    for key in KEYS:
        value = os.getenv(key)
        if value:
            config[key] = value
            source[key] = "environment" if key in from_env else ".env"
        elif key in DEFAULTS:
            config[key] = DEFAULTS[key]
            source[key] = "default"
        else:
            config[key] = None
            source[key] = "missing"
    return config, source


def is_local(url: str) -> bool:
    return url.startswith("sqlite") or "localhost" in url \
        or "127.0.0.1" in url


def display_status(config: dict[str, str | None],
                   source: dict[str, str]) -> None:
    mode = config["MATRIX_MODE"] or "development"
    if mode not in ("development", "production"):
        print(f"[WARNING] Unknown mode '{mode}', "
              "falling back to development")
        mode = "development"
    production = mode == "production"

    defaulted = [k for k, s in source.items() if s == "default"]
    missing = [k for k, s in source.items() if s == "missing"]
    if defaulted:
        print(f"[WARNING] Not configured, using defaults: "
              f"{', '.join(defaulted)}")
    if missing:
        print(f"[WARNING] Not configured, no default: {', '.join(missing)}")
    print("\nConfiguration loaded:" if defaulted or missing
          else "Configuration loaded:")

    print(f"Mode: {mode}")

    db = config["DATABASE_URL"] or ""
    if is_local(db):
        print("Database: Connected to local instance")
        if production:
            print("  [WARNING] Production should not use a local database")
    else:
        print("Database: Connected to remote cluster")

    api_key = config["API_KEY"]
    if api_key and api_key != PLACEHOLDER:
        print("API Access: Authenticated")
    elif production:
        print("API Access: DENIED - an API key is required in production")
    else:
        print("API Access: Not configured (offline development)")

    level = config["LOG_LEVEL"] or "DEBUG"
    if production and level == "DEBUG":
        print("Log Level: DEBUG -> raised to WARNING in production")
    else:
        print(f"Log Level: {level}")

    if config["ZION_ENDPOINT"]:
        print("Remote Network: Online")
    else:
        print("Remote Network: Offline (ZION_ENDPOINT not set)")

    if not production:
        print("\nDevelopment details (where each value came from):")
        for key in KEYS:
            print(f"  {key}: {source[key]}")


def no_hardcoded_secrets(config: dict[str, str | None]) -> bool:
    """A secret is hardcoded if its value appears in this source file."""
    try:
        with open(os.path.abspath(__file__), "r") as f:
            code = f.read()
    except OSError:
        return False
    for key in SECRETS:
        value = config[key]
        if value and value not in DEFAULTS.values() \
                and value != PLACEHOLDER and value in code:
            return False
    return True


def env_ignored_by_git() -> bool:
    try:
        with open(GITIGNORE_FILE, "r") as f:
            lines = [line.strip() for line in f]
    except OSError:
        return False
    return ".env" in lines


def security_check(config: dict[str, str | None],
                   source: dict[str, str]) -> None:
    print("\nConfiguration security check:")
    if no_hardcoded_secrets(config):
        print("[OK] No hardcoded secrets detected")
    else:
        print("[ALERT] A secret value was found in the source code!")

    if env_ignored_by_git():
        print("[OK] .env file properly ignored by git")
    else:
        print("[WARNING] .env is not listed in ex1/.gitignore")

    overrides = [k for k, s in source.items() if s == "environment"]
    if overrides:
        print("[OK] Production overrides available "
              f"({', '.join(overrides)} from environment)")
    else:
        print("[OK] Production overrides available "
              "(none active: set variables in the environment to override)")

    if not DOTENV_AVAILABLE:
        print("[WARNING] python-dotenv not installed, .env file ignored "
              "(pip install -r ex1/requirements.txt)")
    elif not os.path.isfile(ENV_FILE):
        print("[WARNING] No .env file found "
              "(cp ex1/.env.example ex1/.env)")


def main() -> None:
    print("\nORACLE STATUS: Consulting the configuration...\n")
    config, source = load_configuration()
    display_status(config, source)
    security_check(config, source)
    print("\nThe Oracle sees all configurations.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
