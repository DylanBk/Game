import random
from .items import *
from .enemies import *

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
                 num_rooms: int,
                 entities: int,
                 enemies: int,
                 enemy_types: list,
                 loot: int,
                 loot_rarity: str) -> None:
        self.name = name
        self.num_rooms = num_rooms
        self.entities = entities
        self.enemies = enemies
        self.enemy_types = enemy_types
        self.loot = loot
        self.loot_rarity = loot_rarity

class LevelRoom():
    def __init__(self,
                 name: str,
                 is_entity: bool,
                 is_enemy: bool,
                 is_loot: bool,
                 loot_item: object | None) -> None:
        self.name = name
        self.is_entity = is_entity
        self.is_enemy = is_enemy
        self.is_loot = is_loot
        self.loot_item = loot_item

def spawn_loot(loot: int, loot_rarity: str):
    """
    ...Loads loot for the relative level.

    :params:
        loot (int): The number of loot items.
        loot_rarity (str): The rarity of the loot, can be common, uncommon, rare, or random.

    :returns:
        loot_contents (list): A list of the loot items.
    """
    loot_rarities: dict = {
        "common": common_loot,
        "uncommon": uncommon_loot,
        "rare": rare_loot
    }

    loot_contents = []

    if loot_rarity == "random":
        loot_rarity = random.choice(list(loot_rarities.keys()))

    while True:
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
                break
            case "None":
                continue

    return loot_contents


enemy_types = Enemy.enemy_types
print(enemy_types)

level_tutorial = Level(name="Tutorial", num_rooms=1, entities=2, enemies=1, enemy_types=enemy_types[0], loot=1, loot_rarity="common")

level_1 = Level(name="1", num_rooms=5, entities=5, enemies=4, enemy_types=enemy_types[0], loot=1, loot_rarity="common")
level_2 = Level(name="placeholder2", num_rooms=7, entities=7, enemies=5, enemy_types=enemy_types[0], loot=2, loot_rarity="common")
# maybe use matrix for level structure?

levels: dict = {
"tutorial": level_tutorial,
"1": level_1
}

tutorial_rooms = [1] # list of room names, list because some rooms will be named such as boss battles
level_1_rooms = []

for room in range(level_1.num_rooms):
    level_1_rooms.append(room)

level_rooms: dict = {
    "tutorial": tutorial_rooms,
    "1": level_1_rooms
}

def load_level(name: str | int) -> tuple[dict, int, int]:
    """
    ...Loads the level and the loot inside it.

    :params:
        name: (str | int): The name of the level.

    :returns:
        level (object): The level object.
        loot_contents (list): A list of the loot items inside the level. 
    """
    for key in levels.keys():
        if str(name) == key:
            level = levels[key]

    entities = level.entities
    loot_contents = spawn_loot(level.loot, level.loot_rarity)

    return level, entities, loot_contents

def load_level_room(level: object, entities: int, enemies: list, loot_contents: list) -> tuple[object, int, list, list]:
    """
    ...Loads a room in a level, if there are enemies or loot in the level, there is a chance of an entity being in this room.

    :params:
        level (object): The level object.
        entities (int): The number of entities inside the level.
        enemies (list): The list of enemies inside the level.
        loot_contents (list): The list of loot inside the level.

    :returns:
        room (object): The room object to be loaded.
        entities (int): The number of entities inside the level.
        enemies (list): The list of enemies inside the level.
        loot_contents (list): The list of loot inside the level.
    """
    for key in levels.keys():
        if str(level.name) == key:
            level = levels[key]

    if entities == 0:
        is_entity = False
        room = LevelRoom(name="placeholder_room", is_entity=False, is_enemy=False, is_loot=False, loot_item=None)
    else:
        for entity in range(entities):
            is_entity = True
            entities = entities - 1
            break

    if is_entity == True:
        if len(enemies) == 0:
            is_enemy = False
        else:
            is_enemy = True
            for enemy in enemies:
                # chance = random.randint(1, level.num_rooms)
                # if chance == 1:
                enemies.remove(enemy)

                room = LevelRoom(name="placeholder_room", is_entity=True, is_enemy=True, is_loot=False, loot_item=None)
                break

        if len(loot_contents) == 0:
            is_loot = False
        else:
            if is_enemy == False:
                for loot_item in loot_contents:
                        # chance = random.randint(1, level.num_rooms)
                        # if chance == 1:
                    for loot_item in loot_contents:
                        loot_item = loot_item
                        loot_contents.remove(loot_item)

                        room = LevelRoom(name="placeholder_room", is_entity=True, is_enemy=False, is_loot=True, loot_item=loot_item)
                        break
                else:
                    room = LevelRoom(name="placeholder_room", is_entity=False, is_enemy=False, is_loot=False, loot_item=None)

        return room, entities, enemies, loot_contents

    return room, entities, enemies, loot_contents