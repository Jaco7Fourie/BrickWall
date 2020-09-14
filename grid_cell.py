from typing import Tuple
import pygame


class GridCell:
    # https://coolors.co/a90f33-f78c6b-ffd166-83d483-037758-118ab2-073b4c
    BACKGROUND_COLOUR = (246, 240, 237)  # Isabelline
    PATH_COLOUR = (17, 138, 178) # Blue NSC
    WALL_COLOUR = (80, 49, 42) # Dark Liver Horses
    VISITED_COLOUR = (247, 140, 107) # Middle Red
    OPEN_SET_COLOUR = (131, 212, 131)  # Mantis
    START_COLOUR = (3, 119, 88)  # Tropical rain forest
    GOAL_COLOUR = (169, 15, 51) # Cromson UA

    def __init__(self, surface: pygame.Surface, cell_type: str,
                 bounding_rect: Tuple[int, int, int, int], coord: Tuple[int, int]):
        """
        Initialises a new cell in the grid
        :param surface: The surface that this cell will draw to
        :param cell_type: string to represent the type of the cell,
            one of {empty, path, visited, open_set, wall, start, goal}
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
            pass  # pygame.draw.rect(self.surf, GridCell.BACKGROUND_COLOUR, self.bounds)
        else:
            print(f'Invalid Cell type: {self.cell_type}')
            return pygame.Rect(0, 0, 0, 0)

