from typing import List, Any
from grid_cell import WalledCell
from random import sample, random
from collections import deque


class GrowingTreeMaze:
    """
    Generates a maze based on the growing tree algorithm
    see https://weblog.jamisbuck.org/2011/1/27/maze-generation-growing-tree-algorithm
    """

    def __init__(self, cell_grid: List[List[WalledCell]], backtrack_prob: float = 0.3):
        """
        Creates a new maze generator
        :param cell_grid: The cell grid
        :param backtrack_prob: The probability that the generator will tend towards a recursive back tracker
        """
        self.cell_grid = cell_grid
        self.backtrack_prob = backtrack_prob
        self.working_set = deque()
        # pick a random cell to initialise the generator
        row = sample(cell_grid, 1)[0]
        last_insert = sample(row, 1)[0]
        last_insert.cell_type = 'visited'
        self.working_set.append(last_insert)

        self.done = False
        self.visited = 0

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
        for i in range(render_steps):
            if len(self.working_set) == 0:
                self.done = True
                return f'Maze generation complete -- ({len(self.cell_grid)},{len(self.cell_grid[0])})'

            if random() < self.backtrack_prob:
                cell = self.working_set[-1]
            else:
                cell = sample(self.working_set, 1)[0]
            neighbours = self.get_neighbours(cell)
            if len(neighbours) == 0:
                self.working_set.remove(cell)
                msg = f'Cell removed -- {cell.coord[-1::-1]}'
            else:
                next_cell = sample(neighbours, 1)[0]
                cell.tunnel_to(next_cell)
                next_cell.cell_type = 'visited'
                self.visited += 1
                self.working_set.append(next_cell)
                updates.append(cell.draw_cell())
                updates.append(next_cell.draw_cell())
                msg = f'Tunnelled to {next_cell.coord[-1::-1]}'
        return msg

    def get_neighbours(self, cell: WalledCell) -> List[WalledCell]:
        """
        Returns a list of unvisited neighbours of the cell provided.
        In this case it's the 8 adjacent cells without the diagonal neighbours (4 neighbours).
        :param cell: the WalledCell we want the neighbours for
        :return: a list of neighbours
        """
        row_lim = (max(cell.coord[0] - 1, 0), min(cell.coord[0] + 2, len(self.cell_grid)))
        col_lim = (max(cell.coord[1] - 1, 0), min(cell.coord[1] + 2, len(self.cell_grid[0])))
        lst = []
        for r in range(row_lim[0], row_lim[1]):
            for c in range(col_lim[0], col_lim[1]):
                if (r, c) != cell.coord and (r == cell.coord[0] or c == cell.coord[1]) \
                        and self.cell_grid[r][c].cell_type != 'visited':
                    lst.append(self.cell_grid[r][c])
        return lst
