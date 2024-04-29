import numpy as np
import random
from colorama import Fore, Style


import sys
import math

from Player import Player 



ROWS = 5
COLUMNS = 6

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

class ConnectFourTwist:
	
    def __init__(self):
        self.__player1 = Player(colour="red", number=1, name="Player")
        self.__player2 = Player(colour="yellow", number=2, name="AI")
        self.__board = self.init_board()
        self.__game_over = False

    def init_board(self):
        board = np.zeros((ROWS,COLUMNS))
        return board

    def drop_piece(self, board, row, col, piece):
        board[row][col] = piece

    def is_valid_location(self, board, col):
        return board[ROWS-1][col] == 0

    def get_next_open_row(self, board, col):
        for r in range(ROWS):
            if board[r][col] == 0:
                return r

    def print_board(self, board):
        print(f"{Style.RESET_ALL}=====================")
        for row in board:
            row_output = ""
            for token in row:
                if token == 0:
                    row_output += str(f"{Style.RESET_ALL}{0}")
                if token == 1:
                    row_output += str(f"{self.__player1.get_text_colour()}{self.__player1.get_number()}")
                if token == 2:
                    row_output += str(f"{self.__player2.get_text_colour()}{self.__player2.get_number()}")

            print(row_output)
        print(f"{Style.RESET_ALL}=====================")

    def winning_move(self, board, player_number):
        # Horizontal Check - Columns are cyclical (hence mod operation)
            for col in range(COLUMNS):
                for row in range(ROWS):
                    if board[row][col] != 0: # Skip if first token is empty
                        t1 = board[row][col]
                        t2 = board[row][(col + 1)%(COLUMNS - 1)]
                        t3 = board[row][(col + 2)%(COLUMNS - 1)]
                        t4 = board[row][(col + 3)%(COLUMNS - 1)]
                        
                        if t1 == player_number and t2 == player_number and t3 == player_number and t4 == player_number:
                            return True 
                        
            # Vertical Check
            for col in range(COLUMNS):
                for row in range(ROWS - 3):
                    
                    if board[row][col] != 0: # Skip if first token is empty
                        t1 = board[row][col]
                        t2 = board[row + 1][col]
                        t3 = board[row + 2][col]
                        t4 = board[row + 3][col]

                        if t1 == player_number and t2 == player_number and t3 == player_number and t4 == player_number:
                            return True 
                        
            # Diagonal Left Right Up Check - Also Cyclical
            for col in range(COLUMNS):
                for row in range(ROWS - 3):
                    if board[row][col] != 0: # Skip if first token is empty
                        t1 = board[row][col]
                        t2 = board[row + 1][(col + 1)%(COLUMNS - 1)]
                        t3 = board[row + 2][(col + 2)%(COLUMNS - 1)]
                        t4 = board[row + 3][(col + 3)%(COLUMNS - 1)]
                        
                        if t1 == player_number and t2 == player_number and t3 == player_number and t4 == player_number:
                            return True 
                                            
            # Diagonal Left Right Up Check - Also Cyclical
            for col in range(COLUMNS):
                for row in range(ROWS - 3):
                    if board[row][col] != 0: # Skip if first token is empty
                        t1 = board[row][col]
                        t2 = board[row - 1][(col + 1)%(COLUMNS - 1)]
                        t3 = board[row - 2][(col + 2)%(COLUMNS - 1)]
                        t4 = board[row - 3][(col + 3)%(COLUMNS - 1)]
                        
                        if t1 == player_number and t2 == player_number and t3 == player_number and t4 == player_number:
                            return True 
                        
            return False           

    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = PLAYER_PIECE
        if piece == PLAYER_PIECE:
            opp_piece = AI_PIECE

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
            score -= 4

        return score

    def score_position(self, board, piece):
        score = 0

        ## Score center column
        center_array = [int(i) for i in list(board[:, COLUMNS//2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        ## Score Horizontal
        for r in range(ROWS):
            row_array = [int(i) for i in list(board[r,:])]
            print(row_array)
            for c in range(COLUMNS-3):
                window = row_array[c:c+WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        ## Score Vertical
        for c in range(COLUMNS):
            col_array = [int(i) for i in list(board[:,c])]
            for r in range(ROWS-3):
                window = col_array[r:r+WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        ## Score posiive sloped diagonal
        for r in range(ROWS-3):
            for c in range(COLUMNS-3):
                window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        for r in range(ROWS-3):
            for c in range(COLUMNS-3):
                window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        return score

    def is_terminal_node(self, board):
        return self.winning_move(board, PLAYER_PIECE) or self.winning_move(board, AI_PIECE) or len(self.get_valid_locations(board)) == 0

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.winning_move(board, AI_PIECE):
                    return (None, 100000000000000)
                elif self.winning_move(board, PLAYER_PIECE):
                    return (None, -10000000000000)
                else: # Game is over, no more valid moves
                    return (None, 0)
            else: # Depth is zero
                return (None, self.score_position(board, AI_PIECE))
        if maximizingPlayer:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                b_copy = board.copy()
                self.drop_piece(b_copy, row, col, AI_PIECE)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else: # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                b_copy = board.copy()
                self.drop_piece(b_copy, row, col, PLAYER_PIECE)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def get_valid_locations(self, board):
        valid_locations = []
        for col in range(COLUMNS):
            if self.is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations

    def pick_best_move(self, board, piece):

        valid_locations = self.get_valid_locations(board)
        best_score = -10000
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = self.get_next_open_row(board, col)
            temp_board = board.copy()
            self.drop_piece(temp_board, row, col, piece)
            score = self.score_position(temp_board, piece)
            if score > best_score:
                best_score = score
                best_col = col

        return best_col
    
    def get_game_over(self):
        return self.__game_over
    
    def set_game_over(self, gamestate):
        self.__game_over = gamestate

    def get_board(self):
        return self.__board

    

game = ConnectFourTwist()

turn = random.randint(PLAYER, AI)

board = game.get_board()

while not game.get_game_over():

    # Ask for Player 1 Input
    if turn == PLAYER:
        
        col = int(input("COL:"))

        if game.is_valid_location(board, col):
            row = game.get_next_open_row(board, col)
            game.drop_piece(board, row, col, PLAYER_PIECE)

            if game.winning_move(board, PLAYER_PIECE):
                #game_over = True
                game.set_game_over(True)

            turn += 1
            turn = turn % 2

            game.print_board(board)
           
	# # Ask for Player 2 Input
    if turn == AI and not game.get_game_over():				

		#col = random.randint(0, COLUMNS-1)
		#col = pick_best_move(board, AI_PIECE)
        col, minimax_score = game.minimax(board, 5, -math.inf, math.inf, True)

        if game.is_valid_location(board, col):
			#pygame.time.wait(500)
            row = game.get_next_open_row(board, col)
            game.drop_piece(board, row, col, AI_PIECE)

            if game.winning_move(board, AI_PIECE):
                game_over = True

            game.print_board(board)
            

            turn += 1
            turn = turn % 2
