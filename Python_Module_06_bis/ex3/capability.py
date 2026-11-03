from abc import ABC, abstractmethod


class TransformCapability(ABC):
    """An ability, not a kind of entity: it does NOT inherit from Creature.

    Only the entities that really can transform mix it in.
    """

    def __init__(self) -> None:
        self.transformed = False

    @abstractmethod
    def transform(self) -> str:
        pass

    @abstractmethod
    def revert(self) -> str:
        pass
