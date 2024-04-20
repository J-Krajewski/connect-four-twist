from colorama import Fore, Style
import matplotlib.pyplot as plt
import numpy as np
import copy

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
## BLOCK_THREE_CONNECTED_NODES = 15
## BLOCK_TWO_CONNECTED_NODES = 10

# This class represents the game state 



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
                    #print(token)
                    row_output += str(f"{Style.RESET_ALL}{token}")
                else:
                    #print(token.get_symbol())
                    row_output += str(f"{token.get_player().get_text_colour()}{token.get_symbol()}")

            print(row_output)
        print(f"{Style.RESET_ALL}=====================")

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
        if direction == "clockwise":
            self.__board[row_index] = self.__board[row_index][-1:] + self.__board[row_index][:-1]
            self.apply_gravity()
            self.update_graphs()
            return True  # Rotation applied
        elif direction == "counterclockwise":
            self.__board[row_index] = self.__board[row_index][1:] + self.__board[row_index][:1]
            self.apply_gravity()
            self.update_graphs()
            return True  # Rotation applied
        elif direction == "no direction":
            #self.apply_gravity()
            return True # Player chose not to rotate
            
        else:
            print(f"{direction} is not a direction option, rotation not applied")
            return False # rotation not applied 

    def drop_piece(self, col, player):
        for row in range(self.__rows -1, -1, -1):
            if self.__board[row][col] == 0:
                token = Token(player, [col, ROWS - row - 1])
                self.__board[row][col] = token
                player.add_token(str(token.get_position()))
                self.update_graphs()
                return True # piece is allowed to be dropped here
        return False # Col is full, cant drop piece 
    
    
    def update_graphs(self):
        
        for y in range(0, ROWS):
            for x in range(0, COLUMNS):
                token = self.__board[y][x]

                if token != 0:
                    player = token.get_player()
                    
                    # check  and update horizontal
                    right_token = self.__board[y][(x+1)%(COLUMNS)]
                    if right_token != 0: # slot to the right is not empty
                        if right_token.get_player() == player: # Token to the right is same colour
                            
                            token_name = str(token.get_position())
                            right_token_name = str(right_token.get_position())
                            player.add_horizontal_connection(token_name, right_token_name)
                            
                    # check and update vertical
                    if y < ROWS - 1:
                        #print(y+1)
                        upper_token = self.__board[y+1][(x)]
                        if upper_token != 0: # slot above is not empty
                            
                            #print(f"upper token:{upper_token.get_position()}")
                            #print(f"lower token:{token.get_position()}")
                            if upper_token.get_player() == player: # If token above is the same colour
                                
                                player.add_vertical_connection(token.get_token_name(), upper_token.get_token_name())

                    # check and update diagonal LRU
                    if y != 0:
                        upper_right_token = self.__board[y-1][(x+1)%(COLUMNS)]
                        if upper_right_token != 0:
                            if upper_right_token.get_player() == player: 
                                player.add_diagonal_lru_connection(token.get_token_name(), upper_right_token.get_token_name())

                    # check and update diagonal LRD
                    if y != (ROWS-1):
                        lower_right_token = self.__board[y+1][(x+1)%(COLUMNS)]
                        if lower_right_token != 0:
                            if lower_right_token.get_player() == player:
                                player.add_diagonal_lrd_connection(token.get_token_name(), lower_right_token.get_token_name())
        
    
    def player_turn(self, drop_col, direction, rotation_row):
        
        self.__current_player = self.__players[self.__turn_number % len(self.__players)]

        if self.__print_game_stats:
            print(f"\n Turn {self.__turn_number} - {self.__current_player.get_text_colour()}Player {self.__current_player.get_number()}'s Turn{Style.RESET_ALL}")

        # Dropping the token
        self.drop_piece(col=drop_col, player=self.__current_player)
        
        self.__won, self.__win_direction, self.__win_tokens, self.__winner = self.get_current_player().check_win(self.__print_game_stats)

        # If the player chooses to rotate the board, rotate the board
        if direction != "no direction":
            self.rotate_board(direction=direction, row_index=rotation_row)

            if self.__print_game_stats:
                self.print_board()

            if self.__display_board:
                self.display_board()
            
            self.__won, self.__win_direction, self.__win_tokens, self.__winner = self.get_current_player().check_win(self.__print_game_stats)

        if self.__print_game_stats:
            self.print_board()

        if self.__display_board:
            self.display_board()

        self.__turn_number += 1

    def print_win_statistics(self):

        if self.__print_game_stats:
            winner_text_colour = self.__winner.get_text_colour()

            print(f"Winner: {winner_text_colour}Player {self.__winner.get_number()}{Style.RESET_ALL}")
            print(f"Turns: {winner_text_colour}{self.__turn_number}{Style.RESET_ALL}")
            print(f"Win Direction: {winner_text_colour}{self.__win_direction}{Style.RESET_ALL}")
            print(f"Win Tokens: {winner_text_colour}{self.__win_tokens}{Style.RESET_ALL}")

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
        directions = ["clockwise", "counterclockwise", "no direction"]

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

    def get_total_score(self):
        return self.__current_player.get_score_total()
    
    def run_minimax(self, depth):
        best_move, best_score = self.minimax(depth, True)
        return best_move, best_score

    def minimax(self, depth, maximizing_player):
        if depth == 0 or self.get_won():
            return None, self.get_total_score()

        if maximizing_player:
            max_score = float('-inf')
            possible_moves = self.calc_possible_moves()
            best_move = None

            for move in possible_moves:
                child_node = copy.deepcopy(self)
                child_node.player_turn(*move)
                _, score = child_node.minimax(depth - 1, False)
                if score > max_score:
                    max_score = score
                    best_move = move
            return best_move, max_score

        else:
            min_score = float('inf')
            possible_moves = self.calc_possible_moves()
            best_move = None

            for move in possible_moves:
                child_node = copy.deepcopy(self)
                child_node.player_turn(*move)
                _, score = child_node.minimax(depth - 1, True)
                if score < min_score:
                    min_score = score
                    best_move = move
            return best_move, min_score
    

def run_game():
    game = ConnectFourTwist(display_board=False, print_game_stats=False)
    possible_moves = game.calc_possible_moves()
    scored_moves = []


    for possible_move in possible_moves:
        # Create a copy of the game state for each possible move
        test_gamestate = copy.deepcopy(game)

        # Simulate the move on the copied game state
        drop_col, direction, rotation_row = possible_move
        test_gamestate.player_turn(drop_col=drop_col, direction=direction, rotation_row=rotation_row)

        # Calc score and add it to the list of scores
        move_score = test_gamestate.get_total_score()  
        scored_moves.append((possible_move, move_score))

    # Now scored_moves contains tuples of possible moves and their scores
    for move, score in scored_moves:
        print(f"Move: {move}, Score: {score}")

def run_minimax():
    game = ConnectFourTwist(display_board=False, print_game_stats=False)
    best_move, best_score = game.run_minimax(depth=3)  # Adjust depth as needed
    print(f"Best Move: {best_move}, Best Score: {best_score}")

run_minimax()

#run_game()
#run_minimax()