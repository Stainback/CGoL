def generate_universe(height, width):
    """Generates array which represents the universe of Conway's Game of Life.
       The universe of the Game of Life is two-dimensional orthogonal grid of square cells,
       each of which is in one of two possible states, live or dead."""
    universe = [[0]*height for i in range(width)]
    return universe


def change_cell_state(universe, x, y):
    if universe[y-1][x-1] == 0:
        universe[y-1][x-1] = 1
    else:
        universe[y - 1][x - 1] = 0
    return universe


def calculate_cell_index(universe):
    """Cell index is a sum of itself and cell within its reach.
       1st step - create temporary matrix which contains universe field with 0 on borders of it. Purpose of it - avoid
       issues with going outside universe borders.
       2nd step - for each cell in universe calculate cell index and put a result into cell index matrix."""
    expanded_universe = [[0]*(len(universe[0])+2) for i in range(len(universe)+2)]
    for exp_row in range(1, len(expanded_universe)-2):
        for exp_col in range(1, len(expanded_universe[0])-2):
            expanded_universe[exp_row][exp_col] = universe[exp_row-1][exp_col-1]
    cell_index_matrix = [[0]*(len(universe[0])) for i in range(len(universe))]
    for cim_row in range(len(cell_index_matrix)):
        for cim_col in range(len(cell_index_matrix[0])):
            cell_index_matrix[cim_row][cim_col] = (expanded_universe[cim_row][cim_col]
                                                   + expanded_universe[cim_row][cim_col+1]
                                                   + expanded_universe[cim_row][cim_col+2]
                                                   + expanded_universe[cim_row+1][cim_col]
                                                   + expanded_universe[cim_row+1][cim_col+1]
                                                   + expanded_universe[cim_row+1][cim_col+2]
                                                   + expanded_universe[cim_row+2][cim_col]
                                                   + expanded_universe[cim_row+2][cim_col+1]
                                                   + expanded_universe[cim_row+2][cim_col+2])
    return cell_index_matrix


def calculate_new_gen(universe, cell_index_matrix):
    """Every cell interacts with its eight neighbours, which are the cells that are horizontally, vertically,
           or diagonally adjacent. At each step in time, the following transitions occur:
           - Any live cell with two or three live neighbours survives.
           - Any dead cell with three live neighbours becomes a live cell.
           - All other live cells die in the next generation. Similarly, all other dead cells stay dead."""
    new_gen = [[0]*(len(universe[0])) for i in range(len(universe))]
    for gen_row in range(len(cell_index_matrix)):
        for gen_col in range(len(cell_index_matrix[0])):
            if ((universe[gen_row][gen_col] == 0 and cell_index_matrix[gen_row][gen_col] == 3)
                or (universe[gen_row][gen_col] == 1 and (cell_index_matrix[gen_row][gen_col] == 3
                                                         or cell_index_matrix[gen_row][gen_col] == 4))):
                new_gen[gen_row][gen_col] = 1
    return new_gen
