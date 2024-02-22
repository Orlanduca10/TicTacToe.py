import pygame
import sys
import numpy as np
import copy as cp
import random
from constants import *
from math import inf

pygame.init()
screen = pygame.display.set_mode((GAME_WIDTH, HEIGHT))
pygame.display.set_caption("TIC TAC TOE")
screen.fill(BG_COLOR)


class Board:

    def __init__(self):
        self.squares = np.zeros( (ROWS, COLS) )

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player

    def is_empty(self, row, col):
        return self.squares[row][col] == 0
    
    def is_full (self):
        for col in range (COLS):
            for row in range (ROWS):
                if self.squares[row][col] == 0:
                    return False
        return True
    
    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.is_empty(row, col):
                    empty_sqrs.append( (row,col) )
        return empty_sqrs
    
    def final_state(self, show = False):
        '''
        return 0 if no winner yet
        return 1 if player1 wins
        return 2 if player2 wins
        '''
        #vertical winner
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    if self.squares[1][col] == 2: color = CIRCLE_COLOR
                    else: color = CROSS_COLOR
                    ipos = (SQSIZE * col + SQSIZE//2, 20)
                    fpos = (SQSIZE * col + SQSIZE//2, GAME_HEIGHT - 20)
                    pygame.draw.line(screen, color, ipos, fpos, LINE_WIDTH)
                return self.squares[0][col]       
        #horizontal winner
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    if self.squares[row][1] == 2: color = CIRCLE_COLOR
                    else: color = CROSS_COLOR
                    ipos = (20, SQSIZE * row + SQSIZE//2)
                    fpos = (GAME_WIDTH - 20, SQSIZE * row + SQSIZE//2)
                    pygame.draw.line(screen, color, ipos, fpos, LINE_WIDTH)
                return self.squares[row][0]
        # RL diagonal winner
            if self.squares[0][2] == self.squares[1][1] == self.squares[2][0] != 0:
                if show:
                    if self.squares[1][1] == 2: color = CIRCLE_COLOR
                    else: color = CROSS_COLOR
                    ipos = (GAME_WIDTH - 20, 20)
                    fpos = (20, GAME_HEIGHT - 20)
                    pygame.draw.line(screen, color, ipos, fpos, LINE_WIDTH)
                return self.squares[1][1]
            # LR diagonal winner
            if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
                if show:
                    if self.squares[1][1] == 2: color = CIRCLE_COLOR
                    else: color = CROSS_COLOR
                    ipos = (20, 20)
                    fpos = (GAME_WIDTH - 20, GAME_HEIGHT - 20)
                    pygame.draw.line(screen, color, ipos, fpos, LINE_WIDTH)
                return self.squares[1][1]
        return 0
    
    def score(self, counter1, counter2):
        font = pygame.font.SysFont(None, 100)
        img = font.render(str(counter1), True, "black")
        screen.blit(img, (150, 630))

        font = pygame.font.SysFont(None, 100)
        img = font.render(str(counter2), True, "black")
        screen.blit(img, (350, 630))


class AI:
    def __init__(self, player = 2):
        self.player = player

    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))
    
    def minimax(self, board, maximizing, alpha, beta):

        # terminal case
        case = board.final_state()

        # player 1 wins
        if case == 1:
            return 1, None # eval, move

        # player 2 wins
        if case == 2:
            return -1, None

        # draw
        elif board.is_full():
            return 0, None

        if maximizing:
            max_eval = -10000
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = cp.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False, alpha, beta)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
                if max_eval > alpha:
                    alpha = max_eval
                if beta <= alpha:
                    break

            return max_eval, best_move

        elif not maximizing:
            min_eval = 10000
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = cp.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True, alpha, beta)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
                if beta > min_eval:
                    beta = min_eval
                if beta <= alpha:
                    break

            return min_eval, best_move

    def eval(self, board):
        eval, move = self.minimax(board, False, -inf, inf)
        return move # row, col


class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1   # 1-cross 2-circle
        self.running = True
        self.show_scoreboard()
        self.show_lines()

    def show_lines(self):
        #vertical
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, GAME_HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (GAME_WIDTH-SQSIZE, 0), (GAME_WIDTH-SQSIZE, GAME_HEIGHT), LINE_WIDTH)

        #horizontal
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (GAME_WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, GAME_HEIGHT-SQSIZE), (GAME_WIDTH, GAME_HEIGHT-SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, "black", (0, GAME_HEIGHT), (GAME_WIDTH, GAME_HEIGHT), LINE_WIDTH)
    
    def show_scoreboard(self):
        #score tab
        pygame.draw.line(screen, CROSS_COLOR, (50, 630), (110, 690), LINE_WIDTH)
        pygame.draw.line(screen, CROSS_COLOR, (110,630), (50,690), LINE_WIDTH)
        pygame.draw.circle(screen, CIRCLE_COLOR, (280,660), 35, 10)
        #controls (reset and gamemode)
        font = pygame.font.SysFont(None, 30)
        img = font.render("Reset: R", True, "black")
        screen.blit(img, (450, 625))

        img = font.render("Gamemode: G", True, "black")
        screen.blit(img, (430, 660))

    def change_gamemode(self, gamemode):
        if gamemode == "ai": gamemode = "pvp"
        else: gamemode = "ai"
        return gamemode

    def change_player(self):
        self.player = self.player % 2 + 1

    def draw_fig(self, row, col):

        if self.player == 1:
            # left to right cross line
            lr_start = (col * SQSIZE + BUFF, row * SQSIZE + BUFF)
            lr_end = ((col+1) * SQSIZE - BUFF, (row+1)* SQSIZE - BUFF)
            pygame.draw.line(screen, CROSS_COLOR, lr_start, lr_end, LINE_WIDTH)

            # right to left cross line
            rl_start = ((col+1) * SQSIZE - BUFF, row *SQSIZE + BUFF)
            rl_end = (col * SQSIZE + BUFF, (row+1) * SQSIZE - BUFF)
            pygame.draw.line(screen, CROSS_COLOR, rl_start, rl_end, LINE_WIDTH)
        
        else:
            #circle
            center = (col * SQSIZE + SQSIZE //2, row * SQSIZE + SQSIZE //2)
            pygame.draw.circle(screen, CIRCLE_COLOR, center, RADIUS, LINE_WIDTH)

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.change_player()

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.is_full()
    
    def reset(self):
        screen.fill(BG_COLOR)
        self.__init__()
    
def main():
    global gamemode
    #object
    game = Game()
    board = game.board
    ai = game.ai
    counter1, counter2 = 0,0

    #mainloop
    while True:
        #hide previous score until restart
        screen.fill(BG_COLOR,(30, 630, 110, 690))
        screen.fill(BG_COLOR,(230,610, 320, 690))
        game.show_scoreboard()
        board.score(counter1, counter2)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                #reset the game
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                # change gamemode between AI and PvP
                if event.key == pygame.K_g and not game.running:
                    counter1, counter2 = 0, 0
                    gamemode = game.change_gamemode(gamemode)
                    game.reset()
                    board = game.board
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE

                if pos[1] > GAME_WIDTH or pos[0] > GAME_HEIGHT:    #avoids game closing if scoreboard is clicked
                    continue

                if board.is_empty(row, col) and game.running:
                    game.make_move(row, col)

                    if game.isover():
                        if board.final_state(True) == 1: counter1 += 1
                        elif board.final_state(True) == 2: counter2 += 1
                        screen.fill(BG_COLOR,(150, 610, 110, 690))
                        screen.fill(BG_COLOR,(230, 610, 320, 690))
                        game.running = False
                
                if gamemode == "ai" and game.player == ai.player and not (board.is_full() or board.final_state() != 0):
                    # update the screen
                    pygame.display.update()

                    # eval
                    row, col = ai.eval(board)
                    game.make_move(row, col)

                    if game.isover():
                        if board.final_state(True) == 1: counter1 += 1
                        elif board.final_state(True) == 2: counter2 += 1
                        screen.fill(BG_COLOR,(150, 610, 110, 690))
                        screen.fill(BG_COLOR,(230,610, 320, 690))
                        game.running = False
                        
        pygame.display.update()
main()