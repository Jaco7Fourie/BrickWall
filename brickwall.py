from typing import Tuple, List, Any

import pygame
import pygame_gui
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
    # background size
    BACKGROUND_SIZE = (720, 1440)
    # background size
    UI_SIZE = (760, 200)
    # text border size
    TEXT_BORDER = 2
    # Font size
    TEXT_SIZE = 16
    # Text area in UI
    TEXT_GUTTER = TEXT_SIZE + 4
    # the max length of status messages
    T_SIZE = 60

    def __init__(self, width: int = 1640, height: int = 764,
                 fps: int = 120, rows: int = 60, random_walls: float = 0.35):
        """
        Initialize pygame, window, background, font,...
        :param width: the width of the main app window
        :param height: the height of the main app window
        :param fps: the frame rate in frames per second
        :param rows: The number of rows in the grid (columns get calculated based on this)
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
        self.manager = pygame_gui.UIManager((self.width, self.height))
        self.fps = fps

        self.font = pygame.font.SysFont('mono', self.TEXT_SIZE, bold=True)
        # text = '???'
        # text = f'{text:<{self.T_SIZE}}'
        # fw, fh = self.font.size(text)  # fw: font width,  fh: font height
        # self.button_width = fw

        # check rows
        if self.BACKGROUND_SIZE[0] % rows != 0:
            print(f'The number of rows must divide evenly into 720. Factors: 2 x 2 x 2 x 2 x 3 x 3 x 5')
            rows = 120
        self.grid_size = [rows, rows * 2]
        self.random_walls = random_walls

        self.solver = None
        self.heuristic = 'euclidean'
        self.grid_map = None
        self.s_cell = None
        self.g_cell = None
        self.running = True
        self.paused = False
        self.step = False
        # if true left-click draws walls and right_click erases them.
        # If false left-click moves start point and right click moves goal
        self.draw_mode_walls = True

        # GUI elements
        self.toggle_draw_button = None
        self.heuristic_menu = None
        self.reset_button = None
        self.reset_search_button = None
        self.grid_rows_label = None
        self.grid_rows_label_text_box = None
        self.add_gui()
        # events
        pygame.event.set_allowed(None)
        pygame.event.set_allowed(pygame.QUIT)
        pygame.event.set_allowed(pygame.KEYDOWN)
        pygame.event.set_allowed(pygame.KEYUP)
        pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
        pygame.event.set_allowed(pygame.USEREVENT)

    def add_gui(self):
        gui_borders = (
            self.TEXT_BORDER + self.BACKGROUND_SIZE[1] + 2, self.TEXT_BORDER, self.width - 1, self.height - 1)
        pos = gui_borders[0:2]
        size = (196, self.TEXT_GUTTER - self.TEXT_BORDER)
        self.toggle_draw_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(pos, size),
                                                               text='Draw mode (walls)',
                                                               manager=self.manager)
        pos = (pos[0], pos[1] + 20)
        size = (196, self.TEXT_GUTTER - self.TEXT_BORDER)
        self.heuristic_menu = pygame_gui.elements.UIDropDownMenu(['euclidean', 'manhattan'],
                                                                 relative_rect=pygame.Rect(pos, size),
                                                                 starting_option='euclidean',
                                                                 manager=self.manager)
        pos = (pos[0], pos[1] + 20)
        size = (196, self.TEXT_GUTTER - self.TEXT_BORDER)
        self.reset_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(pos, size),
                                                         text='Reset maze',
                                                         manager=self.manager)
        pos = (pos[0], pos[1] + 20)
        size = (196, self.TEXT_GUTTER - self.TEXT_BORDER)
        self.reset_search_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(pos, size),
                                                                text='Reset search',
                                                                manager=self.manager)
        pos = (pos[0] + 20, pos[1] + 20)
        size = (150, self.TEXT_GUTTER - self.TEXT_BORDER)
        self.grid_rows_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(pos, size),
                                                           text='Grid rows',
                                                           manager=self.manager)
        pos = (pos[0] - 20, pos[1] + 20)
        size = (196, self.TEXT_GUTTER - self.TEXT_BORDER)
        self.grid_rows_label_text_box = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(pos, size),
                                                                   manager=self.manager)
        self.grid_rows_label_text_box.set_text(str(self.grid_size[0]))

    def reset_run(self) -> List[Any]:
        """
        Starts a new run using the same grid
        :return: list of rectangles to indicate which parts of the background needs redrawing
        """
        updates = self.grid_map.reset_grid()
        self.solver = PathSolverAStar(self.grid_map.cell_grid, self.s_cell, self.g_cell,
                                      heuristic=self.heuristic, movement='manhattan', heuristic_weight=2)
        self.running = True
        self.paused = False
        self.step = False
        return updates

    def start_new_run(self):
        """
        Starts a new run on a new random grid
        :return:
        """
        self.background.fill(self.BACKGROUND_COLOUR)
        self.grid_map = GridMap(self.background,
                                [self.TEXT_BORDER,
                                 self.TEXT_GUTTER + self.TEXT_BORDER,
                                 self.TEXT_BORDER + self.BACKGROUND_SIZE[1],
                                 self.TEXT_GUTTER + self.TEXT_BORDER + self.BACKGROUND_SIZE[0]],
                                self.grid_size)
        self.grid_map.draw_grid()
        self.s_cell, self.g_cell = self.grid_map.init_grid(random_walls_ratio=self.random_walls)
        self.grid_map.render_cells()
        self.solver = PathSolverAStar(self.grid_map.cell_grid, self.s_cell, self.g_cell,
                                      heuristic=self.heuristic, movement='manhattan', heuristic_weight=2)
        self.screen.blit(self.background, (0, 0))
        self.running = True
        self.paused = False
        self.step = False

    def run(self):
        """
        The mainloop
        """
        msg = ''
        bounds = []
        self.start_new_run()
        self.background.convert()
        while self.running:
            tick = self.clock.tick(self.fps)

            self.process_events(bounds, tick / 1000.0)
            # pygame.event.pump()
            if not self.solver.done and not self.paused:
                msg = self.solver.next_step(bounds)
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

            # pygame.display.update(bounds)
            # add ui area to bounds
            gui_borders = (self.TEXT_BORDER + self.BACKGROUND_SIZE[1], self.TEXT_BORDER,
                           self.UI_SIZE[1], self.UI_SIZE[1])
            bounds.append(gui_borders)
            for r in bounds:
                self.screen.blit(self.background, r, r)
            self.manager.draw_ui(self.screen)
            pygame.display.flip()
            bounds = []

        pygame.quit()

    def process_events(self, bounds: List[Any], time_delta: float):
        """
        Processes the event queue
        :param bounds: list of rectangles to indicate which parts of the background need to be redrawn
        :param time_delta: a time delta value used by the ui manager
        """
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
                elif event.key == pygame.K_d:
                    self.draw_mode_walls = not self.draw_mode_walls
                elif event.key == pygame.K_t:
                    # reset the scores for the goal cell
                    self.g_cell.f_score = float('inf')
                    self.g_cell.g_score = float('inf')
                    bounds.extend(self.reset_run())

            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.toggle_draw_button:
                        self.draw_mode_walls = not self.draw_mode_walls
                        mode = 'walls' if self.draw_mode_walls else 'start/goal'
                        text = f'Draw mode ({mode})'
                        self.toggle_draw_button.set_text(text)
                    elif event.ui_element == self.reset_button:
                        self.start_new_run()
                    elif event.ui_element == self.reset_search_button:
                        # reset the scores for the goal cell
                        self.g_cell.f_score = float('inf')
                        self.g_cell.g_score = float('inf')
                        bounds.extend(self.reset_run())
                elif event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.ui_element == self.heuristic_menu:
                        self.heuristic = self.heuristic_menu.selected_option
                        # reset the scores for the goal cell
                        self.g_cell.f_score = float('inf')
                        self.g_cell.g_score = float('inf')
                        bounds.extend(self.reset_run())
                elif event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    if event.ui_element == self.grid_rows_label_text_box:
                        self.grid_size[0] = int(self.grid_rows_label_text_box.get_text())
                        self.grid_size[1] = self.grid_size[0] * 2
                        self.start_new_run()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT and not self.draw_mode_walls:
                    mouse_x, mouse_y = self.grid_map.cell_coords_from_mouse_coords(pygame.mouse.get_pos())
                    if mouse_x == -1 or mouse_y == -1:
                        self.manager.process_events(event)
                        continue
                    # also reset the scores for the goal cell
                    self.g_cell.f_score = float('inf')
                    self.g_cell.g_score = float('inf')
                    self.s_cell.cell_type = 'empty'
                    self.s_cell.f_score = float('inf')
                    self.s_cell.g_score = float('inf')
                    bounds.append(self.s_cell.draw_cell())
                    self.s_cell = self.grid_map.cell_grid[mouse_y][mouse_x]
                    self.s_cell.cell_type = 'start'
                    self.s_cell.f_score = float('inf')
                    self.s_cell.g_score = float('inf')
                    bounds.append(self.s_cell.draw_cell())
                    bounds.extend(self.reset_run())
                elif event.button == pygame.BUTTON_RIGHT and not self.draw_mode_walls:
                    mouse_x, mouse_y = self.grid_map.cell_coords_from_mouse_coords(pygame.mouse.get_pos())
                    if mouse_x == -1 or mouse_y == -1:
                        self.manager.process_events(event)
                        continue
                    self.g_cell.cell_type = 'empty'
                    self.g_cell.f_score = float('inf')
                    self.g_cell.g_score = float('inf')
                    bounds.append(self.g_cell.draw_cell())
                    self.g_cell = self.grid_map.cell_grid[mouse_y][mouse_x]
                    self.g_cell.cell_type = 'goal'
                    self.g_cell.f_score = float('inf')
                    self.g_cell.g_score = float('inf')
                    bounds.append(self.g_cell.draw_cell())
                    bounds.extend(self.reset_run())

            self.manager.process_events(event)

        if self.draw_mode_walls:
            (button1, button2, button3) = pygame.mouse.get_pressed()
            if button1:
                mouse_x, mouse_y = self.grid_map.cell_coords_from_mouse_coords(pygame.mouse.get_pos())
                if mouse_x == -1 or mouse_y == -1:
                    return
                if self.grid_map.cell_grid[mouse_y][mouse_x].cell_type == 'empty':
                    self.grid_map.cell_grid[mouse_y][mouse_x].cell_type = 'wall'
                    bounds.append(self.grid_map.cell_grid[mouse_y][mouse_x].draw_cell())
            elif button3:
                mouse_x, mouse_y = self.grid_map.cell_coords_from_mouse_coords(pygame.mouse.get_pos())
                if mouse_x == -1 or mouse_y == -1:
                    return
                if self.grid_map.cell_grid[mouse_y][mouse_x].cell_type == 'wall':
                    self.grid_map.cell_grid[mouse_y][mouse_x].cell_type = 'empty'
                    bounds.append(self.grid_map.cell_grid[mouse_y][mouse_x].draw_cell())
        self.manager.update(time_delta)

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

        if pos_index == 1:
            text = f'{text:<{self.T_SIZE}}'
            fw, fh = self.font.size(text)  # fw: font width,  fh: font height
            surface = self.font.render(text, True, col, self.BACKGROUND_COLOUR)
            pos = (self.TEXT_BORDER, self.TEXT_BORDER)
        elif pos_index == 2:
            text = f'{text:>{self.T_SIZE}}'
            fw, fh = self.font.size(text)  # fw: font width,  fh: font height
            surface = self.font.render(text, True, col, self.BACKGROUND_COLOUR)
            pos = (self.TEXT_BORDER + self.BACKGROUND_SIZE[1] - fw, self.TEXT_BORDER)
        elif pos_index == 3:
            text = f'{text:>{self.T_SIZE}}'
            fw, fh = self.font.size(text)  # fw: font width,  fh: font height
            surface = self.font.render(text, True, col, self.BACKGROUND_COLOUR)
            pos = (self.TEXT_BORDER + self.BACKGROUND_SIZE[1] - fw, (self.height - fh - self.TEXT_BORDER))
        else:
            text = f'{text:<{self.T_SIZE}}'
            fw, fh = self.font.size(text)  # fw: font width,  fh: font height
            surface = self.font.render(text, True, col, self.BACKGROUND_COLOUR)
            pos = (self.TEXT_BORDER, (self.height - fh - self.TEXT_BORDER))
        bounds = pygame.Rect(pos[0], pos[1], fw, fh)
        self.background.blit(surface, pos)
        return bounds


if __name__ == '__main__':
    # get screen resolution
    m = get_monitors()[0]
    # call with width of window and fps
    BrickWall().run()
    # BrickWall(width=int(m.width - m.width * 0.1), height=int(m.height - m.height * 0.1)).run()
