from typing import Tuple
import pygame
from enum import Flag, auto

class GridCell:
    # https://coolors.co/a90f33-f78c6b-ffd166-83d483-037758-118ab2-073b4c
    BACKGROUND_COLOUR = (246, 240, 237)  # Isabelline
    PATH_COLOUR = (17, 138, 178)  # Blue NSC
    WALL_COLOUR = (80, 49, 42)  # Dark Liver Horses
    VISITED_COLOUR = (247, 140, 107)  # Middle Red
    OPEN_SET_COLOUR = (131, 212, 131)  # Mantis
    START_COLOUR = (3, 119, 88)  # Tropical rain forest
    GOAL_COLOUR = (169, 15, 51)  # Cromson UA

    def __init__(self, surface: pygame.Surface, cell_type: str,
                 bounding_rect: Tuple[int, int, int, int], coord: Tuple[int, int]):
        """
        Initialises a new cell in the grid
        :param surface: The surface that this cell will draw to
        :param cell_type: string to represent the type of the cell,
            one of {empty, path, visited, open_set, wall, start, goal}
        :param bounding_rect: draw the grid only within these bounds
        (top_left_x, top_left_y, bottom_right_x, bottom_right_y)
        :param coord: The coordinate of this cell in the grid (row, column)
        """
        self.draw_bounds = (bounding_rect[0], bounding_rect[1], bounding_rect[2] - bounding_rect[0] + 1,
                            bounding_rect[3] - bounding_rect[1] + 1)
        self.surf = surface
        self.cell_type = cell_type
        self.coord = coord

        inner_border = 2  # ((self.bounds[2] - self.bounds[0])*0.9) // 2
        self.inner_bound = (self.draw_bounds[0] + inner_border, self.draw_bounds[1] + inner_border,
                            self.draw_bounds[2] - inner_border * 2, self.draw_bounds[3] - inner_border * 2)

        self.f_score = float('inf')
        self.g_score = float('inf')
        # currently all cells have a cost of 1 but we leave this here as placeholder for future advanced terrain cells
        self.cost = 1
        self.comes_from = None

    def reset_scores(self):
        """
        resets the scores of this cell without changing the cell coordinates or drawing bounds
        :return:
        """
        self.f_score = float('inf')
        self.g_score = float('inf')
        # currently all cells have a cost of 1 but we leave this here as placeholder for future advanced terrain cells
        self.cost = 1
        self.comes_from = None
        self.cell_type = 'empty'

    def __lt__(self, other):
        return self.f_score < other.f_score

    def __gt__(self, other):
        return self.f_score > other.f_score

    def __le__(self, other):
        return self.f_score <= other.f_score

    def __ge__(self, other):
        return self.f_score >= other.f_score

    def __ne__(self, other):
        return not self.f_score == other.f_score

    def __eq__(self, other):
        return self.coord == other.coord

    def __hash__(self):
        return hash(self.coord)

    def draw_cell(self) -> pygame.Rect:
        """
        Draws the cell based on the cell type and return the bounds of the drawing
        :return: rectangle that defines the bounds of the drawing
        """
        if self.cell_type == 'path':
            return pygame.draw.rect(self.surf, GridCell.PATH_COLOUR, self.draw_bounds)
        elif self.cell_type == 'visited':
            return pygame.draw.rect(self.surf, GridCell.VISITED_COLOUR, self.inner_bound)
        elif self.cell_type == 'open_set':
            return pygame.draw.rect(self.surf, GridCell.OPEN_SET_COLOUR, self.inner_bound)
        elif self.cell_type == 'wall':
            return pygame.draw.rect(self.surf, GridCell.WALL_COLOUR, self.draw_bounds)
        elif self.cell_type == 'start':
            return pygame.draw.rect(self.surf, GridCell.START_COLOUR, self.draw_bounds)
        elif self.cell_type == 'goal':
            return pygame.draw.rect(self.surf, GridCell.GOAL_COLOUR, self.draw_bounds)
        elif self.cell_type == 'empty':
            return pygame.draw.rect(self.surf, GridCell.BACKGROUND_COLOUR, self.draw_bounds)
        else:
            print(f'Invalid Cell type: {self.cell_type}')
            return pygame.Rect(0, 0, 0, 0)


class Walls(Flag):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()


class WalledCell(GridCell):
    """
    Expands on GridCell class to include cells that have explicit walls for generating mazes
    """
    # don't use an even number here
    WALL_THICKNESS = 1
    WALL_COLOUR = (0, 0, 0)

    def __init__(self, surface: pygame.Surface, cell_type: str,
                 bounding_rect: Tuple[int, int, int, int], coord: Tuple[int, int]):
        super().__init__(surface, cell_type, bounding_rect, coord)
        self.walls = Walls.NORTH | Walls.SOUTH | Walls.EAST | Walls.WEST
        self.bounding_rect = bounding_rect

    def tunnel_to(self, cell: 'WalledCell'):
        """
        removes walls from this cell and its appropriate neighbour to reflect a passage between the cells
        :param cell: the cell to form a passage to (must be a WalledCell)
        :return: None
        """
        if self.coord[0] < cell.coord[0]:
            # tunnel to the SOUTH
            self.walls &= ~Walls.SOUTH
            cell.walls &= ~Walls.NORTH
        elif self.coord[0] > cell.coord[0]:
            # tunnel to the NORTH
            self.walls &= ~Walls.NORTH
            cell.walls &= ~Walls.SOUTH
        elif self.coord[1] > cell.coord[1]:
            # tunnel to the WEST
            self.walls &= ~Walls.WEST
            cell.walls &= ~Walls.EAST
        else:
            # tunnel to the EAST
            self.walls &= ~Walls.EAST
            cell.walls &= ~Walls.WEST

    def draw_cell(self) -> pygame.Rect:
        """
        Draws the cell based on the cell type and return the bounds of the drawing
        :return: rectangle that defines the bounds of the drawing
        """
        pygame.draw.rect(self.surf, GridCell.BACKGROUND_COLOUR, self.draw_bounds)
        if self.cell_type == 'path':
            rect = pygame.draw.rect(self.surf, GridCell.PATH_COLOUR, self.draw_bounds)
        elif self.cell_type == 'visited':
            rect = pygame.draw.rect(self.surf, GridCell.VISITED_COLOUR, self.inner_bound)
        elif self.cell_type == 'open_set':
            rect = pygame.draw.rect(self.surf, GridCell.OPEN_SET_COLOUR, self.inner_bound)
        elif self.cell_type == 'start':
            rect = pygame.draw.rect(self.surf, GridCell.START_COLOUR, self.draw_bounds)
        elif self.cell_type == 'goal':
            rect = pygame.draw.rect(self.surf, GridCell.GOAL_COLOUR, self.draw_bounds)
        elif self.cell_type == 'empty':
            rect = pygame.draw.rect(self.surf, GridCell.BACKGROUND_COLOUR, self.draw_bounds)
        else:
            print(f'Invalid Cell type: {self.cell_type}')
            return pygame.Rect(0, 0, 0, 0)

        # draw the walls
        # start with a background of no walls

        if Walls.NORTH in self.walls:
            pygame.draw.line(self.surf, self.WALL_COLOUR, self.bounding_rect[0:2], self.bounding_rect[-2:0:-1],
                             self.WALL_THICKNESS)
            rect = self.draw_bounds
        if Walls.SOUTH in self.walls:
            pygame.draw.line(self.surf, self.WALL_COLOUR, self.bounding_rect[0:4:3], self.bounding_rect[-2:4],
                             self.WALL_THICKNESS)
            rect = self.draw_bounds
        if Walls.WEST in self.walls:
            pygame.draw.line(self.surf, self.WALL_COLOUR, self.bounding_rect[0:2], self.bounding_rect[0:4:3],
                             self.WALL_THICKNESS)
            rect = self.draw_bounds
        if Walls.EAST in self.walls:
            pygame.draw.line(self.surf, self.WALL_COLOUR, self.bounding_rect[-2:0:-1], self.bounding_rect[-2:4],
                             self.WALL_THICKNESS)
            rect = self.draw_bounds
        return rect

