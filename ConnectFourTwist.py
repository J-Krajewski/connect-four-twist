from colorama import Fore, Style
import matplotlib.pyplot as plt
import numpy as np
import copy
import math
import itertools
import random

from Player import Player 
from Token import Token


# Constants
TOKENS_TO_WIN = 4
ROWS = 5
COLUMNS = 6

## Scoring Values
WIN_SCORE = 1000 # maybe should be infinity
LOSS_SCORE = -1000 # maybe should be negative infinity
THREE_CONNECTED_NODES = 15
TWO_CONNNECTED_NODES = 10


PLAYER_1 = Player("red", 1)
PLAYER_2 = Player("yellow", 2)


class ConnectFourTwist:
    def __init__(self, display_board, print_game_stats, rows=ROWS, cols=COLUMNS):
        self.__rows = rows
        self.__cols = cols
        self.__board = [[0] * cols for x in range(rows)]
        
        self.__display_board = display_board
        self.__print_game_stats = print_game_stats

        self.__turn_number = 0
        self.__player1 = PLAYER_1
        self.__player2 = PLAYER_2
        self.__players = [self.__player1, self.__player2]
        self.__current_player = None

        # Win Information
        self.__winner = None
        self.__won = False
        self.__win_direction = None
        self.__win_tokens = None

        self.__possible_moves = None
        
    def print_board(self):
        print(f"{Style.RESET_ALL}=====================")
        for row in self.__board:
            #print(row)
            row_output = ""
            for token in row:
                if token == 0:
                    row_output += str(f"{Style.RESET_ALL}{token}")
                if token == 1:
                    row_output += str(f"{self.__player1.get_text_colour()}{1}")
                if token == 2:
                    row_output += str(f"{self.__player2.get_text_colour()}{2}")

            print(row_output)
        print(f"{Style.RESET_ALL}=====================")

    def column_is_not_full(self, board, col):
        # checking top position only of given column
        return board[ROWS - 1][col] == 0
    
    def get_next_available_row(self, col):
        # finding the next free position on that column 
        for row in range(ROWS):
            if self.__board[row][col] == 0:
                return row
            
    def drop_token(self, board, row, col, piece):
        board[row][col] = piece

    def check_for_win(self, board, player_number):
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
      

    def display_board(self):
        colourmap = {'white': 0, 'red': 1, 'yellow': 2} 
        custom_cmap = plt.cm.colors.ListedColormap(['white', 'red', 'yellow'])
        board_colours = np.zeros((len(self.__board), len(self.__board[0])), dtype=int)

        for i in range(len(self.__board)):
            for j in range(len(self.__board[0])):
                token = self.__board[i][j]
                if token != 0:
                    colour = token.get_player().get_colour()
                    board_colours[i][j] = colourmap[colour]

        fig, axs = plt.subplots(1, 3, figsize=(15, 5), facecolor='white')  # 1 row and 3 columns of subplots
        axs[0].set_aspect('equal', 'box')
        
        # Set normalization to None and specify vmin and vmax
        axs[0].imshow(board_colours, cmap=custom_cmap, origin='upper', norm=None, vmin=0, vmax=2)  
        
        axs[0].set_yticks(range(len(self.__board)))
        axs[0].set_yticklabels(range(len(self.__board)-1, -1, -1))
        

        ## Drawing Labels 
        for i in range(ROWS):
            for j in range(COLUMNS):
                token = self.__board[i][j]
                if token != 0:
                    display_text = f"{token.get_position()} \n P{token.get_player().get_number()}"
                    axs[0].text(j, i, display_text, ha='center', va='center', color='black')

        # Plot player 1's graph in the second subplot
        axs[1].set_aspect('equal', 'box')
        self.__player1.draw_graph(axs[1])  
        axs[1].set_title('Player 1 Nodes')

        # Plot player 2's graph in the third subplot
        axs[2].set_aspect('equal', 'box')
        self.__player2.draw_graph(axs[2])  
        axs[2].set_title('Player 2 Nodes')

        plt.show()
 
    def apply_gravity(self):
        for col in range(self.__cols):
            for row in range(self.__rows - 1, 0, -1):
                if self.__board[row][col] == 0:
                    for r in range(row - 1, -1, -1):
                        if self.__board[r][col] != 0:
                            self.__board[row][col], self.__board[r][col] = self.__board[r][col], self.__board[row][col]
                            break

    def rotate_board(self, direction, row_index):
        if direction == "right":
            self.__board[row_index] = self.__board[row_index][-1:] + self.__board[row_index][:-1]

            self.apply_gravity()
            self.update_graphs()
            return True  
        elif direction == "left":
            self.__board[row_index] = self.__board[row_index][1:] + self.__board[row_index][:1]
            self.apply_gravity()
            self.update_graphs()
            return True  
        elif direction == "no direction":
            return True 
        else:
            print(f"{direction} is not a direction option, rotation not applied")
            return False  
        
    #def drop_piece(self, col, player):
    #    for row in range(self.__rows -1, -1, -1):
    #        if self.__board[row][col] == 0:
    #            #token = Token(player, [col, ROWS - row - 1])
    #            self.__board[row][col] = player.get_number()
    #            
    #            return True # piece is allowed to be dropped here
    #    return False # Col is full, cant drop piece 

    
    def player_turn(self, drop_col, direction, rotation_row):
        
        self.__current_player = self.__players[self.__turn_number % len(self.__players)]

        if self.__print_game_stats:
            print(f"\n Turn {self.__turn_number} - {self.__current_player.get_text_colour()}Player {self.__current_player.get_number()}'s Turn{Style.RESET_ALL}")

        # Dropping the token
        self.drop_piece(col=drop_col, player=self.__current_player)
        #self.update_graphs()

        if self.__print_game_stats:
            self.print_board()

        if self.__display_board:
            self.display_board()
        
        #self.__won, self.__win_direction, self.__win_tokens, self.__winner = self.get_current_player().check_win(self.__print_game_stats)
        print(self.check_for_win(self.__current_player.get_number()))


        # If the player chooses to rotate the board, rotate the board
        if direction != "no direction":
            self.rotate_board(direction=direction, row_index=rotation_row)

            if self.__print_game_stats:
                self.print_board()

            if self.__display_board:
                self.display_board()
            
            #self.__won, self.__win_direction, self.__win_tokens, self.__winner = self.get_current_player().check_win(self.__print_game_stats)
            print(self.check_for_win(self.__current_player.get_number()))
        #self.update_graphs()

        self.__turn_number += 1

    def print_win_statistics(self):

        if self.__print_game_stats:
            winner_text_colour = self.__winner.get_text_colour()

            print(f"Winner: {winner_text_colour}Player {self.__winner.get_number()}{Style.RESET_ALL}")
            print(f"Turns: {winner_text_colour}{self.__turn_number}{Style.RESET_ALL}")
            print(f"Win Direction: {winner_text_colour}{self.__win_direction}{Style.RESET_ALL}")
            print(f"Win Tokens: {winner_text_colour}{self.__win_tokens}{Style.RESET_ALL}")

    def score_block(self, block, token):
        score = 0

        if token == self.__player1.get_number():
            opposition_token = self.__player2.get_number()
        else:
            opposition_token = self.__player1.get_number()

        if block.count(token) == 4:                             # connect 4
            score += 100
        elif block.count(token) == 3 and block.count(0) == 1:   # 3 connected with space for 1
            score += 5
        elif block.count(token) == 2 and block.count(0) == 2:   # 2 connected with space for 2
            score += 2

        # Check if the enemy player can win on the next move   
        elif block.count(token) == 3 and block.count(0) == 1:
            score -= 4
        
        return score

    def score_board(self, board, token):

        # Horizontal scoring
        #for row in range(ROWS):
        #    #rows = [int(i) for i in list(board[row,:])]
        #    rows = [int(i) for i in list(board[row,:])]
        #    for col in range(COLUMNS):
        #    
        #        block = rows[col:(col+TOKENS_TO_WIN % COLUMNS - 1)]
        #        print(block)
        #        score += self.score_block(block, token)

        
        # Vertical scoring
        #for col in range(COLUMNS):
        #    cols = [int(i) for i in list(board[:,col])]
        #    for r in range(ROWS-3):
        #        block = cols[r:r+TOKENS_TO_WIN]
        #        print(block)
        #        score += self.score_block(block, token)

        print("TEMP")

        return 10

        # Implement Diagonal

    def is_leaf_node(self, board):
        condition1 = self.check_for_win(board, self.__player1)
        condition2 = self.check_for_win(board, self.__player2)
        no_more_moves = len(self.find_possible_locations(board)) == 0

        return condition1 or condition2 or no_more_moves

    

    def get_won(self):
        return self.__won
    
    def get_winner(self):
        return self.__winner
    
    def get_win_direction(self):
        return self.__win_direction
    
    def get_win_tokens(self):
        return self.__win_tokens
    
    def get_current_player(self):
        return self.__current_player
    
    def get_turn_number(self):
        return self.__turn_number
    
    def calc_possible_drops(self):
        possible_drop = []
        

        # Generate possible moves for dropping a token in each column
        for col in range(self.__cols):
            if self.__board[0][col] == 0:
                #print(f"column {col} has at least one space")
                possible_drop.append((col))  # ('drop', column, direction, rotation_row)

        ##print(f"Possible Combinations of Moves: {len(rows_with_tokens) * len(possible_drop) * len(directions)} ")
        
        return possible_drop
    
    def calc_possible_rotations(self):
        highest_token_row = ROWS
        rows_with_tokens = []
        
        for row in range(self.__rows):
            # If the board is not empty 
            if self.__board[row] != [0 for _ in range(self.__cols)]:
                highest_token_row = row
                
        ## Remember this is reversed 
        #print(f"Row of Highest Token on Board: {highest_token_row}")

        rows_with_tokens = [row for row in range(highest_token_row - 1, ROWS)]
        
        return rows_with_tokens

    def calc_possible_moves(self):
        possible_moves = []
        #directions = ["left", "right", "no direction"]
        directions = ["no direction"]

        # Generate possible moves for dropping a token in each column
        possible_drops = self.calc_possible_drops()
        possible_row_rotations = self.calc_possible_rotations()
        

        # Generate all possible combinations of drop and rotation
        for drop_col in possible_drops:
            for rotation_row in possible_row_rotations:
                for direction in directions:
                    possible_moves.append((drop_col, direction, rotation_row))


        #self.__possible_moves = possible_moves

        return possible_moves    

    
    
    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = self.find_possible_locations(board)
        is_terminal = self.is_leaf_node(board)

        if depth == 0 or is_terminal:
            if is_terminal:
                if self.check_for_win(board, self.__player2.get_number()):
                    return (None, 100000000000000)
                elif self.check_for_win(board, self.__player1.get_number()):
                    return (None, -10000000000000)
                else: # Game is over, no more valid moves
                    return (None, 0)
            else: # Depth is zero
                return (None, self.score_board(board, self.__player2.get_number()))
            
        if maximizingPlayer:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board, col)

                print(row)

                b_copy = board.copy()
                self.drop_token(b_copy, row, col, self.__player2.get_number())
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
                self.drop_token(b_copy, row, col, self.__player1.get_number())
                new_score = self.minimax(b_copy, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value
        
    def find_possible_locations(self, board):
        possible_locations = []
        for col in range(COLUMNS):
            if self.column_is_not_full(board, col):
                possible_locations.append(col)

        print(possible_locations)
        return possible_locations
    
    def get_next_open_row(self, board, col):

        

        for row in range(ROWS):
            print(f"{col}, {row} - {board[row][col]}")
            
            if board[row][col] == 0:
                return row

    def get_best_move(self, board, piece):

        valid_locations = self.find_possible_locations(board)
        best_score = -10000
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = self.get_next_open_row(board, col)
            temp_board = board.copy()
            self.drop_token(temp_board, row, col, piece)
            score = self.score_board(temp_board, piece)
            if score > best_score:
                best_score = score
                best_col = col

        return best_col

      
    def set_display(self, display_board, print_board):
        self.__display_board = display_board
        self.__print_game_stats = print_board

    def get_board(self):
        return self.__board
    
    def get_player_1(self):
        return self.__player1

    def get_player_2(self):
            return self.__player2

def run_game():
    game = ConnectFourTwist(display_board=False, print_game_stats=False)
    turn = 0
    
    col = 0 
    row = game.get_next_open_row(game.get_board(), col)

    print(row)
    game.drop_token(game.get_board(), col, row, game.get_player_1().get_number())
    turn += 1

    game.print_board()

    ## AI TURN
    col, minimax_score = game.minimax(game.get_board(), 5, -math.inf, math.inf, True)   

    if game.column_is_not_full(game.get_board(), col):
        row = game.get_next_open_row(game.get_board(), col)

        print(row)
        game.drop_token(game.get_board(), row, col, game.get_player_2().get_number())

    game.print_board()
    
    turn += 1



run_game()