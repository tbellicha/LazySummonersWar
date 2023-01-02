#!/usr/bin/env python3
import json
import sys

from values import *

class Rune:
    def __init__(self, rune):
        self.rune_id            = rune["rune_id"]
        self.equipped           = rune["occupied_type"]
        self.slot               = rune["slot_no"]
        self.quality            = rune["rank"]
        self.nb_stars           = rune["class"]
        self.set                = rune["set_id"]
        self.main_stat_id       = rune["pri_eff"][0]
        self.innate_stat_id     = rune["prefix_eff"][0]
        self.innate_stat_value  = rune["prefix_eff"][1]
        self.substats           = []
        for substat in rune["sec_eff"]:
            self.substats.append(substat)
        self.efficiency = 0


class Modifier:
    def __init__(self, modifier):
        max_char        = len(str(modifier["craft_type_id"]))
        self.type       = modifier["craft_type"]
        self.set        = int(str(modifier["craft_type_id"])[0:max_char - 4])
        self.stat       = int(str(modifier["craft_type_id"])[max_char - 4:max_char - 2])
        self.quality    = int(str(modifier["craft_type_id"])[max_char - 2:max_char])


def calc_efficiency(rune):
    if rune.nb_stars == Stars.SIX.value or Stars.SIX_ANTIC.value:
        eff_main = 1
        eff_innate = 0
        eff_subs = 0
        if rune.innate_stat_id != Stat.NONE.value:
            eff_innate = rune.innate_stat_value / (MaxValueStat6[Stat(rune.innate_stat_id).name].value * 5)
        for substat in rune.substats:
            if substat[0] != Stat.NONE.value:
                eff_subs += (substat[1] + substat[3]) / (MaxValueStat6[Stat(substat[0]).name].value * 5)
        rune.efficiency = ((eff_main + eff_innate + eff_subs) / 2.8) * 100
        return
    if rune.nb_stars == Stars.FIVE.value or Stars.FIVE_ANTIC.value:
        eff_main = 1 # to change
        eff_innate = 0
        eff_subs = 0
        if rune.innate_stat_id != Stat.NONE.value:
            eff_innate = rune.innate_stat_value / (MaxValueStat5[Stat(rune.innate_stat_id).name].value * 5)
        for substat in rune.substats:
            if substat[0] != Stat.NONE.value:
                eff_subs += (substat[1] + substat[3]) / (MaxValueStat5[Stat(substat[0]).name].value * 5)
        rune.efficiency = ((eff_main + eff_innate + eff_subs) / 2.8) * 100
        return


def compute_rune(rune):
    crune = Rune(rune)
    calc_efficiency(crune)
    return crune


def process(argv):
    try:
        file = open(argv[1], encoding="utf8")
    except OSError:
        print("Cannot open file", file=sys.stderr)
        return 84
    data = json.load(file)
    name = data["wizard_info"]["wizard_name"]
    all_account_runes = []
    all_account_modifiers = []
    print(name)
    i = 0
    #  Runes from monsters
    for monster in data["unit_list"]:
        for rune in monster["runes"]:
            crune = compute_rune(rune)
            if crune.efficiency >= 100:
                i += 1
            all_account_runes.append(crune)
    #  Runes from inventory
    for rune in data["runes"]:
        crune = compute_rune(rune)
        if crune.efficiency >= 100:
            i += 1
        all_account_runes.append(crune)
    print('Nb runes +100%: ' + str(i))
    for modifier in data["rune_craft_item_list"]:
        cmodifier = Modifier(modifier)
        all_account_modifiers.append(cmodifier)
    file.close()
    return 0
