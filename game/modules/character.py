from .weapon import *
from .health_bar import *

class Character ():

    def __init__(self, name: str, health: int) -> None:
        self.name = name
        self.health = health
        self.health_max = health
        self.weapon = default_weapon

    def equip(self, weapon) -> None:
        self.weapon = weapon
        print(f"{self.name} equipped a {self.weapon.name}")

    def drop(self) -> None:
        print(f"{self.name} dropped a {self.weapon.name}")
        self.weapon = self.default_weapon

    def attack(self, target) -> None:
        target.health -= self.weapon.damage
        target.health = max(target.health, 0)
        target.health_bar.update()

        print(f"{self.name} dealt {self.weapon.damage} damage to {target.name} with {self.weapon.name}")

class Hero(Character):
    def __init__(self, name: str, health: int) -> None:
        super().__init__(name=name, health=health)

        self.default_weapon = Weapon.fists
        self.health_bar = HealthBar(self, colour="green")

class Enemy(Character):
    def __init__(self, name: str, health: int) -> None:
        super().__init__(name, health)
        self.weapon = Weapon.fists
        self.health_bar = HealthBar(self, colour="red")