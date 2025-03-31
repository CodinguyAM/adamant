## A second attempt at Adamant Games logic.
## Uses classes to represent a game this time.
## Game codes (yay!):
## SXO - Tic-Tac-Toe
## UXO - Ultimate Tic-Tac-Toe
## QXO - Quantum Tic-Tac-Toe
## DDO - Dudo/Liar's Dice
## DAB - Dots and Boxes
## HTL - Hold that Line
## ADW - Adverdle
## General principles:
##    __init__ should begin a new game
##    cwin should check winning status
##    move should make a move.
##   .win whould reflect the winner (.5 for draw)
##   .to_move should reflect the player who is to move.
##   .moves should be a list of tuples, each being abled to be starred into move.
##   .initp should be a tuple, able to be starred into __init__

## Yes, this can be very effectively achieved through inheritance, but I like this way. (Sorry to whoever is maintaining this base; probably future me.)
## Ignore the next two comments.

# Beset by Anglicans, beset by Irishmen, beset by Grecian lands and clime; harken to my joy-filled tidings of the golden future time.
# Nothing engaolled can stay.

# setup for Wordle-based games (Adverdle, mostly)

import random as random # Only for assisting, like for generating a random nonobscure word for Adverdle.
from django.conf import settings

ANSWS = []
GUESS = []

with open(settings.BASE_DIR / 'games' / 'ancillary-data' / 'wordle' / 'ans.txt') as fhand:
    for line in fhand:
        ANSWS.append(line[:-1]) # skip the newline

random.shuffle(ANSWS)
print(random.choice(ANSWS), random.choice(ANSWS))

with open(settings.BASE_DIR / 'games' / 'ancillary-data' / 'wordle' / 'ans.txt') as fhand:
    for line in fhand:
        GUESS.append(line[:-1]) # skip the newline

random.shuffle(GUESS)
print(random.choice(GUESS), random.choice(GUESS))

# Generalized game builder
def build_game(name, initp, moves):
    Game = eval(name)
    game = Game(*initp)
    for move in moves:
        game.move(*move)
    return game

# Generalized game flattener
def deflate_game(game):
    return [game.__class__.__name__, game.moves, game.initp]

class SXO:
    def __init__(self):
        self.board = [[-1, -1, -1],
                      [-1, -1, -1],
                      [-1, -1, -1]]
        self.to_move = 0
        self.symbols = ['\033[31mX\033[0m', '\033[36mO\033[0m', '-']
        self.N = 3
        self.K = 2
        self.win = -1

        self.moves = []
        self.initp = ()

    def cwin(self):
        R = [[] for i in range(self.N)] # rows
        C = [[] for i in range(self.N)] # columns
        D = [[] for i in range(2*self.N + 1)] # diags 1
        E = [[] for i in range(2*self.N + 1)] # diags 2
        for i in range(self.N):
            for j in range(self.N):
                Q = self.board[i][j]
                R[i].append(Q)
                C[j].append(Q)
                D[i+j].append(Q)
                E[i-j].append(Q)

        A =  R + C + E + D # D + E fits with the rest of the code, but ARCED!!

        for i in range(self.K):
            if [i] * self.N in A: return i

        return -1
            
        
    def move(self, x, y):
        if self.board[y][x] == self.win == -1:
            self.board[y][x] = self.to_move
            self.win = self.cwin()
            self.to_move = (self.to_move + 1) % self.K
            self.moves.append((x, y))
            return True
        else:
            return False

    def play(self):
        while (self.win == -1):
            for i in range(self.N):
                for j in range(self.N):
                    print(self.symbols[self.board[i][j]], end=' ')
                print()
            print()

            x, y = input(f'Player {self.to_move}, enter row and column: ').split()
            x, y = int(x), int(y)
            if not self.move(x, y):
                print('Invalid move.')

            if len(self.moves) == self.N**2:
                self.win = 0.5
    
            
class UXO:
    def __init__(self):
        self.board = [[SXO(), SXO(), SXO()],
                      [SXO(), SXO(), SXO()],
                      [SXO(), SXO(), SXO()]] # Yes, it's literally 9 tic-tac-toe games. If you (i.e. me, but in the future) have found a bug, it's probably this.
        
        self.mini_board = SXO() # ... make that 10 games.
        self.to_move = 0
        self.symbols = self.mini_board.symbols
        self.N = 3
        self.K = 2
        self.win = -1

        self.last_x = -1
        self.last_y = -1

        self.last_bx = -1
        self.last_by = -1

        self.moves = []
        self.initp = ()
        
        # To past me: thanks for the comment!
        # END MESSAGE TO PAST ME
        # Anyways, thought I'd help *you* out, so here's what's going on:
        # The small tic-tac-toe boards abstract away the logic of three-in-a-rows, and the mini_board does the same for the larger game.

    def cwin(self):
        return self.mini_board.cwin()
        
    def move(self, x, y, bx, by):
        asb = self.board[by][bx] # the board selected by the user
        if (asb != self.board[self.last_y][self.last_x]) != (self.board[self.last_y][self.last_x].win != -1): # If either A: They're playing on a different board, and this board hasn't been won, or B: They're playing on this board, which has been won, that's illegal.
            return False
        if self.win != -1:
            return False
        asb.to_move = self.to_move
        if asb.move(x, y):
            if asb.win != -1:
                self.mini_board.to_move = asb.win
                self.mini_board.move(bx, by)
                self.win = self.mini_board.win
            self.last_x = x
            self.last_y = y
            self.to_move = (self.to_move + 1) % self.K
            self.moves.append((x, y, bx, by))
        else:
            return False

class ADW:
    def __init__(self, w):
        self.w = []
        
        for word in w:
            self.w.append(word.lower())

        N = len(self.w)
        self.w = self.w # Should really be a list, if only for the sake of generality.
        # Well, now it is!
        # And now it's generalized, too!

        self.guesses = [[] for i in range(N)]
        self.fb = [
            [
                [][:] for i in range(N)
            ][:]
            for j in range(N)] # Feedback and guesses from a and b. self.fb[1][0] should return the feedback on guesses at A's word by B.  Although, there's an idea - inverse Wordle - given the solution and the feedback, figure out the words used.

        self.to_move = 0
        self.win = -1

        self.moves = []
        self.initp = (w,)

        self.N = N # number of players

    def cwin(self):
        for i in range(self.N):
            if ('@@@@@' in sum(self.fb[i], [])) and ('@@@@@' not in self.fb[i][i]):
                return i # If they have made a guess that all-correct feedback recieved, and haven't guessed their own word, declare them the winner.
        return -1

    def validate(self, ans, guess):
        corr_symbol = '@' # Symbol for correct letter GREEN
        opos_symbol = '+' # Symbol for wrong position YELLOW
        nooc_symbol = '.' # SYmbol for non-ex. letter BLACK

        r = ''
        count = {}
        occ = {}

        ans_count = {}
        for c in ans:
            ans_count[c] = ans_count.get(c, 0) + 1
        
        for i in range(len(guess)):
            c = guess[i]
            
            cc = count.get(c, 0) # count of c thus far
            acc = ans_count.get(c, 0) # count of c in answer

            count[c] = cc + 1
            occ[c] = occ.get(c, ()) + (i,)

            if ans[i] == c:
                if count[c] > acc:
                    r = r[:occ[c][0]] + nooc_symbol + r[occ[c][0]+1:]
                    occ[c] = occ[c][1:]
                r += corr_symbol
                continue
            
            if not acc:
                r += nooc_symbol
                continue

            if count[c] > acc:
                r += nooc_symbol
                continue

            else:
                r += opos_symbol
                continue

        return r
            
                

    def move(self, guess):
        global GUESS
        if guess not in GUESS: return False

        self.moves.append((guess,))

        self.guesses[self.to_move].append(guess)

        for i in range(self.N):
            self.fb[i][self.to_move][i].append(self.validate(self.w[i], guess))

        self.win = self.cwin()
        

        
tst_adw = ADW(['SPOON', 'LADLE'])

print(
tst_adw.validate('CLASH', 'HEATS'),
tst_adw.validate('CLASH', 'BANAL'),
tst_adw.validate('CLASH', 'SASSY'),
tst_adw.validate('CLASH', 'HATCH'),
        

tst_adw.validate('BRASS', 'BANAL'),
tst_adw.validate('BRASS', 'SPASM'),
tst_adw.validate('BRASS', 'CRASS'),)
