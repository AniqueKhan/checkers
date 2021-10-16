from copy import deepcopy
import pygame 
from checkers.constants import *


def minimax(position,depth,max_player,game):

    # position is telling us the position of the ai_move
    # position is a board object actually

    # depth defines the depth of the decision tree , recursive call with decrement 

    # max_player is a boolean value , which tells either we are minimizing or 
    # maximizing the value

    # game is the game object

    if depth == 0 or position.winner() != None:
        return position.evaluate() , position
    
    if max_player:
        max_evaluation = float("-inf") 
        # initially defining it as -ve infinity so everything is higher than this

        best_move = None

        for move in get_all_moves(position,WHITE,game):
            evaluation = minimax(move,depth-1,False,game)[0]
            max_evaluation = max(max_evaluation,evaluation)
            if max_evaluation == evaluation:
                best_move = move

        return max_evaluation,best_move
    else:
        min_evaluation = float("inf") 
        # initially defining it as +ve infinity so everything is lower than this

        best_move = None

        for move in get_all_moves(position,RED,game):
            evaluation = minimax(move,depth-1,True,game)[0]
            min_evaluation = min(min_evaluation,evaluation)
            if min_evaluation == evaluation:
                best_move = move
                
        return min_evaluation,best_move

def simulate_move(piece,move,board,game,skip):
    board.move(piece,move[0],move[1]) # spilitting it up bc it is a tuple
    if skip:
        board.remove(skip)
    return board 

def get_all_moves(board , color , game):
    moves =[]

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)

        for move , skip in valid_moves.items():
            # draw_moves(game,board,piece)
            temporary_board = deepcopy(board)
            # Here we are making a temporary board where we are trying all the possible moves
            # Then picking the best move as per highest or lowest score
            # We dont want to change the original board when trying stuff

            temporary_piece = temporary_board.get_piece(piece.row,piece.col)

            new_board = simulate_move(temporary_piece,move,temporary_board,game,skip)
            moves.append(new_board)

    return moves

def draw_moves(game , board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win,GREEN,(piece.x,piece.y),50,5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    pygame.time.delay(100) # 0.1 seconds