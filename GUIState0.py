import pygame
from Colors import *


reload_image = pygame.image.load("reload.png")
mouse_pressed = False
def renderGUI0(screen, window_size):
    font = font = pygame.font.SysFont('Comic Sans MS', int(30))

    # solve
    pygame.draw.rect(screen, gui_color, (
        int(window_size[0] * 0.505), int(window_size[1] * 0.9), int(window_size[0] * 0.485),
        int(window_size[1] * 0.09)))

    surface = font.render("Solve", True, (0, 0, 0))
    screen.blit(surface, (int(window_size[0] * 0.7475 - surface.get_width()/2), int(window_size[1] * 0.945 - surface.get_height()/2)))

    # solve stepwise
    pygame.draw.rect(screen, gui_color, (
        int(window_size[0] * 0.01), int(window_size[1] * 0.9), int(window_size[0] * 0.485),
        int(window_size[1] * 0.09)))

    surface = font.render("Solve step-by-step", True, (0, 0, 0))
    screen.blit(surface, (int(window_size[0] * 0.2525 - surface.get_width()/2), int(window_size[1] * 0.945 - surface.get_height()/2)))

    # restart
    min_window_size = min(window_size)
    pygame.draw.rect(screen, gui_color, (
        int(window_size[0] * 0.01), int(window_size[1] * 0.01), int(min_window_size * 0.1),
        int(min_window_size * 0.1)))
    surface = pygame.transform.smoothscale(reload_image, (int(min_window_size * 0.1), int(min_window_size * 0.1)))
    screen.blit(surface, (window_size[0] * 0.01, window_size[1] * 0.01))

def mouseIsInGUI0(window_size):
    mouse_pos = pygame.mouse.get_pos()
    inSolveBox = int(window_size[0] * 0.505) < mouse_pos[0] < int(window_size[0] * 0.99) and int(window_size[1] * 0.9)<mouse_pos[1] < int(window_size[1] * 0.99)
    inSolveStepBox = int(window_size[0] * 0.01) < mouse_pos[0] < int(window_size[0] * 0.495) and int(window_size[1] * 0.9)<mouse_pos[1] < int(window_size[1] * 0.99)
    return inSolveBox or inSolveStepBox


def updateState0(window_size):

    global mouse_pressed

    # if mouse is pressed
    if pygame.mouse.get_pressed()[0]:
        if not mouse_pressed:
            mouse_pressed = True
            mouse_pos = pygame.mouse.get_pos()
            # if mouse is in solve button
            if int(window_size[0] * 0.505) < mouse_pos[0] < int(window_size[0] * 0.99) and int(window_size[1] * 0.9) < mouse_pos[1] < int(window_size[1] * 0.99):
                return 2
            if int(window_size[0] * 0.01) < mouse_pos[0] < int(window_size[0] * 0.495) and int(window_size[1] * 0.9)<mouse_pos[1] < int(window_size[1] * 0.99):
                return 1
            if int(window_size[0] * 0.01) < mouse_pos[0] < int(min(window_size) * 0.11) and int(window_size[1] * 0.01) < mouse_pos[1] < int(min(window_size) * 0.99):
                return -1
    else:
        mouse_pressed = False
    return 0
