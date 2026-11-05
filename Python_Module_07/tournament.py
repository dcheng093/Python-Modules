from ex0 import CreatureFactory, FlameFactory, AquaFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2 import (BattleStrategy, InvalidStrategyError, NormalStrategy,
                 AggressiveStrategy, DefensiveStrategy)

Opponent = tuple[CreatureFactory, BattleStrategy]


def format_opponents(opponents: list[Opponent]) -> str:
    pairs = [f"({factory.label()}+{strategy.name})"
             for factory, strategy in opponents]
    return "[ " + ", ".join(pairs) + " ]"


def battle(opponents: list[Opponent]) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")
    for i in range(len(opponents)):
        for j in range(i + 1, len(opponents)):
            factory1, strat1 = opponents[i]
            factory2, strat2 = opponents[j]
            c1 = factory1.create_base()
            c2 = factory2.create_base()
            print("\n* Battle *")
            print(c1.describe())
            print("vs.")
            print(c2.describe())
            print("now fight!")
            try:
                for action in strat1.act(c1):
                    print(action)
                for action in strat2.act(c2):
                    print(action)
            except InvalidStrategyError as e:
                print(f"Battle error, aborting tournament: {e}")
                return


def main() -> None:
    flame = FlameFactory()
    aqua = AquaFactory()
    healing = HealingCreatureFactory()
    transform = TransformCreatureFactory()
    normal = NormalStrategy()
    aggressive = AggressiveStrategy()
    defensive = DefensiveStrategy()
    tournaments: list[tuple[str, list[Opponent]]] = [
        ("Tournament 0 (basic)", [(flame, normal), (healing, defensive)]),
        ("Tournament 1 (error)", [(flame, aggressive), (healing, defensive)]),
        ("Tournament 2 (multiple)", [(aqua, normal), (healing, defensive),
                                     (transform, aggressive)]),
    ]
    for index, (title, opponents) in enumerate(tournaments):
        if index > 0:
            print()
        print(title)
        print(format_opponents(opponents))
        battle(opponents)


if __name__ == "__main__":
    main()
