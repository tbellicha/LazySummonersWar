#!/usr/bin/env python3
import copy
import json
import pip._vendor.requests
import sys
import time

from values import *
from choose_grind import *
from choose_enchant import *

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
        self.rune_id                    = rune["rune_id"]
        self.equipped                   = rune["occupied_type"]
        self.slot                       = rune["slot_no"]
        self.quality                    = rune["rank"]
        self.nb_stars                   = rune["class"]
        self.set                        = rune["set_id"]
        self.main_stat_id               = rune["pri_eff"][0]
        self.innate_stat_id             = rune["prefix_eff"][0]
        self.innate_stat_value          = rune["prefix_eff"][1]
        self.substats                   = []
        self.efficiency                 = 0
        self.max_grind_efficiency       = 0
        self.max_gem_efficiency         = 0
        self.gem                        = Modifier
        for substat in rune["sec_eff"]:
            self.substats.append(RuneStat(substat))
        self.efficiency = calc_efficiency(self)
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
        if self.type % 2 == 0:
            return \
                f'Grind: {Stat(self.stat).name} {Set(self.set).name} {Quality(self.quality).name}'
        if self.type % 2 == 1:
            return \
                f'Gem: {Stat(self.stat).name} {Set(self.set).name} {Quality(self.quality).name}'


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


def compute_json(argv):
    try:
        file = open(argv[1], encoding="utf8")
    except OSError:
        print("Cannot open file", file=sys.stderr)
        return 84
    data = json.load(file)
    name = data["wizard_info"]["wizard_name"]
    all_account_runes = []
    all_account_modifiers = []
    print(f'----[{name}]----')
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
    all_account_modifiers.sort(key=lambda x: x.quality, reverse=True)
    file.close()
    return all_account_runes, all_account_modifiers


def process_enchant(argv):
    start_time = time.time()
    all_account_runes, all_account_modifiers = compute_json(argv)
    choose_enchant(all_account_runes, all_account_modifiers)
    all_account_runes.sort(key=lambda x: x.max_gem_efficiency, reverse=True)
    for rune in all_account_runes:
        if rune.max_gem_efficiency != 0:
            print(f'{rune} -> + {rune.max_gem_efficiency}%\n{rune.gem}\n')
    print(f'\n----[{round((time.time() - start_time), 2)} seconds]----')


def process_grind(argv):
    start_time = time.time()
    all_account_runes, all_account_modifiers = compute_json(argv)
    choose_grind(all_account_runes, all_account_modifiers)
    all_account_runes.sort(key=lambda x: x.max_grind_efficiency, reverse=True)
    print(all_account_runes[0], all_account_runes[0].max_grind_efficiency)
    print(f'\n----[{round((time.time() - start_time), 2)} seconds]----')
    return 0


podValues = {
    "Sets" : {
        "ALL"       : 1,
        "DESPAIR"   : 2,
        "DESTROY"   : 2,
        "VIOLENT"   : 3,
        "WILL"      : 3,
    },
    "Eff" : {
        "130"       : 4,
        "120"       : 3,
        "110"       : 2,
        "100"       : 1,
    }
}


def process_score(argv):
    start_time = time.time()
    all_account_runes = compute_json(argv)[0]
    all_account_runes.sort(key=lambda x: x.efficiency, reverse=True)
    total_score = 0
    map_score = [[0 for i in podValues["Eff"]] for i in podValues["Sets"]]
    map_sets = [x for x in podValues["Sets"]]
    for r, rune in enumerate(all_account_runes):
        curr_score = 0
        for e, podEff in enumerate(podValues["Eff"]):
            if rune.efficiency >= int(podEff):
                curr_score += int(podValues["Eff"][podEff])
                if Set(rune.set).name in podValues["Sets"]:
                    curr_score *= podValues["Sets"][Set(rune.set).name]
                    map_score[map_sets.index(Set(rune.set).name)][e] += 1
                else:
                    curr_score *= podValues["Sets"]["ALL"]
                    map_score[map_sets.index("ALL")][e] += 1
                break
        total_score += curr_score
    print(f'Score: {total_score}\n')
    tmp_pod_eff = list(podValues["Eff"])
    tmp_pod_eff.reverse()
    for x in tmp_pod_eff:
        print(f'\t{x}', end='')
    print()
    total_check = [0 for i in podValues["Eff"]]
    for c, x in enumerate(map_sets):
        print(f'{x}\t', end='')
        map_score[c].reverse()
        for i in range(len(map_score[c])):
            print(f'{map_score[c][i]}\t', end='')
            total_check[i] += map_score[c][i]
        print()
    print(f'\nTotal', end='')
    for i in total_check:
        print(f'\t{i}', end='')
    print()
    print(f'\n----[{round((time.time() - start_time), 2)} seconds]----')
    return 0


def process_update(argv):
    start_time = time.time()
    nb = 0
    curr_computed = 0
    f = open("monsters.json", "w")
    while 1:
        nb += 1
        response = pip._vendor.requests.get\
            ("https://swarfarm.com/api/v2/monsters/?id__in=&com2us_id=&family_id=&base_stars=&base_stars__lte=&base_stars__gte=&natural_stars=&natural_stars__lte=&natural_stars__gte=2&obtainable=&fusion_food=&homunculus=&name=&order_by=&page=" + str(nb))
        api_json = response.json()
        count = api_json["count"]
        curr_computed += len(api_json["results"])
        print(f'{curr_computed}/{count}: [{round(curr_computed/count * 100, 2)}%]')
        for i, curr in enumerate(api_json["results"]):
            del curr["url"]
            del curr["image_filename"]
            del curr["obtainable"]
            del curr["can_awaken"]
            del curr["awaken_bonus"]
            del curr["skills"]
            del curr["leader_skill"]
            del curr["homunculus_skills"]
            del curr["base_hp"]
            del curr["base_attack"]
            del curr["base_defense"]
            del curr["speed"]
            del curr["crit_rate"]
            del curr["crit_damage"]
            del curr["resistance"]
            del curr["accuracy"]
            del curr["raw_hp"]
            del curr["raw_attack"]
            del curr["raw_defense"]
            del curr["max_lvl_hp"]
            del curr["max_lvl_attack"]
            del curr["max_lvl_defense"]
            del curr["awakens_from"]
            del curr["awakens_to"]
            del curr["awaken_cost"]
            del curr["source"]
            del curr["fusion_food"]
            del curr["homunculus"]
            del curr["craft_cost"]
            del curr["craft_materials"]
        f.write(json.dumps(api_json["results"], indent=4))
        if not api_json["next"]:
            break
        # if nb == 8:
        #     break
    print(f'\n----[{round((time.time() - start_time), 2)} seconds]----')
    return 0