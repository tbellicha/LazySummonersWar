#!/usr/bin/env python3
import copy
import json
import sys

from values import *
from choose_grind import *

class RuneStat:
    def __init__(self, substats):
        self.stat_id    = substats[0]
        self.value      = substats[1]
        self.third      = substats[2]
        self.grind      = substats[3]
    def __str__(self) -> str:
        return f'{self.value + self.grind} (+{self.grind}) {Stat(self.stat_id).name}'


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
            self.substats.append(RuneStat(substat))
        self.efficiency = 0
        calc_efficiency(self)
        self.efficiency = round(self.efficiency, 2)
    def __str__(self) -> str:
        if len(self.substats) == 1:
            return \
                f'{Set(self.set).name} {Stat(self.main_stat_id).name} {self.slot} {Stars(self.nb_stars).name}\n'\
                f'{self.innate_stat_value} {Stat(self.innate_stat_id).name}\n'\
                f'{self.substats[0].value + self.substats[0].grind} (+{self.substats[0].grind}) {Stat(self.substats[0].stat_id).name}\n'\
                f'Efficiency: {self.efficiency}'
        if len(self.substats) == 2:
            return \
                f'{Set(self.set).name} {Stat(self.main_stat_id).name} {self.slot} {Stars(self.nb_stars).name}\n'\
                f'{self.innate_stat_value} {Stat(self.innate_stat_id).name}\n'\
                f'{self.substats[0].value + self.substats[0].grind} (+{self.substats[0].grind}) {Stat(self.substats[0].stat_id).name}\n'\
                f'{self.substats[1].value + self.substats[1].grind} (+{self.substats[1].grind}) {Stat(self.substats[1].stat_id).name}\n'\
                f'Efficiency: {self.efficiency}'
        if len(self.substats) == 3:
            return \
                f'{Set(self.set).name} {Stat(self.main_stat_id).name} {self.slot} {Stars(self.nb_stars).name}\n'\
                f'{self.innate_stat_value} {Stat(self.innate_stat_id).name}\n'\
                f'{self.substats[0].value + self.substats[0].grind} (+{self.substats[0].grind}) {Stat(self.substats[0].stat_id).name}\n'\
                f'{self.substats[1].value + self.substats[1].grind} (+{self.substats[1].grind}) {Stat(self.substats[1].stat_id).name}\n'\
                f'{self.substats[2].value + self.substats[2].grind} (+{self.substats[2].grind}) {Stat(self.substats[2].stat_id).name}\n'\
                f'Efficiency: {self.efficiency}'
        if len(self.substats) == 4:
            return \
                f'{Set(self.set).name} {Stat(self.main_stat_id).name} {self.slot} {Stars(self.nb_stars).name}\n'\
                f'{self.innate_stat_value} {Stat(self.innate_stat_id).name}\n'\
                f'{self.substats[0].value + self.substats[0].grind} (+{self.substats[0].grind}) {Stat(self.substats[0].stat_id).name}\n'\
                f'{self.substats[1].value + self.substats[1].grind} (+{self.substats[1].grind}) {Stat(self.substats[1].stat_id).name}\n'\
                f'{self.substats[2].value + self.substats[2].grind} (+{self.substats[2].grind}) {Stat(self.substats[2].stat_id).name}\n'\
                f'{self.substats[3].value + self.substats[3].grind} (+{self.substats[3].grind}) {Stat(self.substats[3].stat_id).name}\n'\
                f'Efficiency: {self.efficiency}'


class Modifier:
    """Modifier class
    type: CraftType (ENCHANTED_GEM to ANCIENT_GRINDSTONE)
    set: Set (ENERGY to TOLERANCE)
    stat: Stat (NONE to ACC)
    quality: Quality (NORMAL to LEGEND_ANTIC)
    quantity: int
    """
    def __init__(self, modifier):
        max_char        = len(str(modifier["craft_type_id"]))
        self.type       = modifier["craft_type"]
        self.set        = int(str(modifier["craft_type_id"])[0:max_char - 4])
        self.stat       = int(str(modifier["craft_type_id"])[max_char - 4:max_char - 2])
        self.quality    = int(str(modifier["craft_type_id"])[max_char - 2:max_char])
        self.quantity   = modifier["amount"]
    def __str__(self) -> str:
        return \
            f'Stat: {Stat(self.stat).name}\n'\
            # f'Set: {Set(self.set).name}\n'\
            # f'Type: {CraftType(self.type).name}\n'\
            # f'Quality: {Quality(self.quality).name}\n'


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
    print(f'========[{name}]========')
    i = 0
    #  Runes from monsters
    for monster in data["unit_list"]:
        for rune in monster["runes"]:
            crune = Rune(rune)
            all_account_runes.append(crune)
    #  Runes from inventory
    for rune in data["runes"]:
        crune = Rune(rune)
        all_account_runes.append(crune)
    all_account_runes.sort(key=lambda x: x.efficiency, reverse=True)
    #  Modifiers from inventory
    for modifier in data["rune_craft_item_list"]:
        cmodifier = Modifier(modifier)
        all_account_modifiers.append(cmodifier)
    all_account_modifiers.sort(key=lambda x: x.quantity, reverse=True)
    file.close()
    return 0
