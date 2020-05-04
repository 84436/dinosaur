class Cell:
    def __init__(self, _x, _y):
        self.x = _x - 1
        self.y = _y - 1


TGREEN = '\033[32m'   # Gas
TBLUE = '\033[36m'    # Path
TRED = '\033[31m'     # Wall
TYELLOW = '\033[33m'  # Star
TWHITE = '\033[37m'   # Entry
# print (TBLUE + "This is some blue text!")
print('\033[40m')
x, y = map(int, input().split())
start_cell = Cell(x, y)
gas_value = int(input())
n, m = map(int, input().split())
Grid2D = [None] * n
for i in range(n):
    Grid2D[i] = list(map(int, input().split()))

symbol = {"gas": chr(36), "star": '*', "path": '.', "wall": '#'}

for i in range(n):
    for j in range(m):
        if i == start_cell.x and j == start_cell.y:
            print(TWHITE + "0",end="")
            continue
        if Grid2D[i][j] == 0:
            print(TRED + symbol["wall"], end="")
        elif Grid2D[i][j] == 1:
            print(TBLUE + symbol["path"], end="")
        elif Grid2D[i][j] == 2:
            print(TGREEN + symbol["gas"], end="")
        elif Grid2D[i][j] == 3:
            print(TYELLOW + symbol["star"], end="")
    print()
