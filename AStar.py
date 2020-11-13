import math
from Heap import MazeHeap


class PathfindingAlgorithm:

    def __init__(self, mapToSolve):
        self.open = MazeHeap(mapToSolve.size)
        self.open.addTile(mapToSolve.start, mapToSolve)

    def solveNextStep(self, mapToSolve):

        # choose tile to process
        current_tile = self.open.getFirstTile(mapToSolve)

        # set tile closed
        mapToSolve.setClosed(current_tile)
        mapToSolve.setTileToNeighborsExplored(current_tile)

        # if tile is end finish
        if current_tile == mapToSolve.end:
            print("finished")

            last_path_tile = mapToSolve.getParent(mapToSolve.end)
            while not last_path_tile == mapToSolve.start:
                mapToSolve.setTileToPath(last_path_tile)
                last_path_tile = mapToSolve.getParent(last_path_tile)

            return True

        # process each neighbour
        for neighbour in self.getNeighbours(current_tile, mapToSolve):
            # skip tile if wall or already closed
            if mapToSolve.isWall(neighbour) or mapToSolve.isClosed(neighbour):
                continue

            # calculate HCost if it isn't already calculated
            if mapToSolve.getHCost(neighbour) == 0:
                self.setHCost(neighbour, mapToSolve)

            g_cost = self.calculateGCost(neighbour, current_tile, mapToSolve.getGCost(current_tile))

            if g_cost < mapToSolve.getGCost(neighbour):
                self.open.updateTile(neighbour,mapToSolve)
                mapToSolve.setGCost(neighbour, g_cost)
                mapToSolve.setParent(neighbour, current_tile)

            if not self.open.contains(neighbour):
                mapToSolve.setGCost(neighbour, g_cost)
                mapToSolve.setParent(neighbour, current_tile)
                self.open.addTile(neighbour, mapToSolve)
                mapToSolve.setTileToExplored(neighbour)
        return False


    def getNeighbours(self, coords, mapToSolve):
        neighbours = []
        for x in range(coords[0]-1, coords[0]+2):
            for y in range(coords[1] - 1, coords[1] + 2):
                # test if tile is still in map
                if 0 <= x < mapToSolve.size[0] and 0 <= y < mapToSolve.size[1]:
                    neighbours.append((x, y))
        return neighbours

    def setHCost(self, coords, mapToSolve):

        distance_to_end_tile = (abs(mapToSolve.end[0] - coords[0]), abs(mapToSolve.end[1] - coords[1]))
        h_cost = min(distance_to_end_tile) * 14 + (max(distance_to_end_tile) - min(distance_to_end_tile)) * 10
        mapToSolve.setHCost(coords, h_cost)

    def calculateGCost(self, child_coords, parent_coords, parent_g_cost):
        return parent_g_cost + int(math.sqrt((abs(child_coords[0] - parent_coords[0]) ** 2 + abs(child_coords[1] - parent_coords[1]) ** 2)) * 10)



