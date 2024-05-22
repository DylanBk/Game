import pandas as pd
import os, time
from modules import *

def continue_game(df):
    pass

def new_game(df):
    def create_character() -> Character:
        name: str = input("Character Name: ") # !!! add more options in future !!!
        player = Character(name=name, health=100)

        return player

    def get_difficulty() -> str:
        while True:
            difficulty = input("Select a Difficulty:\n[1] Easy\n[2] Medium\n[3] Hard")

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

    player_info: dict = {
        "difficulty": [difficulty],
        "character_name": [player.name],
        "character_health": [player.health],
        "weapon": [weapon.default_weapon]        
        }

    player_info_df = pd.DataFrame(player_info)

    if len(df) > 1: # create new file instead of overwriting current
        with open ('game/data/plus_data.csv', mode='w', newline='') as f:
            player_info_df.to_csv('game/data/plus_data.csv', mode='a', index=False, header=True)
    else:
        player_info_df.to_csv('game/data/data.csv', mode='a', index=False, header=False)


        print(f"\nCharacter Created\nWelcome {player.name}!")
        print(player.weapon.name)

def settings(df): # difficulty, etc
    pass

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