# The package interface: factories only, never the concrete entities.
from .factory import CreatureFactory, FlameFactory, TransformCreatureFactory

__all__ = ["CreatureFactory", "FlameFactory", "TransformCreatureFactory"]
