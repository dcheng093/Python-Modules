def validate_ingredients(ingredients: str) -> str:
    # Late import: resolved when the function is CALLED, not when this
    # module is loaded. By then light_spellbook is fully initialised, so
    # the mutual dependency never sees a half-built module.
    from .light_spellbook import light_spell_allowed_ingredients

    allowed = light_spell_allowed_ingredients()
    cleaned = "".join(c if c.isalpha() else " " for c in ingredients.lower())
    if any(word in allowed for word in cleaned.split()):
        return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"
