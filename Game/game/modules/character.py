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
        if item in Weapon.all_weapons:
            self.weapon = item
        elif item in Shield.all_shields:
            self.shield = Shield
        elif item in Armour.all_armours:
            self.armour = item
        print(f"{self.name} equipped a(n) {item.name}")

    def drop(self) -> None:
        print(f"{self.name} dropped a {self.weapon.name}")
        self.weapon = self.default_weapon

    def attack(self, target) -> None:
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
            hit = random.randint(1, 2) # 1 == hit, 2 == shield blocked hit
            if hit == 1:
                target.health -= self.weapon.damage
                target.health = max(target.health, 0)
                damage = self.weapon.damage
            else:
                damage = 0
        else:                                                                     # shield and armour
            hit = random.randint(1, 2)
            if hit == 1:
                target.health -= (self.weapon.damage * 0.75)
                target.health = max(target.health, 0)
                target.armour.durability -= (self.weapon.damage * 0.75)
                target.armour.durability = max(target.armour.durability, 0)
                damage = self.weapon.damage
            else:
                damage = 0

        target.health_bar.update()

        if damage == 0:
            print(f"{target.name} blocked {self.name}'s hit with their shield!")
        else:
            print(f"{self.name} dealt {damage} damage to {target.name} with {self.weapon.name}")