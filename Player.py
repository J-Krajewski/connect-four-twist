from colorama import Fore, Style

class Player():

    def __init__(self, colour, number, name):
        self.__colour = colour
        self.__number = number
        self.__name = name
        self.__text_colour = self.init_text_colour()
        
    def init_text_colour(self):
        if self.__colour == "red":
            return Fore.RED
        elif self.__colour == "yellow":
            return Fore.YELLOW

    def get_number(self):
        return self.__number
    
    def get_colour(self):
        return self.__colour
    
    def get_text_colour(self):
        return self.__text_colour
    



   

