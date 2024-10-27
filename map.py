from opensimplex import OpenSimplex
import numpy as np
from pprint import pformat
from tileenum import TileEnum
from tile import Tile

class Map:
    def __init__(self, seed):
        self.seed = seed
        self.noise = OpenSimplex(self.seed)
        self.width = 20
        self.height = 20
        self.water_level = 0.0
        self.field_level = 0.25
        self.forest_level = 1
        self.map = self._generate_map()
        

    def __str__(self):
        return pformat([[str(tile) for tile in row] for row in self.map], indent=2, width=1000)
    
    def _simple_curve(self, x, y):
        value = value = self.noise.noise2(x, y)
        start = 0.3
        end = 0.4
        if value < start:
            return 0.0
        if value > end:
            return 1.0
        return (value - start) * ( 1 / (end - start))
    
    def _flat(self, x, y):
        value = self.noise.noise2(x, y)
        value = value + 0.15
        if value > 0:
            value = value**0.25
        return value
    
    def _jagged(self, x, y):
        value = self.noise.noise2(x*6.0, y*3.0)
        return value * 2.0
    
    def _combined(self, x, y):
        j = self._jagged(x, y)
        f = self._flat(x, y)
        w = self._simple_curve(x, y)
        return (f * w) + (j * (1 - w))
    
    def _generate_map(self):
        map = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                val = self._combined(i, j)
                if val <= self.water_level:
                    row.append(Tile(TileEnum.WATER))
                elif self.water_level < val <= self.field_level:
                     row.append(Tile(TileEnum.SAND))
                elif self.field_level < val <= self.forest_level:
                     row.append(Tile(TileEnum.FOREST))
                else:
                     row.append(Tile(TileEnum.MOUNTAIN))
            map.append(row)
        return map