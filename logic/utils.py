import re
from logic.constants import plural_rules

def build_unit_regex(entity_name, short_entity):
    all_units = set()

    for units in entity_name.values():
        all_units.update(units)

    for full_unit, short_units in short_entity.items():
        all_units.add(full_unit)
        if isinstance(short_units, set):
            all_units.update(short_units)
        else:
            all_units.add(short_units)

    unit_pattern = '|'.join(re.escape(unit) for unit in all_units)
    return unit_pattern

def normalize_unit(unit):
    return plural_rules.get(unit.lower(), unit.lower())
