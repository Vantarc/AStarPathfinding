from Map import Map
from display_manager import MazeDisplay
from AStar import PathfindingAlgorithm


map_size = (20, 20)
if __name__ == '__main__':
    display = MazeDisplay(map_size)
    mazeMap = Map(map_size)
    state = 0
    """states are: -1: reset Map
                   0: Build Map
                   1: Run step by step
                   2: Solve completely
                   3: waiting for input"""

    pathFinder = PathfindingAlgorithm(mazeMap)

    while not display.isClosed():

        display.updateViewport()
        display.handleEvents()

        # reset map
        if state == -1:
            mazeMap = Map(map_size)
            pathFinder = PathfindingAlgorithm(mazeMap)

            state = 0
        # building the map
        elif state == 0:

            display.updateMap(mazeMap)

        # run one pathfinder
        elif state == 1:
            pathFinder.solveNextStep(mazeMap)
            state = 0
        elif state == 2:
            if pathFinder.solveNextStep(mazeMap):
                state = 0

        display.renderMap(mazeMap)
        display.drawGUI(state)
        display.updateScreen()
        state = display.updateState(state)

    display.quit()
