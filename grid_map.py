from typing import Tuple, List

from  grid_cell import GridCell
import pygame


class GridMap:
    """
    Defines the map of cells and keeps track of cell states
    """
    # the size in pixels of borders between cells
    BORDER_SIZE = 1

    def __init__(self, surface: pygame.Surface, bounding_rect: List[int], grid_size: Tuple[int, int]):
        """
        Initialises the grid as a list of GridCell objects
        :param surface: the background surface to draw on
        :param bounding_rect: draw the grid only within these bounds
        (top_left_x, top_left_y, bottom_right_x, bottom_right_y)
        :param grid_size: number of cells as (rows, columns)
        """
        self.surf = surface
        self.bounds = bounding_rect
        self.grid_size = grid_size

        self.cell_size = self.__get_cell_size()
        # update the bounds based on square sells
        self.bounds[2] = self.bounds[0] + self.cell_size*self.grid_size[1]
        self.bounds[3] = self.bounds[1] + self.cell_size * self.grid_size[0]
        self.cell_grid = [[None]*grid_size[1]]*grid_size[0]
        for i in range(grid_size[0]):
            for j in range(grid_size[1]):
                x_min, x_max = j * self.cell_size + self.BORDER_SIZE, (j + 1) * self.cell_size - self.BORDER_SIZE
                y_min, y_max = i * self.cell_size + self.BORDER_SIZE, (i + 1) * self.cell_size - self.BORDER_SIZE
                # noinspection PyTypeChecker
                self.cell_grid[i][j] = GridCell(self.surf, 'empty', (x_min, y_min, x_min, x_max))

    def __get_cell_size(self) -> int:
        """
        utility function to calcualte the size of the grid cells
        """
        x_size = (self.bounds[2] - self.bounds[0]) // self.grid_size[1]
        y_size = (self.bounds[3] - self.bounds[1]) // self.grid_size[0]
        return min(x_size, y_size)

    def draw_grid(self, border_colour: Tuple[int] = (0, 0, 0)):
        """
        Draws the grid borders to the area defined by bounding_rect and grid_size
        :param border_colour: Grid colour as (R, G, B)
        """
        # draw large square to define extents of grid
        pygame.draw.rect(self.surf, border_colour, (self.bounds[0], self.bounds[1],
                                                    self.bounds[2] - self.bounds[0], self.bounds[3] - self.bounds[1]),
                         self.BORDER_SIZE)
        # Draw horizontal bars
        x_min, x_max = self.bounds[0], self.bounds[2]
        for i in range(self.grid_size[0]):
            pygame.draw.line(self.surf, border_colour, (x_min, self.bounds[1] + i*self.cell_size),
                             (x_max, self.bounds[1] + i*self.cell_size),
                             self.BORDER_SIZE)
        # Draw vertical bars
        y_min, y_max = self.bounds[1], self.bounds[3]
        for i in range(self.grid_size[1]):
            pygame.draw.line(self.surf, border_colour, (self.bounds[0] + i*self.cell_size, y_min),
                             (self.bounds[0] + i*self.cell_size, y_max),
                             self.BORDER_SIZE)
