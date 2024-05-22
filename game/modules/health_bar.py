import os

os.system("")

class HealthBar():
    symbol_remaining: str = "🟩"
    symbol_lost: str = "_"
    barrier: str = "|"
    colours: dict = {
        "red": "\033[91m",
        "yellow": "\33[93m",
        "green": "\033[92m",
        "default": "\033[0m"
    }

    def __init__(self,
                entity,
                length: int = 20,
                is_coloured: bool = True,
                colour: str = "") -> None:
        self.entity = entity
        self.length = length
        self.is_coloured = is_coloured
        self.colour = self.colours.get(colour) or self.colours["default"]

        self.current_value = entity.health
        self.max_value = entity.health_max

    def update(self) -> None:
        self.current_value = self.entity.health

    def draw(self) -> None:
        remaining_bars = round(self.current_value / self.max_value * self.length)
        lost_bars = self.length - remaining_bars

        print(f"{self.entity.name}'s health: {self.entity.health}/{self.entity.health_max}")
        print(f"{self.barrier}"
              f"{self.colour if self.is_coloured else ''}"
              f"{remaining_bars * self.symbol_remaining}"
              f"{lost_bars * self.symbol_lost}"
              f"{self.colours['default'] if self.is_coloured else ''}"
              f"{self.barrier}"
        )