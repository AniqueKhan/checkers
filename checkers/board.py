from checkers.piece import Piece
from .constants import *
import pygame
class Board:
    def __init__(self):
        # self.board is just going to be 2D lists
        self.board = []

        # [[
        # Piece() , 0 , Piece()
        # 0 , 0 , Piece()
        # ]]

        # How many reds and whites are left on the board
        # In the starting , there are 12 pieces of both the colors
        self.red_left = self.white_left = 12


        # Kings on the board 
        # Starting from 0
        self.red_kings = self.white_kings = 0

        self.create_board()

    def draw_squares(self,win):
        # Filling the whole window with black
        # Then making red cubes on it
        win.fill(BLACK)

        for row in range(ROWS):
            for col in range(row % 2 , COLS , 2):
                pygame.draw.rect(win , RED , (
                    row * SQUARE_SIZE ,
                    col * SQUARE_SIZE ,
                    SQUARE_SIZE , 
                    SQUARE_SIZE
                    ))

    # The better this function , the better the ai is going to be
    def evaluate(self):
        return self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)
    
    def get_all_pieces(self,color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self,piece,row,col):
        self.board[piece.row][piece.col] , self.board[row][col] = self.board[row][col] , self.board[piece.row][piece.col]
        piece.move(row,col)

        # Making the piece a king 

        if row == ROWS -1   or row == 0:
            piece.make_king()
    
        # Now some can argue that initially the pieces are in the 
        # first and the last rows , so wont those pieces are 
        # going to be king

        # Well , the answer is no , because you have to move in the
        # first or last row in order to become a king

        # An ordinary piece is not allowed to move backwards
        # So that is how this logic works

            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    def get_piece(self,row,col):
        return self.board[row][col]

    def create_board(self):
        for row in range (ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row,col,WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row,col,RED))
                    else:
                        # In the rows where there are no pieces 
                        # We are appending zeros in those squares
                        # So we know where the pieces are and what
                        # squares are empty represented by zeros
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self,win):
        self.draw_squares(win)

        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    
    def remove(self,pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -=1
                else:
                    self.white_left-=1

    def winner(self):
        if self.red_left <= 0:
            return "WHITE"
        elif self.white_left <=0:
            return "RED"
        return None


    def get_valid_moves(self,piece):
        moves = {}
        left = piece.col - 1 
        right = piece.col + 1 
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row-1,max(row-3,-1),-1,piece.color,left))
            moves.update(self._traverse_right(row-1,max(row-3,-1),-1,piece.color,right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row+1,min(row+3,ROWS),1,piece.color,left))
            moves.update(self._traverse_right(row+1,min(row+3,ROWS),1,piece.color,right))
        return moves
            
    def _traverse_left(self,start,stop,step,color,left,skipped=[]):
        moves = {}
        last = []
        for r in range(start,stop,step):
            if left < 0:
                break
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,left)]=last+skipped
                else:
                    moves[(r,left)] = last
                if last:
                    if step == -1:
                        row = max(r-3,0)
                    else:
                        row = min(r+3,ROWS)
                    moves.update(self._traverse_left(r+step,row,step,color,left-1,skipped=last))
                    moves.update(self._traverse_right(r+step,row,step,color,left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last=[current]
            left -=1
        return moves


    def _traverse_right(self,start,stop,step,color,right,skipped=[]):
        moves = {}
        last = []
        for r in range(start,stop,step):
            if right >=COLS:
                break
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)]=last+skipped
                else:
                    moves[(r,right)] = last
                if last:
                    if step == -1:
                        row = max(r-3,0)
                    else:
                        row = min(r+3,ROWS)
                    moves.update(self._traverse_left(r+step,row,step,color,right-1,skipped=last))
                    moves.update(self._traverse_right(r+step,row,step,color,right-1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last=[current]
            right +=1
        return moves



    
