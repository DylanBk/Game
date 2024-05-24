class Weapon():

    def __init__(self, name: str, weapon_type: str, damage: int) -> None:
        self.name = name
        self.weapon_type = weapon_type
        self.damage = damage

default_weapon = Weapon("Fists", "Blunt", 4)
# fists = Weapon("Fists", "Blunt", 4)
iron_sword = Weapon("Iron Sword", "Sword", 10)
iron_axe = Weapon("Iron Axe", "Axe", 8)