from ex3 import CreatureFactory, FlameFactory, TransformCreatureFactory
from ex4 import (AggressiveStrategy, BattleStrategy, InvalidStrategyError,
                 NormalStrategy)

Opponent = tuple[CreatureFactory, BattleStrategy]


def show_opponents(opponents: list[Opponent]) -> None:
    labels = [f"({factory.create_base().name}+{strategy.name})"
              for factory, strategy in opponents]
    print(f"[ {', '.join(labels)} ]")


def battle(opponents: list[Opponent]) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")
    try:
        for i, (first_factory, first_strategy) in enumerate(opponents):
            for second_factory, second_strategy in opponents[i + 1:]:
                first = first_factory.create_base()
                second = second_factory.create_base()
                print("\n* Battle *")
                print(first.describe())
                print("vs.")
                print(second.describe())
                print("now fight!")
                for line in first_strategy.act(first):
                    print(line)
                for line in second_strategy.act(second):
                    print(line)
    except InvalidStrategyError as e:
        print(f"Battle error, aborting tournament: {e}")


def main() -> None:
    flame = FlameFactory()
    transform = TransformCreatureFactory()
    normal = NormalStrategy()
    aggressive = AggressiveStrategy()

    tournaments: list[tuple[str, list[Opponent]]] = [
        ("Tournament 0 (basic)",
         [(flame, normal), (transform, aggressive)]),
        ("Tournament 1 (error)",
         [(transform, aggressive), (flame, aggressive)]),
        ("Tournament 2 (multiple)",
         [(flame, normal), (transform, aggressive), (transform, normal)]),
    ]
    for index, (title, opponents) in enumerate(tournaments):
        if index:
            print()
        print(title)
        show_opponents(opponents)
        battle(opponents)


if __name__ == "__main__":
    main()
