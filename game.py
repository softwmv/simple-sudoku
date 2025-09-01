import pygame
import os
import ctypes
from grid import Grid

os.environ['SDL_VIDEO_CENTERED'] = '1'  # Center the window on the screen

pygame.init()
ctypes.windll.user32.SetProcessDPIAware()

FPS = 60
WIDTH, HEIGHT = 1200, 900
BACKGROUND_COLOR = (36, 39, 58)
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Game")

FONT = pygame.font.SysFont('Inter', 34, bold=False)

def main(window): 
    clock = pygame.time.Clock()
    grid = Grid(pygame, FONT)
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN and not grid.win:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    grid.get_mouse_click(pos[0], pos[1])
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and grid.win:
                    grid.restart()

            # Draw grid
            window.fill(BACKGROUND_COLOR)
            grid.draw_all(window)

            if grid.win:
                font2 = pygame.font.SysFont('Inter', 60, bold=False)
                text_surface = font2.render("You won!", True, (255, 255, 255))

                window.blit(text_surface,(510, 400))

                instruction_surface = FONT.render("Press Space to restart.", True, (255, 255, 255))
                window.blit(instruction_surface, (475, 450))


            pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main(WINDOW)