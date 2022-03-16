import time
from state import State
import numpy as np
import pygame as pg
from mcts import MCTS
from random_player import Random_Player
from state import detection_kernels
from scipy.signal import convolve2d

# game logical variables:
# First player: color=red, number on the borad=1, turn=0, type: search algorithm
# Second player: color=green, number on the borad=-1, turn=1, type: search algorithm
ROW_COUNT=6
COLUMN_COUNT=7
FPLAYER_PIECE=1
SPLAYER_PIECE=-1
FPLAYER_COLOR=(255,0,0)
SPLAYER_COLOR=(0,255,0)



#game visualization variables:
SQUARESIZE=80
WIDTH=COLUMN_COUNT*SQUARESIZE
HEIGHT=(ROW_COUNT+1)*SQUARESIZE
PURPLE=(128, 0, 128)
WHITE=(255,255,255)
BLACK=(0,0,0)
MONITOR=(0, 150, 255)
RADIUS = int(SQUARESIZE/2 - 5)

def is_valid_loc(board,row,col):
    return board[row][col]==0

def draw_board(board,screen,turn,font):

    for c in range(COLUMN_COUNT):
        pg.draw.rect(screen, MONITOR, (c * SQUARESIZE, 0, SQUARESIZE, SQUARESIZE))

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pg.draw.rect(screen, PURPLE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            if board[r][c]==0:
                pg.draw.circle(screen, WHITE, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c]==1:
                pg.draw.circle(screen, FPLAYER_COLOR,(int(c * SQUARESIZE + SQUARESIZE / 2), int((r + 1) * SQUARESIZE + SQUARESIZE / 2)),RADIUS)
            else:
                pg.draw.circle(screen, SPLAYER_COLOR, (int(c * SQUARESIZE + SQUARESIZE / 2), int((r + 1) * SQUARESIZE + SQUARESIZE / 2)),RADIUS)
    pg.display.update()

def end_of_game(board):
    for kernel in detection_kernels:
        result_board = convolve2d(board, kernel, mode="valid")
        if 4 in result_board or -4 in result_board:
            return "win or loss"

    if len(np.where(board == 0)[0]) == 0:
        return "draw"

    return "not ended"

def turn_monitor(screen,font,turn):
    if turn==1:
        text = font.render('Green turn', True,SPLAYER_COLOR)
        textRect = text.get_rect()
        textRect.center = ((COLUMN_COUNT*SQUARESIZE)/2, SQUARESIZE/2)
        screen.blit(text, textRect)
    else:
        text = font.render('Red turn', True, FPLAYER_COLOR)
        textRect = text.get_rect()
        textRect.center = ((COLUMN_COUNT * SQUARESIZE) / 2, SQUARESIZE / 2)
        screen.blit(text, textRect)
    pg.display.update()


def show_result(screen,font,turn):
    if turn==1:
        text = font.render('Second Player won!', True,SPLAYER_COLOR)
        textRect = text.get_rect()
        textRect.center = ((COLUMN_COUNT*SQUARESIZE)/2, SQUARESIZE/2)
        screen.blit(text, textRect)
    elif turn==0:
        text = font.render('First Player won!', True, FPLAYER_COLOR)
        textRect = text.get_rect()
        textRect.center = ((COLUMN_COUNT * SQUARESIZE) / 2, SQUARESIZE / 2)
        screen.blit(text, textRect)
    else:
        text = font.render('That is a tie', True, BLACK)
        textRect = text.get_rect()
        textRect.center = ((COLUMN_COUNT * SQUARESIZE) / 2, SQUARESIZE / 2)
        screen.blit(text, textRect)
    pg.display.update()
    time.sleep(10)
    quit()

def game_loop():

    # pygame initializaions
    pg.init()
    font = pg.font.Font('freesansbold.ttf', 32)
    pg.display.set_caption("Connect4")
    screen=pg.display.set_mode((WIDTH,HEIGHT))

    # set game parameters nd show the first status of the game
    game_over=False
    game_board=np.zeros((ROW_COUNT,COLUMN_COUNT))
    turn=0
    draw_board(game_board, screen, turn, font)
    turn_monitor(screen, font, turn)

    # instantiate players
    root1 = State(None, True, game_board,cp=-1,N=1)
    root2 = State(None, True, game_board,cp=-1,N=1)
    player1=MCTS(root1,MCTS.simulation2,5)
    player2=MCTS(root2,MCTS.simulation1,5)

    while not game_over:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()

        #get the next move from players and change their boards
        if turn==0:
            #player1 has to play
            row,cul=player1.search()
            player2.change_root(row,cul)
        else:
            #player2 has to play
            row,cul=player2.search()
            player1.change_root(row,cul)

        #put the new piece on the board and show it
        if is_valid_loc(game_board,row,cul):
            if turn==0:
                game_board[row][cul] = FPLAYER_PIECE
            else:
                game_board[row][cul] = SPLAYER_PIECE
        else:
            raise Exception("The move is not valid.")
        draw_board(game_board, screen, turn, font)

        #check if game ends and announce the winner
        result=end_of_game(game_board)
        if result=="win or loss":
            game_over=True
            if turn==0:
                #player1 wins
                show_result(screen,font,0)
            else:
                #player2 wins
                show_result(screen, font, 1)
        if game_over=="draw":
            # this is a tie
            game_over=True
            show_result(screen, font, 2)

        #change turn and print it
        turn=1-turn
        turn_monitor(screen,font,turn)



if __name__ == '__main__':
    game_loop()