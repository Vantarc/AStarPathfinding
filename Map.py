import numpy as np
import random


class Map:

    WALL = 0
    FREE = 1
    START_END = 2
    EXPLORED = 3
    ALL_NEIGHBORS_EXPLORED = 4
    PATH = 5

    def __init__(self, size):
        # wall: 0 -> wall,1 -> free, 2 -> start/end, 3-> explored, 4-> all neighbors explored, 5-> path
        tile_dt = np.dtype([('wall', np.int), ('g_cost', np.int), ('h_cost', np.int), ('parent_tile_x', np.int), ('parent_tile_y', np.int), ('closed', np.bool)])
        self.map_matrix = np.zeros(size, dtype=tile_dt)

        self.size = size

        # set start
        self.start = (random.randint(0, size[0]-1), random.randint(0, size[1]-1))
        self.map_matrix[self.start][0] = 2

        self.end = (random.randint(0, size[0] - 1), random.randint(0, size[1] - 1))
        self.map_matrix[self.end][0] = 2

        for x in range(self.size[0]):
            for y in range(self.size[1]):
                self.setTileToFree((x, y))

    def setTileToWall(self, coords):
        if coords not in (self.start, self.end):
            self.map_matrix[coords][0] = self.WALL

    def setTileToFree(self, coords):
        if coords not in (self.start, self.end):
            self.map_matrix[coords][0] = self.FREE

    def setTileToExplored(self, coords):
        if coords not in (self.start, self.end):
            self.map_matrix[coords][0] = self.EXPLORED

    def setTileToNeighborsExplored(self, coords):
        if coords not in (self.start, self.end):
            self.map_matrix[coords][0] = self.ALL_NEIGHBORS_EXPLORED

    def setTileToPath(self, coords):
        if coords not in (self.start, self.end):
            self.map_matrix[coords][0] = self.PATH

    def getGCost(self, coords):
        return self.map_matrix[coords][1]

    def getHCost(self, coords):
        return self.map_matrix[coords][2]

    def getFCost(self, coords):
        return self.getHCost(coords) + self.getGCost(coords)

    def setGCost(self, coords, cost):
        self.map_matrix[coords][1] = cost

    def setHCost(self, coords, cost):
        self.map_matrix[coords][2] = cost

    def isWall(self, coords):
        return self.map_matrix[coords][0] == self.WALL

    def isClosed(self, coords):
        return self.map_matrix[coords][5]

    def setClosed(self, coords):
        self.map_matrix[coords][5] = True

    def setParent(self, coords, parent):
        self.map_matrix[coords][3] = parent[0]
        self.map_matrix[coords][4] = parent[1]

    def getParent(self, coords):
        return self.map_matrix[coords][3], self.map_matrix[coords][4]