import unittest
from ConnectFourTwist import ConnectFourTwist

class TestConnectFourTwist(unittest.TestCase):
    def test_vertical_win_condition(self):
        game = ConnectFourTwist()

        # First player will place in column 0
        game.player_turn(0, "no direction", 0)
        game.check_gamestate(game.get_current_player())
        self.assertFalse(game.get_won())  # Game should not be won yet
        
        # Second player will place in column 1
        game.player_turn(1, "no direction", 0)
        game.check_gamestate(game.get_current_player())
        self.assertFalse(game.get_won())  # Game should not be won yet

        # First player will place in column 0
        game.player_turn(0, "no direction", 0)
        game.check_gamestate(game.get_current_player())
        self.assertFalse(game.get_won())  # Game should not be won yet

        # Second player will place in column 1
        game.player_turn(1, "no direction", 0)
        game.check_gamestate(game.get_current_player())
        self.assertFalse(game.get_won())  

        # First player will place in column 0
        game.player_turn(0, "no direction", 0)
        game.check_gamestate(game.get_current_player())
        self.assertFalse(game.get_won())  # Game should not be won yet

        # etc 
        game.player_turn(1, "no direction", 0)
        game.check_gamestate(game.get_current_player())
        self.assertFalse(game.get_won())  # Game should not be won yet

       
        game.player_turn(0, "no direction", 0)
        game.check_gamestate(game.get_current_player())
        self.assertTrue(game.get_won())  # Game should be won

