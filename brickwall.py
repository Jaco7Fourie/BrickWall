from typing import Tuple

import pygame
from screeninfo import get_monitors

from grid_map import GridMap
from path_solver_astar import PathSolverAStar


class BrickWall:
    """
    Demo app to teach pygame and A*
    """

    # https://coolors.co/a90f33-f78c6b-ffd166-83d483-037758-118ab2-073b4c
    BACKGROUND_COLOUR = (255, 255, 255)  # (246, 240, 237)  # Isabelline
    TEXT_COLOUR = (7, 59, 76)  # Midnight green eagle green
    HIGHLIGHT_COLOUR = (250, 250, 25)
    # text border size
    TEXT_BORDER = 2
    TEXT_SIZE = 16
    TEXT_GUTTER = TEXT_SIZE + 4

    def __init__(self, width: int = 1280, height: int = 800,
                 fps: int = 120, grid_size: Tuple[int, int] = (93, 170), random_walls: float = 0.35):
        """
        Initialize pygame, window, background, font,...
        :param width: the width of the main app window
        :param height: the height of the main app window
        :param fps: the frame rate in frames per second
        :param grid_size: The size of the grid as tuple of (rows, columns)
        :param random_walls: probability of a cell randomly becoming a wall to generate random rooms
        """

        pygame.init()
        pygame.display.set_caption("BrickWall -- Press ESC to quit")
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.screen.set_alpha(None)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill(self.BACKGROUND_COLOUR)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.font = pygame.font.SysFont('mono', self.TEXT_SIZE, bold=True)
        # some lost background is inevitable unless we fix the screen size and grid size
        # I prefer to customise this. Current value based on on w/d = 1.828
        self.grid_size = grid_size
        self.random_walls = random_walls

        self.solver = None
        self.grid_map = None
        self.running = True
        self.paused = False
        self.step = False

        pygame.event.set_allowed(None)
        pygame.event.set_allowed(pygame.QUIT)
        pygame.event.set_allowed(pygame.KEYDOWN)
        pygame.event.set_allowed(pygame.KEYUP)

    def start_new_run(self):
        self.background.fill(self.BACKGROUND_COLOUR)
        self.grid_map = GridMap(self.background,
                           [self.TEXT_BORDER, self.TEXT_GUTTER + self.TEXT_BORDER,
                            self.width - self.TEXT_BORDER, self.height - self.TEXT_GUTTER - self.TEXT_BORDER],
                           self.grid_size)
        self.grid_map.draw_grid()
        s_cell, g_cell = self.grid_map.init_grid(random_walls_ratio=self.random_walls)
        self.grid_map.render_cells()
        self.solver = PathSolverAStar(self.grid_map.cell_grid, s_cell, g_cell,
                                      heuristic='euclidean', movement='manhattan', heuristic_weight=2)
        self.screen.blit(self.background, (0, 0))
        self.running = True
        self.paused = False
        self.step = False

    def run(self):
        """
        The mainloop
        """
        msg = ''
        ui_msg = ''
        bounds = []
        self.start_new_run()
        self.background.convert()
        while self.running:
            self.clock.tick(self.fps)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_r:
                        self.start_new_run()
                    elif event.key == pygame.K_s:
                        self.step = True
                        self.paused = False
            # pygame.event.pump()
            if not self.solver.done and not self.paused:
                msg, bounds = self.solver.next_step()
            if self.step:
                self.paused = True
                self.step = False
                bounds.append(pygame.draw.rect(self.background, self.HIGHLIGHT_COLOUR, bounds[0]))

            if self.paused:
                ui_msg = '|PAUSED|'
            else:
                ui_msg = '|SOLVING|'
            mouse_x, mouse_y = self.grid_map.cell_coords_from_mouse_coords(pygame.mouse.get_pos())
            if self.paused:
                h = self.solver.heuristic(self.grid_map.cell_grid[mouse_y][mouse_x], self.solver.goal_cell)
                ui_msg += f' -- f#:{self.grid_map.cell_grid[mouse_y][mouse_x].f_score:.2f}, ' \
                          f'g#:{self.grid_map.cell_grid[mouse_y][mouse_x].g_score:.2f}, ' \
                          f'h#{h:.2f}'
            bounds.append(self.draw_text(f"Cell: {(mouse_x, mouse_y)} " + ui_msg, 4, self.TEXT_COLOUR))
            bounds.append(self.draw_text(f"FPS: {self.clock.get_fps():>5.2f}", 3, self.TEXT_COLOUR))
            bounds.append(self.draw_text(msg, 1, self.TEXT_COLOUR))
            bounds.append(self.draw_text(f'visited: {self.solver.visited} candidates: {self.solver.openSet.size()}',
                                         2, self.TEXT_COLOUR))
            pygame.display.flip()
            #pygame.display.update(bounds)
            for r in bounds:
                self.screen.blit(self.background, r, r)

        pygame.quit()

    def draw_text(self, text, pos_index=0, col=(230, 230, 230)) -> pygame.Rect:
        """
        Draws text to the screen in the position index indicatred by pos_index
        pos_index can be numbers 1-4 which represent the 4 corners of the screen starting in the top-left and moving
        clockwise
        :param text: str representing the text to be printed
        :param pos_index: index 0-4 representing the index to print
        :param col: colour of the text as a rgb tuple
        :return: rectangle that defines the bounds of the font
        """
        if not 1 <= pos_index <= 4:
            print(f'ERROR: invalid corner position: {pos_index}')
            return pygame.Rect(0, 0, 0, 0)

        fw, fh = self.font.size(text)  # fw: font width,  fh: font height
        surface = self.font.render(text, True, col, self.BACKGROUND_COLOUR)
        if pos_index == 1:
            pos = (self.TEXT_BORDER, self.TEXT_BORDER)
        elif pos_index == 2:
            pos = ((self.width - fw - self.TEXT_BORDER), self.TEXT_BORDER)
        elif pos_index == 3:
            pos = ((self.width - fw - self.TEXT_BORDER), (self.height - fh - self.TEXT_BORDER))
        else:
            pos = (self.TEXT_BORDER, (self.height - fh - self.TEXT_BORDER))
        bounds = pygame.Rect(pos[0], pos[1], fw, fh)
        self.background.blit(surface, pos)
        return bounds


if __name__ == '__main__':
    # get screen resolution
    m = get_monitors()[0]
    # call with width of window and fps
    BrickWall(width=int(m.width - m.width*0.1), height=int(m.height - m.height*0.1)).run()
