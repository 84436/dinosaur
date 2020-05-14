import random
import time
from enum import Enum
from heapq import *
from collections import deque
import sys, getopt

travesal_step = [(0, -1), (0, 1), (-1, 0), (1, 0)]
grid2d = []
n, m = 0, 0
gas_state = []
gas_start = 0
visited = [[False] * n for _ in range(m)]


class type(Enum):
    UNKNOWN = -1
    WALL = 0
    PATH = 1
    GAS = 2
    STAR = 3


class Cell:
    """ A cell class for Dijkstra path_finding"""
    gas = 0

    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y

    def __lt__(self, others):
        self.gas = gas_state[self.x][self.y]

        if grid2d[self.x][self.y] > grid2d[others.x][others.y] and random.randint(0, 4):
            return True
        return self.gas > gas_state[others.x][others.y]


def isValid(x, y):
    return x in range(n) and y in range(m)


def Dijkstra(src):
    global gas_start, grid2d, gas_state, visited
    acyclic_graph = []
    acyclic_graph.append((src.x, src.y))
    tmp_gas_state = gas_state
    visited_l = [[0] * n for _ in range(m)]
    visited[src.x][src.y] = True
    visited_l[src.x][src.y] = 1
    pq = [src]
    dis = []
    while pq:
        top = heappop(pq)
        gas = tmp_gas_state[top.x][top.y]
        cell_type = type(grid2d[top.x][top.y])
        if gas < 0:
            continue
        if cell_type == type.GAS and (top.x, top.y) not in acyclic_graph:
            if grid2d[src.x][src.y] != 2 or not visited[top.x][top.y]:
                acyclic_graph.append((top.x, top.y))
               # visited[top.x][top.y] = True
            else:
                dis.append((top.x, top.y))
        elif cell_type == type.STAR and (top.x, top.y) not in acyclic_graph and (len(astar(grid2d,(src.x,src.y),(top.x,top.y))) < gas_start//3):

            acyclic_graph.append((top.x, top.y))
            grid2d[top.x][top.y] = 1

        if len(acyclic_graph) == 2:
            return acyclic_graph
        for dx, dy in travesal_step:
            x = top.x + dx
            y = top.y + dy
            if isValid(x, y):
                if grid2d[x][y] != 0 and grid2d[x][y] != 3 and (visited_l[x][y] == 1 or gas - 1 > tmp_gas_state[x][
                    y]):  # gas - 1 > gas_state[x][y] #or visited_l[x][y] == 1):

                    tmp_gas_state[x][y] = gas - 1
                    if grid2d[x][y] == 2:
                        gas_state[x][y] = gas_start
                        tmp_gas_state[x][y] = gas_start
                    visited_l[x][y] += 1
                    heappush(pq, Cell(x, y))
                elif grid2d[x][y] == 3 and visited_l[x][y] < 2:
                    gas_state[x][y] = gas_start
                    tmp_gas_state[x][y] = gas_start
                    visited_l[x][y] += 1
                    heappush(pq, Cell(x, y))
    if dis:
        acyclic_graph.append(dis.pop())
    return acyclic_graph


class Node():
    """A node class for A* path_finding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children
        children = []
        for new_position in travesal_step:  # Adjacent squares up down left right

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] == 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                    (child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


def main(argv):
    global m, n, gas_state, fin_fd, gas_start, visited, fout_fd
    input_file = ''
    output_file = ''
    flag = [0, 0]
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('test.py -i <input_file> -o <output_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <input_file> -o <output_file>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
            flag[0] = 1
        elif opt in ("-o", "--ofile"):
            output_file = arg
            flag[1] = 1
    import os
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    fin_fd = open("map_100_100.txt", "r")
    if flag[0]:
        input_file = os.path.join(THIS_FOLDER, input_file)
        fin_fd = open(input_file, "r")
    if flag[1]:
        out_file = os.path.join(THIS_FOLDER, output_file)
        fout_fd = open(str(output_file), "wt")

    x_start, y_start = map(int, fin_fd.readline().split())
    x_start = x_start - 1
    y_start = y_start - 1
    gas_start = int(fin_fd.readline())
    n, m = map(int, fin_fd.readline().split())
    for i in range(n):
        grid2d.append(list(map(int, fin_fd.readline().split())))
    gas_state = [[-1] * m for _ in range(n)]
    visited = [[False] * n for _ in range(m)]
    gas_state[x_start][y_start] = gas_start
    print(x_start, y_start)
    print(gas_start)
    print(n, m)
    print(grid2d)
    acylic_graph = [(x_start, y_start), (x_start, y_start)]
    res = [(x_start, y_start)]
    print("Rendering Optimal Path ...")
    # gas_state[1][48] = 19
    # print(Dijkstra(Cell(1,48),grid2d))
    while True:
        acylic_graph = Dijkstra(Cell(acylic_graph[1][0], acylic_graph[1][1]))
        if len(acylic_graph) != 2:
            break
        path = astar(grid2d, acylic_graph[0], acylic_graph[1])
        print(path)
        for ele in path[1:]:
            res.append(ele)

    for x, y in res:
        outstr = f"{x + 1} {y + 1}\n"
        print(outstr)
        if flag[1]:
            fout_fd.write(outstr)


if __name__ == "__main__":
    main(sys.argv[1:])

#
# if __name__ == '__main__':
#     main()
