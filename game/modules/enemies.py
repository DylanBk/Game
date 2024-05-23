import random
from .health_bar import *
from .items import *

class Enemy():
    def __init__(self,
                 name: str,
                 health: int,
                 damage_multiplier: float) -> None:
        self.name = name
        self.health = health
        self.health_max = health
        self.health_bar = HealthBar(self, colour="red")
        self.damage_multiplier = damage_multiplier
        self.weapon = default_weapon
        self.shield = default_shield
        self.armour = default_armour

    def equip(self, weapon) -> None:
        self.weapon = weapon
        print(f"{self.name} equipped a {self.weapon.name}")

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
            hit = random.randint(1, 4) # 1 == hit, 2 == shield blocked hit
            if hit == 1:
                target.health -= self.weapon.damage
                target.health = max(target.health, 0)
                damage = self.weapon.damage
            else:
                damage = 0
        else:                                                                     # shield and armour
            hit = random.randint(1, 4)
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

class EasyEnemy(Enemy):
    def __init__(self,
                 name: str,
                 health: int,
                 damage_multiplier: float) -> None:
        super().__init__(name, health, damage_multiplier)
        self.health_bar = HealthBar(self, colour="red")
        self.damage_multiplier = 1

class MediumEnemy(Enemy):
    def __init__(self,
                 name: str,
                 health: int,
                 damage_multiplier: float) -> None:
        super().__init__(name, health, damage_multiplier)
        self.health_bar = HealthBar(self, colour="red")
        self.damage_multiplier = 1.25

class HardEnemy(Enemy):
    def __init__(self,
                 name: str,
                 health: int,
                 damage_multiplier: float) -> None:
        super().__init__(name, health, damage_multiplier)
        self.health_bar = HealthBar(self, colour="red")
        self.damage_multiplier = 1.5

def spawn_enemy(name: str, difficulty: str, health: int, damage_multipler: float) -> Enemy:
    enemy_difficulties: dict = {
        "Easy": EasyEnemy,
        "Medium": MediumEnemy,
        "Hard": HardEnemy
    }
    enemy_type = enemy_difficulties.get(difficulty, EasyEnemy) # EasyEnemy is a fallback incase no difficulty

    return enemy_type(name, health, damage_multipler)