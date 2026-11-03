import alchemy.grimoire


def main() -> None:
    print("=== Kaboom 0 ===")
    print("Using grimoire module directly")
    record = alchemy.grimoire.light_spell_record
    print("Testing record light spell: "
          f"{record('Fantasy', 'Earth, wind and fire')}")
    print("Testing record light spell: "
          f"{record('Shadow', 'Bats and frogs')}")


if __name__ == "__main__":
    main()
