import pygame
from checkers.game import Game
from checkers.constants import *
from minimax.algorithm import minimax


FPS = 60
WIN = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption("Checkers By Anique")

def get_row_col_from_mouse_position(pos):
    x , y = pos
    row = y // SQUARE_SIZE 
    col = x // SQUARE_SIZE 

    return row , col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    
    
    while run:

        clock.tick(FPS)

        if game.turn == WHITE:
            value , new_board = minimax(game.get_board() , 2 , WHITE , game)
            # we are not going to use this value here

            # Here the depth I am giving is 2
            # The higher the depth is , the better the ai is going to be 
            # But thats going to slow the program
            # So , in this case , 2 works out 
            game.ai_move(new_board)

        if game.winner() != None:
            print(game.winner(),"wins!")
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row , col = get_row_col_from_mouse_position(pos)
                game.select(row,col)
        game.update()
    pygame.quit()

# Main Function
main()

