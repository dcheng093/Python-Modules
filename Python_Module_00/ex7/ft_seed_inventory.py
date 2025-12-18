def ft_seed_inventory(seed: str, count: int, unit: str) -> None:
    if unit not in ("grams", "packets", "area"):
        unit = "Unknown unit type"
    if unit == "packets":
        print(seed.capitalize(), "seeds:", count, unit, "available")
    if unit == "grams":
        print(seed.capitalize(), "seeds:", count, unit, "total")
    if unit == "area":
        print(seed.capitalize(), "seeds: covers", count, "square meters")
