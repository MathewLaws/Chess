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

    def draw(self, screen):
        x_pos = self.x * (512/8)
        y_pos = self.y * (512/8)

        # draw this
        if self.team == "w":
            g = W[self.img]
        else:
            g = B[self.img]

        screen.blit(g, (x_pos, y_pos))

        if self.selected:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(
                (self.x*(512/8)), (self.y*(512/8)), (512/8), (512/8)), 2)

    def isSelected(self):
        return self.selected


class Pawn(Piece):
    img = 0

    def valid_moves(self, board):
        moves = []

        if self.team == "w":
            moves.append([self.x, (self.y - 1)])
            moves.append([self.x, (self.y - 2)])

        return moves


class Bishop(Piece):
    img = 1

    def valid_moves(self, board):
        pass


class Knight(Piece):
    img = 2

    def valid_moves(self, board):
        pass


class Rook(Piece):
    img = 3

    def valid_moves(self, board):
        pass


class Queen(Piece):
    img = 4

    def valid_moves(self, board):
        pass


class King(Piece):
    img = 5

    def valid_moves(self, board):
        pass
