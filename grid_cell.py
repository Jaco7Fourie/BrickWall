from typing import Tuple
import pygame


class GridCell:

    def __init__(self, surface: pygame.Surface, cell_type: str, bounding_rect: Tuple[int, int, int, int]):
        """
        Initialises a new cell in the grid
        :param surface: The surface that this cell will draw to
        :param cell_type: string to represent the type of the cell, one of {empty, path, visited, wall}
        :param bounding_rect: draw the grid only within these bounds
        (top_left_x, top_left_y, bottom_left_x, bottom_left_y)
        """
        self.bounds = bounding_rect
        self.surf = surface
        self.cell_type = cell_type

