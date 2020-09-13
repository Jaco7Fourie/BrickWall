import pygame
from screeninfo import get_monitors

from grid_map import GridMap
from path_solver_astar import PathSolverAStar


class BrickWall:
    """
    Demo app to teach pygame and A*
    """

    # https://coolors.co/a90f33-f78c6b-ffd166-83d483-037758-118ab2-073b4c
    BACKGROUND_COLOUR = (246, 240, 237)  # Isabelline
    TEXT_COLOUR = (7, 59, 76)  # Midnight green eagle green
    # text border size
    TEXT_BORDER = 2
    TEXT_SIZE = 16
    TEXT_GUTTER = TEXT_SIZE + 3

    def __init__(self, width: int = 1280, height: int = 800, fps: int = 120):
        """
        Initialize pygame, window, background, font,...
        :param width: the width of the main app window
        :param height: the height of the main app window
        :param fps: the frame rate in frames per second
        """

        pygame.init()
        pygame.display.set_caption("BrickWall -- Press ESC to quit")
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill(self.BACKGROUND_COLOUR)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.font = pygame.font.SysFont('mono', self.TEXT_SIZE, bold=True)
        # some lost background is inevitable unless we fix the screen size and grid size
        # I prefer to customise this. Current value based on on w/d = 1.828
        self.grid_size = (93, 170)
        self.random_walls = 0.25

        self.solver = None
        self.grid_map = None
        self.running = True
        self.paused = False

    def start_new_run(self):
        self.background.fill(self.BACKGROUND_COLOUR)
        self.grid_map = GridMap(self.background,
                           [self.TEXT_BORDER, self.TEXT_GUTTER,
                            self.width - self.TEXT_BORDER, self.height - self.TEXT_GUTTER],
                           self.grid_size)
        self.grid_map.draw_grid()
        s_cell, g_cell = self.grid_map.init_grid(random_walls_ratio=self.random_walls)
        self.grid_map.render_cells()
        self.solver = PathSolverAStar(self.grid_map.cell_grid, s_cell, g_cell, heuristic='euclidean', movement='manhattan')
        self.running = True
        self.paused = False

    def run(self):
        """
        The mainloop
        """
        msg = ''
        self.start_new_run()
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

            if not self.solver.done and not self.paused:
                msg = self.solver.next_step()

            mouse_x, mouse_y = self.grid_map.cell_coords_from_mouse_coords(pygame.mouse.get_pos())
            self.draw_text(f"Cell: {(mouse_x, mouse_y)}", 4, self.TEXT_COLOUR)
            self.draw_text(f"FPS: {self.clock.get_fps():>5.2f}", 3, self.TEXT_COLOUR)
            self.draw_text(msg, 1, self.TEXT_COLOUR)
            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))

        pygame.quit()

    def draw_text(self, text, pos_index=0, col=(230, 230, 230)):
        """
        Draws text to the screen in the position index indicatred by pos_index
        pos_index can be numbers 1-4 which represent the 4 corners of the screen starting in the top-left and moving
        clockwise
        :param text: str representing the text to be printed
        :param pos_index: index 0-4 representing the index to print
        :param col: colour of the text as a rgb tuple
        :return: None
        """
        if not 1 <= pos_index <= 4:
            print(f'ERROR: invalid corner position: {pos_index}')
            return

        fw, fh = self.font.size(text)  # fw: font width,  fh: font height
        surface = self.font.render(text, True, col)
        if pos_index == 1:
            pos = (self.TEXT_BORDER, self.TEXT_BORDER)
        elif pos_index == 2:
            pos = ((self.width - fw - self.TEXT_BORDER), self.TEXT_BORDER)
        elif pos_index == 3:
            pos = ((self.width - fw - self.TEXT_BORDER), (self.height - fh - self.TEXT_BORDER))
        else:
            pos = (self.TEXT_BORDER, (self.height - fh - self.TEXT_BORDER))
        self.screen.blit(surface, pos)


if __name__ == '__main__':
    # get screen resolution
    m = get_monitors()[0]
    # call with width of window and fps
    BrickWall(width=int(m.width - m.width*0.1), height=int(m.height - m.height*0.1)).run()
