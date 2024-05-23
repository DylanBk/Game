import pickle
import pandas as pd
import os, time
from modules import *

def load_game_data(df: pd.DataFrame) -> dict:
    """
    ...Loads data from the DataFrame and puts it inside a dictionary, to_dict() is unsuitable because objects are stored.

    :params:
        df: The DataFrame to be accessed.

    :returns:
        player_info (dict): The dictionary containing data from the DataFrame.
    """
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

    player_info: dict = {
        "player": player,
        "difficulty": df.difficulty.values[0],
        "level": df.level.values[0],
        "character_name": df.character_name.values[0],
        "character_health": df.character_health.values[0],
        "weapon": weapon,
        "shield": shield,
        "armour": armour
    }

    return player_info

# CAMPAIGN
def campaign(): # load levels, location, etc
    pass

def exploring(): # exploring the world
    pass

def fight(): # fight enemy
    pass

def flee(): # run away
    pass

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
    tutorial_loot = level_tutorial.spawn_loot(loot=1, loot_rarity="common")
    tutorial_enemy = spawn_enemy(name="placeholder", difficulty=player_info["difficulty"], health=100, damage_multipler=1)

    os.system("cls")
    print("Welcome to the Tutorial, before you can jump into the action you must complete this.")
    input("Press [ENTER] to continue")
    print("Throughout the world you will find loot, loot includes weapons, shields, and armour, there are three rarities; common, uncommon, and rare.")
    input("Press [ENTER] to continue")
    print("You will also come across many enemies who will try to kill you, you can either fight them or flee. Some enemies wil drop loot.")
    input("Press [ENTER] to continue")
    print("Try fighting this placeholder, here's some loot to help you win.")

    for item in tutorial_loot:
        player.equip(item)

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

    print(f"\nWell done! You have defeated your first enemy, you can keep the {item}.")
    input("Press [ENTER] to exit Tutorial")


# MENU SUBROUTINES

def continue_game(df: pd.DataFrame):
    player_info = load_game_data(df)

def new_game(df: pd.DataFrame):
    def create_character() -> Character:
        """
        ...Allows the user to enter data to customise their character.

        :returns:
            player (obj): The player object which has been customised by the user.
        """
        while True:
            name: str = input("\nCharacter Name: ") # !!! add more options in future !!!

            if name.isalnum():
                player = Character(name=name, health=100)
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
    difficulty = get_difficulty()
    player_serialised = pickle.dumps(player).hex() # converts obj to str
    weapon_serialised = pickle.dumps(weapon).hex()
    shield_serialised = pickle.dumps(shield).hex()
    armour_serialised = pickle.dumps(armour).hex()

    player_info: dict = {
        "player": player_serialised,
        "difficulty": difficulty,
        "level": 1,
        "character_name": player.name,
        "character_health": player.health,
        "weapon": weapon_serialised,
        "shield": shield_serialised,
        "armour": armour_serialised
        }

    player_info_df = pd.DataFrame([player_info])

    if len(df) > 1: # create new file instead of overwriting current
        with open ('game/data/plus_data.csv', mode='w', newline='') as f:
            player_info_df.to_csv('game/data/plus_data.csv', mode='a', index=False, header=True)
    else:
        player_info_df.to_csv('game/data/data.csv', mode='a', index=False, header=False)

    print(f"\nWelcome {player.name}!")

    data = pd.read_csv('game/data/data.csv') # forces data to save then use an updated DataFrame/CSV
    df = pd.DataFrame(data)

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

    choice = input("Welcome to Placeholder\n[1] Continue Game\n[2] New Game\n[3] New Game+\n[4] Help\n[5] Exit\n> ")

    if choice.isalnum():
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

menu()