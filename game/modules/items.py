class Weapon():
    all_weapons: list = []

    def __init__(self,
                 rarity: str,
                 name: str,
                 weapon_type: str,
                 damage: int) -> None:
        self.rarity = rarity
        self.name = name
        self.weapon_type = weapon_type
        self.damage = damage

        Weapon.all_weapons.append(self)

class Shield():
    all_shields: list = []

    def __init__(self, rarity: str, name: str, durability: int) -> None:
        self.rarity = rarity
        self.name = name
        self.durability = durability

        Shield.all_shields.append(self)

class Armour():
    all_armours: list = []

    def __init__(self, rarity: str, name: str, durability: int) -> None:
        self.rarity = rarity
        self.name = name
        self.durability = durability

        Armour.all_armours.append(self)

# --- WEAPONS ---

# default (fists)
default_weapon = Weapon(rarity="common", name="Fists", weapon_type="Blunt",damage=4)
default_shield = Shield(rarity=None, name="No Shield", durability=0)
default_armour = Armour(rarity=None, name="No Armour", durability=0)

#Knives/Daggers
curved_dagger = Weapon(rarity="common", name="Curved Dagger", weapon_type="Knife", damage=6)

# Swords
iron_sword = Weapon(rarity="uncommon", name="Iron Sword", weapon_type="Sword", damage=10)

# Axes
iron_axe = Weapon(rarity="uncommon", name="Iron Axe", weapon_type="Axe", damage=8)

#Blunt
wooden_club = Weapon(rarity="common", name="Wooden Club", weapon_type="Blunt", damage=6)

# --- SHIELDS ---
# reduces target.damage ?

wooden_shield_light = Shield(rarity="common", name="Light Wooden Shield", durability=100)
wooden_shield_heavy = Shield(rarity="common", name="Heavy Wooden Shield", durability=150)

# kite_shield = Shield() # !!! UNORGANISED CURRENTLY !!!
# buckler_shield = Shield()
# targe_shield = Shield()
# heater_shield = Shield()
# tower_shield = Shield()
# pavise_shield = Shield()


# --- ARMOURS ---

leather_armour = Armour(rarity="common", name="Leather Armour", durability=300)
chainmail_armour = Armour(rarity="uncommon", name="Chainmail Armour", durability=750)
iron_armour = Armour(rarity="rare", name="Iron Armour", durability=1000)