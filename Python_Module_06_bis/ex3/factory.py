from abc import ABC, abstractmethod

from .creature import Creature
from .flame import Flameling, Pyrodon
from .shift import Morphagon, Shiftling


class CreatureFactory(ABC):
    @abstractmethod
    def create_base(self) -> Creature:
        pass

    @abstractmethod
    def create_evolved(self) -> Creature:
        pass


class FlameFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return Flameling()

    def create_evolved(self) -> Creature:
        return Pyrodon()


class TransformCreatureFactory(CreatureFactory):
    # Covariant return types: callers holding this factory know they get
    # transform-capable entities, without ever importing the entity classes.
    def create_base(self) -> Shiftling:
        return Shiftling()

    def create_evolved(self) -> Morphagon:
        return Morphagon()
