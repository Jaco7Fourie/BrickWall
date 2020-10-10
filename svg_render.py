from typing import List
import drawSvg as SDraw
from drawSvg import DrawingBasicElement, NoElement
from grid_cell import GridCell, WalledCell, Walls
import os

# https://coolors.co/a90f33-f78c6b-ffd166-83d483-037758-118ab2-073b4c
BACKGROUND_COLOUR = (246, 240, 237)  # Isabelline
PATH_COLOUR = (17, 138, 178)  # Blue NSC
WALL_COLOUR = (80, 49, 42)  # Dark Liver Horses
VISITED_COLOUR = (247, 140, 107)  # Middle Red
OPEN_SET_COLOUR = (131, 212, 131)  # Mantis
START_COLOUR = (3, 119, 88)  # Tropical rain forest
GOAL_COLOUR = (169, 15, 51)  # Cromson UA


def colorstr(rgb): return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])


def render_cell(drawing: SDraw.Drawing, cell: GridCell, x_pos: int, y_pos: int):
    """
    renders a cell as an svg element
    :param drawing: The svg drawing that we will render this cell to
    :param cell: a single GridCell object
    :param x_pos: the svg x coordinate to the top-left of this cell
    :param y_pos: the svg y coordinate to the top-left of this cell
    :return: None
    """
    if isinstance(cell, WalledCell):
        if cell.cell_type == 'path':
            r = SDraw.Rectangle(x_pos, y_pos, 10, 10, fill=colorstr(GridCell.PATH_COLOUR))
            drawing.append(r)
        elif cell.cell_type == 'visited':
            r = SDraw.Rectangle(x_pos + 2, y_pos + 2, 6, 6, fill=colorstr(GridCell.VISITED_COLOUR))
            drawing.append(r)
        elif cell.cell_type == 'open_set':
            r = SDraw.Rectangle(x_pos + 2, y_pos + 2, 6, 6, fill=colorstr(GridCell.OPEN_SET_COLOUR))
            drawing.append(r)
        elif cell.cell_type == 'start':
            r = SDraw.Rectangle(x_pos, y_pos, 10, 10, fill=colorstr(GridCell.START_COLOUR))
            drawing.append(r)
        elif cell.cell_type == 'goal':
            r = SDraw.Rectangle(x_pos, y_pos, 10, 10, fill=colorstr(GridCell.GOAL_COLOUR))
            drawing.append(r)
        elif cell.cell_type == 'empty':
            pass
        else:
            print(f'Invalid Cell type: {cell.cell_type}')
            return NoElement

        # draw the walls
        if Walls.NORTH in cell.walls:
            r = SDraw.Line(x_pos, y_pos, x_pos + 10, y_pos,
                           stroke='black', stroke_width=2, fill='none')
            drawing.append(r)
        if Walls.SOUTH in cell.walls:
            r = SDraw.Line(x_pos, y_pos + 10, x_pos + 10, y_pos + 10,
                           stroke='black', stroke_width=2, fill='none')
            drawing.append(r)
        if Walls.WEST in cell.walls:
            r = SDraw.Line(x_pos, y_pos, x_pos, y_pos + 10,
                           stroke='black', stroke_width=2, fill='none')
            drawing.append(r)
        if Walls.EAST in cell.walls:
            r = SDraw.Line(x_pos + 10, y_pos, x_pos + 10, y_pos + 10,
                           stroke='black', stroke_width=2, fill='none')
            drawing.append(r)
    else:
        print('export to svg implemented for WalledCells only')


def render_to_svg(path: str, cell_grid: List[List[GridCell]], save_png: bool):
    """
    render a grid_cell as an svg file
    :param path: path to the svg file that we will save to
    :param cell_grid: the cell_grid object that can either be GridCells or WalledCells
    :param save_png: if true will also save a png version of the maze
    :return: None
    """
    rows = len(cell_grid)
    cols = len(cell_grid[0])
    drawing = SDraw.Drawing(cols * 10, rows * 10, origin=(0, 0), displayInline=False)
    # draw the border
    r = SDraw.Rectangle(0, 0, cols * 10, rows * 10, stroke_width=2, fill='none', stroke='black')
    drawing.append(r)
    for i in range(rows):
        for j in range(cols):
            x_pos = j * 10
            y_pos = rows * 10 - i * 10
            r = render_cell(drawing, cell_grid[i][j], x_pos, y_pos)
            drawing.append(r)

    drawing.setPixelScale(2)  # Set number of pixels per geometry unit
    drawing.saveSvg(path)
    if save_png:
        png_path = os.path.splitext(path)[0]
        drawing.savePng(png_path + '.png')
