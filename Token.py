

class Token():

    def __init__(self, order, player):
        self.__player = player
        self.__order = order
        self.__symbol = self.apply_symbol(player)
        self.__colour = self.apply_colour(player)

    def apply_symbol(self, player):   
        if player == 1:
            return "X"
        if player == 2:
            return "O" 

    def apply_colour(self, player):
        if player == 1:
            return "red"
        if player == 2:
            return "yellow"