
# Constants
TOKENS_TO_WIN = 4
ROWS = 5
COLUMNS = 6

# This class represents the game state 

class ConnectFourTwist:
    def __init__(self, rows=ROWS, cols=COLUMNS):
        self.__rows = rows
        self.__cols = cols
        self.__board = [[0] * cols for x in range(rows)]
        
        self.__turn_number = 0
        self.__players = [1, 2]
        self.__winner = None
        self.__won = False
        
        self.__current_player = None
        self.__max_turns = 36

    def print_board(self):
        print("=====================")
        for row in self.__board:
            print(row)

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
            return True  # Rotation applied
        elif direction == "counterclockwise":
            self.__board[row_index] = self.__board[row_index][1:] + self.__board[row_index][:1]
            self.apply_gravity()
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
                self.__board[row][col] = player
                return True # piece is allowed to be dropped here
        return False # Col is full, cant drop piece 
    
    def check_gamestate(self, player):
        # Check horizontal
        for row in range(self.__rows):
            for col in range(self.__cols - 3):
                if self.__board[row][col] == player and \
                   self.__board[row][col + 1] == player and \
                   self.__board[row][col + 2] == player and \
                   self.__board[row][col + 3] == player:
                    self.__winner = player
                    self.__won = True
                    return True  

        # Check vertical
        for row in range(self.__rows - 3):
            for col in range(self.__cols):
                if self.__board[row][col] == player and \
                   self.__board[row + 1][col] == player and \
                   self.__board[row + 2][col] == player and \
                   self.__board[row + 3][col] == player:
                    self.__winner = player
                    self.__won = True
                    return True  

        # Check diagonals (top-left to bottom-right)
        for row in range(self.__rows - 3):
            for col in range(self.__cols - 3):
                if self.__board[row][col] == player and \
                   self.__board[row + 1][col + 1] == player and \
                   self.__board[row + 2][col + 2] == player and \
                   self.__board[row + 3][col + 3] == player:
                    self.__winner = player
                    self.__won = True
                    return True  

        # Check diagonals (top-right to bottom-left)
        for row in range(3, self.__rows):
            for col in range(self.__cols - 3):
                if self.__board[row][col] == player and \
                   self.__board[row - 1][col + 1] == player and \
                   self.__board[row - 2][col + 2] == player and \
                   self.__board[row - 3][col + 3] == player:
                    self.__winner = player
                    self.__won = True
                    return True  

        return False  # No win condition met
        
    
    def player_turn(self, drop_col, direction, rotation_row):
        if self.__turn_number == self.__max_turns:
            self.__state = "Draw"
            return 

        self.__current_player = self.__players[self.__turn_number % len(self.__players)]
        print(f"\n Turn {self.__turn_number} - Player {self.__current_player}'s Turn")

        self.drop_piece(col=drop_col, player=self.__current_player)
        self.print_board()
        self.rotate_board(direction=direction, row_index=rotation_row)
        self.print_board()
        
    
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

    while game.get_won() == False:
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
        

        
    
#test_vertical_win_condition()



