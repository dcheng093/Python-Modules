def ft_seed_inventory(seed: str, count: int, unit: str) -> None:
    if unit == "packets":
        print(seed.capitalize(), "seeds:", count, unit, "available")
    elif unit == "grams":
        print(seed.capitalize(), "seeds:", count, unit, "total")
    elif unit == "area":
        print(seed.capitalize(), "seeds: covers", count, "square meters")
    else:
        unit = "Unknown unit type"
