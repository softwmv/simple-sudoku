from random import sample

import pygame
from selection import NumberSelection
from copy import deepcopy

ROWS, COLS = 9, 9
CELL_COLOR = (98, 104, 128)
BORDER_COLOR = (255, 255, 255)
TEXT_COLOR = (202, 211, 245)

BASE_SIZE = 3
GRID_SIZE = BASE_SIZE * BASE_SIZE
GRID_X_POS = 285
GRID_Y_POS = 135

def pattern(row_num: int, col_num: int) -> int:
    return (BASE_SIZE *(row_num % BASE_SIZE) + row_num // BASE_SIZE + col_num) % GRID_SIZE

# Return a shuffled list of numbers from 1 to 9
def shuffle(samp: range) -> list:
    return sample(samp, len(samp))

def create_grid():
    rBase = range(BASE_SIZE)
    rows = [g * BASE_SIZE + r for g in shuffle(rBase) for r in rBase]
    cols = [g * BASE_SIZE + c for g in shuffle(rBase) for c in rBase]
    nums = shuffle(range(1, GRID_SIZE + 1))

    return [[nums[pattern(r, c)] for c in cols] for r in rows]

class Grid:
    def __init__(self, pg, font):
        self.pg = pg
        self.game_font = font
        self.cell_size = 70
        self.x_offset = 31
        self.y_offset = 26
        self.grid = create_grid()
        self.__test_grid = deepcopy(self.grid)
        self.win = False
        
        self.remove_numbers(self.grid)
        self.occupied_cells_coords = self.get_preoccupied_cells()
        self.selection = NumberSelection(pg, self.game_font)

    def __draw_grid(self, surface):
        self.pg.draw.rect(surface, BORDER_COLOR, (GRID_X_POS, GRID_Y_POS, COLS * self.cell_size, ROWS * self.cell_size), 2)
        for row in range(1, ROWS):
            y = row * self.cell_size
            if row % 3 == 0:
                self.pg.draw.line(surface, BORDER_COLOR, (GRID_X_POS, y + GRID_Y_POS), (COLS * self.cell_size + GRID_X_POS, y + GRID_Y_POS), 2)
            else:
                self.pg.draw.line(surface, CELL_COLOR, (GRID_X_POS, y + GRID_Y_POS), (COLS * self.cell_size + GRID_X_POS, y + GRID_Y_POS), 1)
        for col in range(1, COLS):
            x = col * self.cell_size
            if col % 3 == 0:
                self.pg.draw.line(surface, BORDER_COLOR, (x + GRID_X_POS, GRID_Y_POS), (x + GRID_X_POS, ROWS * self.cell_size + GRID_Y_POS), 2)
            else:
                self.pg.draw.line(surface, CELL_COLOR, (x + GRID_X_POS, GRID_Y_POS), (x + GRID_X_POS, ROWS * self.cell_size + GRID_Y_POS), 1)
            
    def __draw_numbers(self, surface):
        # Traverse row, then column
        for y in range(ROWS):
            for x in range(COLS):
                if self.get_cell(y, x) != 0:
                    if (y,x) in self.occupied_cells_coords:
                        text_surface = self.game_font.render(str(self.get_cell(y, x)), True, TEXT_COLOR)
                    elif self.get_cell(y,x) != self.__test_grid[y][x]:
                        text_surface = self.game_font.render(str(self.get_cell(y, x)), True, (210, 15, 57))
                    else:
                        text_surface = self.game_font.render(str(self.get_cell(y, x)), True, (114, 135, 253))

                    surface.blit(text_surface, (x * self.cell_size + self.x_offset + GRID_X_POS, y * self.cell_size + self.y_offset + GRID_Y_POS))

    def remove_numbers(self, grid: list[list[int]]) -> None:
        squares = GRID_SIZE * GRID_SIZE
        empties = squares * 3 // 6  # Higher the number, the easier the game. 4 is lowest
        for i in sample(range(squares), empties):
            grid[i // GRID_SIZE][i % GRID_SIZE] = 0

    def get_preoccupied_cells(self):
        occupied = []
        for y in range(ROWS):
            for x in range(COLS):
                if self.get_cell(y, x) != 0:
                    occupied.append((y, x))
        return occupied

    def is_preoccupied(self, row: int, col: int) -> bool:
        return (row, col) in self.occupied_cells_coords
    
    def check_grids(self):
        for y in range(ROWS):
            for x in range(COLS):
                if self.grid[y][x] != self.__test_grid[y][x]:
                    return False
        return True

    def get_mouse_click(self, x:int, y:int):
        if GRID_X_POS <= x <= (COLS * self.cell_size + GRID_X_POS) and GRID_Y_POS <= y <= (ROWS * self.cell_size + GRID_Y_POS):
            row, col = (y - GRID_Y_POS) // self.cell_size, (x - GRID_X_POS) // self.cell_size
            if not self.is_preoccupied(row, col):
                self.set_cell(row, col, self.selection.selected_num)
        self.selection.button_click(x, y)
        if self.check_grids():
            self.win = True

    def draw_all(self, surface):
        self.__draw_grid(surface)
        self.__draw_numbers(surface)
        self.selection.draw_buttons(surface)

    def get_cell(self, row: int, col: int) -> int:
        return self.grid[row][col]

    def set_cell(self, row: int, col: int, value: int):
        if not self.is_preoccupied(row, col):
            self.grid[row][col] = value


    def restart(self) -> None:
        self.grid = create_grid()
        self.__test_grid = deepcopy(self.grid)
        self.remove_numbers(self.grid)
        self.occupied_cells_coords = self.get_preoccupied_cells()
        self.win = False