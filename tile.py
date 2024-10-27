from tileenum import TileEnum

class Tile:

    def __init__(self, type: TileEnum):
        self.type = type


    def __str__(self):
        return self.type.value