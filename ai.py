from copy import deepcopy
from random import choice
hw = 8
eta = 0.9


def empty(y, x, grid): return grid[y][x] == -1 

def inside(y, x): return 0 <= y < hw and 0 <= x < hw

def reversed_piece(y, x, grid, player):
    dydx = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    ret = []
    for dy, dx in dydx:
        ny, nx = y, x
        rs = []
        ny += dy
        nx += dx 
        while inside(ny, nx) and not empty(ny, nx, grid):
            if grid[ny][nx] == player:
                for i, j in rs:
                    ret.append((i, j))
                break
            rs.append((ny, nx))
            ny += dy
            nx += dx
    return ret

def corner(y, x):
    return (y == 0 or y == hw-1) and (x == 0 or x == hw-1)

def near_corner(y, x):
    dydx = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for dy, dx in dydx:
        ny, nx = y+dy, x+dx 
        if corner(ny, nx): return True
    return False

def can_put(grid, player):
    able_pieces = []
    for i in range(hw):
        for j in range(hw):
            if not empty(i, j, grid): continue
            if reversed_piece(i, j, grid, player):
                able_pieces.append((i, j))
    return able_pieces

def eva_score(y, x, player, grid, depth):
    flag = player == ai_player
    ret = 0
    if depth == 0: return 1
    if corner(y, x):
        ret += 10 if flag else -10
    if near_corner(y, x):
        ret += -5 if flag else 5 

    copied_grid = deepcopy(grid)
    copied_grid[y][x] = player

    nx_hands = can_put(copied_grid, 1-player)
    for ny, nx in nx_hands:
        ret += eva_score(ny, nx, 1-player, copied_grid, depth-1) * eta / len(nx_hands)

    return ret 

ai_player = int(input())
grid = [[int(i) for i in input().split()] for _ in range(hw)]
mx_score = -10 ** 6
mx_y, mx_x = -1, -1
able_pieces = can_put(grid, ai_player)
for y, x in able_pieces:
    score = eva_score(y, x, ai_player, grid, 4)
    # print(y, x, score)
    if mx_score < score:
        mx_score = score
        mx_y, mx_x = y, x
print(mx_y, mx_x)

'''
   0 1 2 3 4 5 6 7
00 . . . . . . ◯ ☆
10 . . . . ☆ . ◯ .
20 . . . ☆ ◯ ● ◯ ☆
30 . . ☆ ◯ ● . . .
40 . ☆ ◯ ● ◯ ☆ . .
50 . . ● . ☆ . . .
60 . . . . . . . .
70 . . . . . . . .

0
-1 -1 -1 -1 -1 -1 1 -1 
-1 -1 -1 -1 -1 -1 1 -1 
-1 -1 -1 -1 1 0 1 -1 
-1 -1 -1 1 0 -1 -1 -1 
-1 -1 1 0 1 -1 -1 -1 
-1 -1 0 -1 -1 -1 -1 -1 
-1 -1 -1 -1 -1 -1 -1 -1 
-1 -1 -1 -1 -1 -1 -1 -1 
'''