

class Token():

    def __init__(self, player, position):
        self.__player = player
        self.__symbol = self.__player.get_number()
        self.__colour = self.__player.get_colour()
        self.__position = position
        self.__token_name = str(position)
        self.__order = 0

    def update(self):
        self.__token_name = str(self.__position)

    def get_symbol(self):
        return self.__symbol
    
    def get_player(self):
        return self.__player
    
    def get_position(self):
        return self.__position
    
    def get_token_name(self):
        return self.__token_name
    
    def set_token_name(self, token_name):
        self.__token_name = token_name

    def set_position(self, position):
        self.__position = position

    