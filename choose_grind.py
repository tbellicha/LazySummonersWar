#!/usr/bin/env python3
import copy


from values import *

def calc_efficiency(rune):
    if rune.nb_stars == Stars.SIX.value or Stars.SIX_ANTIC.value:
        eff_main = 1
        eff_innate = 0
        eff_subs = 0
        if rune.innate_stat_id != Stat.NONE.value:
            eff_innate = rune.innate_stat_value / (MaxValueStat6[Stat(rune.innate_stat_id).name].value * 5)
        for substat in rune.substats:
            if substat.value != Stat.NONE.value:
                eff_subs += (substat.value + substat.grind) / (MaxValueStat6[Stat(substat.stat_id).name].value * 5)
        return round(((eff_main + eff_innate + eff_subs) / 2.8) * 100, 2)
    if rune.nb_stars == Stars.FIVE.value or Stars.FIVE_ANTIC.value:
        eff_main = 1 # to change
        eff_innate = 0
        eff_subs = 0
        if rune.innate_stat_id != Stat.NONE.value:
            eff_innate = rune.innate_stat_value / (MaxValueStat5[Stat(rune.innate_stat_id).name].value * 5)
        for substat in rune.substats:
            if substat.value != Stat.NONE.value:
                eff_subs += (substat.value + substat.grind) / (MaxValueStat5[Stat(substat.stat_id).name].value * 5)
        return round(((eff_main + eff_innate + eff_subs) / 2.8) * 100, 2)


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


def applicable_grind(substat, modifier, rune, i):
    grinded_rune = copy.deepcopy(rune)
    if substat.stat_id != modifier.stat:
        return 0
    if substat.grind < grindValues[Quality(modifier.quality).name][Stat(modifier.stat).name][1]:
        grinded_rune.substats[i].grind = grindValues[Quality(modifier.quality).name][Stat(modifier.stat).name][1]
        grinded_rune.efficiency = calc_efficiency(grinded_rune)
        return grinded_rune.efficiency - rune.efficiency
    return 0


def choose_grind(runes, modifiers):
    count = 0
    for rune in runes:
        rune.max_grind_efficiency = 0
        curr_modifier = list(filter(lambda x: x.set == rune.set and x.type % 2 == 0, modifiers))
        for modifier in curr_modifier:
            if rune.quality > 10 and modifier.type != CraftType.ANCIENT_GRINDSTONE.value or \
                rune.quality < 11 and modifier.type == CraftType.ANCIENT_GRINDSTONE.value:
                continue
            best_winnable_eff = 0
            for i, substat in enumerate(rune.substats):
                winnable_eff = applicable_grind(substat, modifier, rune, i)
                rune.max_grind_efficiency += winnable_eff
                if winnable_eff > best_winnable_eff:
                    best_winnable_eff = winnable_eff
            if best_winnable_eff > 0:
                count += 1
