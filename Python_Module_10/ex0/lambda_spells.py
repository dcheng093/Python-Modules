def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(artifacts,
                  key=lambda artifact: artifact['power'],
                  reverse=True)


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return list(filter(lambda mage: mage['power'] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda spell: f"* {spell} *", spells))


def mage_stats(mages: list[dict]) -> dict:
    if not mages:
        return {'max_power': 0, 'min_power': 0, 'avg_power': 0.0}
    max_power: int = max(mages, key=lambda mage: mage['power'])['power']
    min_power: int = min(mages, key=lambda mage: mage['power'])['power']
    avg_power: float = round(
        sum(map(lambda mage: mage['power'], mages)) / len(mages), 2
    )
    return {
        'max_power': max_power,
        'min_power': min_power,
        'avg_power': avg_power
        }


def main() -> None:
    print()
    print("Testing artifact sorter...")
    artifacts = [
        {'name': 'Crystal Orb', 'power': 85, 'type': 'crystal'},
        {'name': 'Fire Staff', 'power': 92, 'type': 'fire'},
    ]
    mages = [{'name': 'Phoenix',
              'power': 100,
              'element': 'fire'},
             {'name': 'Jordan',
              'power': 84,
              'element': 'ice'},
             {'name': 'Kai',
              'power': 92,
              'element': 'light'},
             {'name': 'Kai',
              'power': 82,
              'element': 'fire'},
             {'name': 'Rowan',
              'power': 59,
              'element': 'fire'}]
    sorted_artifacts = artifact_sorter(artifacts)
    for i in range(len(sorted_artifacts) - 1):
        first = sorted_artifacts[i]
        second = sorted_artifacts[i + 1]
        print(f"{first['name']} ({first['power']} power) comes before "
              f"{second['name']} ({second['power']} power)")
    print("\nTesting spell transformer...")
    spells = ['fireball', 'heal', 'shield']
    transformed_spells = spell_transformer(spells)
    print(" ".join(transformed_spells))
    print("\nTesting power filter...")
    filtered = power_filter(mages, 70)
    for mage in filtered:
        print(f"{mage['name']} ({mage['power']} power) - {mage['element']}")
    print("\nTesting mage stats...")
    stats = mage_stats(mages)
    for key, value in stats.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
