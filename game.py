import pygame
import os
from sys import exit
from pygame.constants import MOUSEBUTTONDOWN
from piece import Pawn, Bishop, Knight, Rook, Queen, King

from pygame.time import Clock

pygame.init()
width = 512
height = 512
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

board_img = pygame.image.load(os.path.join("img", "board.png"))
board_rect = board_img.get_rect()

board = [[0 for _ in range(8)] for _ in range(8)]
selected = 0
turn = "w"

board[0][0] = Rook(0, 0, "b")
board[0][1] = Knight(1, 0, "b")
board[0][2] = Bishop(2, 0, "b")
board[0][3] = Queen(3, 0, "b")
board[0][4] = King(4, 0, "b")
board[0][5] = Bishop(5, 0, "b")
board[0][6] = Knight(6, 0, "b")
board[0][7] = Rook(7, 0, "b")

board[6][0] = Pawn(0, 6, "w")
board[6][1] = Pawn(1, 6, "w")
board[6][2] = Pawn(2, 6, "w")
board[6][3] = Pawn(3, 6, "w")
board[6][4] = Pawn(4, 6, "w")
board[6][5] = Pawn(5, 6, "w")
board[6][6] = Pawn(6, 6, "w")
board[6][7] = Pawn(7, 6, "w")

board[7][0] = Rook(0, 7, "w")
board[7][1] = Knight(1, 7, "w")
board[7][2] = Bishop(2, 7, "w")
board[7][3] = Queen(3, 7, "w")
board[7][4] = King(4, 7, "w")
board[7][5] = Bishop(5, 7, "w")
board[7][6] = Knight(6, 7, "w")
board[7][7] = Rook(7, 7, "w")

board[1][0] = Pawn(0, 1, "b")
board[1][1] = Pawn(1, 1, "b")
board[1][2] = Pawn(2, 1, "b")
board[1][3] = Pawn(3, 1, "b")
board[1][4] = Pawn(4, 1, "b")
board[1][5] = Pawn(5, 1, "b")
board[1][6] = Pawn(6, 1, "b")
board[1][7] = Pawn(7, 1, "b")


def draw():
    for i in range(8):
        for j in range(8):
            if board[i][j] != 0:
                board[i][j].draw(screen)


def click(pos):
    x = pos[0]
    y = pos[1]
    # calculating index of position clicked
    i = (x//(512//8))
    j = (y//(512//8))

    return [j, i]


def select(index):
    for i in range(8):
        for j in range(8):
            if board[i][j] != 0:
                board[i][j].selected = False

    selected = 0

    box = board[index[0]][index[1]]
    box.selected = True
    return box


def move(index):
    board[index[0]][index[1]] = board[selected.y][selected.x]
    board[selected.y][selected.x].x = index[1]
    board[selected.y][selected.x].y = index[0]
    board[selected.y][selected.x].selected = False


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            index = click(pos)
            # change
            if selected != 0:
                if [index[1], index[0]] in selected.valid_moves(board):
                    move(index)
                    selected = 0
                    turn = "b"

            if board[index[0]][index[1]] != 0:
                if board[index[0]][index[1]].team == turn:
                    selected = select(index)

    screen.fill("#18191A")

    screen.blit(board_img, board_rect)
    draw()

    clock.tick(60)
    pygame.display.update()
