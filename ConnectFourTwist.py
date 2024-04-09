from colorama import Fore, Style
# Constants
TOKENS_TO_WIN = 4
ROWS = 5
COLUMNS = 6

# This class represents the game state 

from Player import Player 
from Token import Token

class ConnectFourTwist:
    def __init__(self, rows=ROWS, cols=COLUMNS):
        self.__rows = rows
        self.__cols = cols
        self.__board = [[0] * cols for x in range(rows)]
        
        self.__turn_number = 0
        self.__player1 = Player("red", 1)
        self.__player2 = Player("yellow", 2)
        self.__players = [self.__player1, self.__player2]
        self.__winner = None
        self.__won = False
        
        self.__current_player = None
        self.__max_turns = 36

    def print_board(self):
        print("=====================")
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
                        print(y+1)
                        upper_token = self.__board[y+1][(x)]
                        if upper_token != 0: # slot above is not empty
                            
                            print(f"upper token:{upper_token.get_position()}")
                            print(f"lower token:{token.get_position()}")
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



    
    def check_gamestate(self, player):
        # Check horizontal

        player.depth_first_search()
        

        
        return False  # No win condition met
        
    
    def player_turn(self, drop_col, direction, rotation_row, show_graph):
        
        self.__current_player = self.__players[self.__turn_number % len(self.__players)]

        print(f"\n Turn {self.__turn_number} - {self.__current_player.get_text_colour()}Player {self.__current_player.get_number()}'s Turn{Style.RESET_ALL}")

        # Dropping the token
        self.drop_piece(col=drop_col, player=self.__current_player)
        self.print_board()
        self.get_current_player().check_win()

        # If the player chooses to rotate the board, rotate the board
        if direction != "no direction":
            self.rotate_board(direction=direction, row_index=rotation_row)
            self.print_board()
            self.get_current_player().check_win()

        if show_graph:
            self.get_current_player().draw_graph()
        
        self.__turn_number += 1

    def print_win_statistics(self):
        print(f"Winner: {self.__winner}")
        print(f"Turns: {self.__turn_number}")

    def get_won(self):
        return self.__won
    
    def get_current_player(self):
        return self.__current_player


   
def test_vertical_win_condition():
    game = ConnectFourTwist()

    #while game.get_won() == False:
    for i in range(0, 4):
        # First player will place in column 0
        game.player_turn(0, "no direction", 0)
        if game.check_gamestate(game.get_current_player()):
            game.print_win_statistics()
            exit()
        
        # Second player will place in column 1
        game.player_turn(1, "no direction", 0) 
        if game.check_gamestate(game.get_current_player()):
            game.print_win_statistics()
            exit()

def test_vertical_win():
    game = ConnectFourTwist()
    
    game.player_turn(drop_col=0, direction="no direction", rotation_row=0, show_graph=False)
    game.player_turn(drop_col=1, direction="no direction", rotation_row=0, show_graph=False)
    game.player_turn(drop_col=0, direction="no direction", rotation_row=0, show_graph=False)
    game.player_turn(drop_col=1, direction="no direction", rotation_row=0, show_graph=False)
    game.player_turn(drop_col=0, direction="no direction", rotation_row=0, show_graph=False)
    game.player_turn(drop_col=1, direction="no direction", rotation_row=0, show_graph=False)
    game.player_turn(drop_col=0, direction="no direction", rotation_row=0, show_graph=True)
   
def test_vertical_paths():
    game = ConnectFourTwist()


    # stacks 3 high in postions 0 and 1
    game.player_turn(drop_col=0, direction="no direction", rotation_row=0, show_graph=False)
    game.player_turn(drop_col=1, direction="no direction", rotation_row=0, show_graph=False)
    game.player_turn(drop_col=0, direction="no direction", rotation_row=0, show_graph=False)
    game.player_turn(drop_col=1, direction="no direction", rotation_row=0, show_graph=False)
    game.player_turn(drop_col=0, direction="no direction", rotation_row=0, show_graph=False)
    game.player_turn(drop_col=1, direction="no direction", rotation_row=0, show_graph=False)

    

    # stacks 3 high in postions 4 and 
    game.player_turn(drop_col=4, direction="no direction", rotation_row=0, show_graph=False)
    game.player_turn(drop_col=5, direction="no direction", rotation_row=0, show_graph=False)
    game.player_turn(drop_col=4, direction="no direction", rotation_row=0, show_graph=False)
    game.player_turn(drop_col=5, direction="no direction", rotation_row=0, show_graph=False)
    game.player_turn(drop_col=4, direction="no direction", rotation_row=0, show_graph=True)
    game.player_turn(drop_col=5, direction="no direction", rotation_row=0, show_graph=True)

def test_what():
    game = ConnectFourTwist()

    game.player_turn(drop_col=0, direction="no direction", rotation_row=0, show_graph=True)
    game.player_turn(drop_col=1, direction="no direction", rotation_row=0, show_graph=True)
    game.player_turn(drop_col=0, direction="no direction", rotation_row=0, show_graph=True)
    game.player_turn(drop_col=1, direction="no direction", rotation_row=0, show_graph=True)

    game.player_turn(drop_col=2, direction="no direction", rotation_row=0, show_graph=True)
    game.player_turn(drop_col=3, direction="no direction", rotation_row=0, show_graph=True)
    game.player_turn(drop_col=2, direction="no direction", rotation_row=0, show_graph=True)
    game.player_turn(drop_col=3, direction="no direction", rotation_row=0, show_graph=True)

    game.player_turn(drop_col=1, direction="no direction", rotation_row=0, show_graph=True)
    game.player_turn(drop_col=2, direction="no direction", rotation_row=0, show_graph=True)

def test_alternating_horizontal():
    game = ConnectFourTwist()

    # Place Alternating Tokens on Row 0
    game.player_turn(drop_col=0, direction="no direction", rotation_row=0, show_graph=True)
    game.player_turn(drop_col=1, direction="no direction", rotation_row=0, show_graph=True)
    game.player_turn(drop_col=2, direction="no direction", rotation_row=0, show_graph=True)
    game.player_turn(drop_col=3, direction="no direction", rotation_row=0, show_graph=True)
    game.player_turn(drop_col=4, direction="no direction", rotation_row=0, show_graph=True)
    game.player_turn(drop_col=5, direction="no direction", rotation_row=0, show_graph=True)

    # Repeat Alternating Tokens on Row 1
    game.player_turn(drop_col=0, direction="no direction", rotation_row=0, show_graph=True)
    game.player_turn(drop_col=1, direction="no direction", rotation_row=0, show_graph=True)
    game.player_turn(drop_col=2, direction="no direction", rotation_row=0, show_graph=True)
    game.player_turn(drop_col=3, direction="no direction", rotation_row=0, show_graph=True)
    game.player_turn(drop_col=4, direction="no direction", rotation_row=0, show_graph=True)
    game.player_turn(drop_col=5, direction="no direction", rotation_row=0, show_graph=True)


#test_vertical_paths()
#test_vertical_win()
#test_what()
test_alternating_horizontal()

