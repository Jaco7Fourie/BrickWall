from typing import Tuple
import pygame


class GridCell:
    # https://coolors.co/28536b-c2948a-7ea8be-f6f0ed-bbb193-8f2d56-c5d86d-dfefca-fff9a5-23ce6b
    BACKGROUND_COLOUR = (246, 240, 237)  # Isabelline
    PATH_COLOUR = (197, 216, 109) # June bud
    WALL_COLOUR = (194, 148, 138) # Rosy Brown
    VISITED_COLOUR = (126, 168, 190) # Pewter Blue
    START_COLOUR = (35, 206, 107)  # Emerald
    GOAL_COLOUR = (143, 45, 86) # Quinacridone Magenta

    def __init__(self, surface: pygame.Surface, cell_type: str,
                 bounding_rect: Tuple[int, int, int, int], coord: Tuple[int, int]):
        """
        Initialises a new cell in the grid
        :param surface: The surface that this cell will draw to
        :param cell_type: string to represent the type of the cell, one of {empty, path, visited, wall, start, goal}
        :param bounding_rect: draw the grid only within these bounds
        :param coord: The coordinate of this cell in the grid (row, column)
        (top_left_x, top_left_y, bottom_right_x, bottom_right_y)
        """
        self.draw_bounds = (bounding_rect[0], bounding_rect[1], bounding_rect[2] - bounding_rect[0]+1,
                            bounding_rect[3] - bounding_rect[1]+1)
        self.surf = surface
        self.cell_type = cell_type
        self.coord = coord

        inner_border = 2  # ((self.bounds[2] - self.bounds[0])*0.9) // 2
        self.inner_bound = (self.draw_bounds[0] + inner_border, self.draw_bounds[1] + inner_border,
                            self.draw_bounds[2] - inner_border*2, self.draw_bounds[3] - inner_border*2)

        self.f_score = float('inf')
        self.g_score = float('inf')
        # currently all cells have a cost of 1 but we leave this here as placeholder for future advanced terrain cells
        self.cost = 1
        self.comes_from = None

    def __lt__(self, other):
        return self.f_score < other.f_score

    def __gt__(self, other):
        return self.f_score > other.f_score

    def __le__(self, other):
        return self.f_score <= other.f_score

    def __ge__(self, other):
        return self.f_score >= other.f_score

    def __eq__(self, other):
        return self.f_score == other.f_score

    def __ne__(self, other):
        return not self.f_score == other.f_score

    def draw_cell(self):
        if self.cell_type == 'path':
            pygame.draw.rect(self.surf, GridCell.PATH_COLOUR, self.inner_bound)
        elif self.cell_type == 'visited':
            pygame.draw.rect(self.surf, GridCell.VISITED_COLOUR, self.inner_bound)
        elif self.cell_type == 'wall':
            pygame.draw.rect(self.surf, GridCell.WALL_COLOUR, self.draw_bounds)
        elif self.cell_type == 'start':
            pygame.draw.rect(self.surf, GridCell.START_COLOUR, self.draw_bounds)
        elif self.cell_type == 'goal':
            pygame.draw.rect(self.surf, GridCell.GOAL_COLOUR, self.draw_bounds)
        elif self.cell_type == 'empty':
            pass  # pygame.draw.rect(self.surf, GridCell.BACKGROUND_COLOUR, self.bounds)
        else:
            print(f'Invalid Cell type: {self.cell_type}')
            return None

