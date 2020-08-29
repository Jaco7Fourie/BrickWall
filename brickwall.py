import pygame


class BrickWall:
    """
    Demo app to teach pygame and A*
    """

    # https://coolors.co/0081a7-00afb9-fdfcdc-fed9b7-f07167
    BACKGROUND_COLOUR = (253, 252, 220)
    TEXT_COLOUR = (0, 129, 167)

    def __init__(self, width=1280, height=800, fps=60):
        """
        Initialize pygame, window, background, font,...
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
        self.playtime = 0.0
        self.font = pygame.font.SysFont('mono', 20, bold=True)

    def run(self):
        """The mainloop
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            milliseconds = self.clock.tick(self.fps)
            self.playtime += milliseconds / 1000.0
            self.draw_text(f"FPS: {self.clock.get_fps():6.3}{' ' * 5}PLAYTIME: {self.playtime:6.3} SECONDS",
                           0, self.TEXT_COLOUR)

            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))

        pygame.quit()

    def draw_text(self, text, pos_index=0, col=(230, 230, 230)):
        """
        Draws text to the screen in the position index indicatred by pos_index
        pos_index can be numbers 1-4 which represnt the 4 corners of the screen starting in the top-left and moving
        clockwise
        :param text: str representing the text to be printed
        :param pos_index: index 0-4 representing the index to print
        :param col: colour of the text as a rgb tuple
        :return: None
        """
        if not 0 <= pos_index <= 4:
            print(f'ERROR: invalid corner position: {pos_index}')
            return

        fw, fh = self.font.size(text)  # fw: font width,  fh: font height
        surface = self.font.render(text, True, col)
        # // makes integer division in python3
        pos  = ((self.width - fw) // 2, (self.height - fh) // 2)
        if pos_index == 0:
            pos = (2, 2)
        self.screen.blit(surface, pos)


if __name__ == '__main__':
    # call with width of window and fps
    BrickWall().run()
