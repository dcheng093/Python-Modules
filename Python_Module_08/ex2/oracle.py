import os
import sys

try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

KEYS: list[str] = [
    "MATRIX_MODE",
    "DATABASE_URL",
    "API_KEY",
    "LOG_LEVEL",
    "ZION_ENDPOINT",
]
SECRETS: list[str] = ["API_KEY", "DATABASE_URL"]
PLACEHOLDER = "your_api_key_here"
SOURCE_FILE = os.path.abspath(__file__)
ENV_FILE = os.path.join(os.path.dirname(SOURCE_FILE), ".env")


def env_overrides() -> list[str]:
    return [key for key in KEYS if key in os.environ]


def load_configuration() -> dict[str, str | None]:
    if DOTENV_AVAILABLE:
        # override=False (the default): real environment variables win.
        load_dotenv(ENV_FILE, override=False)
    return {key: os.getenv(key) for key in KEYS}


def display_status(config: dict[str, str | None]) -> None:
    missing = [k for k, v in config.items() if not v]
    if missing:
        print(f"[WARNING] Missing configuration: {', '.join(missing)}")
        print("Configuration incomplete, using safe fallbacks:")
    else:
        print("Configuration loaded:")

    mode = config["MATRIX_MODE"] or "development"
    if mode not in ("development", "production"):
        print(f"[WARNING] Unknown mode '{mode}', using development")
        mode = "development"
    print(f"Mode: {mode}")

    if not config["DATABASE_URL"]:
        print("Database: Not configured")
    elif mode == "development":
        print("Database: Connected to local instance")
    else:
        print("Database: Connected to secure cluster")

    api_key = config["API_KEY"]
    if api_key and api_key != PLACEHOLDER:
        print("API Access: Authenticated")
    elif mode == "production":
        print("API Access: DENIED - production requires a real API_KEY")
    else:
        print("API Access: Not configured")

    default_level = "DEBUG" if mode == "development" else "WARNING"
    level = config["LOG_LEVEL"] or default_level
    print(f"Log Level: {level}")

    if config["ZION_ENDPOINT"]:
        print("Zion Network: Online")
    else:
        print("Zion Network: Offline")


def hardcoded_secrets(config: dict[str, str | None]) -> list[str]:
    try:
        with open(SOURCE_FILE, "r") as f:
            code = f.read()
    except OSError:
        return []
    found: list[str] = []
    for key in SECRETS:
        value = config[key]
        if value and value != PLACEHOLDER and value in code:
            found.append(key)
    return found


def security_check(config: dict[str, str | None],
                   overrides: list[str]) -> None:
    print("\nEnvironment security check:")
    leaked = hardcoded_secrets(config)
    if leaked:
        print(f"[ALERT] Secret value found in the source code: "
              f"{', '.join(leaked)}")
    else:
        print("[OK] No hardcoded secrets detected")
    api_key = config["API_KEY"]
    if not api_key or api_key == PLACEHOLDER:
        print("[WARNING] API key missing or using default placeholder")

    if not DOTENV_AVAILABLE:
        print("[WARNING] python-dotenv not installed, .env file ignored "
              "(pip install python-dotenv)")
    elif not os.path.isfile(ENV_FILE):
        print("[WARNING] No .env file found (cp .env.example .env)")
    elif any(not config[k] for k in KEYS):
        print("[WARNING] .env file is missing some variables")
    else:
        print("[OK] .env file properly configured")

    if overrides:
        print("[OK] Production overrides available "
              f"(from environment: {', '.join(overrides)})")
    else:
        print("[OK] Production overrides available "
              "(none active: environment variables take precedence)")


def main() -> None:
    print("\nORACLE STATUS: Reading the Matrix...\n")
    overrides = env_overrides()
    config = load_configuration()
    display_status(config)
    security_check(config, overrides)
    print("\nThe Oracle sees all configurations.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
