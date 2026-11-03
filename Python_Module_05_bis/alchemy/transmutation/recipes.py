# Absolute imports: the full path from the project root.
import elements
from alchemy.elements import create_air
# Relative import: one level up from the transmutation subpackage.
from ..potions import strength_potion


def lead_to_gold() -> str:
    return ("Recipe transmuting Lead to Gold: brew "
            f"'{create_air()}' and '{strength_potion()}' "
            f"mixed with '{elements.create_fire()}'")
