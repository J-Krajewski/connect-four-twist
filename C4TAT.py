import numpy as np
import random
from colorama import Fore, Style
import csv
import time
import itertools
import sys
import math
import decimal  

from Player import Player 

ROWS = 5
COLUMNS = 6
WINDOW_LENGTH = 4
EMPTY = 0

MAX_DEPTH = 5

class ConnectFourTwistAndTurn:
	
    def __init__(self, player1, player2, ab_pruning, t_tables):
        self.__player1 = player1
        self.__player2 = player2
        self.__players = {1: self.__player1, 2: self.__player2}
        self.__ab_pruning = ab_pruning
        self.__t_tables = t_tables
        
        self.__board = self.create_board()
        self.__game_over = False
        self.__transposition_table = {}
        self.__current_node_count = 0
        
        # Winning Stats Collected 
        self.__winner = None
        self.__total_turns = 0
        self.__starter = None
        self.__win_direction = None

        
        
        
    def create_board(self):
        board = np.zeros((ROWS,COLUMNS), dtype=int)
        
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
        for c in range(COLUMNS):
            for r in range(ROWS):
                if board[r][(c + 3) % COLUMNS] == piece and \
                    board[r][(c + 2) % COLUMNS] == piece and \
                    board[r][(c + 1) % COLUMNS] == piece and \
                    board[r][c] == piece:
                        self.__win_direction = "horizontal"
                        return True

        # Check vertical locations for win
        for c in range(COLUMNS):
            for r in range(ROWS-3):
                if board[r][c] == piece and \
                    board[r+1][c] == piece and \
                    board[r+2][c] == piece and \
                    board[r+3][c] == piece:
                        self.__win_direction = "vertical"
                        return True
                
        # Check positively sloped diaganols (lru)
        for c in range(COLUMNS):
            for r in range(ROWS - 3):
                if board[r][c] == piece and \
                    board[r+1][(c + 1) % COLUMNS] == piece and \
                    board[r+2][(c + 2) % COLUMNS] == piece and \
                    board[r+3][(c + 3) % COLUMNS] == piece:
                        self.__win_direction = "lru"
                        return True
                
        # Check negatively sloped diaganols (lrd)
        for c in range(COLUMNS):
            for r in range(3, ROWS):
                if board[r][c] == piece and \
                board[r-1][(c + 1) % COLUMNS] == piece and \
                board[r-2][(c + 2) % COLUMNS] == piece and \
                board[r-3][(c + 3) % COLUMNS] == piece:
                    self.__win_direction = "lrd"
                    return True
                
                                           
    def evaluate_window(self, window, piece, direction):
        score = 0
        multiplier = 1
        
        opp_piece = 3 - piece

        if (direction == "vertical") or (direction == "lru") or (direction == "lrd"):
            multiplier = 1.5

        if window.count(piece) == 4:
            score += 100
            score = score * multiplier

        if window.count(opp_piece) == 4:
            score -= 100
            score = score * multiplier

        if window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 50
            score = score * multiplier

        if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
            score -= 50
            score = score * multiplier
            
        if window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 2
            score = score * multiplier

        if window.count(opp_piece) == 2 and window.count(EMPTY) == 2:
            score -= 2
            score = score * multiplier

        # Ways you can lose in one move 

        # Vertically this is one move away from winning due to rotation move 
        if window.count(piece) == 3 and window.count(opp_piece) == 1 and direction == "vertical":
            score += 5

        # Vertically this is one move away from winning due to rotation move 
        if window.count(opp_piece) == 3 and window.count(piece) == 1 and direction == "vertical":
            score -= 5

        return score
    
    def score_board(self, board, piece):
        score = 0
        score_value = 50

        opp_piece = 3 - piece

        

        # Checking for common win method  - which is a win in one turn 
        # Currently only works for vertical
        for row in range(ROWS - 2):
            for col in range(COLUMNS):
                token_1 = board[row][col]
                token_2 = board[row + 1][col]
                token_3 = board[row + 2][col]

                tokens = [token_1, token_2, token_3]

                # TODO if any of the tokens are 0 skip
                
                if tokens == [opp_piece, opp_piece, piece]:
                    #print(tokens)
                    #print("looking at token 3 and adjacent locations")
                    left_token_3 = board[row + 2][(col - 1) % COLUMNS]
                    right_token_3 = board[row + 2][(col + 1) % COLUMNS]

                    # if the adjacent token to your piece is opp piece, punish
                    if left_token_3 == opp_piece:
                        score -= score_value
                        #print(f"{tokens} - left token 3: {left_token_3}")
                    elif right_token_3 == opp_piece:
                        score -= score_value
                        #print(f"{tokens} - right token 3: {right_token_3}")

                elif tokens == [opp_piece, piece, opp_piece]:
                    #print(tokens)
                    #print("looking at token 2 and adjacent locations")
                    left_token_2 = board[row + 1][(col - 1) % COLUMNS]
                    right_token_2 = board[row + 1][(col + 1) % COLUMNS]

                    # if the adjacent token to your piece is opp piece, punish
                    if left_token_2 == opp_piece:
                        score -= score_value
                        #print(f"{tokens} - left token 2: {left_token_2}")
                    elif right_token_2 == opp_piece:
                        score -= score_value
                        #print(f"{tokens} - right token 2: {right_token_2}")
            
                elif tokens == [piece, opp_piece, opp_piece]:
                    #print(tokens)
                    #print("looking at token 1 and adjacent locations")
                    left_token_1 = board[row][(col - 1) % COLUMNS]
                    right_token_1 = board[row][(col + 1) % COLUMNS]

                    # if the adjacent token to your piece is opp piece, punish
                    if left_token_1 == opp_piece:
                        score -= score_value
                        #print(f"{tokens} - left token 1: {left_token_1}")
                    elif right_token_1 == opp_piece:
                        score -= score_value
                        #print(f"{tokens} - right token 1: {right_token_1}")
                        
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
            for c in range(COLUMNS):
                window = [board[r+i][(c + i) % COLUMNS] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece, "lru")

        for r in range(ROWS-3):
            for c in range(COLUMNS):
                window = [board[r-i][(c - i) % COLUMNS] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece, "lrd")

        score += self.score_board(board, piece)
                
        return score

    def check_leaf_node(self, board):
        p1_winning_move = self.winning_move(board, 1)
        p2_winning_move = self.winning_move(board, 2)
        no_more_moves = (len(self.get_valid_locations(board)) == 0)

        return  p1_winning_move or p2_winning_move or no_more_moves

    def minimax_old(self, board, depth, alpha, beta, maximizingPlayer, minimax_number, opp_number):
        valid_locations = self.get_valid_locations(board)
        occupied_rows = self.find_occupied_rows(board)
        is_leaf = self.check_leaf_node(board)

        #print(node_count)

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
                
        self.__current_node_count += 1
            
        if depth == 0 or is_leaf:
            if is_leaf:
                if self.winning_move(board, minimax_number):
                    return (None, 100000000000000)
                elif self.winning_move(board, opp_number):
                    return (None, -10000000000000)
                else: # Game is over, no more valid moves
                    return (None, 0)
            else: # Depth is zero
                return (None, self.score_position(board, minimax_number))
            
        if maximizingPlayer:
            value = -math.inf
            column = random.choice(valid_locations)
            direction = None
            row = None

            for drop_col in valid_locations:
                for rotation_direction in ["left", "right", "no direction"]:
                    for rotation_row in occupied_rows:
                        b_copy = board.copy()
                        drop_row = self.get_next_open_row(b_copy, drop_col)

                        b_copy = self.drop_piece(b_copy, drop_row, drop_col, minimax_number)
                        
                        if rotation_direction != "no direction":
                            # Rotate the board
                            rotated_board = self.rotate_board(rotation_row, rotation_direction, b_copy, occupied_rows)
                        else:
                            rotated_board = b_copy

                        new_score = self.minimax(rotated_board, depth-1, alpha, beta, False, minimax_number, opp_number)[1]
                        if new_score > value:
                            #print(f"maximising player - new score {new_score} - dc: {drop_col} rr: {rotation_row} rd: {rotation_direction}")
                            value = new_score
                            column = drop_col
                            direction = rotation_direction
                            row = rotation_row
                        alpha = max(alpha, value)
                        if alpha >= beta:
                            break

            # Adding the state to the transposition table 
            self.__transposition_table[key] = {
                'depth': depth,
                'score': value,
                'type': 'exact' if value >= beta else ('lowerbound' if value > alpha else 'upperbound')
            }

            return column, value, direction, row

        else: # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            rotation_direction = None
            rotation_row = None

            for drop_col in valid_locations:
                for rotation_direction in ["left", "right", "no direction"]:
                    for rotation_row in occupied_rows:
                        b_copy = board.copy()
                        drop_row = self.get_next_open_row(b_copy, drop_col)

                        b_copy = self.drop_piece(b_copy, drop_row, drop_col, opp_number)
                        
                        if rotation_direction != "no direction":
                            # Rotate the board
                            rotated_board = self.rotate_board(rotation_row, rotation_direction, b_copy, occupied_rows)
                        else:
                            rotated_board = b_copy

                        new_score = self.minimax(rotated_board, depth-1, alpha, beta, True, minimax_number, opp_number)[1]
                        if new_score < value:
                            #print(f"minimising player - new score {new_score} - dc: {drop_col} rr: {rotation_row} rd: {rotation_direction}")
                            value = new_score
                            column = drop_col
                            direction = rotation_direction
                            row = rotation_row
                        beta = min(beta, value)
                        if alpha >= beta:
                            break
            return column, value, direction, row


    def minimax(self, board, depth, alpha, beta, maximizingPlayer, minimax_number, opp_number):
        valid_locations = self.get_valid_locations(board)
        occupied_rows = self.find_occupied_rows(board)
        is_leaf = self.check_leaf_node(board)

        
        key = str(board)
        if self.__t_tables:  
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
                
        self.__current_node_count += 1
            
        if depth == 0 or is_leaf:
            if is_leaf:
                if self.winning_move(board, minimax_number):
                    return (None, 100000000000000)
                elif self.winning_move(board, opp_number):
                    return (None, -10000000000000)
                else: # Game is over, no more valid moves
                    return (None, 0)
            else: # Depth is zero
                return (None, self.score_position(board, minimax_number))
            
        if maximizingPlayer:
            value = -math.inf
            column = random.choice(valid_locations)
            direction = None
            row = None

            for drop_col in valid_locations:
                for rotation_direction in ["left", "right", "no direction"]:
                    for rotation_row in occupied_rows:
                        b_copy = board.copy()
                        drop_row = self.get_next_open_row(b_copy, drop_col)

                        b_copy = self.drop_piece(b_copy, drop_row, drop_col, minimax_number)
                        
                        if rotation_direction != "no direction":
                            # Rotate the board
                            rotated_board = self.rotate_board(rotation_row, rotation_direction, b_copy, occupied_rows)
                        else:
                            rotated_board = b_copy

                        new_score = self.minimax(rotated_board, depth-1, alpha, beta, False, minimax_number, opp_number)[1]
                        if new_score > value:
                            value = new_score
                            column = drop_col
                            direction = rotation_direction
                            row = rotation_row
                        if self.__ab_pruning:
                            alpha = max(alpha, value)
                            if alpha >= beta:
                                break

            # Adding the state to the transposition table 
            if self.__t_tables:
                self.__transposition_table[key] = {
                    'depth': depth,
                    'score': value,
                    'type': 'exact' if value >= beta else ('lowerbound' if value > alpha else 'upperbound')
                }

            return column, value, direction, row

        else: # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            rotation_direction = None
            rotation_row = None

            for drop_col in valid_locations:
                for rotation_direction in ["left", "right", "no direction"]:
                    for rotation_row in occupied_rows:
                        b_copy = board.copy()
                        drop_row = self.get_next_open_row(b_copy, drop_col)

                        b_copy = self.drop_piece(b_copy, drop_row, drop_col, opp_number)
                        
                        if rotation_direction != "no direction":
                            # Rotate the board
                            rotated_board = self.rotate_board(rotation_row, rotation_direction, b_copy, occupied_rows)
                        else:
                            rotated_board = b_copy

                        new_score = self.minimax(rotated_board, depth-1, alpha, beta, True, minimax_number, opp_number)[1]
                        if new_score < value:
                            value = new_score
                            column = drop_col
                            direction = rotation_direction
                            row = rotation_row
                        if self.__ab_pruning:
                            beta = min(beta, value)
                            if alpha >= beta:
                                break
            return column, value, direction, row

        
    def negamax(self, board, depth, alpha, beta, sign):
        valid_locations = self.get_valid_locations(board)
        occupied_rows = self.find_occupied_rows(board)
        is_leaf = self.check_leaf_node(board)

        # Checking if board state is in the transposition table
        key = str(board)
        if self.__t_tables:
            if key in self.__transposition_table:
                entry = self.__transposition_table[key]
                if entry['depth'] >= depth:
                    if entry['type'] == 'exact':
                        return None, entry['score'], None, None
                    elif entry['type'] == 'lowerbound':
                        alpha = max(alpha, entry['score'])
                    elif entry['type'] == 'upperbound':
                        beta = min(beta, entry['score'])
                    if alpha >= beta:
                        return None, entry['score'], None, None
                
        self.__current_node_count += 1
                
        if depth == 0 or is_leaf:
            if is_leaf:
                if self.winning_move(board, sign):
                    return None, 100000000000000, None, None
                elif self.winning_move(board, 3 - sign):  # opponent's sign
                    return None, -10000000000000, None, None
                else:  # Game is over, no more valid moves
                    return None, 0, None, None
            else:  # Depth is zero
                return None, self.score_position(board, sign), None, None
                    
        value = -math.inf
        column = random.choice(valid_locations)
        direction = None
        row = None

        for drop_col in valid_locations:
            for rotation_direction in ["left", "right", "no direction"]:
                for rotation_row in occupied_rows:
                    b_copy = board.copy()
                    drop_row = self.get_next_open_row(b_copy, drop_col)
                    b_copy = self.drop_piece(b_copy, drop_row, drop_col, sign)
                    
                    if rotation_direction != "no direction":
                        # Rotate the board
                        rotated_board = self.rotate_board(rotation_row, rotation_direction, b_copy, occupied_rows)
                    else:
                        rotated_board = b_copy

                    new_score = -self.negamax(rotated_board, depth-1, -beta, -alpha, 3 - sign)[1]  # Switch sign
                    if new_score > value:
                        value = new_score
                        column = drop_col
                        direction = rotation_direction
                        row = rotation_row
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break

        # Adding the state to the transposition table 
        self.__transposition_table[key] = {
            'depth': depth,
            'score': value,
            'type': 'exact' if value >= beta else ('lowerbound' if value > alpha else 'upperbound')
        }

        return column, value, direction, row
    
    # This player only plays the immediate next best move
    def greedy_search(self, board, player_number, opp_number):
        valid_locations = self.get_valid_locations(board)
        occupied_rows = self.find_occupied_rows(board)
        
        best_score = -math.inf
        best_col = random.choice(valid_locations)
        best_direction = "no direction"
        best_row = None

        for drop_col in valid_locations:
            for rotation_direction in ["left", "right", "no direction"]:
                for rotation_row in occupied_rows:
                    b_copy = board.copy()
                    drop_row = self.get_next_open_row(b_copy, drop_col)

                    b_copy = self.drop_piece(b_copy, drop_row, drop_col, player_number)
                    
                    if rotation_direction != "no direction":
                        rotated_board = self.rotate_board(rotation_row, rotation_direction, b_copy, occupied_rows)
                    else:
                        rotated_board = b_copy

                    score = self.score_position(rotated_board, player_number)
                    
                    if score > best_score:
                        best_score = score
                        best_col = drop_col
                        best_direction = rotation_direction
                        best_row = rotation_row

        return best_col, best_score, best_direction, best_row

        
 
    def get_valid_locations(self, board):
        valid_locations = []
        for col in range(COLUMNS):
            if self.is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations
    
    def check_winning_move(self, player, board):
        # Check if the given player has a connect 4 
        if self.winning_move(board, player.get_number()):
            # If no other winner has been declared, set winner
            if self.__winner == None:
                self.__game_over = True
                self.__winner = (player.get_name())

    def check_for_win(self, board):

        # Check both players for a potential win or draw
        self.check_winning_move(self.__player1, board)
        self.check_winning_move(self.__player2, board)

        if self.get_game_over():
            print("GAME OVER")
            print(f"Winner is {self.get_winner()}")
            self.write_to_csv()
            

            return True
        
        return False
    
    def write_to_csv(self):
        p1_name = self.__player1.get_name().lower()
        p2_name = self.__player2.get_name().lower()

        filename = f"Results/{p1_name}_vs_{p2_name}.csv"

        with open(filename, mode='a') as file:
            writer = csv.writer(file)
        
            row = [self.__winner, self.__starter.get_name(), self.__total_turns, 
                   self.__win_direction, self.__ab_pruning, self.__t_tables]
            row = self.__player1.add_player_info(row)
            row = self.__player2.add_player_info(row)
            
            writer.writerow(row)

    def generate_scenario(self, tokens_per_player):

        for j in range(tokens_per_player):
            # Determine who places first randomly
            first_player = random.randint(1, 2)
            second_player = 3 - first_player

            # Place and rotate randomly two token
            self, self.__board, turn = random_turn(self, self.__board, None, None, random_number=first_player, opp_number=second_player, display=False)
            self, self.__board, turn = random_turn(self, self.__board, None, None, random_number=second_player, opp_number=first_player, display=False)


        print(f">>> GENERATED SCENARIO")
        self.print_board(self.__board)
    

    
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
    
    def get_starter(self):
        return self.__starter
    
    def get_win_direction(self):
        return self.__win_direction
    
    def get_players(self):
        return self.__players
    
    def get_current_node_count(self):
        return self.__current_node_count
    
    def set_current_node_count(self, current_node_count):
        self.__current_node_count = current_node_count
    
    def update_players(self, player1, player2):
        self.__player1 = player1
        self.__player2 = player2
        self.__players = {1: self.__player1, 2: self.__player2}

    def set_starter(self, starter):
        self.__starter = starter

    def set_player1(self, player1):
        self.__player1 = player1
    
    def set_player1(self, player2):
        self.__player2 = player2
    
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

def player_turn(game, board, turn, depth, player_number, opp_number, display=True):

    # Get the Drop Column
    valid_locations = game.get_valid_locations(board)
    drop_col = int(input("Enter Drop Column"))

    if drop_col not in valid_locations:
        print(f"Column {drop_col} is Not a Valid Location")
        player_turn(game, board, turn, depth, player_number, opp_number)
    
    # Drop the token and apply rotation
    row = game.get_next_open_row(board, drop_col)
    board = game.drop_piece(board, row, drop_col, player_number)
    game.apply_gravity(board)

    print(f">>> PLAYER ({player_number}) - Drop Column: {drop_col}")
    game.print_board(board)

    # Get the Rotation Row
    occupied_rows = game.find_occupied_rows(board)
    rotation_row = int(input("Enter Rotation Row"))

    if rotation_row not in occupied_rows:
        print(f"Row {rotation_row} is Not a Valid Location, no rotation applied")

    # Get the Rotation Direction
    rotation_direction = str(input("Enter Rotation Direction (left/right/no direction)"))

    if rotation_direction != "no direction":
        board = game.rotate_board(rotation_row, rotation_direction, board, occupied_rows)

    print(f">>> PLAYER ({player_number}) - {rotation_direction} Rotation Applied on Row {rotation_row}")

    game.print_board(board)

    return game, board, turn

def random_turn(game, board, turn, depth, random_number, opp_number, display=True):
        
        valid_locations = game.get_valid_locations(board)
        random_column = random.choice(valid_locations)

        # Find occupied rows to select a random row to rotate
        occupied_rows = game.find_occupied_rows(board)

        if occupied_rows:
            
            # Choose a random rotation direction or choose not to rotate
            rotation_direction = random.choice(["left", "right", "no direction"])
            random_rotation_row = random.choice(occupied_rows)

            # Drop the token and apply rotation
            row = game.get_next_open_row(board, random_column)
            board = game.drop_piece(board, row, random_column, random_number)
            game.apply_gravity(board)

            if display: print(f">>> RANDOM ({random_number}) - Drop Column: {random_column}")
            if display: game.print_board(board)

            if rotation_direction != "no direction":
                board = game.rotate_board(random_rotation_row, rotation_direction, board, occupied_rows)

            if display: print(f">>> RANDOM ({random_number}) - {rotation_direction} Rotation Applied on Row {random_rotation_row}")
            if display: game.print_board(board)

        else:
            # If there are no occupied rows, just drop the token without rotation
            row = game.get_next_open_row(board, random_column)
            board = game.drop_piece(board, row, random_column, random_number)
            
            game.apply_gravity(board)
            game.print_board(board)

            if display: print(f">>> RANDOM ({random_number}) - No Rotation Applied on Row")


        return game, board, turn

def minimax_turn(game, board, turn, depth, minimax_number, opp_number, display=True):
    
    column, value, rotation_direction, rotation_row = game.minimax(board, depth, -math.inf, math.inf, True, minimax_number, opp_number)
    
    if (column != None):
        if game.is_valid_location(board, column):
            #pygame.time.wait(500)
            row = game.get_next_open_row(board, column)
            board = game.drop_piece(board, row, column, minimax_number)

            #game.check_for_win(board)

            if display: print(f">>> MINIMAX ({minimax_number}) - Drop Column: {column} - Value {value} ")
            if display: game.print_board(board)

            #game.check_for_win(board)

            if display: print(f">>> MINIMAX ({minimax_number}) - Rotation Dir: {rotation_direction} on Row :{rotation_row} - Value {value} ")

            occupied_rows = game.find_occupied_rows(board)
            board = game.rotate_board(rotation_row, rotation_direction, board, occupied_rows)

            if display: game.print_board(board)
        
            return game, board, turn
        
def greedy_turn(game, board, turn, depth, greedy_number, opp_number, display=True):
    
    column, value, rotation_direction, rotation_row = game.greedy_search(board, greedy_number, opp_number)
    
    if (column != None):
        if game.is_valid_location(board, column):
            row = game.get_next_open_row(board, column)
            board = game.drop_piece(board, row, column, greedy_number)

            if display: print(f">>> GREEDY ({greedy_number}) - Drop Column: {column} - Value {value} ")
            if display: game.print_board(board)

            if display: print(f">>> GREEDY ({greedy_number}) - Rotation Dir: {rotation_direction} on Row :{rotation_row} - Value {value} ")

            occupied_rows = game.find_occupied_rows(board)
            board = game.rotate_board(rotation_row, rotation_direction, board, occupied_rows)

            if display: game.print_board(board)
        
            return game, board, turn

#def negamax_turn(game, board, turn, piece, depth):
def negamax_turn(game, board, turn, depth, negamax_number, opp_number, display=True):

    column, value, rotation_direction, rotation_row = game.negamax(board, depth, -math.inf, math.inf, negamax_number)

    #best_column, value, best_direction, best_row, node_count
    print(f"drop_column = {column} rotation_row = {rotation_row} rotation_direction = {rotation_direction} value = {value}")


    if (column != None):
        if game.is_valid_location(board, column):
            #pygame.time.wait(500)
            row = game.get_next_open_row(board, column)
            board = game.drop_piece(board, row, column, negamax_number)

            #game.check_for_win(board)

            if display: print(f">>> NEGAMAX ({negamax_number}) - Drop Column: {column} - Value {value} ")
            if display: game.print_board(board)

            #game.check_for_win(board)

            if display: print(f">>> NEGAMAX ({negamax_number}) - Rotation Dir: {rotation_direction} on Row :{rotation_row} - Value {value} ")

            occupied_rows = game.find_occupied_rows(board)
            board = game.rotate_board(rotation_row, rotation_direction, board, occupied_rows)

            if display: game.print_board(board)
        
            return game, board, turn


def alternate_turn(start_turn, next_turn):
    while True:
        yield next_turn
        yield start_turn


def run_game(game):

    turn = random.randint(1, 2)
    
    players = game.get_players()

    print(f"Player {1} - {players[1].get_name()} - Token: {players[1].get_number()} - Depth {players[1].get_depth()}")
    print(f"Player {2} - {players[2].get_name()} - Token: {players[2].get_number()} - Depth {players[2].get_depth()}")

    starter = players[turn]
    game.set_starter(starter)

    turn_generator = alternate_turn(turn, 3 - turn)

    board = game.get_board()
    
    while not game.get_game_over():
        game.set_current_node_count(0)
        current_player = players[turn]
        other_player = players[1 + (turn)%2]

        print(f"current player: {current_player.get_name()} turn: {turn} - other player is {other_player.get_name()}")

        start_time = time.time()
        game, board, turn = current_player.run_strategy(game, board, turn)
        end_time = time.time()

        current_player.add_turn_nodes(game.get_current_node_count())
        current_player.add_turn_time(end_time - start_time)

        game.increase_total_turns()

        if turn == 1:
            game.update_players(player1=current_player, player2=other_player)
        elif turn == 2:
            game.update_players(player2=current_player, player1=other_player)

        game.check_for_win(board)
        
        turn = next(turn_generator)


def play_minimax_vs_random(minimax_depth, ab_pruning, t_tables):
    minimax_player = Player("red", 1, "Minimax", minimax_turn, minimax_depth)
    random_player = Player("yellow", 2, "Random", random_turn, None)  
    game = ConnectFourTwistAndTurn(minimax_player, random_player, ab_pruning, t_tables)  

    run_game(game) 

def play_negamax_vs_random(negamax_depth):
    negamax_player = Player("red", 1, "Negamax", negamax_turn, negamax_depth)
    random_player = Player("yellow", 2, "Random", random_turn, None)    
    game = ConnectFourTwistAndTurn(negamax_player, random_player)  

    run_game(game)

def play_random_vs_random():
    random_1_player = Player("red", 1, "Random 1", random_turn, None)
    random_2_player = Player("yellow", 2, "Random 2", random_turn, None) 
    game = ConnectFourTwistAndTurn(random_1_player, random_2_player)

    run_game(game)  

def play_minimax_vs_negamax(minimax_depth, negamax_depth):
    minimax_player = Player("red", 1, "Minimax", minimax_turn, minimax_depth)
    negamax_player = Player("yellow", 2, "Negamax", negamax_turn, negamax_depth)
    game = ConnectFourTwistAndTurn(minimax_player, negamax_player)  

    game.generate_scenario(tokens_per_player=2) # This randomises two yellow and red tokens to create different scenarios

    run_game(game)  

def play_minimax_vs_minimax(minimax_1_depth, minimax_2_depth):
    minimax_player_1 = Player("red", 1, "Minimax 1", minimax_turn, minimax_1_depth)
    minimax_player_2 = Player("yellow", 2, "Minimax 2", minimax_turn, minimax_2_depth)
    game = ConnectFourTwistAndTurn(minimax_player_1, minimax_player_2)  
    game.generate_scenario(tokens_per_player=2)
    run_game(game) 

def play_negamax_vs_negamax(negamax_1_depth, negamax_2_depth):
    negamax_player_1 = Player("red", 1, "Minimax 1", negamax_turn, negamax_1_depth)
    negamax_player_2 = Player("yellow", 2, "Minimax 2", negamax_turn, negamax_2_depth)
    game = ConnectFourTwistAndTurn(negamax_player_1, negamax_player_2)  
    game.generate_scenario(tokens_per_player=2)
    run_game(game) 

def play_player_vs_negamax(negamax_depth):
    player = Player("red", 1, "Player", player_turn, None)
    negamax_player = Player("yellow", 2, "Negamax", negamax_turn, negamax_depth)    
    game = ConnectFourTwistAndTurn(player, negamax_player)  

    run_game(game)   

def play_minimax_vs_greedy(minimax_depth, ab_pruning, t_tables):
    minimax_player = Player("red", 1, "Minimax", minimax_turn, minimax_depth)
    greedy_player = Player("yellow", 2, "Greedy", greedy_turn, None)
    game = ConnectFourTwistAndTurn(minimax_player, greedy_player, ab_pruning, t_tables)  

    game.generate_scenario(tokens_per_player=2) # This randomises two yellow and red tokens to create different scenarios

    run_game(game)  


def generate_win_data(repeat):

    for x in range(repeat):      

        play_minimax_vs_random(MAX_DEPTH)
        play_negamax_vs_random(MAX_DEPTH)
        play_random_vs_random(MAX_DEPTH)
        play_minimax_vs_negamax(MAX_DEPTH, MAX_DEPTH)
        play_minimax_vs_minimax(MAX_DEPTH, MAX_DEPTH)
        play_negamax_vs_negamax(MAX_DEPTH, MAX_DEPTH)

#play_minimax_vs_minimax(minimax_1_depth=MAX_DEPTH, minimax_2_depth=MAX_DEPTH)

def minimax_vs_random_testing():
    count = 0
    for _ in range(4):
        for _ in range(5):
            play_minimax_vs_random(MAX_DEPTH - count, True, True)
            play_minimax_vs_random(MAX_DEPTH - count, True, True)
            play_minimax_vs_random(MAX_DEPTH - count, True, True)
        count += 1

def tt_abp_minimax_testing():
    for _ in range(10):
        play_minimax_vs_random(4, True, True)
        play_minimax_vs_random(4, False, True)
        play_minimax_vs_random(4, True, False)
        play_minimax_vs_random(4, False, False)

def minimax_vs_greedy_testing():
    for _ in range(10):
        
        play_minimax_vs_greedy(5, True, True)
        play_minimax_vs_greedy(4, True, True)
        play_minimax_vs_greedy(3, True, True)
        play_minimax_vs_greedy(2, True, True)
        

#play_minimax_vs_greedy(3, True, True)

#repeat()
#minimax_vs_greedy_testing()


#play_minimax_vs_random(MAX_DEPTH - 3)

minimax_vs_random_testing()