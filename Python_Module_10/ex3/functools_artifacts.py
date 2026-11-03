from collections.abc import Callable
from functools import reduce, partial, lru_cache, singledispatch
from typing import Any
import operator


def spell_reducer(spells: list[int], operation: str) -> int:
    if not spells:
        return 0
    ops: dict[str, Callable[[int, int], int]] = {
        "add": operator.add,
        "multiply": operator.mul,
        "max": max,
        "min": min,
    }
    key = operation.lower()
    if key not in ops:
        raise ValueError(f"Unsupported operation: {operation}")
    return reduce(ops[key], spells)


def partial_enchanter(base_enchantment: Callable) -> dict[str, Callable]:
    return {
        "fire_enchant": partial(base_enchantment, 50, "fire"),
        "ice_enchant": partial(base_enchantment, 50, "ice"),
        "lightning_enchant": partial(base_enchantment, 50, "lightning"),
    }


@lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[[Any], str]:

    @singledispatch
    def cast(arg: Any) -> str:
        return "Unknown spell type"

    @cast.register
    def _(arg: int) -> str:
        return f"Damage spell: {arg} damage"

    @cast.register
    def _(arg: str) -> str:
        return f"Enchantment: {arg}"

    @cast.register
    def _(arg: list) -> str:
        return f"Multi-cast: {len(arg)} spells"

    return cast


def main() -> None:
    print("\nTesting spell reducer...")
    spells = [10, 20, 30, 40]
    print("Sum:", spell_reducer(spells, "add"))
    print("Product:", spell_reducer(spells, "multiply"))
    print("Max:", spell_reducer(spells, "max"))
    print("Min:", spell_reducer(spells, "min"))
    print("Empty:", spell_reducer([], "add"))
    try:
        spell_reducer(spells, "divide")
    except ValueError as e:
        print(f"Error handled: {e}")

    print("\nTesting partial enchanter...")

    def base_enchantment(power: int, element: str, target: str) -> str:
        return f"{element} enchantment with power {power} for {target}"

    enchants = partial_enchanter(base_enchantment)
    print(enchants["fire_enchant"]("sword"))
    print(enchants["ice_enchant"]("shield"))
    print(enchants["lightning_enchant"]("bow"))

    print("\nTesting memoized fibonacci...")
    print("Fib(0):", memoized_fibonacci(0))
    print("Fib(1):", memoized_fibonacci(1))
    print("Fib(10):", memoized_fibonacci(10))
    print("Fib(15):", memoized_fibonacci(15))
    print(memoized_fibonacci.cache_info())

    print("\nTesting spell dispatcher...")
    cast = spell_dispatcher()
    print(cast(42))
    print(cast("fireball"))
    print(cast([1, 2, 3]))
    print(cast({"weird": "thing"}))

    # print("\n\n\nexamples using the actual data from the generator:")
    # spell_powers = [18, 39, 33, 28, 42, 34]
    # operations = ['add', 'multiply', 'max', 'min']
    # fibonacci_tests = [8, 19, 20]
    # print("\nTesting spell_reducer...")
    # for operation in operations:
    #     print(f"{operation}: {spell_reducer(spell_powers, operation)}")
    # print("\nTesting memoized fibonacci...")
    # for integer in fibonacci_tests:
    #     print(f"Fib({integer}): {memoized_fibonacci(integer)}")
    # print("\nTesting partial enchanter...")

    # def base_enchantment(power: int, element: str, target: str) -> str:
    #     return f"{element} enchantment with power {power} for {target}"

    # enchants = partial_enchanter(base_enchantment)
    # print(enchants["fire_enchant"](target="sword"))
    # print(enchants["ice_enchant"](target="shield"))
    # print(enchants["lightning_enchant"](target="bow"))


if __name__ == "__main__":
    main()
