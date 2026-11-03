# Top-level import of a module that is still being initialised: KABOOM.
from .dark_spellbook import dark_spell_allowed_ingredients


def dark_validate_ingredients(ingredients: str) -> str:
    allowed = dark_spell_allowed_ingredients()
    cleaned = "".join(c if c.isalpha() else " " for c in ingredients.lower())
    if any(word in allowed for word in cleaned.split()):
        return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"
