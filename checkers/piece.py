from .constants import CROWN, RED , SQUARE_SIZE , GREY
import pygame

class Piece:
    OUTLINE = 2
    PADDING = 18

    def __init__(self,row,col,color):
        # So we should have info about the row , column and color of each piece
        self.row = row
        self.col = col
        self.color = color

        # Initially, the piece is not a King
        self.king = False

        # Position

        self.x = 0  # Horizontal
        self.y = 0  # Vertical
        self.calc_pos()

    def calc_pos(self):
        # This method is going to calculate the position
        # of the pieces

        # We want to make the circular pieces from the 
        # very center of the squares

        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True

    def draw(self,win):
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win,GREY,(self.x,self.y),radius + self.OUTLINE)
        pygame.draw.circle(win,self.color,(self.x,self.y),radius)

        if self.king:
            win.blit( CROWN,(
                self.x - CROWN.get_width() // 2 ,
                self.y -  CROWN.get_height() // 2
                )
            )
    def move(self,row,col):
        self.row = row
        self.col = col
        self.calc_pos()


    def __repr__(self):
        return str(self.color)