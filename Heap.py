import numpy as np


class MazeHeap:

    def __init__(self, mapSize,):
        self.items = np.zeros((mapSize[0]*mapSize[1], 2), dtype=int)
        self.number_of_items = 0

    def addTile(self, coords, mazeMap):
        self.items[self.number_of_items] = np.array(coords)
        self.sortUp(self.number_of_items, mazeMap)
        self.number_of_items += 1

    def updateTile(self, coords, mazeMap):
        index = np.where((self.items[:] == coords).all(1))[0][0]
        self.sortUp(index, mazeMap)

    def sortUp(self, index, mazeMap):
        while index != 0:
            parent_index = int(index - 1 / 2)
            if self.compare(self.items[index], self.items[parent_index], mazeMap):
                self.swapItems(parent_index, index)
            else:
                break

            index = parent_index

    def sortDown(self, index, mazeMap):
        while True:
            child_index_left = index * 2 + 1
            child_index_right = index * 2 + 2

            swap_index = child_index_left

            # if left index exists item isn't at the bottom of the heap and can be sorted further
            if child_index_left < self.number_of_items:
                if self.compare(self.items[child_index_right], self.items[child_index_left], mazeMap):
                    swap_index = child_index_right

                if self.compare(self.items[swap_index], self.items[index], mazeMap):
                    self.swapItems(swap_index, index)
                    index = swap_index
                else:
                    return
            else:
                return

    def getFirstTile(self, mazeMap):
        firstTile = (self.items[0, 0], self.items[0, 1])

        self.number_of_items -= 1
        self.items[0] = self.items[self.number_of_items]

        self.sortDown(0, mazeMap)

        return firstTile

    def contains(self, tile):
        return any((self.items[:self.number_of_items] == tile).all(1))

    def isEmpty(self):
        if self.number_of_items == 0:
            return True
        return False

    def compare(self, coordsA, coordsB, mazeMap):
        # returns true if a is more important
        coordsA = tuple(coordsA.tolist())
        coordsB = tuple(coordsB.tolist())
        f_costA = mazeMap.getFCost(coordsA)
        f_costB = mazeMap.getFCost(coordsB)
        if f_costA < f_costB:
            return True
        elif f_costA > f_costB:
            return False
        elif mazeMap.getHCost(coordsA) < mazeMap.getHCost(coordsB):
            return True
        return False

    def swapItems(self, indexA, indexB):
        valueA = (self.items[indexA, 0], self.items[indexA, 1])
        self.items[indexA] = self.items[indexB]
        self.items[indexB] = np.array(valueA)
