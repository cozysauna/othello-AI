import subprocess
from random import choice
from sys import stdin, stdout
from time import sleep


hw = 8
class othello():
    def __init__(self):
        '''        
            1: Black 
            0: White
        '''
        self.hw = 8
        self.grid = [[-1 for _ in range(self.hw)] for _ in range(self.hw)]
        self.grid[3][3] = 1
        self.grid[4][4] = 1
        self.grid[3][4] = 0 
        self.grid[4][3] = 0
        self.player = 1
        self.end = False
        self.able_pieces = []


    def inside(self, y, x): return 0 <= y < self.hw and 0 <= x < self.hw
    def empty(self, y, x): return self.grid[y][x] == -1 

    def reversed_piece(self, y, x):
        dydx = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        ret = []
        for dy, dx in dydx:
            ny, nx = y, x
            rs = []
            ny += dy
            nx += dx 
            while self.inside(ny, nx) and not self.empty(ny, nx):
                if self.grid[ny][nx] == self.player:
                    for i, j in rs:
                        ret.append((i, j))
                    break
                rs.append((ny, nx))
                ny += dy
                nx += dx
        return ret

    def can_put(self):
        able_pieces = []
        for i in range(self.hw):
            for j in range(self.hw):
                if not self.empty(i, j): continue
                if self.reversed_piece(i, j):
                    able_pieces.append((i, j))
        return able_pieces

    def reverse(self, y, x):
        rp = self.reversed_piece(y, x)
        for i, j in rp:
            self.grid[i][j] = self.player
        
    def update_end(self):
        player = self.player
        if not self.can_put():
            self.player = 1-player
            if not self.can_put():
                self.end = True 
        self.player = player
          
    def put(self):
        if not self.able_pieces:
            self.player = 1 - self.player
            self.update_end()
            return 
        if self.player == ai_player and ai_mode:
            sleep(1)
            stdin = str(ai_player) + '\n'
            for y in range(hw):
                for x in range(hw):
                    stdin += str(self.grid[y][x]) + ' '
                stdin += '\n'
            # print(stdin)

            ai = subprocess.Popen('python3 ai.py'.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            y, x = [int(i) for i in ai.communicate(stdin.encode('utf-8'))[0].decode('utf-8').split()]
        else:
            try:
                mes = input('Black ')
                if mes == 'f': return 'f'
                y, x = [int(i) for i in mes]
                if (y, x) not in self.able_pieces:
                    return print('Please input correct numbers')
            except:
                return print('Please input correct numbers')
            if not self.inside(y, x) or not self.empty(y, x):
                return print('({}, {}) is not appropriate'.format(y, x))

        self.grid[y][x] = self.player        
        self.reverse(y, x)
        self.player = 1 - self.player
        self.update_end()
    
    def count_pieces(self):
        w, b = 0, 0
        for i in range(self.hw):
            for j in range(self.hw):
                if self.grid[i][j] == 0: w += 1
                if self.grid[i][j] == 1: b += 1
        return [w, b]

    def display(self):
        white = '●'
        black = '◯'
        blank = '.'
        star  = '☆'

        self.able_pieces = self.can_put()
        display_grid = [[-1 for _ in range(self.hw)] for _ in range(self.hw)]
        for i in range(self.hw):
            for j in range(self.hw):
                if self.grid[i][j] == 0: display_grid[i][j] = white
                elif self.grid[i][j] == 1: display_grid[i][j] = black
                else: display_grid[i][j] = blank

        for i, j in self.able_pieces:
            display_grid[i][j] = star

        print()
        print('----- {} Turn -----'.format('Your' if self.player else 'Enemy'))
        if not self.player:
            print('Please wait for a while')
        print()
        print(' '.join(['  '] + [str(i) for i in range(self.hw)]))
        for i, line in enumerate(display_grid):
            print(' '.join([str(i)+'0'] + [e for e in line]))

ai_mode = True
ai_player = 0
ot = othello()


while True:
    ot.display()
    if ot.end:
        ot.display()
        w, b = ot.count_pieces()
        print()
        print('White: {}, Black: {}'.format(w, b))
        if w == b: print('Draw')
        else: print('Winner: {}'.format('White' if w > b else 'Black'))
        break

    if ot.put() == 'f': exit()
