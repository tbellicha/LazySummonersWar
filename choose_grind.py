#!/usr/bin/env python3
from values import *


grindValues = {
    "MAGIC": {
        "HP_PERCENT": (2, 5),
        "ATK_PERCENT": (2, 5),
        "DEF_PERCENT": (2, 5),
        "ATK": (6, 12),
        "DEF": (6, 12),
        "HP": (100, 200),
        "SPD": (1, 2)
    },
    "RARE": {
        "HP_PERCENT": (3, 6),
        "ATK_PERCENT": (3, 6),
        "DEF_PERCENT": (3, 6),
        "ATK": (10, 18),
        "DEF": (10, 18),
        "HP": (180, 250),
        "SPD": (2, 3)
    },
    "HERO": {
        "HP_PERCENT": (4, 7),
        "ATK_PERCENT": (4, 7),
        "DEF_PERCENT": (4, 7),
        "ATK": (12, 22),
        "DEF": (12, 22),
        "HP": (230, 450),
        "SPD": (3, 4)
    },
    "LEGEND": {
        "HP_PERCENT": (5, 10),
        "ATK_PERCENT": (5, 10),
        "DEF_PERCENT": (5, 10),
        "ATK": (18, 30),
        "DEF": (18, 30),
        "HP": (430, 550),
        "SPD": (4, 5)
    },
    "MAGIC_ANTIC": {
        "HP_PERCENT": (2, 7),
        "ATK_PERCENT": (2, 7),
        "DEF_PERCENT": (2, 7),
        "HP": (100, 260),
        "ATK": (6, 16),
        "DEF": (6, 16),
        "SPD": (1, 3)
    },
    "RARE_ANTIC": {
        "HP_PERCENT": (3, 8),
        "ATK_PERCENT": (3, 8),
        "DEF_PERCENT": (3, 8),
        "HP": (180, 310),
        "ATK": (10, 22),
        "DEF": (10, 22),
        "SPD": (2, 4)
    },
    "HERO_ANTIC": {
        "HP_PERCENT": (4, 9),
        "ATK_PERCENT": (4, 9),
        "DEF_PERCENT": (4, 9),
        "HP": (230, 510),
        "ATK": (12, 26),
        "DEF": (12, 26),
        "SPD": (3, 5)
    },
    "LEGEND_ANTIC": {
        "HP_PERCENT": (5, 12),
        "ATK_PERCENT": (5, 12),
        "DEF_PERCENT": (5, 12),
        "HP": (430, 610),
        "ATK": (18, 34),
        "DEF": (18, 34),
        "SPD": (4, 6)
    }
}


def applicable_grind(substat, modifier):
    if substat.stat_id != modifier.stat:
        return False
    if substat.grind < grindValues[Quality(modifier.quality).name][Stat(modifier.stat).name][1]:
        return True
    return False


def choose_grind(runes, modifiers):
    for rune in runes:
        for modifier in modifiers:
            if int(modifier.type) % 2 != 0 :
                continue
            if rune.set == modifier.set:
                if rune.quality > 10 and modifier.type != CraftType.ANCIENT_GRINDSTONE.value or \
                    rune.quality < 11 and modifier.type == CraftType.ANCIENT_GRINDSTONE.value:
                    continue
                for substat in rune.substats:
                    if applicable_grind(substat, modifier):
                        print(rune)
                        print(modifier)
                        return rune, modifier
