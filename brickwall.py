import pygame
from screeninfo import get_monitors

from grid_map import GridMap


class BrickWall:
    """
    Demo app to teach pygame and A*
    """

    # https://coolors.co/28536b-c2948a-7ea8be-f6f0ed-bbb193-8f2d56-c5d86d-dfefca-fff9a5-23ce6b
    BACKGROUND_COLOUR = (246, 240, 237) # Isabelline
    TEXT_COLOUR = (40, 83, 107) # Blue Sapphire
    # text border size
    TEXT_BORDER = 2
    TEXT_SIZE = 16
    TEXT_GUTTER = TEXT_SIZE + 3

    def __init__(self, width: int = 1280, height: int = 800, fps: int = 60):
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

    def run(self):
        """
        The mainloop
        """
        grid_map = GridMap(self.background,
                           [self.TEXT_BORDER, self.TEXT_GUTTER,
                            self.width - self.TEXT_BORDER, self.height - self.TEXT_GUTTER],
                           # some lost background is inevitable unless we fix the screen size and grid size
                           # I prefer to customise this. Current value based on on w/d = 1.828
                           (93, 170))
        grid_map.draw_grid()
        grid_map.test_grid()
        grid_map.render_cells()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            self.clock.tick(self.fps)
            self.draw_text(f"FPS: {self.clock.get_fps():6.3}", 3, self.TEXT_COLOUR)
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
