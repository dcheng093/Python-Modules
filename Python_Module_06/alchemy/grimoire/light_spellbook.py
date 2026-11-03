# The spellbook imports the validator at the top of the file. This is safe
# because light_validator.py does NOT import the spellbook at load time.
from .light_validator import validate_ingredients


def light_spell_allowed_ingredients() -> list[str]:
    return ["earth", "air", "fire", "water"]


def light_spell_record(spell_name: str, ingredients: str) -> str:
    verdict = validate_ingredients(ingredients)
    if verdict.endswith(" - VALID"):
        return f"Spell recorded: {spell_name} ({verdict})"
    return f"Spell rejected: {spell_name} ({verdict})"
