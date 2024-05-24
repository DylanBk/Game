import random
from .health_bar import *
from .items import *

class Enemy():
    enemy_types: list = []

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

        if self.name in Enemy.enemy_types:
            pass
        else:
            Enemy.enemy_types.append(self)

    def equip(self, item) -> None:
        """
        ...Equips an item for an enemy.

        :params:
            item (object): The item to be equipped.
        """
        if item in Weapon.all_weapons:
            self.weapon = item
        elif item in Shield.all_shields:
            self.shield = item
        else:
            self.armour = item

        print(f"{self.name} equipped a {self.item.name}")

    def drop(self, item) -> None:
        """
        ...Removes an item from an enemy's inventory.

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
        ...Allows an enemy to attack the player.

        :params:
            target (object): The player object to be attacked.
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
    """
    ...Spawns an enemy.

    :params:
        name (str): The name of the enemy to be spawned.
        difficulty (str): The game difficulty.
        health (int): The enemy's health.
        damage_multiplier (float): The damage multiplier based on the game's difficulty.

    :returns:
        enemy_type (object): The enemy object.
    """
    enemy_difficulties: dict = {
        "Easy": EasyEnemy,
        "Medium": MediumEnemy,
        "Hard": HardEnemy
    }
    enemy_type = enemy_difficulties.get(difficulty, EasyEnemy) # EasyEnemy is a fallback incase no difficulty

    return enemy_type(name, health, damage_multipler)

zombie = Enemy(name="Zombie", health=50, damage_multiplier=1)
