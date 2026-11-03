from collections.abc import Callable


def check_spells(*spells: Callable) -> None:
    for spell in spells:
        if not callable(spell):
            raise TypeError(f"{spell!r} is not a spell (not callable)")


def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    check_spells(spell1, spell2)

    def combined(target: str, power: int) -> tuple[str, str]:
        return (
            spell1(target, power),
            spell2(target, power),
        )
    return combined


def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    check_spells(base_spell)

    def amplified(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)
    return amplified


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    check_spells(condition, spell)

    def cast(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        return "Spell fizzled"
    return cast


def spell_sequence(spells: list[Callable]) -> Callable:
    check_spells(*spells)

    def sequence(target: str, power: int) -> list[str]:
        return [spell(target, power) for spell in spells]
    return sequence


def main() -> None:
    test_values = [10, 5, 21]
    test_targets = ['Dragon', 'Goblin', 'Wizard', 'Knight']

    def fireball(target: str, power: int) -> str:
        return f"Fireball hits {target}"

    def heal(target: str, power: int) -> str:
        return f"Heals {target}"

    def shield(target: str, power: int) -> str:
        return f"Shield blocks {target}'s attack for {power} damage"

    def power_probe(target: str, power: int) -> str:
        return f"{power}"

    print("\nTesting spell combiner...")
    combined = spell_combiner(fireball, heal)
    result1, result2 = combined(test_targets[0], test_values[0])
    print(f"Combined spell result: {result1}, {result2}")

    print("\nTesting power amplifier...")
    mega_probe = power_amplifier(power_probe, 3)
    print(f"Original: {power_probe(test_targets[0], test_values[0])}, "
          f"Amplified: {mega_probe(test_targets[0], test_values[0])}")
    mega_shield = power_amplifier(shield, 3)
    print(mega_shield(test_targets[3], test_values[0]))

    print("\nTesting conditional caster...")

    def enough_power(target: str, power: int) -> bool:
        return power >= 10

    safe_fireball = conditional_caster(enough_power, fireball)
    print(safe_fireball(test_targets[0], test_values[0]))
    print(safe_fireball(test_targets[1], test_values[1]))

    print("\nTesting spell sequence...")
    combo = spell_sequence([fireball, heal, shield])
    for result in combo(test_targets[2], test_values[2]):
        print(result)

    print("\nTesting callable() guard...")
    try:
        spell_combiner(fireball, "not a spell")  # type: ignore[arg-type]
    except TypeError as e:
        print(f"Rejected: {e}")


if __name__ == "__main__":
    main()
