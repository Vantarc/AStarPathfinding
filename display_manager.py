import pygame
from GUIState0 import *
from Colors import *


class MazeDisplay:
    QUAD_SIZE_IN_PIXELS = 50
    SPACING_BETWEEN_QUADS = 2

    zoom = 1
    x_scroll = 0
    y_scroll = 0
    moveFlag = False

    closed = False

    def __init__(self, grid_size):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1024, 600), pygame.RESIZABLE)
        pygame.display.set_caption("A* Pathfinding")

        self.window_size = (1024, 600)
        self.grid_size = grid_size

        self.x_scroll = -(self.QUAD_SIZE_IN_PIXELS + self.SPACING_BETWEEN_QUADS) * grid_size[0] / 2
        self.y_scroll = -(self.QUAD_SIZE_IN_PIXELS + self.SPACING_BETWEEN_QUADS) * grid_size[1] / 2

    def updateViewport(self):
        if pygame.mouse.get_pressed()[1]:
            if self.moveFlag:
                rel_x, rel_y = pygame.mouse.get_rel()
                self.x_scroll += rel_x
                self.y_scroll += rel_y
            else:
                pygame.mouse.get_rel()
                self.moveFlag = True
        else:
            self.moveFlag = False

    def drawGUI(self, state):
        # choose state
        if state == 0:
            renderGUI0(self.screen, self.window_size)

    def updateScreen(self):
        pygame.display.update()
        self.clock.tick(60)
        self.screen.fill(backround_color)

    def drawTile(self, color, tile):
        pygame.draw.rect(self.screen, color, (
            (tile[0] * (self.QUAD_SIZE_IN_PIXELS + self.SPACING_BETWEEN_QUADS) + self.x_scroll) * self.zoom +
            self.window_size[0] / 2,
            (tile[1] * (self.QUAD_SIZE_IN_PIXELS + self.SPACING_BETWEEN_QUADS) + self.y_scroll) * self.zoom +
            self.window_size[1] / 2,
            self.QUAD_SIZE_IN_PIXELS * self.zoom,
            self.QUAD_SIZE_IN_PIXELS * self.zoom), 0)

    def drawGCost(self, g_cost, tile, font):
        self.screen.blit(font.render(str(g_cost), True, (0, 0, 0)), (
            (tile[0] * (self.QUAD_SIZE_IN_PIXELS + self.SPACING_BETWEEN_QUADS) + self.x_scroll) * self.zoom +
            self.window_size[0] / 2,
            (tile[1] * (self.QUAD_SIZE_IN_PIXELS + self.SPACING_BETWEEN_QUADS) + self.y_scroll) * self.zoom +
            self.window_size[1] / 2))

    def drawHCost(self, h_cost, tile, font):
        surface = font.render(str(h_cost), True, (0, 0, 0))
        self.screen.blit(surface, (
            (tile[0] * (self.QUAD_SIZE_IN_PIXELS + self.SPACING_BETWEEN_QUADS) + self.x_scroll) * self.zoom + self.window_size[0] / 2 - surface.get_width() + self.QUAD_SIZE_IN_PIXELS * self.zoom,
            (tile[1] * (self.QUAD_SIZE_IN_PIXELS + self.SPACING_BETWEEN_QUADS) + self.y_scroll) * self.zoom + self.window_size[1] / 2))

    def drawFCost(self, f_cost, tile, font):
        surface = font.render(str(f_cost), True, (0, 0, 0))
        self.screen.blit(surface, (
            (tile[0] * (self.QUAD_SIZE_IN_PIXELS + self.SPACING_BETWEEN_QUADS) + self.x_scroll) * self.zoom + self.window_size[0] / 2 - surface.get_width() / 2 + self.QUAD_SIZE_IN_PIXELS / 2 * self.zoom,
            (tile[1] * (self.QUAD_SIZE_IN_PIXELS + self.SPACING_BETWEEN_QUADS) + self.y_scroll) * self.zoom + self.window_size[1] / 2 - surface.get_height() + self.QUAD_SIZE_IN_PIXELS * self.zoom))

    def renderMap(self, mapToRender):

        font = pygame.font.SysFont('Comic Sans MS', int(30 * self.zoom))
        big_font = pygame.font.SysFont('Comic Sans MS', int(40 * self.zoom))

        self.grid_size = mapToRender.size
        for x in range(mapToRender.size[0]):
            for y in range(mapToRender.size[1]):
                draw_costs = False
                tile_state = mapToRender.map_matrix[x, y][0]
                if tile_state == mapToRender.WALL:
                    self.drawTile(wall_color, (x, y))
                elif tile_state == mapToRender.FREE:
                    self.drawTile(free_tile_color, (x, y))
                elif tile_state == mapToRender.START_END:
                    self.drawTile(path_color, (x, y))
                elif tile_state == mapToRender.EXPLORED:
                    self.drawTile(explored_color, (x, y))
                    draw_costs = True
                elif tile_state == mapToRender.ALL_NEIGHBORS_EXPLORED:
                    self.drawTile(all_neighbors_explored_color, (x, y))
                    draw_costs = True
                elif tile_state == mapToRender.PATH:
                    self.drawTile(path_color, (x, y))
                    draw_costs = True

                if draw_costs and self.zoom > 0.3:

                    g_cost = mapToRender.getGCost((x, y))
                    h_cost = mapToRender.getHCost((x, y))
                    self.drawGCost(g_cost, (x, y), font)
                    self.drawHCost(h_cost, (x, y), font)
                    self.drawFCost(g_cost + h_cost, (x, y), big_font)

    def isClosed(self):
        return self.closed

    def handleEvents(self):
        # set closed variable to true if window was close requested
        if pygame.event.get(pygame.QUIT):
            self.closed = True

        for event in pygame.event.get():
            # handle mouse wheel input
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.zoom += 0.01
                if event.button == 5:
                    self.zoom -= 0.01

            # handle resize event
            elif event.type == pygame.VIDEORESIZE:
                self.window_size = event.size
                pygame.display.flip()

    def quit(self):
        pygame.display.quit()

    def getCurrentCell(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x_pos = ((mouse_x - self.window_size[0] / 2) / self.zoom - self.x_scroll)
        y_pos = ((mouse_y - self.window_size[1] / 2) / self.zoom - self.y_scroll)
        if x_pos <= 0 or (self.QUAD_SIZE_IN_PIXELS + self.SPACING_BETWEEN_QUADS) * self.grid_size[0] <= x_pos or \
                y_pos <= 0 or (self.QUAD_SIZE_IN_PIXELS + self.SPACING_BETWEEN_QUADS) * self.grid_size[0] <= y_pos:
            return
        return int(x_pos / (self.QUAD_SIZE_IN_PIXELS + self.SPACING_BETWEEN_QUADS)), int(
            y_pos / (self.QUAD_SIZE_IN_PIXELS + self.SPACING_BETWEEN_QUADS))

    def updateMap(self, mapToUpdate):
        if pygame.mouse.get_pressed()[0] and not mouseIsInGUI0(self.window_size):
            cell = self.getCurrentCell()
            if cell is None:
                return
            mapToUpdate.setTileToWall(cell)
        if pygame.mouse.get_pressed()[2] and not mouseIsInGUI0(self.window_size):
            cell = self.getCurrentCell()
            if cell is None:
                return
            mapToUpdate.setTileToFree(cell)

    def updateState(self, state):
        if state == 0:
            return updateState0(self.window_size)
        elif state == 2:
            return 2

