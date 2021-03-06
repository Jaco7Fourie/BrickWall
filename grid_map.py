from typing import Tuple, List, Any
from random import random
from grid_cell import GridCell, WalledCell
import pygame


class GridMap:
    """
    Defines the map of cells and keeps track of cell states
    """
    # the size in pixels of borders between cells
    BORDER_SIZE = 1

    def __init__(self, surface: pygame.Surface, bounding_rect: List[int],
                 grid_size: List[int], maze_grid: bool = False):
        """
        Initialises the grid as a list of GridCell objects
        :param surface: the background surface to draw on
        :param bounding_rect: draw the grid only within these bounds
        (top_left_x, top_left_y, bottom_right_x, bottom_right_y)
        :param grid_size: number of cells as (rows, columns)
        :param maze_grid: if true then this grid consists of WalledCell objects with walls as part of the cell
        """
        self.surf = surface
        self.bounds = bounding_rect
        self.grid_size = grid_size
        self.maze_grid = maze_grid

        self.cell_size = self.__get_cell_size()
        # update the bounds based on square sells
        self.bounds[2] = self.bounds[0] + self.cell_size * self.grid_size[1]
        self.bounds[3] = self.bounds[1] + self.cell_size * self.grid_size[0]
        self.cell_grid = []
        for i in range(grid_size[0]):
            row_list = []
            for j in range(grid_size[1]):

                if self.maze_grid:
                    x_min = j * self.cell_size
                    x_max = (j + 1) * self.cell_size
                    y_min = i * self.cell_size
                    y_max = (i + 1) * self.cell_size
                    row_list.append(WalledCell(self.surf, 'empty', (self.bounds[0] + x_min, self.bounds[1] + y_min,
                                                                    self.bounds[0] + x_max, self.bounds[1] + y_max),
                                               (i, j)))
                else:
                    x_min = j * self.cell_size + self.BORDER_SIZE
                    x_max = (j + 1) * self.cell_size - self.BORDER_SIZE
                    y_min = i * self.cell_size + self.BORDER_SIZE
                    y_max = (i + 1) * self.cell_size - self.BORDER_SIZE
                    row_list.append(GridCell(self.surf, 'empty', (self.bounds[0] + x_min, self.bounds[1] + y_min,
                                                                  self.bounds[0] + x_max, self.bounds[1] + y_max),
                                             (i, j)))
            self.cell_grid.append(row_list)

    def __get_cell_size(self) -> int:
        """
        utility function to calculate the size of the grid cells
        """
        x_size = (self.bounds[2] - self.bounds[0]) // self.grid_size[1]
        y_size = (self.bounds[3] - self.bounds[1]) // self.grid_size[0]
        return min(x_size, y_size)

    def cell_coords_from_mouse_coords(self, mouse_coords: Tuple[int, int]) -> Tuple[int, int]:
        """
        converts mouse coordinates to cell grid coordinates.
        :param mouse_coords: tuple of mouse x and y coordinate
        :return: tuple of grid coordinate
        """
        if mouse_coords[0] < self.bounds[0] or mouse_coords[0] > self.bounds[2] or \
                mouse_coords[1] < self.bounds[1] or mouse_coords[1] > self.bounds[3]:
            return -1, -1
        norm_coord = max(mouse_coords[0] - self.bounds[0], 0), max(mouse_coords[1] - self.bounds[1], 0)
        return min(norm_coord[0] // self.cell_size, self.grid_size[1] - 1), \
               min(norm_coord[1] // self.cell_size, self.grid_size[0] - 1)

    def draw_grid(self, border_colour: Tuple[int, int, int] = (0, 0, 0)):
        """
        Draws the grid borders to the area defined by bounding_rect and grid_size
        :param border_colour: Grid colour as (R, G, B)

        """
        if self.maze_grid:
            # the grid is drawn when the cells are rendered
            pass
        else:
            # draw large square to define extents of grid
            pygame.draw.rect(self.surf, border_colour, (self.bounds[0], self.bounds[1],
                                                        self.bounds[2] - self.bounds[0] + 1,
                                                        self.bounds[3] - self.bounds[1] + 1),
                             self.BORDER_SIZE)
            # Draw horizontal bars
            x_min, x_max = self.bounds[0], self.bounds[2]
            for i in range(self.grid_size[0]):
                pygame.draw.line(self.surf, border_colour, (x_min, self.bounds[1] + i * self.cell_size),
                                 (x_max, self.bounds[1] + i * self.cell_size),
                                 self.BORDER_SIZE)
            # Draw vertical bars
            y_min, y_max = self.bounds[1], self.bounds[3]
            for i in range(self.grid_size[1]):
                pygame.draw.line(self.surf, border_colour, (self.bounds[0] + i * self.cell_size, y_min),
                                 (self.bounds[0] + i * self.cell_size, y_max),
                                 self.BORDER_SIZE)

    def render_cells(self):
        """
        Renders the list of grid cells based on their type to the background surface
        :return:
        """
        self.surf.lock()
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                self.cell_grid[i][j].draw_cell()
        self.surf.unlock()

    # noinspection PyUnresolvedReferences
    def test_grid(self):
        """
        fills in some of the cells with test types to test the rendering
        The grid size needs to be at least 15x15
        :return: None
        """
        # for i in range(self.grid_size[0]):
        #     for j in range(self.grid_size[1]):
        #         print(f'{i},{j} -- {self.cell_grid[i][j].bounds}')
        self.cell_grid[5][5].cell_type = 'start'
        self.cell_grid[15][15].cell_type = 'goal'

        # the path
        self.cell_grid[5][6].cell_type = 'path'
        self.cell_grid[5][7].cell_type = 'path'
        self.cell_grid[6][7].cell_type = 'path'
        self.cell_grid[7][8].cell_type = 'path'
        self.cell_grid[8][9].cell_type = 'path'
        self.cell_grid[9][9].cell_type = 'path'
        self.cell_grid[10][9].cell_type = 'path'
        self.cell_grid[10][10].cell_type = 'path'
        self.cell_grid[10][11].cell_type = 'path'
        self.cell_grid[10][12].cell_type = 'path'
        self.cell_grid[11][12].cell_type = 'path'
        self.cell_grid[12][13].cell_type = 'path'
        self.cell_grid[13][14].cell_type = 'path'
        self.cell_grid[14][14].cell_type = 'path'
        self.cell_grid[15][14].cell_type = 'path'

        # visited
        self.cell_grid[6][6].cell_type = 'visited'
        self.cell_grid[7][6].cell_type = 'visited'
        self.cell_grid[8][6].cell_type = 'visited'
        self.cell_grid[7][7].cell_type = 'visited'
        self.cell_grid[8][7].cell_type = 'visited'
        self.cell_grid[8][8].cell_type = 'visited'
        self.cell_grid[11][11].cell_type = 'visited'
        self.cell_grid[12][11].cell_type = 'visited'
        self.cell_grid[12][12].cell_type = 'visited'
        self.cell_grid[13][12].cell_type = 'visited'
        self.cell_grid[13][13].cell_type = 'visited'
        self.cell_grid[14][13].cell_type = 'visited'
        self.cell_grid[15][13].cell_type = 'visited'
        self.cell_grid[10][13].cell_type = 'visited'
        self.cell_grid[11][13].cell_type = 'visited'
        self.cell_grid[12][14].cell_type = 'visited'
        self.cell_grid[14][15].cell_type = 'visited'

        # walls
        self.cell_grid[9][8].cell_type = 'wall'
        self.cell_grid[10][8].cell_type = 'wall'
        self.cell_grid[11][8].cell_type = 'wall'
        self.cell_grid[12][8].cell_type = 'wall'
        self.cell_grid[13][8].cell_type = 'wall'
        self.cell_grid[14][8].cell_type = 'wall'
        self.cell_grid[9][10].cell_type = 'wall'
        self.cell_grid[9][11].cell_type = 'wall'
        self.cell_grid[9][12].cell_type = 'wall'
        self.cell_grid[9][13].cell_type = 'wall'
        self.cell_grid[9][14].cell_type = 'wall'
        self.cell_grid[9][15].cell_type = 'wall'
        self.cell_grid[12][9].cell_type = 'wall'
        self.cell_grid[12][10].cell_type = 'wall'
        self.cell_grid[13][10].cell_type = 'wall'
        self.cell_grid[14][10].cell_type = 'wall'
        self.cell_grid[15][10].cell_type = 'wall'

    def init_grid(self, start_coords: Tuple[int, int] = (1, 1),
                  goal_coords: Tuple[int, int] = (-2, -2),
                  random_walls_ratio: float = 0.0) -> Tuple[GridCell, GridCell]:
        """
        Initialises the grid with a start point and end point.
        :param start_coords:The row and column coordinates for the starting point
        :param goal_coords:The row and column coordinates for the goal point. Negative indices counts
            backwards from the end of the grid
        :param random_walls_ratio: Value between 0 and 1 to control how much of the
            grid should be randomly turned to walls
        :return: Tuple of (start_cell, goal_cell)
        """
        if random_walls_ratio > 0 and not self.maze_grid:
            for i in range(self.grid_size[0]):
                for j in range(self.grid_size[1]):
                    if random() < random_walls_ratio:
                        self.cell_grid[i][j].cell_type = 'wall'

        self.cell_grid[start_coords[0]][start_coords[1]].cell_type = 'start'
        self.cell_grid[goal_coords[0]][goal_coords[1]].cell_type = 'goal'
        return self.cell_grid[start_coords[0]][start_coords[1]], self.cell_grid[goal_coords[0]][goal_coords[1]]

    def reset_grid(self) -> List[Any]:
        """
        Cleans all non-wall, non-goal, and non-start cells and redraws the grid
        :return: list of rectangles to indicate which parts of the background needs redrawing
        """
        updates = []
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                if self.cell_grid[i][j].cell_type == 'path' or self.cell_grid[i][j].cell_type == 'visited' or \
                        self.cell_grid[i][j].cell_type == 'open_set':
                    self.cell_grid[i][j].reset_scores()
                    updates.append(self.cell_grid[i][j].draw_cell())

        return updates

    def post_maze_cleanup(self, start_coords: Tuple[int, int] = (1, 1),
                          goal_coords: Tuple[int, int] = (-2, -2)) -> List[Any]:
        """
        Cleans up the generation graphics to prepare the maze for solving
        :param start_coords:The row and column coordinates for the starting point
        :param goal_coords:The row and column coordinates for the goal point. Negative indices counts
            backwards from the end of the grid
        :return: list of rectangles to indicate which parts of the background needs redrawing
        """
        updates = []
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                self.cell_grid[i][j].comes_from = None
                if (i, j) == start_coords:
                    self.cell_grid[i][j].cell_type = 'start'
                elif (i, j) == goal_coords:
                    self.cell_grid[i][j].cell_type = 'goal'
                else:
                    self.cell_grid[i][j].cell_type = 'empty'
                updates.append(self.cell_grid[i][j].draw_cell())
        return updates
