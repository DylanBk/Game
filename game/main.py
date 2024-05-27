import pickle # used for object serialisation (to store in CSV)
import pandas as pd
import os, time
from modules import *

# SAVE/LOAD GAME DATA
def save_game_data(player: object, difficulty: str, level: str | int) -> pd.DataFrame:
    """
    ...Saves game data to a dictionary and then writes the dictionary into a new temporary DataFrame and then to the relevant CSV file.

    :params:
        player (object): The player object to be accessed and saved.
        difficulty (str): The difficulty of the game.
        level (str): The level that the player is on.
    """
    try:
        data = pd.read_csv('game/data/plus_data.csv')
        file = 'game/data/plus.csv'
    except:
        data = pd.read_csv('game/data/data.csv')
        file = ('game/data/data.csv')

    player_serialised = pickle.dumps(player).hex() # converts obj to str
    weapon_serialised = pickle.dumps(player.weapon).hex()
    shield_serialised = pickle.dumps(player.shield).hex()
    armour_serialised = pickle.dumps(player.armour).hex()
    potion_serialised = pickle.dumps(player.potion).hex()

    player_info: dict = {
        "player": player_serialised,
        "difficulty": difficulty,
        "level": level,
        "character_name": player.name,
        "character_health": player.health,
        "weapon": weapon_serialised,
        "shield": shield_serialised,
        "armour": armour_serialised,
        "potion": potion_serialised
        }

    df = pd.DataFrame([player_info])
    df.to_csv(file, mode='w', index=False, header=True)

    return df

def load_game_data(df: pd.DataFrame) -> dict:
    """
    ...Loads data from the DataFrame and puts it inside a dictionary, to_dict() is unsuitable because objects are stored.

    :params:
        df (pd.DataFrame): The DataFrame to be accessed.

    :returns:
        player_info (dict): The dictionary containing data from the DataFrame.
    """
    if df.empty:
        print("Error: No Data Found")
        input("Press [ENTER] to return to main menu")
        menu()

    player_serialised = df.player.values[0]
    player_serialised = bytes.fromhex(player_serialised) # converts str to obj
    player = pickle.loads(player_serialised)

    weapon_serialised = df.weapon.values[0]
    weapon_serialised = bytes.fromhex(weapon_serialised)
    weapon = pickle.loads(weapon_serialised)

    shield_serialised = df.shield.values[0]
    shield_serialised = bytes.fromhex(shield_serialised)
    shield = pickle.loads(shield_serialised)

    armour_serialised = df.armour.values[0]
    armour_serialised = bytes.fromhex(armour_serialised)
    armour = pickle.loads(armour_serialised)

    potion_serialised = df.potion.values[0]
    potion_serialised = bytes.fromhex(potion_serialised)
    potion = pickle.loads(potion_serialised)

    player_info: dict = {
        "player": player,
        "difficulty": df.difficulty.values[0],
        "level": df.level.values[0],
        "character_name": df.character_name.values[0],
        "character_health": df.character_health.values[0],
        "weapon": weapon,
        "shield": shield,
        "armour": armour,
        "potion": potion
    }

    return player_info


# CAMPAIGN

def campaign(df: pd.DataFrame) -> None: # load levels, location, etc
    """
    ...Loads into the previous save point of the game, will load the player into the last level they were on.

    :params:
        df (pd.DataFrame): The DataFrame to be accessed.
    """
    os.system("cls")
    player_info = load_game_data(df)
    player = player_info["player"]
    difficulty = player_info["difficulty"]
    level_name = player_info["level"]
    level_name = 1
    level, entities, loot_contents = load_level(name=level_name)
    match difficulty:
        case "Easy":
            damage_multiplier = 1
        case "Medium":
            damage_multiplier = 1.25
        case "Hard":
            damage_multiplier = 1.5

    enemies_temp: list = []
    enemies: list = []
    i = 0
    for enemy in range(level.enemies):
        i += 1
        enemy = spawn_enemy(name=(f"enemy{i}"), difficulty=difficulty, health=100, damage_multipler=damage_multiplier)
        enemies_temp.append(enemy)
        enemies.append(enemy)

    rooms: dict = {}
    for i in range(level.num_rooms):
        room, entities, enemies_temp, loot_contents = load_level_room(level=level, entities=entities, enemies=enemies_temp, loot_contents=loot_contents)
        rooms[i] = room
    # print(room.is_entity, room.is_enemy, room.is_loot)

    for index, room in enumerate(rooms.values()):
        current_room = index
        if room.is_enemy:
            print(f"{player.name} stumbles upon a(n) {enemy.name} in this room.")
            while True:
                choice = input("Choose an action:\n[1] Fight\n[2] Drink a Potion\n[3] Flee\n> ")
                if choice.isalnum():
                    if choice.isalpha():
                        print("\nInvalid input: Please choose a valid option.\n")
                        continue
                    else:
                        match choice:
                            case "1":
                                enemy_state = fight(player, enemies)
                                room.is_enemy = enemy_state
                            case "2":
                                player.heal()
                            case "3":
                                current_room = flee(player, level, enemy, rooms, current_room)
                                break
                else:
                    print("\nInvalid input: Please choose a valid option.\n")
                    continue
        elif room.is_loot:
            if len(loot_contents) > 0:
                for loot_item in loot_contents:
                    print(f"You have found a(n) {loot_item.name}!")

                    while True:
                        choice = input("Would you like to equip this item? [Y/N]: ")
                        if choice.isalnum():
                            if choice.isnumeric():
                                print("\nInvalid input: Please select Y or N.\n")
                                continue
                            else:
                                player.equip(loot_item)
                                break
                        else:
                            print("\nInvalid input: Please select Y or N.\n")
                            continue
                    loot_contents.remove(loot_item)
                    break
        else:
            print("This room is empty, you are safe from enemies for now. But there is also no loot.")
            input("Press [ENTER] to move on")



def exploring(): # exploring the world
    pass

def fight(player: object, enemies: list): # fight enemy
    if len(enemies) > 0:
        for enemy in enemies:
            while player.health > 0 and enemy.health > 0:
                print()
                player.health_bar.draw()
                enemy.health_bar.draw()
                print()

                if enemy.health > 0:
                    if player.health > 0:
                        choice = input("Choose an Action:\n[1] Attack\n[2] Drink a Potion\n[3] Flee\n> ")
                        if choice.isalnum():
                            if choice.isalpha():
                                pass
                            else:
                                match choice:
                                    case "1":
                                        player.attack(enemy)
                                        enemy.attack(player)
                                        continue
                                    case "2":
                                        player.health = player.heal() # testing !!!!!!!
                                        enemy.attack(player)
                                        continue
                                    case "3":
                                        continue # !!! sort it out !!!
                                    case default:
                                        print("\nInvalid input: Please choose a valid action.\n")
                                        continue
                        else:
                            print("\nInvalid input: Please choose a valid action.\n")
                            continue
                    else:
                        pass # player death subroutine
                else:
                    enemy_state = False
                    print(f"{player.name} has defeated {enemy.name}!")
    else:
        enemy_state = False
        print("This room is empty, you are safe from enemies for now. But there is also no loot.")
        input("Press [ENTER] to move on")

    return enemy_state

def flee(player:object, level: object, enemy: object, rooms: list, current_room: int) -> int: # run away
    """
    ...Allows the user to run to the previous room.

    :params:
        player (object): The player object.
        level (object): The level object.
        enemy (object): The enemy object inside the current room.
        rooms (list): List of rooms inside the level.
        current_room (int): The current room.

    :returns:
        current_room (int): The new current room.
    """
    if current_room == 0:
        print(f"{player.name} attempts to run back out of {level.name} but realises they cannot escape, there is no option but fight.")
        return current_room
    else:
        print(f"{player.name} flees from the {enemy.name} into the safety of the previous room.")
        current_room = rooms[current_room - 1]

    return current_room


# TUTORIAL

def tutorial(df: pd.DataFrame) -> None:
    """
    ...The Tutorial for the game, the user is told information, given a random common loot item, and then fights a low level enemy.

    :params:
        df (pd.DataFrame): The DataFrame to be accessed.
    """
    player_info = load_game_data(df)
    player = player_info["player"]
    level = level_tutorial
    _, _, loot_contents = load_level("tutorial") # _ bins the expected data as it is not needed

    tutorial_enemy = spawn_enemy(name="placeholder", difficulty=player_info["difficulty"], health=100, damage_multipler=1)

    os.system("cls")
    print("Welcome to the Tutorial, before you can jump into the action you must complete this.")
    input("Press [ENTER] to continue")
    print("Throughout the world you will find loot, loot includes weapons, shields, and armour, there are three rarities; common, uncommon, and rare.")
    input("Press [ENTER] to continue")
    print("You will also come across many enemies who will try to kill you, you can either fight them or flee. Some enemies wil drop loot.")
    input("Press [ENTER] to continue")
    print("Try fighting this placeholder, here's some loot to help you win.")

    for item in loot_contents:
        player.equip(item)

    # for attr in vars(player):
    #     print(attr)
    # for attr in vars(tutorial_enemy):
    #     print(attr)

    while player.health > 0 and tutorial_enemy.health > 0:
        print()
        player.health_bar.draw()
        tutorial_enemy.health_bar.draw()
        print()

        if player.health > 0:
            player.attack(tutorial_enemy)

        if tutorial_enemy.health > 0:
            tutorial_enemy.attack(player)

        time.sleep(1)
    tutorial_enemy.health_bar.draw()

    print(f"\nWell done! You have defeated your first enemy, you can keep the {item.name}.")
    input("Press [ENTER] to exit Tutorial")

    player.health = 100
    player.health_bar.update()
    level = 1
    difficulty = player_info["difficulty"]

    df = save_game_data(player, difficulty, level)
    campaign(df)


# MENU SUBROUTINES

def continue_game(df: pd.DataFrame):
    player_info = load_game_data(df)
    campaign(df)

def new_game(df: pd.DataFrame):
    def create_character() -> Character:
        """
        ...Allows the user to enter data to customise their character.

        :returns:
            player (object): The player object which has been customised by the user.
        """
        while True:
            name: str = input("\nCharacter Name: ") # !!! add more options in future !!!

            if name.isalnum():
                player: object = Character(name=name, health=100)
                break
            else:
                print("\nYour name must be alphanumeric\n")
                continue

        return player

    def get_difficulty() -> str:
        """
        ...Allows the user to choose the difficulty of the game.

        :returns:
            difficulty (str): The chosen difficulty.
        """
        while True:
            difficulty = input("\nSelect a Difficulty:\n[1] Easy\n[2] Medium\n[3] Hard\n> ")

            if difficulty.isalnum():
                match difficulty:
                    case "1":
                        difficulty = "Easy"
                        break
                    case "2":
                        difficulty = "Medium"
                        break
                    case "3":
                        difficulty = "Hard"
                        break
                    case default:
                        print("\nInvalid input: Please choose a valid option.\n")
                        continue
            else:
                print("\nInvalid input: Please choose a valid option.\n")
                continue

        return difficulty

    player = create_character()
    player.potion = healing_potion_large
    difficulty = get_difficulty()

    df = save_game_data(player, difficulty, level="tutorial")

    print(f"\nWelcome {player.name}!")

    tutorial(df)

def settings(df: pd.DataFrame): # difficulty, etc
    menu()

def menu():
    try:
        data = pd.read_csv('game/data/plus_data.csv')
        df = pd.DataFrame(data)
        print("New Game+ file found")
    except:
        data = pd.read_csv('game/data/data.csv')
        df = pd.DataFrame(data)
        print("No New Game+ file found")

    os.system("cls")

    choice = input("Welcome to Placeholder\n[1] Continue Game\n[2] New Game\n[3] New Game+\n[4] Help\n[5] Exit\n> ")

    if choice.isalnum():
        if choice.isalpha():
            print("\nInvalid input: Please select a valid option.\n")
            time.sleep(2)
            menu()
        else:
            match choice:
                case "1":
                    continue_game(df)
                case "2":
                    new_game(df)
                case "3":
                    new_game(df)
                case "4":
                    settings(df)
                case "5":
                    os.system("cls")
                    exit()
                case default:
                    print("\nInvalid input: Please select a valid option.\n")
                    time.sleep(2)
                    menu()
    else:
        print("\nInvalid input: Please select a valid option.\n")
        time.sleep(2)
        menu()

menu()