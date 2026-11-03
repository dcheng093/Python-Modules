from ex1 import HealingCreatureFactory, TransformCreatureFactory


def test_healing(factory: HealingCreatureFactory) -> None:
    print("Testing Creature with healing capability")
    print("base:")
    base = factory.create_base()
    print(base.describe())
    print(base.attack())
    print(base.heal())
    print("evolved:")
    evo = factory.create_evolved()
    print(evo.describe())
    print(evo.attack())
    print(evo.heal())


def test_transform(factory: TransformCreatureFactory) -> None:
    print("Testing Creature with transform capability")
    print("base:")
    base = factory.create_base()
    print(base.describe())
    print(base.attack())
    print(base.transform())
    print(base.attack())
    print(base.revert())
    print("evolved:")
    evo = factory.create_evolved()
    print(evo.describe())
    print(evo.attack())
    print(evo.transform())
    print(evo.attack())
    print(evo.revert())


def main() -> None:
    healing_factory = HealingCreatureFactory()
    transform_factory = TransformCreatureFactory()
    test_healing(healing_factory)
    print()
    test_transform(transform_factory)


if __name__ == "__main__":
    main()
