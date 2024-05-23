import random
from .items import *

common_weapons: list = []
common_shields: list = []
common_armours: list = []

uncommon_weapons: list = []
uncommon_shields: list = []
uncommon_armours: list = []

rare_weapons: list = []
rare_shields: list = []
rare_armours: list = []

common_loot: dict = {
    "common_weapons": common_weapons,
    "common_shields": common_shields,
    "common_armours": common_armours
}

uncommon_loot: dict = {
    "uncommon_weapons": uncommon_weapons,
    "uncommon_shields": uncommon_shields,
    "uncommon_armours": uncommon_armours
}

rare_loot: dict = {
    "rare_weapons": rare_weapons,
    "rare_shields": rare_shields,
    "rare_armours": rare_armours
}

for weapon in Weapon.all_weapons:
    match weapon.rarity:
        case "common":
            common_weapons.append(weapon)
        case "uncommon":
            uncommon_weapons.append(weapon)
        case "rare":
            rare_weapons.append(weapon)

for shield in Shield.all_shields:
    match shield.rarity:
        case "common":
            common_shields.append(shield)
        case "uncommon":
            uncommon_shields.append(shield)
        case "rare":
            rare_shields.append(shield)

for armour in Armour.all_armours:
    match armour.rarity:
        case "common":
            common_armours.append(armour)
        case "uncommon":
            uncommon_armours.append(armour)
        case "rare":
            rare_armours.append(armour)

class Level():
    def __init__(self,
                 name: str,
                 entities: int,
                 enemies: int,
                 loot: int,
                 loot_rarity: str) -> None:
        self.name = name
        self.entities = entities
        self.enemies = enemies
        self.loot = loot
        self.loot_rarity = loot_rarity

    def spawn_loot(self, loot: int, loot_rarity: str) -> None:
        loot_rarities: dict = {
            "common": common_loot,
            "uncommon": uncommon_loot,
            "rare": rare_loot
        }

        loot_contents = []

        if loot_rarity == "random":
            loot_rarity = random.choice(list(loot_rarities.keys()))

        match loot_rarity:
            case "common":
                for i in range(loot):
                    while True:
                        loot_type = random.choice(list(common_loot.keys()))

                        match loot_type:
                            case "common_weapons":
                                loot_item = random.choice(common_weapons)
                            case "common_shields":
                                loot_item = random.choice(common_shields)
                            case "common_armours":
                                loot_item = random.choice(common_armours)

                        if loot_item in loot_contents:
                            continue
                        else:
                            loot_contents.append(loot_item)
                            break
            case "uncommon":
                for i in range(loot):
                    while True:
                        loot_type = random.choice(list(uncommon_loot.keys()))
                        match loot_type:
                            case "uncommon_weapons":
                                loot_item = random.choice(uncommon_weapons)
                            case "uncommon_shields":
                                loot_item = random.choice(uncommon_shields)
                            case "uncommon_armours":
                                loot_item = random.choice(uncommon_armours)

                        if loot_item in loot_contents:
                            continue
                        else:
                            loot_contents.append(loot_item)
                            break
            case "rare":
                for i in range(loot):
                    while True:
                        loot_type = random.choice(list(rare_loot.keys()))
                        match loot_type:
                            case "rare_weapons":
                                loot_item = random.choice(rare_weapons)
                            case "rare_shields":
                                loot_item = random.choice(rare_shields)
                            case "rare_armours":
                                loot_item = random.choice(rare_armours)

                        if loot_item in loot_contents:
                            continue
                        else:
                            loot_contents.append(loot_item)
                            break

        return loot_contents


level_tutorial = Level(name="Tutorial", entities=2, enemies=1, loot=1, loot_rarity="common")

level_1 = Level(name="placeholder", entities=5, enemies=4, loot=1, loot_rarity="common")
# maybe use matrix for level structure?