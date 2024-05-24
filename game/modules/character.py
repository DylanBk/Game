import random
from .items import *
from .health_bar import *

class Character ():
    def __init__(self,
                 name: str,
                 health: int) -> None:
        self.name = name
        self.health = health
        self.health_max = health
        self.health_bar = HealthBar(self, colour="green")
        self.weapon = default_weapon
        self.shield = default_shield
        self.armour = default_armour

    def equip(self, item) -> None:
        """
        ...Equips an item for the player.

        :params:
            item (object): The item to be equipped.
        """
        if item in Weapon.all_weapons:
            self.weapon = item
        elif item in Shield.all_shields:
            self.shield = Shield
        elif item in Armour.all_armours:
            self.armour = item
        print(f"{self.name} equipped a(n) {item.name}")

    def drop(self, item) -> None:
        """
        ...Removes an item from the player's inventory

        :params:
            item (object): The item to be removed.
        """
        if item in Weapon.all_weapons:
            self.weapon = default_weapon
        elif item in Shield.all_shields:
            self.shield = default_shield
        else:
            self.armour = default_armour

        print(f"{self.name} dropped a {item.name}")

    def attack(self, target: object) -> None:
        """
        ...Allows the player to attack an enemy.

        :params:
            target (object): The enemy object to be attacked.
        """
        if target.armour == default_armour and target.shield == default_shield: # no shield and no armour
            target.health -= self.weapon.damage
            target.health = max(target.health, 0)
            damage = self.weapon.damage
        elif target.armour != default_armour and target.shield == default_shield: # armour and no shield
            target.health -= (self.weapon.damage * 0.75)
            target.health = max(target.health, 0)
            target.armour.durability -= (self.weapon.damage * 0.75)
            target.armour.durability = max(target.armour.durability, 0)
            damage = self.weapon.damage
        elif target.armour == default_armour and target.shield != default_shield: # no armour but shield
            hit = random.randint(1, 4) # 1 == shield blocked hit, 2,3,4 == hit
            if hit == 1:
                damage = 0
            else:
                target.health -= self.weapon.damage
                target.health = max(target.health, 0)
                damage = self.weapon.damage
        else:                                                                     # shield and armour
            hit = random.randint(1, 4)
            if hit == 1:
                damage = 0
            else:
                target.health -= (self.weapon.damage * 0.75)
                target.health = max(target.health, 0)
                target.armour.durability -= (self.weapon.damage * 0.75)
                target.armour.durability = max(target.armour.durability, 0)
                damage = self.weapon.damage

        target.health_bar.update()

        if damage == 0:
            print(f"{target.name} blocked {self.name}'s hit with their shield!")
        else:
            print(f"{self.name} dealt {damage} damage to {target.name} with {self.weapon.name}")