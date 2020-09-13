from math import sqrt
from typing import List
from depq import DEPQ

from grid_cell import GridCell


def euclidean_heuristic(c_1: GridCell, c_2: GridCell) -> float:
    """
    calculates the euclidean distance between the two cells to use as distance heuristic
    :param c_1: a GridCell object
    :param c_2: a GridCell object
    :return: the distance as a float
    """
    return sqrt((c_1.coord[0] - c_2.coord[0]) ** 2 + (c_1.coord[1] - c_2.coord[1]) ** 2)


def manhattan_heuristic(c_1: GridCell, c_2: GridCell) -> float:
    """
    calculates the manhattan distance between the two cells to use as distance heuristic
    :param c_1: a GridCell object
    :param c_2: a GridCell object
    :return: the distance as a float
    """
    return abs(c_1.coord[0] - c_2.coord[0]) + abs(c_1.coord[1] - c_2.coord[1])


class PathSolverAStar:
    """
    Finds the shortest path between the start and end point in the grid using the A* algorithm
    Heuristic can either be Euclidean distance or Manhattan distance
    """

    def __init__(self, cell_grid: List[List[GridCell]], start_cell: GridCell, goal_cell: GridCell,
                 heuristic: str = 'euclidean', movement: str = 'manhattan'):
        """
        Creates a new path solver and initialises the start and end point
        :param cell_grid: The cell grid
        :param start_cell: The starting cell
        :param goal_cell:  The goal cell
        :param heuristic:  The heuristic distance measure to use. One of {'euclidean', 'manhattan'}
        :param movement: The way the agent is allowed to move. One of {'euclidean', 'manhattan'}
        """
        self.cell_grid = cell_grid
        self.openSet = DEPQ(maxlen=len(cell_grid)*len(cell_grid[0]))
        self.start_cell = start_cell
        self.goal_cell = goal_cell
        self.openSet.insert(start_cell, start_cell.f_score)
        # a hash table to keep track of nodes in the Fibonacci heap
        # self.nodes_table = {start_cell.coord: elem}

        if heuristic == 'euclidean':
            self.heuristic = euclidean_heuristic
        elif heuristic == 'manhattan':
            self.heuristic = manhattan_heuristic
        else:
            print(f'Invalid choice for heuristic. Must be either euclidean or manhattan not {heuristic}')
            exit(0)

        if movement == 'euclidean':
            self.neighbours = self.euclidean_neighbours
        elif movement == 'manhattan':
            self.neighbours = self.manhattan_neighbours
        else:
            print(f'Invalid choice for movement. Must be either euclidean or manhattan not {heuristic}')
            exit(0)
                        
        self.start_cell.f_score = self.heuristic(self.start_cell, self.goal_cell)
        self.start_cell.g_score = 0

        self.done = False

    def euclidean_neighbours(self, cell: GridCell) -> List[GridCell]:
        """
        Returns a list of neighbours of the cell provided. In this case it's the 8 adjacent cells
        :param cell: the GridCell we want the neighbours for
        :return: a list of neighbours
        """
        row_lim = (max(cell.coord[0]-1, 0), min(cell.coord[0] + 2, len(self.cell_grid)))
        col_lim = (max(cell.coord[1] - 1, 0), min(cell.coord[1] + 2, len(self.cell_grid[0])))
        lst = []
        for r in range(row_lim[0], row_lim[1]):
            for c in range(col_lim[0], col_lim[1]):
                if (r, c) != cell.coord and self.cell_grid[r][c].cell_type != 'wall':
                    lst.append(self.cell_grid[r][c])
        return lst

    def manhattan_neighbours(self, cell: GridCell) -> List[GridCell]:
        """
        Returns a list of neighbours of the cell provided. In this case it's the 8 adjacent cells without the diagonal
        neighbours (4 neighbours).
        :param cell: the GridCell we want the neighbours for
        :return: a list of neighbours
        """
        row_lim = (max(cell.coord[0]-1, 0), min(cell.coord[0]+2, len(self.cell_grid)))
        col_lim = (max(cell.coord[1] - 1, 0), min(cell.coord[1] + 2, len(self.cell_grid[0])))
        lst = []
        for r in range(row_lim[0], row_lim[1]):
            for c in range(col_lim[0], col_lim[1]):
                if (r, c) != cell.coord and (r == cell.coord[0] or c == cell.coord[1]) \
                        and self.cell_grid[r][c].cell_type != 'wall':
                    lst.append(self.cell_grid[r][c])
        return lst
        
    def next_step(self) -> str:
        """
        performs the next step in the algorithm and updates the cells accordingly
        :return: a status message
        """
        updated = 0
        inserted = 0
        if self.done or self.openSet.is_empty():
            self.done = True
            return 'Done'
        # remove the smallest f_score
        current = self.openSet.poplast()[0]
        msg = f'current = {current.coord}'
        if current.coord == self.goal_cell.coord:
            current.cell_type = 'goal'
            current.draw_cell()
            msg = f'goal reached at {self.goal_cell.coord}. Total distance: {current.f_score}'
            # trace the path
            while current.comes_from is not None:
                current = current.comes_from
                if current.cell_type != 'start':
                    current.cell_type = 'path'
                current.draw_cell()
            self.done = True
            return msg

        if current.cell_type != 'start':
            current.cell_type = 'visited'
            current.draw_cell()
        for neighbour in self.neighbours(current):
            t_score = current.g_score + neighbour.cost
            updated = 0
            inserted = 0
            if t_score < neighbour.g_score:
                # this is a better path to the neighbour so update the g_score
                neighbour.comes_from = current
                neighbour.g_score = t_score
                neighbour.f_score = t_score + self.heuristic(neighbour, self.goal_cell)
                # only add the neighbour to the open set if it is not already in the open set
                if neighbour not in self.openSet:
                    self.openSet.insert(neighbour, neighbour.f_score)
                    # self.nodes_table[neighbour.coord] = elem
                    neighbour.cell_type = 'open_set'
                    neighbour.draw_cell()
                    inserted += 1
                else:
                    # elem = Node(neighbour)
                    self.openSet.remove(neighbour)
                    self.openSet.insert(neighbour, neighbour.f_score)
                    # self.openSet.decrease_key(self.nodes_table[neighbour.coord], neighbour)
                    # self.nodes_table[neighbour.coord] = elem
                    updated += 1
        return msg + f' -- ({updated} updated: {inserted} inserted)'
