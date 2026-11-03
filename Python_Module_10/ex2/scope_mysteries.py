from collections.abc import Callable
from typing import Any


def mage_counter() -> Callable[[], int]:
    count = 0

    def counter() -> int:
        nonlocal count
        count += 1
        return count

    return counter


def spell_accumulator(initial_power: int) -> Callable[[int], int]:
    total = initial_power

    def accumulate(power: int) -> int:
        nonlocal total
        total += power
        return total

    return accumulate


def enchantment_factory(enchantment_type: str) -> Callable[[str], str]:
    def enchant(item_name: str) -> str:
        return f"{enchantment_type} {item_name}"
    return enchant


def memory_vault() -> dict[str, Callable]:
    memory: dict[str, Any] = {}

    def store(key: str, value: Any) -> None:
        memory[key] = value

    def recall(key: str) -> Any:
        return memory.get(key, "Memory not found")

    return {"store": store, "recall": recall}


def main() -> None:
    print("Testing mage counter...")
    counter_a = mage_counter()
    counter_b = mage_counter()

    print("counter_a call 1:", counter_a())
    print("counter_a call 2:", counter_a())
    print("counter_b call 1:", counter_b())

    print("\nTesting spell accumulator...")
    acc = spell_accumulator(100)
    print("Base 100, add 20:", acc(20))
    print("Base 100, add 30:", acc(30))

    print("\nTesting enchantment factory...")
    flaming = enchantment_factory("Flaming")
    frozen = enchantment_factory("Frozen")
    print(flaming("Sword"))
    print(frozen("Shield"))

    print("\nTesting memory vault...")
    vault = memory_vault()
    print("Store 'secret' = 42")
    vault["store"]("secret", 42)
    print("Recall 'secret':", vault["recall"]("secret"))
    print("Recall 'unknown':", vault["recall"]("unknown"))

    # print("\n\n\nexamples using the actual data from the generator:")
    # initial_powers = [45, 73, 39]
    # power_additions = [14, 15, 13, 11, 14]
    # print("\nTesting spell accumulator...")
    # for power in initial_powers:
    #     acc = spell_accumulator(power)
    #     print()
    #     for addition in power_additions:
    #         print(f"Base {power}, add {addition}:", acc(addition))
    # print("\nTesting enchantment factory...\n")
    # enchantment_types = ['Dark', 'Frozen', 'Radiant']
    # items_to_enchant = ['Amulet', 'Armor', 'Shield', 'Cloak']
    # for enchantment in enchantment_types:
    #     factory = enchantment_factory(enchantment)
    #     print()
    #     for item in items_to_enchant:
    #         print(factory(item))


if __name__ == "__main__":
    main()
