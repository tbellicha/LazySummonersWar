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
                if substat.third > 0:
                    eff_subs += (substat.value) / (MaxValueStat6[Stat(substat.stat_id).name].value * 5)
                else:
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

enchantValues = {
    "MAGIC": {
        "HP_PERCENT": (3, 7),
        "ATK_PERCENT": (3, 7),
        "DEF_PERCENT": (3, 7),
        "ATK": (10, 16),
        "DEF": (10, 16),
        "HP": (130, 220),
        "SPD": (2, 4),
        "CRIT_RATE": (2, 4),
        "CRIT_DMG": (3, 5),
        "RES": (3, 6),
        "ACC": (3, 6)
    },
    "RARE": {
        "HP_PERCENT": (5, 9),
        "ATK_PERCENT": (5, 9),
        "DEF_PERCENT": (5, 9),
        "ATK": (15, 23),
        "DEF": (15, 23),
        "HP": (200, 310),
        "SPD": (3, 6),
        "CRIT_RATE": (3, 5),
        "CRIT_DMG": (4, 6),
        "RES": (5, 8),
        "ACC": (5, 8)
    },
    "HERO": {
        "HP_PERCENT": (7, 11),
        "ATK_PERCENT": (7, 11),
        "DEF_PERCENT": (7, 11),
        "ATK": (20, 30),
        "DEF": (20, 30),
        "HP": (290, 420),
        "SPD": (5, 8),
        "CRIT_RATE": (4, 7),
        "CRIT_DMG": (5, 8),
        "RES": (6, 9),
        "ACC": (6, 9)
    },
    "LEGEND": {
        "HP_PERCENT": (9, 13),
        "ATK_PERCENT": (9, 13),
        "DEF_PERCENT": (9, 13),
        "ATK": (28, 40),
        "DEF": (28, 40),
        "HP": (400, 580),
        "SPD": (7, 10),
        "CRIT_RATE": (6, 9),
        "CRIT_DMG": (7, 10),
        "RES": (8, 11),
        "ACC": (8, 11)
    },
    "MAGIC_ANTIC": {
        "HP_PERCENT": (3, 9),
        "ATK_PERCENT": (3, 9),
        "DEF_PERCENT": (3, 9),
        "HP": (130, 280),
        "ATK": (10, 20),
        "DEF": (10, 20),
        "SPD": (2, 5),
        "CRIT_RATE": (2, 5),
        "CRIT_DMG": (3, 7),
        "RES": (3, 8),
        "ACC": (3, 8),
    },
    "RARE_ANTIC": {
        "HP_PERCENT": (5, 11),
        "ATK_PERCENT": (5, 11),
        "DEF_PERCENT": (5, 11),
        "HP": (200, 370),
        "ATK": (15, 27),
        "DEF": (15, 27),
        "SPD": (3, 7),
        "CRIT_RATE": (3, 6),
        "CRIT_DMG": (4, 8),
        "RES": (5, 10),
        "ACC": (5, 10),
    },
    "HERO_ANTIC": {
        "HP_PERCENT": (7, 13),
        "ATK_PERCENT": (7, 13),
        "DEF_PERCENT": (7, 13),
        "HP": (290, 480),
        "ATK": (20, 34),
        "DEF": (20, 34),
        "SPD": (5, 9),
        "CRIT_RATE": (4, 8),
        "CRIT_DMG": (5, 10),
        "RES": (6, 11),
        "ACC": (6, 11),
    },
    "LEGEND_ANTIC": {
        "HP_PERCENT": (9, 15),
        "ATK_PERCENT": (9, 15),
        "DEF_PERCENT": (9, 15),
        "HP": (400, 640),
        "ATK": (28, 44),
        "DEF": (28, 44),
        "SPD": (7, 11),
        "CRIT_RATE": (6, 10),
        "CRIT_DMG": (7, 12),
        "RES": (8, 13),
        "ACC": (8, 13),
    }
}


def choose_enchant(runes, modifiers):
    count = 0
    for rune in runes:
        rune.max_gem_efficiency = 0
        curr_modifier = list(filter(lambda x: x.set == rune.set and x.type % 2 == 1, modifiers))
        for s, substat in enumerate(rune.substats):
            if substat.third > 0:
                applicable_enchant = list(filter(lambda x: x.set == rune.set and x.type % 2 == 1 \
                    and x.stat == substat.stat_id, curr_modifier))
                if len(applicable_enchant) == 0:
                    continue
                for modifier in applicable_enchant:
                    if rune.quality > 10 and modifier.type != CraftType.ANCIENT_GEM.value or \
                        rune.quality < 11 and modifier.type == CraftType.ANCIENT_GEM.value:
                        continue
                    if substat.value < enchantValues[Quality(modifier.quality).name][Stat(modifier.stat).name][1]:
                        curr_efficiency = calc_efficiency(rune)
                        tmp_substat = copy.deepcopy(substat)
                        substat.value = enchantValues[Quality(modifier.quality).name][Stat(modifier.stat).name][1]
                        possible_efficiency = calc_efficiency(rune)
                        rune.substats[s] = copy.deepcopy(tmp_substat)
                        rune.max_gem_efficiency = round(possible_efficiency - curr_efficiency, 2)
                        rune.gem = modifier
                        count += 1
                        break
                break

