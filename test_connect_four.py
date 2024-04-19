import unittest
import time
from ConnectFourTwist import ConnectFourTwist

TOKENS_TO_WIN = 4
ROWS = 5
COLUMNS = 6

class TestConnectFour(unittest.TestCase):

    '''
    Testing that the number of possible moves are correct 
    '''
    def test_possible_moves(self):
        game = ConnectFourTwist(display_board=False, print_game_stats=False)
        possible_moves = game.get_possible_moves()
        self.assertTrue(len(possible_moves) == 2 * ROWS + COLUMNS)
        # Add more assertions as needed

    def test_alternating_horizontal(self):
        game = ConnectFourTwist(display_board=False, print_game_stats=False)

        col = 0
        while game.get_won() == False:
            col = col % COLUMNS
            
            game.player_turn(drop_col=col, direction="no direction", rotation_row=0)
            col += 1
        else:
            #print(game.print_win_statistics())

            self.assertTrue(game.get_winner().get_number() == 1)
            self.assertTrue(game.get_win_tokens() == {'[0, 3]', '[0, 0]', '[0, 2]', '[0, 1]'})
            self.assertTrue(game.get_win_direction() == 'vertical')
            self.assertTrue(game.get_turn_number() == 19)

    def test_checkerboard(self):
        game = ConnectFourTwist(display_board=False, print_game_stats=False)
        count = 0
        col = 0
        while game.get_won() == False:
            col = col % ROWS
            count += 1
            
            game.player_turn(drop_col=col, direction="no direction", rotation_row=0)

            if count > ROWS - 1:
                count = 0
                col += 1
            
        else:
            #print(game.print_win_statistics())

            self.assertTrue(game.get_winner().get_number() == 2)
            self.assertTrue(game.get_win_tokens() == {'[0, 3]', '[2, 1]', '[1, 2]', '[3, 0]'})
            self.assertTrue(game.get_win_direction() == 'diagonal lrd')
            self.assertTrue(game.get_turn_number() == 16)

    def test_horizontal_lines(self):
        game = ConnectFourTwist(display_board=False, print_game_stats=False)
        count = 0
        col = 0
        while game.get_won() == False:
            col = col % ROWS
            count += 1
            
            game.player_turn(drop_col=col, direction="no direction", rotation_row=0)

            if count > 1:
                count = 0
                col += 1
            
        else:
            
            #print(game.print_win_statistics())
            
            self.assertTrue(game.get_winner().get_number() == 1)
            self.assertTrue(game.get_win_tokens() == {'[0, 0]', '[3, 0]', '[1, 0]', '[2, 0]'})
            self.assertTrue(game.get_win_direction() == 'horizontal')
            self.assertTrue(game.get_turn_number() == 7)

if __name__ == '__main__':
    unittest.main()
