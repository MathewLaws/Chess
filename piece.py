import this
import pygame
import os

w_pawn = pygame.image.load(os.path.join("img", "w_pawn.png"))
w_bishop = pygame.image.load(os.path.join("img", "w_bishop.png"))
w_knight = pygame.image.load(os.path.join("img", "w_knight.png"))
w_rook = pygame.image.load(os.path.join("img", "w_rook.png"))
w_queen = pygame.image.load(os.path.join("img", "w_queen.png"))
w_king = pygame.image.load(os.path.join("img", "w_king.png"))

b_pawn = pygame.image.load(os.path.join("img", "b_pawn.png"))
b_bishop = pygame.image.load(os.path.join("img", "b_bishop.png"))
b_knight = pygame.image.load(os.path.join("img", "b_knight.png"))
b_rook = pygame.image.load(os.path.join("img", "b_rook.png"))
b_queen = pygame.image.load(os.path.join("img", "b_queen.png"))
b_king = pygame.image.load(os.path.join("img", "b_king.png"))

W = [w_pawn, w_bishop, w_knight, w_rook, w_queen, w_king]
B = [b_pawn, b_bishop, b_knight, b_rook, b_queen, b_king]


class Piece:
    def __init__(self, x, y, team):
        self.x = x
        self.y = y
        self.team = team
        self.selected = False

    def draw(self, board, screen):
        x_pos = self.x * (512/8)
        y_pos = self.y * (512/8)

        if self.team:
            g = W[self.img]
        else:
            g = B[self.img]

        screen.blit(g, (x_pos, y_pos))

        if self.selected:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(
                (self.x*(512/8)), (self.y*(512/8)), (512/8), (512/8)), 2)
            for i in self.valid_moves(board):
                pygame.draw.ellipse(screen, (255, 0, 0), pygame.Rect(
                    ((i[0]*(512/8))+(512/8)/2-10), ((i[1]*(512/8))+(512/8)/2-10), 20, 20))

    def isSelected(self):
        return self.selected


class Pawn(Piece):
    img = 0

    def valid_moves(self, board):
        moves = []

        if self.team:
            moves.append([self.x, (self.y - 1)])
            moves.append([self.x, (self.y - 2)])
            if self.x-1 >= 0:
                if board[self.y-1][self.x-1] != 0:
                    if board[self.y-1][self.x-1].team != self.team:
                        moves.append([self.x-1, self.y-1])
            if self.x+1 <= 7:
                if board[self.y-1][self.x+1] != 0:
                    if board[self.y-1][self.x+1].team != self.team:
                        moves.append([self.x+1, self.y-1])
        else:
            moves.append([self.x, (self.y + 1)])
            moves.append([self.x, (self.y + 2)])
            if self.x-1 >= 0:
                if board[self.y+1][self.x-1] != 0:
                    if board[self.y+1][self.x-1].team != self.team:
                        moves.append([self.x-1, self.y+1])
            if self.x+1 <= 7:
                if board[self.y+1][self.x+1] != 0:
                    if board[self.y+1][self.x+1].team != self.team:
                        moves.append([self.x+1, self.y+1])

        return moves


class Bishop(Piece):
    img = 1

    def valid_moves(self, board):
        moves = []

        for i in range(1, 8):
            if self.y-1*i >= 0 and self.x-1*i >= 0:
                if board[self.y-1*i][self.x-1*i] != 0:
                    if board[self.y-1*i][self.x-1*i].team != self.team:
                        moves.append([self.x-1*i, self.y-1*i])
                else:
                    moves.append([self.x-1*i, self.y-1*i])
            if self.y-1*i >= 0 and self.x+1*i <= 7:
                if board[self.y-1*i][self.x+1*i] != 0:
                    if board[self.y-1*i][self.x+1*i].team != self.team:
                        moves.append([self.x+1*i, self.y-1*i])
                else:
                    moves.append([self.x+1*i, self.y-1*i])
            if self.y+1*i <= 7 and self.x+1*i <= 7:
                if board[self.y+1*i][self.x+1*i] != 0:
                    if board[self.y+1*i][self.x+1*i].team != self.team:
                        moves.append([self.x+1*i, self.y+1*i])
                else:
                    moves.append([self.x+1*i, self.y+1*i])
            if self.y+1*i <= 7 and self.x-1*i >= 0:
                if board[self.y+1*i][self.x-1*i] != 0:
                    if board[self.y+1*i][self.x-1*i].team != self.team:
                        moves.append([self.x-1*i, self.y+1*i])
                else:
                    moves.append([self.x-1*i, self.y+1*i])

        return moves


class Knight(Piece):
    img = 2

    def valid_moves(self, board):
        moves = []
        X = [2, 1, -1, -2, -2, -1, 1, 2]
        Y = [1, 2, 2, 1, -1, -2, -2, -1]

        for i in range(len(X)):
            if self.x+X[i] >= 0 and self.x+X[i] <= 7 and self.y+Y[i] >= 0 and self.y+Y[i] <= 7:
                if board[self.y+Y[i]][self.x+X[i]] != 0:
                    if board[self.y+Y[i]][self.x+X[i]].team != self.team:
                        moves.append([self.x+X[i], self.y+Y[i]])
                else:
                    moves.append([self.x+X[i], self.y+Y[i]])

        return moves


class Rook(Piece):
    img = 3

    def valid_moves(self, board):
        moves = []
        for i in range(7):
            if i != self.y:
                if board[i][self.x] != 0:
                    if board[i][self.x].team != self.team:
                        moves.append([self.x, i])
                else:
                    moves.append([self.x, i])
        for i in range(7):
            if i != self.x:
                if board[self.y][i] != 0:
                    if board[self.y][i].team != self.team:
                        moves.append([i, self.y])
                else:
                    moves.append([i, self.y])
        return moves


class Queen(Piece):
    img = 4

    def valid_moves(self, board):
        moves = []
        # up/down
        for i in range(7):
            if i != self.y:
                if board[i][self.x] != 0:
                    if board[i][self.x].team != self.team:
                        moves.append([self.x, i])
                else:
                    moves.append([self.x, i])
        for i in range(7):
            if i != self.x:
                if board[self.y][i] != 0:
                    if board[self.y][i].team != self.team:
                        moves.append([i, self.y])
                else:
                    moves.append([i, self.y])
        # diagnals

        for i in range(1, 8):
            if self.y-1*i >= 0 and self.x-1*i >= 0:
                if board[self.y-1*i][self.x-1*i] != 0:
                    if board[self.y-1*i][self.x-1*i].team != self.team:
                        moves.append([self.x-1*i, self.y-1*i])
                else:
                    moves.append([self.x-1*i, self.y-1*i])
            if self.y-1*i >= 0 and self.x+1*i <= 7:
                if board[self.y-1*i][self.x+1*i] != 0:
                    if board[self.y-1*i][self.x+1*i].team != self.team:
                        moves.append([self.x+1*i, self.y-1*i])
                else:
                    moves.append([self.x+1*i, self.y-1*i])
            if self.y+1*i <= 7 and self.x+1*i <= 7:
                if board[self.y+1*i][self.x+1*i] != 0:
                    if board[self.y+1*i][self.x+1*i].team != self.team:
                        moves.append([self.x+1*i, self.y+1*i])
                else:
                    moves.append([self.x+1*i, self.y+1*i])
            if self.y+1*i <= 7 and self.x-1*i >= 0:
                if board[self.y+1*i][self.x-1*i] != 0:
                    if board[self.y+1*i][self.x-1*i].team != self.team:
                        moves.append([self.x-1*i, self.y+1*i])
                else:
                    moves.append([self.x-1*i, self.y+1*i])

        return moves


class King(Piece):
    img = 5

    def valid_moves(self, board):
        moves = []
        for i in range(-1, 1):
            for j in range(-1, 1):
                if i == 0 and j == 0:
                    pass
                moves.append([self.x+j, self.y+i])
        return moves
