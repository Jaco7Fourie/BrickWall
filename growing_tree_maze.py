from typing import List, Any
from grid_cell import WalledCell
from random import sample
from depq import DEPQ


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
        self.working_set = DEPQ(maxlen=len(cell_grid)*len(cell_grid[0]))
        # pick a random cell to initialise the generator
        row = sample(cell_grid, 1)
        self.working_set.addfirst(sample(row, 1))

    def next_step(self, updates: List[Any]) -> str:
        """
        performs the next step in the algorithm and updates the cells accordingly
        :param updates: a list of rectangles that represent limits of the background that need to be updated at the
        next draw
        :return: a status message
        """
