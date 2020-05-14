
try:
    # Enable Ansi color on Windows terminal
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
except:
    pass

from enum import Enum
class AnsiColor(Enum):
    BLACK = "\u001b[30m"
    BLUE = "\033[36m"
    GREEN = "\033[32m"
    RED = "\033[31m"
    WHITE = "\u001b[37m"
    YELLOW = "\033[33m"

# class Color(Enum):
#     VERTEX = AnsiColor.BLUE
#     EDGE = AnsiColor.BLUE
#     GAS = AnsiColor.GREEN
#     STAR = AnsiColor.YELLOW
#     START = AnsiColor.RED

# class Symbol(Enum):
#     VERTEX = "•"
#     HORIZONTAL_EDGE = "━"
#     VERTICAL_EDGE = "┃"

COLOR_VERTEX = AnsiColor.WHITE.value
COLOR_EDGE = AnsiColor.WHITE.value
COLOR_GAS = AnsiColor.GREEN.value
COLOR_STAR = AnsiColor.YELLOW.value
COLOR_START = AnsiColor.RED.value

# TODO: CHOOSE THE MOST SUITABLE SYMBOL
# https://en.wikipedia.org/wiki/Box-drawing_character
SYMBOL_VERTEX = "•"             # "•" "."
SYMBOL_GAS = "∎"                # "∎"
SYMBOL_STAR = "∎"               # "⁕" "⁂" "※" "⁎" "$"
SYMBOL_START = "∎"              # "×" "x"
SYMBOL_HORIZONTAL_EDGE = "━━"   # "━━" "━━━" "__" "-"
SYMBOL_VERTICAL_EDGE = "┃"      # "|"


def input_graph_data()->(tuple, list):

    # Start position
    start_x, start_y = map(int, input().split())

    # Change to 0-based indexing
    start_cell = (start_x - 1, start_y - 1)

    # skip "gas value"
    _ = input()

    n_row, _ = map(int, input().split())
    
    grid_2D = [None] * n_row
    for i in range(n_row):
        grid_2D[i] = list(map(int, input().split()))

    return (start_cell, grid_2D)


"""
Get a str object repesenting a vertex
"""
def vertex(cell_value: int, start_coord=(-1, -1), current_coord=(-1, -1))->str:
    
    is_gas = lambda value: value == 2
    is_star = lambda value: value == 3  

    vertex = COLOR_VERTEX + SYMBOL_VERTEX
    if is_gas(cell_value):
        vertex = COLOR_GAS + SYMBOL_GAS
    elif is_star(cell_value):
        vertex = COLOR_STAR + SYMBOL_STAR

    if start_coord != (-1, -1) and current_coord == start_coord:
        vertex = COLOR_START + SYMBOL_START

    return vertex


def print_graph(start_coord: tuple, grid_2D: list):
    
    if len(grid_2D) == 0:
        return

    is_wall = lambda value: value == 0

    no_vertex_str =  " " * (len(SYMBOL_VERTEX)+ len(SYMBOL_HORIZONTAL_EDGE))

    # Print first row to the second-last row
    for i in range(len(grid_2D) - 1): 
        
        # The line displays horizontal edges and vertices
        first_line_str = ""
        # The line displays vertical edges
        second_line_str = ""

        for j in range(len(grid_2D[i])):
            current_coord = (i, j)

            # if this cell is not at the last row
            if j != len(grid_2D[i]) - 1:
                
                # TODO: Break this mess into smaller pieces
                if is_wall(grid_2D[i][j]):
                    first_line_str += no_vertex_str
                    second_line_str += no_vertex_str
                else:
                    
                    first_line_str += vertex(grid_2D[i][j], start_coord=start_coord, current_coord=current_coord)

                    if is_wall(grid_2D[i][j + 1]):
                        first_line_str +=  " " * len(SYMBOL_HORIZONTAL_EDGE)
                    else:
                        first_line_str += (COLOR_EDGE + SYMBOL_HORIZONTAL_EDGE)
                    
                    if is_wall(grid_2D[i + 1][j]):
                        second_line_str += " " * len(SYMBOL_VERTEX)
                    else:
                        second_line_str += (COLOR_EDGE + SYMBOL_VERTICAL_EDGE)
                    
                    second_line_str += " " * len(SYMBOL_HORIZONTAL_EDGE) 
                        
            else:
                if not is_wall(grid_2D[i][j]):
                    first_line_str += vertex(grid_2D[i][j], start_coord=start_coord, current_coord=current_coord)

                    if not is_wall(grid_2D[i + 1][j]):
                        second_line_str += COLOR_EDGE + SYMBOL_VERTICAL_EDGE
                      
        print(first_line_str)
        print(second_line_str)


    i = len(grid_2D) - 1
    last_row_str = ""
    for j in range(len(grid_2D[i])):

        current_coord = (i, j)
        if j != len(grid_2D[i]) - 1:
            
            if is_wall(grid_2D[i][j]):
                last_row_str += no_vertex_str
            else:
                last_row_str += vertex(grid_2D[i][j], start_coord=start_coord, current_coord=current_coord)

                if is_wall(grid_2D[i][j + 1]):
                    last_row_str +=  " " * len(SYMBOL_HORIZONTAL_EDGE)
                else:
                    last_row_str += COLOR_EDGE + SYMBOL_HORIZONTAL_EDGE
        else:
            if not is_wall(grid_2D[i][j]):
                last_row_str += vertex(grid_2D[i][j], start_coord=start_coord, current_coord=current_coord)

    print(last_row_str)


# python codes\\validate\\visualize_graph.py < docs\\Maps\\"[Summer_Coding] Sample Map 50x50.txt"
# python code/validate/visualize_graph.py < docs/Maps/"[Summer_Coding] Sample Map 50x50.txt"
# PLEASE ZOOM OUT THE COMMAND WINDOWS AS BIG AS POSSIBLE 
if __name__ == "__main__":
    cell_coord, data = input_graph_data()
    print_graph(cell_coord, data)