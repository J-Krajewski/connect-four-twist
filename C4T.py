import numpy as np
import random
from colorama import Fore, Style
import csv


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
	
    def __init__(self, starter):
        self.__player1 = Player(colour="red", number=1, name="Player")
        self.__player2 = Player(colour="yellow", number=2, name="AI")
        self.__board = self.init_board()
        self.__game_over = False
        self.__transposition_table = {}
        self.__winner = None
        self.__total_turns = 0
        self.__starter = starter

    def init_board(self):
        board = np.zeros((ROWS,COLUMNS), dtype=int)
        #board = [[0 * COLUMNS] for x in range(ROWS)]
        return board

    def drop_piece(self, board, row, col, piece):
        board[row][col] = piece
        return board 

    def is_valid_location(self, board, col):
        #print(board[ROWS-1][col])
        drop_col = (board[ROWS-1][col] == 0)
        #print(f"col {col} - {drop_col} - {board[ROWS-1][col]}")

        return drop_col

    def get_next_open_row(self, board, col):
        for r in range(ROWS):
            if board[r][col] == 0:
                return r
            
    def find_occupied_rows(self, board):
        occupied_rows = []

        for row in range(ROWS):
            empty_row = [0 for _ in range(0, COLUMNS)]
            if any(board[row][col] != empty_row[col] for col in range(COLUMNS)):
                occupied_rows.append(row)

        #print(f"Occupied Rows {occupied_rows}")    
        return occupied_rows
    
    def apply_gravity(self, board):
        
        for col in range(COLUMNS):
            for row in range(ROWS):
                if board[row][col] == 0:
                    for r in range(row + 1, ROWS):
                        if board[r][col] != 0:
                            board[row][col], board[r][col] = board[r][col], board[row][col]
                            break

            
    def rotate_board(self, row, direction, board, occupied_rows):

        #if row not in occupied_rows:
        #    print(f"There is no token on row {row}")
        #    return board

        if direction == "right":
            board[row] = np.roll(board[row],+1)
            self.apply_gravity(board)
            
            return board
        elif direction == "left":
            board[row] = np.roll(board[row],-1)
            self.apply_gravity(board)

            return board
 
        elif direction == "no direction":
            return board
        else:
            print(f"{direction} is not a direction option, rotation not applied")
            return board

    def print_board(self, board):
        rev_board = board[::-1] # Reverse just for printing 
        print(f"{Style.RESET_ALL}======")
        for row in rev_board:
            row_output = ""
            for token in row:
                if token == 0:
                    row_output += str(f"{Style.RESET_ALL}{0}")
                if token == 1:
                    row_output += str(f"{self.__player1.get_text_colour()}{self.__player1.get_number()}")
                if token == 2:
                    row_output += str(f"{self.__player2.get_text_colour()}{self.__player2.get_number()}")

            print(row_output)
        print(f"{Style.RESET_ALL}======")

    def winning_move(self, board, piece):
        # Check horizontal locations for win
        for c in range(COLUMNS-3):
            for r in range(ROWS):
                if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(COLUMNS):
            for r in range(ROWS-3):
                if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(COLUMNS-3):
            for r in range(ROWS-3):
                if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(COLUMNS-3):
            for r in range(3, ROWS):
                if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                    return True
                
    
                                                   
    def evaluate_window(self, window, piece, direction):
        score = 0
        #opp_piece = PLAYER_PIECE
        #if piece == PLAYER_PIECE:
        #    opp_piece = AI_PIECE
        
        if piece == 1:
            opp_piece = 2
        elif piece == 2:
            opp_piece = 1

        if window.count(piece) == 4:
            score += 1000
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 100
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 10

        # Ways you can lose in one move 

        # If there is a free space next to three in a block, punish
        if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
            score -= 1000

        # Vertically this is one move away from winning due to rotation move 
        if window.count(opp_piece) == 4 and window.count(piece) == 1 and direction == "vertical":
            score -= 1000

        if window.count(opp_piece) == 3 and window.count(piece) == 1 and direction == "vertical":
            score -= 1000

        if window.count(opp_piece) == 2 and window.count(piece) == 1 and direction == "vertical":
            score -= 1000

        return score
    
    def score_position(self, board, piece):
        score = 0

        for r in range(ROWS):
            for c in range(COLUMNS):
                window = [board[r][(c + i) % COLUMNS] for i in range(WINDOW_LENGTH)]

                #print(f"lrd window {window}")
                score += self.evaluate_window(window, piece, "horizontal")

        ## Score Vertical
        for c in range(COLUMNS):
            col_array = [int(i) for i in list(board[:,c])]
            for r in range(ROWS-3):
                window = col_array[r:r+WINDOW_LENGTH]
                score += self.evaluate_window(window, piece, "vertical")

        # left right up diagonal
        for r in range(ROWS-3):
            for c in range(COLUMNS-3):
                window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece, "lru")

        for r in range(ROWS-3):
            for c in range(COLUMNS-3):
                window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece, "lrd")

        ## Check for common win method 
        for c in range(COLUMNS):
            col_array = [int(i) for i in list(board[:,c])]
            for r in range(ROWS-2):
                window = col_array[r:r+WINDOW_LENGTH+1]
                score += self.evaluate_window(window, piece, "vertical")

        return score

    def is_terminal_node(self, board):
        return self.winning_move(board, PLAYER_PIECE) or self.winning_move(board, AI_PIECE) or len(self.get_valid_locations(board)) == 0

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = self.get_valid_locations(board)
        occupied_rows = self.find_occupied_rows(board)
        is_terminal = self.is_terminal_node(board)

        #if piece == 1:
        #    opp_piece = 2
        #elif piece == 2:
        #    opp_piece = 1

        # Checking if board state is in the transposition table
        key = str(board)
        if key in self.__transposition_table:
            entry = self.__transposition_table[key]
            if entry['depth'] >= depth:
                if entry['type'] == 'exact':
                    return None, entry['score']
                elif entry['type'] == 'lowerbound':
                    alpha = max(alpha, entry['score'])
                elif entry['type'] == 'upperbound':
                    beta = min(beta, entry['score'])
                if alpha >= beta:
                    return None, entry['score']
            
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
            rotation_direction = None
            rotation_row = None
            for col in valid_locations:
                for direction in ["left", "right", "no direction"]:
                    for row in occupied_rows:
                        b_copy = board.copy()
                        b_copy = self.drop_piece(b_copy, row, col, AI_PIECE)
                        
                        if direction != "no direction":
                            # Rotate the board
                            rotated_board = self.rotate_board(row, direction, b_copy, occupied_rows)
                        else:
                            rotated_board = b_copy

                        new_score = self.minimax(rotated_board, depth-1, alpha, beta, False)[1]
                        if new_score > value:
                            value = new_score
                            column = col
                            rotation_direction = direction
                            rotation_row = row
                        alpha = max(alpha, value)
                        if alpha >= beta:
                            break

            # Adding the state to the transposition table 
            self.__transposition_table[key] = {
                'depth': depth,
                'score': value,
                'type': 'exact' if value >= beta else ('lowerbound' if value > alpha else 'upperbound')
            }

            return column, value, rotation_direction, rotation_row

        else: # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            rotation_direction = None
            rotation_row = None
            for col in valid_locations:
                for direction in ["left", "right", "no direction"]:
                    for row in occupied_rows:
                        b_copy = board.copy()
                        b_copy = self.drop_piece(b_copy, row, col, PLAYER_PIECE)
                        
                        if direction != "no direction":
                            # Rotate the board
                            rotated_board = self.rotate_board(row, direction, b_copy, occupied_rows)
                        else:
                            rotated_board = b_copy

                        new_score = self.minimax(rotated_board, depth-1, alpha, beta, True)[1]
                        if new_score < value:
                            value = new_score
                            column = col
                            rotation_direction = direction
                            rotation_row = row
                        beta = min(beta, value)
                        if alpha >= beta:
                            break
            return column, value, rotation_direction, rotation_row
        
    def negamax(self, board, depth, alpha, beta, color):
        valid_locations = self.get_valid_locations(board)
        occupied_rows = self.find_occupied_rows(board)
        is_terminal = self.is_terminal_node(board)

        # Checking if board state is in the transposition table
        key = str(board)
        if key in self.__transposition_table:
            entry = self.__transposition_table[key]
            if entry['depth'] >= depth:
                if entry['type'] == 'exact':
                    return None, entry['score']
                elif entry['type'] == 'lowerbound':
                    alpha = max(alpha, entry['score'])
                elif entry['type'] == 'upperbound':
                    beta = min(beta, entry['score'])
                if alpha >= beta:
                    return None, entry['score']
            
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.winning_move(board, AI_PIECE):
                    return (None, 100000000000000 * color)
                elif self.winning_move(board, PLAYER_PIECE):
                    return (None, -10000000000000 * color)
                else: # Game is over, no more valid moves
                    return (None, 0)
            else: # Depth is zero
                return (None, color * self.score_position(board, AI_PIECE))
            
        value = -math.inf
        column = random.choice(valid_locations)
        rotation_direction = None
        rotation_row = None
        for col in valid_locations:
            for direction in ["left", "right", "no direction"]:
                for row in occupied_rows:
                    b_copy = board.copy()
                    b_copy = self.drop_piece(b_copy, row, col, color)
                    
                    if direction != "no direction":
                        # Rotate the board
                        rotated_board = self.rotate_board(row, direction, b_copy, occupied_rows)
                    else:
                        rotated_board = b_copy

                    new_score = -self.negamax(rotated_board, depth-1, -beta, -alpha, -color)[1]
                    if new_score > value:
                        value = new_score
                        column = col
                        rotation_direction = direction
                        rotation_row = row
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break

        # Adding the state to the transposition table 
        self.__transposition_table[key] = {
            'depth': depth,
            'score': value,
            'type': 'exact' if value >= beta else ('lowerbound' if value > alpha else 'upperbound')
        }

        return column, value, rotation_direction, rotation_row


    def get_valid_locations(self, board):
        valid_locations = []
        for col in range(COLUMNS):
            if self.is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations
    
    def get_game_over(self):
        return self.__game_over
    
    def set_game_over(self, gamestate):
        self.__game_over = gamestate

    def get_board(self):
        return self.__board
    
    def set_winner(self, winner):
        self.__winner = winner

    def get_winner(self):
        return self.__winner
    
    def increase_total_turns(self):
        self.__total_turns += 1

    def get_total_turns(self):
        return self.__total_turns

def write_to_csv(winner, total_turns):
    with open('minimax_vs_negamax.csv', mode='a') as file:
        writer = csv.writer(file)
        writer.writerow([winner, total_turns])

def turn_drop_token(col, game, turn, player, board):

    row = game.get_next_open_row(board, col)
    board = game.drop_piece(board, row, col, player)

    turn += 1
    turn = turn % 2

    game.print_board(board)

    return game, turn 

def turn_rotate_board(row, direction, game, board):
    occupied_rows = game.find_occupied_rows(board)
    board = game.rotate_board(row, direction, board, occupied_rows)
    game.print_board(board)

    return game

def minimax_turn(game, board, turn, piece):
    
    column, value, rotation_direction, rotation_row = game.minimax(board, 4, -math.inf, math.inf, True)

    if (column != None):
        if game.is_valid_location(board, column):
            #pygame.time.wait(500)
            row = game.get_next_open_row(board, column)
            board = game.drop_piece(board, row, column, piece)

            if game.winning_move(board, piece):
                game.set_game_over(True)
                game.set_winner("minimax")

            print(f"MINIMAX {piece} - Before Rotation ")
            game.print_board(board)

            print(f"MINIMAX - {rotation_direction} Rotation Applied on Row {rotation_row}")
            occupied_rows = game.find_occupied_rows(board)
            board = game.rotate_board(rotation_row, rotation_direction, board, occupied_rows)

            game.print_board(board)

            if game.winning_move(board, piece):
                game.set_game_over(True)
                game.set_winner("minimax")

            game.increase_total_turns()
            turn += 1
            turn = turn % 2

            return game, board, turn

def negamax_turn(game, board, turn, piece):

    column, value, rotation_direction, rotation_row = game.negamax(board, 4, -math.inf, math.inf, 1)

    if (column != None):
        if game.is_valid_location(board, column):
            row = game.get_next_open_row(board, column)
            board = game.drop_piece(board, row, column, piece)

            if game.winning_move(board, piece):
                game.set_game_over(True)
                game.set_winner("negamax")

            print(f"NEGAMAX {piece} - Before Rotation ")
            game.print_board(board)

            print(f"NEGAMAX - {rotation_direction} Rotation Applied on Row {rotation_row}")
            occupied_rows = game.find_occupied_rows(board)
            board = game.rotate_board(rotation_row, rotation_direction, board, occupied_rows)

            game.print_board(board)

            if game.winning_move(board, piece):
                game.set_game_over(True)
                game.set_winner("negamax")

            game.increase_total_turns()
            turn += 1
            turn = turn % 2

            return game, board, turn

def player_turn(game, board, turn):
    col = int(input("COL:"))

    if game.is_valid_location(board, col):
        row = game.get_next_open_row(board, col)
        board = game.drop_piece(board, row, col, PLAYER_PIECE)

        if game.winning_move(board, PLAYER_PIECE):
            game.set_game_over(True)

        game.print_board(board)

        game.increase_total_turns()
        turn += 1
        turn = turn % 2

        return game, board, turn
    
def play_against_minimax():
    game = ConnectFourTwist()
    turn = random.randint(PLAYER, AI)
    board = game.get_board()

    while not game.get_game_over():

        # Ask for Player 1 Input
        if turn == PLAYER:  
            game, board = player_turn(game, board)
            
        # # Ask for Player 2 Input
        if turn == AI and not game.get_game_over():				
            game, board = minimax_turn(game, board)

        print(game.get_game_over())
        if game.get_game_over():
            print("GAME OVER")
            exit()

def play_against_negamax():
    game = ConnectFourTwist()
    turn = random.randint(PLAYER, AI)
    board = game.get_board()

    while not game.get_game_over():

        # Ask for Player 1 Input
        if turn == PLAYER:
            game, board = player_turn(game, board)
            
        # Ask for Player 2 Input
        if turn == AI and not game.get_game_over():				
            game, board = negamax_turn(game, board)
            
        print(game.get_game_over())
        if game.get_game_over():
            print("GAME OVER")
            exit()

winning_board = []

def play_minimax_vs_negamax():
    MINIMAX = 1
    NEGAMAX = 2

    turn = random.randint(MINIMAX, NEGAMAX)
    game = ConnectFourTwist(turn)
    
    board = game.get_board()

    while not game.get_game_over():


        # Ask for Player 1 Input
        if turn == 0 and not game.get_game_over():
            game, board, turn = minimax_turn(game, board, turn, MINIMAX)

        if game.winning_move(board, MINIMAX):
            game.set_game_over(True)
            game.set_winner("minimax")

        if game.winning_move(board, NEGAMAX):
            game.set_game_over(True)
            game.set_winner("negamax")

        #print(game.get_game_over())
        if game.get_game_over():
            print("GAME OVER")
            print(f"Winner is {game.get_winner()}")
            write_to_csv(game.get_winner(), game.get_total_turns())
            winning_board.append(board)
            #exit()
            
        # Ask for Player 2 Input
        if turn == 1 and not game.get_game_over():				
            game, board, turn = negamax_turn(game, board, turn, NEGAMAX)

        if game.winning_move(board, MINIMAX):
            game.set_game_over(True)
            game.set_winner("minimax")

        if game.winning_move(board, NEGAMAX):
            game.set_game_over(True)
            game.set_winner("negamax")

        #print(game.get_game_over())
        if game.get_game_over():
            print("GAME OVER")
            print(f"Winner is {game.get_winner()}")
            write_to_csv(game.get_winner(), game.get_total_turns())
            winning_board.append(board)
            #exit()
            
            #play_minimax_vs_negamax()
            
        

#play_minimax_vs_negamax()

#play_against_minimax()
#play_against_negamax()

#for i in range(0, 10):
#    play_minimax_vs_negamax()
play_minimax_vs_negamax()
play_minimax_vs_negamax()
play_minimax_vs_negamax()
play_minimax_vs_negamax()

print(winning_board)

for board in winning_board:
    print("=========")
    for row in board:
        print(row)