import pygame
import os
import copy

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

legal_moves = {
    "Pawn": [],
    "Rook": [],
    "Knight": [],
    "Bishop": [],
    "Queen": [],
    "King": []
}


def move(index, board, selected):
    if isinstance(board[selected.y][selected.x], King):

        if index[1] == (selected.x - 2):
            if board[selected.y][selected.x].team:
                board[7][0] = 0
                board[index[0]][index[1]+1] = Rook(
                    index[1]+1, index[0], board[selected.y][selected.x].team)
            else:
                board[0][0] = 0
                board[index[0]][index[1]+1] = Rook(
                    index[1]+1, index[0], board[selected.y][selected.x].team)
        if index[1] == (selected.x + 2):
            if board[selected.y][selected.x].team:
                board[7][7] = 0
                board[index[0]][index[1]-1] = Rook(
                    index[1]-1, index[0], board[selected.y][selected.x].team)
            else:
                board[0][7] = 0
                board[index[0]][index[1]-1] = Rook(
                    index[1]-1, index[0], board[selected.y][selected.x].team)

    board[index[0]][index[1]] = board[selected.y][selected.x]
    board[selected.y][selected.x] = 0
    board[index[0]][index[1]].x = index[1]
    board[index[0]][index[1]].y = index[0]
    board[index[0]][index[1]].selected = False
    board[index[0]][index[1]].first = False

    if isinstance(board[index[0]][index[1]], Pawn) and (board[index[0]][index[1]].y == 7 or board[index[0]][index[1]].y == 0):
        board[index[0]][index[1]] = Queen(
            board[index[0]][index[1]].x, board[index[0]][index[1]].y, board[index[0]][index[1]].team)

    return board


def check_mate():
    mate = True
    for piece in legal_moves:
        if len(legal_moves[piece]) > 0:
            mate = False

    if mate:
        return True
    return False


def generate_legal(team, board):
    global legal_moves
    legal_moves = {
        "Pawn": [],
        "Rook": [],
        "Knight": [],
        "Bishop": [],
        "Queen": [],
        "King": []
    }
    temp_board = board

    for i in range(8):
        for j in range(8):
            temp_board = board
            if temp_board[i][j] != 0:
                if temp_board[i][j].team == team:
                    print(temp_board[i][j], temp_board[i]
                          [j].valid_moves(temp_board, True))
                    for k in temp_board[i][j].valid_moves(temp_board, True):
                        temp_board = copy.deepcopy(board)
                        temp_board = move(
                            [k[1], k[0]], temp_board, temp_board[i][j])
                        if not check(team, temp_board):
                            legal_moves[board[i][j].name].append(k)


def check(team, board):
    opponent_moves = []
    king = None
    for i in range(8):
        for j in range(8):
            if board[i][j] != 0:
                if board[i][j].team == team and isinstance(board[i][j], King):
                    king = board[i][j]

    for i in range(8):
        for j in range(8):
            if board[i][j] != 0:
                if board[i][j].team != team:
                    opponent_moves += board[i][j].valid_moves(board, True)

    if [king.x, king.y] in opponent_moves:
        return True
    return False


class Piece:
    def __init__(self, x, y, team):
        self.x = x
        self.y = y
        self.team = team
        self.selected = False
        self.first = True

    def draw(self, board, screen):
        x_pos = self.x * (512/8)
        y_pos = self.y * (512/8)

        if self.team:
            g = W[self.img]
        else:
            g = B[self.img]

        if self.selected:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(
                (self.x*(512/8)), (self.y*(512/8)), (512/8), (512/8)), 2)
            for i in self.valid_moves(board):
                pygame.draw.ellipse(screen, (255, 0, 0), pygame.Rect(
                    ((i[0]*(512/8))+(512/8)/2-5), ((i[1]*(512/8))+(512/8)/2-5), 10, 10))

        screen.blit(g, (x_pos, y_pos))

    def isSelected(self):
        return self.selected


class Pawn(Piece):
    img = 0

    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.name = "Pawn"

    def valid_moves(self, board, validation=False):
        moves = []

        if self.team:
            if board[self.y-1][self.x] == 0:
                moves.append([self.x, (self.y - 1)])
            if (self.first):
                if board[self.y-2][self.x] == 0:
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
            if board[self.y+1][self.x] == 0:
                moves.append([self.x, (self.y + 1)])
            if (self.first):
                if board[self.y+2][self.x] == 0:
                    moves.append([self.x, (self.y + 2)])
            if self.x-1 >= 0:
                if board[self.y+1][self.x-1] != 0:
                    if board[self.y+1][self.x-1].team != self.team:
                        moves.append([self.x-1, self.y+1])
            if self.x+1 <= 7:
                if board[self.y+1][self.x+1] != 0:
                    if board[self.y+1][self.x+1].team != self.team:
                        moves.append([self.x+1, self.y+1])

        valid_moves = []
        if not validation:
            for i in moves:
                if i in legal_moves[self.name]:
                    valid_moves.append(i)
            return valid_moves

        return moves


class Bishop(Piece):
    img = 1

    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.name = "Bishop"

    def valid_moves(self, board, validation=False):
        moves = []

        for i in range(1, 8):
            if self.y-1*i >= 0 and self.x-1*i >= 0:
                if board[self.y-1*i][self.x-1*i] != 0:
                    if board[self.y-1*i][self.x-1*i].team != self.team:
                        moves.append([self.x-1*i, self.y-1*i])
                    break
                else:
                    moves.append([self.x-1*i, self.y-1*i])
        for i in range(1, 8):
            if self.y-1*i >= 0 and self.x+1*i <= 7:
                if board[self.y-1*i][self.x+1*i] != 0:
                    if board[self.y-1*i][self.x+1*i].team != self.team:
                        moves.append([self.x+1*i, self.y-1*i])
                    break
                else:
                    moves.append([self.x+1*i, self.y-1*i])
        for i in range(1, 8):
            if self.y+1*i <= 7 and self.x+1*i <= 7:
                if board[self.y+1*i][self.x+1*i] != 0:
                    if board[self.y+1*i][self.x+1*i].team != self.team:
                        moves.append([self.x+1*i, self.y+1*i])
                    break
                else:
                    moves.append([self.x+1*i, self.y+1*i])
        for i in range(1, 8):
            if self.y+1*i <= 7 and self.x-1*i >= 0:
                if board[self.y+1*i][self.x-1*i] != 0:
                    if board[self.y+1*i][self.x-1*i].team != self.team:
                        moves.append([self.x-1*i, self.y+1*i])
                    break
                else:
                    moves.append([self.x-1*i, self.y+1*i])
        valid_moves = []
        if not validation:
            for i in moves:
                if i in legal_moves[self.name]:
                    valid_moves.append(i)
            return valid_moves

        return moves


class Knight(Piece):
    img = 2

    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.name = "Knight"

    def valid_moves(self, board, validation=False):
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
        valid_moves = []
        if not validation:
            for i in moves:
                if i in legal_moves[self.name]:
                    valid_moves.append(i)

        return valid_moves


class Rook(Piece):
    img = 3

    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.name = "Rook"

    def valid_moves(self, board, validation=False):
        moves = []
        for i in range(self.y, 8):
            if board[i][self.x] != self:
                if board[i][self.x] != 0:
                    if board[i][self.x].team != self.team:
                        moves.append([self.x, i])
                    break
                else:
                    moves.append([self.x, i])
        for i in range(self.y, -1, -1):
            if board[i][self.x] != self:
                if board[i][self.x] != 0:
                    if board[i][self.x].team != self.team:
                        moves.append([self.x, i])
                    break
                else:
                    moves.append([self.x, i])
        for i in range(self.x, 8):
            if board[self.y][i] != self:
                if board[self.y][i] != 0:
                    if board[self.y][i].team != self.team:
                        moves.append([i, self.y])
                    break
                else:
                    moves.append([i, self.y])
        for i in range(self.x, -1, -1):
            if board[self.y][i] != self:
                if board[self.y][i] != 0:
                    if board[self.y][i].team != self.team:
                        moves.append([i, self.y])
                    break
                else:
                    moves.append([i, self.y])
        valid_moves = []
        if not validation:
            for i in moves:
                if i in legal_moves[self.name]:
                    valid_moves.append(i)
            return valid_moves

        return moves


class Queen(Piece):
    img = 4

    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.name = "Queen"

    def valid_moves(self, board, validation=False):
        moves = []
        # up/down
        for i in range(self.y, 8):
            if board[i][self.x] != self:
                if board[i][self.x] != 0:
                    if board[i][self.x].team != self.team:
                        moves.append([self.x, i])
                    break
                else:
                    moves.append([self.x, i])
        for i in range(self.y, -1, -1):
            if board[i][self.x] != self:
                if board[i][self.x] != 0:
                    if board[i][self.x].team != self.team:
                        moves.append([self.x, i])
                    break
                else:
                    moves.append([self.x, i])

        for i in range(self.x, 8):
            if board[self.y][i] != self:
                if board[self.y][i] != 0:
                    if board[self.y][i].team != self.team:
                        moves.append([i, self.y])
                    break
                else:
                    moves.append([i, self.y])
        for i in range(self.x, -1, -1):
            if board[self.y][i] != self:
                if board[self.y][i] != 0:
                    if board[self.y][i].team != self.team:
                        moves.append([i, self.y])
                    break
                else:
                    moves.append([i, self.y])
        # diagnals

        for i in range(1, 8):
            if self.y-1*i >= 0 and self.x-1*i >= 0:
                if board[self.y-1*i][self.x-1*i] != 0:
                    if board[self.y-1*i][self.x-1*i].team != self.team:
                        moves.append([self.x-1*i, self.y-1*i])
                    break
                else:
                    moves.append([self.x-1*i, self.y-1*i])
        for i in range(1, 8):
            if self.y-1*i >= 0 and self.x+1*i <= 7:
                if board[self.y-1*i][self.x+1*i] != 0:
                    if board[self.y-1*i][self.x+1*i].team != self.team:
                        moves.append([self.x+1*i, self.y-1*i])
                    break
                else:
                    moves.append([self.x+1*i, self.y-1*i])
        for i in range(1, 8):
            if self.y+1*i <= 7 and self.x+1*i <= 7:
                if board[self.y+1*i][self.x+1*i] != 0:
                    if board[self.y+1*i][self.x+1*i].team != self.team:
                        moves.append([self.x+1*i, self.y+1*i])
                    break
                else:
                    moves.append([self.x+1*i, self.y+1*i])
        for i in range(1, 8):
            if self.y+1*i <= 7 and self.x-1*i >= 0:
                if board[self.y+1*i][self.x-1*i] != 0:
                    if board[self.y+1*i][self.x-1*i].team != self.team:
                        moves.append([self.x-1*i, self.y+1*i])
                    break
                else:
                    moves.append([self.x-1*i, self.y+1*i])
        valid_moves = []
        if not validation:
            for i in moves:
                if i in legal_moves[self.name]:
                    valid_moves.append(i)
            return valid_moves

        return moves


class King(Piece):
    img = 5

    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.name = "King"

    def valid_moves(self, board, validation=False):
        moves = []
        opponent_moves = []

        for i in range(0, 7):
            for j in range(0, 7):
                if board[i][j] != 0:
                    if board[i][j].team != self.team and not isinstance(board[i][j], King):
                        if isinstance(board[i][j], Pawn):
                            if board[i][j].team:
                                opponent_moves.append([j+1, i-1])
                                opponent_moves.append([j-1, i-1])
                            else:
                                opponent_moves.append([j+1, i+1])
                                opponent_moves.append([j-1, i+1])
                            continue

                        opponent_moves += board[i][j].valid_moves(board)

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    pass
                if self.x+j <= 7 and self.x+j >= 0 and self.y+i <= 7 and self.y+i >= 0:
                    if board[self.y+i][self.x+j] != 0:
                        if board[self.y+i][self.x+j].team != self.team and [self.x+j, self.y+i] not in opponent_moves:
                            moves.append([self.x+j, self.y+i])
                    else:
                        if [self.x+j, self.y+i] not in opponent_moves:
                            moves.append([self.x+j, self.y+i])

        if self.team:
            if board[7][0] != 0:
                if isinstance(board[7][0], Rook) and board[7][1] == 0 and board[7][2] == 0 and board[7][3] == 0:
                    moves.append([self.x-2, self.y])
            if board[7][7] != 0:
                if isinstance(board[7][7], Rook) and board[7][6] == 0 and board[7][5] == 0:
                    moves.append([self.x+2, self.y])
        else:
            if board[0][7] != 0:
                if isinstance(board[0][7], Rook) and board[0][6] == 0 and board[0][5] == 0:
                    moves.append([self.x+2, self.y])
            if board[0][0] != 0:
                if isinstance(board[0][0], Rook) and board[0][1] == 0 and board[0][2] == 0 and board[0][3] == 0:
                    moves.append([self.x-2, self.y])
        valid_moves = []
        if not validation:
            for i in moves:
                if i in legal_moves[self.name]:
                    valid_moves.append(i)
            return valid_moves

        return moves
