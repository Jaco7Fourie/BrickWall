from typing import List, Any, Tuple
from grid_cell import WalledCell
from random import sample


class WilsonMaze:
    """
    Generates a maze based on Wilson's algorithm that interprets the maze as a uniform spanning tree of the graph
    of cells. The algorithm is based on random walks between cells that have their loops erased. This creates a maze
    with no biases. This implementation is not efficient but is implemented in a way to make each step explicit and
    recorded for the purpose of animating the process
    see http://weblog.jamisbuck.org/2011/1/20/maze-generation-wilson-s-algorithm
    """

    def __init__(self, cell_grid: List[List[WalledCell]]):
        """
        Creates a new maze generator
        :param cell_grid: The cell grid
        """
        self.cell_grid = cell_grid
        # build a set of non-visited cells to sample from
        self.working_set = set()
        for i in range(len(self.cell_grid)):
            for j in range(len(self.cell_grid[0])):
                self.working_set.add(self.cell_grid[i][j].coord)

        self.current_origin = None
        self.current_step = None
        self.done = False
        self.last_origin = None
        self.visited = 1
        self.init_required = True

    def next_step(self, updates: List[Any], render_steps: int) -> str:
        """
        performs the next step in the algorithm and updates the cells accordingly
        :param updates: a list of rectangles that represent limits of the background that need to be updated at the
        next draw
        :param render_steps: the number of steps to process before returning. This is used to speed up the the animation
        by not rendering every generation step
        :return: a status message
        """
        msg = ''
        if self.init_required:
            self.init(updates)
            self.init_required = False
        for i in range(render_steps):
            if len(self.working_set) == 0:
                self.done = True
                return f'Maze generation complete -- ({len(self.cell_grid)},{len(self.cell_grid[0])})'

            # have we reached a visited cell or should we continue walking?
            cell = self.cell_grid[self.current_step[0]][self.current_step[1]]
            if cell.cell_type == 'visited':
                # backtrack to find the path and remove it from the working set
                while cell.comes_from is not None:
                    cell.tunnel_to(cell.comes_from)
                    cell = cell.comes_from
                    if cell.cell_type == 'visited':
                        break
                    cell.cell_type = 'visited'
                    self.working_set.remove(cell.coord)
                    updates.append(cell.draw_cell())
                msg = f'New path found from {self.current_origin} to {cell.coord}'
                # get a new random starting point for the next walk
                if len(self.working_set) > 0:
                    self.current_origin = sample(self.working_set, 1)[0]
                    self.cell_grid[self.current_origin[0]][self.current_origin[1]].comes_from = None
                    # self.working_set.remove(self.current_origin)
                    neighbours = self.get_neighbours(self.current_origin)
                    self.current_step = sample(neighbours, 1)[0]
                    self.last_origin = self.cell_grid[self.current_step[0]][self.current_step[1]].comes_from
                    self.cell_grid[self.current_step[0]][self.current_step[1]].comes_from = \
                        self.cell_grid[self.current_origin[0]][self.current_origin[1]]
            elif cell.cell_type == 'open_set':
                # this random walk resulted in a loop we need to remove it before continuing
                while cell.comes_from is not None:
                    cell = cell.comes_from
                    if cell.coord == self.current_step:
                        break
                    else:
                        cell.cell_type = 'empty'
                    updates.append(cell.draw_cell())
                if cell.comes_from is None:
                    print('WARNING: Backtrack loop ended without finding loop origin. Maze integrity lost.')
                msg = f'Loop removed at {self.current_step}'
                # reset the original comes_from direction that was hopefully saved before the loop
                cell.comes_from = self.last_origin
                # start walk again in a (hopefully) different direction
                neighbours = self.get_neighbours(self.current_step)
                tmp = sample(neighbours, 1)[0]
                self.last_origin = self.cell_grid[tmp[0]][tmp[1]].comes_from
                self.cell_grid[tmp[0]][tmp[1]].comes_from = self.cell_grid[self.current_step[0]][self.current_step[1]]
                self.current_step = tmp
            else:
                # TODO: Add appropriate msg
                # This should only include empty cells. All we can do is take the next random direction
                cell.cell_type = 'open_set'
                updates.append(cell.draw_cell())
                msg = f'Walked to {self.current_step}'
                neighbours = self.get_neighbours(self.current_step)
                tmp = sample(neighbours, 1)[0]
                self.last_origin = self.cell_grid[tmp[0]][tmp[1]].comes_from
                self.cell_grid[tmp[0]][tmp[1]].comes_from = self.cell_grid[self.current_step[0]][self.current_step[1]]
                self.current_step = tmp

        return msg

    def get_neighbours(self, cell: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Returns a list of neighbours of the cell coordinate provided.
        In this case it's the 8 adjacent cells without the diagonal neighbours (4 neighbours).
        :param cell: the WalledCell coordinate tuple we want the neighbours for
        :return: a list of neighbours
        """
        row_lim = (max(cell[0] - 1, 0), min(cell[0] + 2, len(self.cell_grid)))
        col_lim = (max(cell[1] - 1, 0), min(cell[1] + 2, len(self.cell_grid[0])))
        lst = []
        for r in range(row_lim[0], row_lim[1]):
            for c in range(col_lim[0], col_lim[1]):
                if (r, c) != cell and (r == cell[0] or c == cell[1]):
                    lst.append((r, c))
        return lst

    def init(self, updates: List[Any]):
        # pick a random cell to initialise the generator
        row = sample(self.cell_grid, 1)[0]
        last_insert = sample(row, 1)[0]
        last_insert.cell_type = 'visited'
        updates.append(last_insert.draw_cell())
        self.working_set.remove(last_insert.coord)
        self.current_origin = sample(self.working_set, 1)[0]
        # initial random direction for first step of first walk
        neighbours = self.get_neighbours(self.current_origin)
        self.current_step = sample(neighbours, 1)[0]
        self.cell_grid[self.current_step[0]][self.current_step[1]].comes_from = \
            self.cell_grid[self.current_origin[0]][self.current_origin[1]]

