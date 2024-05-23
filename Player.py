from colorama import Fore, Style
import decimal

class Player():

    def __init__(self, colour, number, name, strategy, depth):
        self.__colour = colour
        self.__number = number
        self.__name = name
        self.__strategy = strategy
        self.__depth = depth
        self.__text_colour = self.init_text_colour()
        self.__turn_times = []
        self.__turn_nodes = []
        
        self.__opp_number = self.find_opp_number()

    def find_opp_number(self):

        if self.__number == 1:
            return 2
        elif self.__number == 2:
            return 1

        
    def run_strategy(self, game, board, turn):
        output = self.__strategy(game, board, turn, self.__depth, self.__number, self.__opp_number)
                                
        return output

    def add_player_info(self, row):
        # Dont add this information if the player is human or random 
        non_metric_players = ["Random", "Player", "Greedy", "Random1", "Random2"]

        if self.__name in non_metric_players:
            return row
        else:
            player_depth = self.__depth
            turn_times = self.__turn_times
            turn_nodes = self.__turn_nodes
            turn_times_average = self.calculate_average_turn_value(turn_times)
            turn_nodes_average = self.calculate_average_turn_value(turn_nodes)
            columns = player_depth, turn_times, turn_times_average, turn_nodes, turn_nodes_average

            print(f"{self.__name} - {columns}")

            for data_column in columns:
                row.append(data_column)
            
            #print(f"{self.__name} - {row}")
            return row
        
    def init_text_colour(self):
        if self.__colour == "red":
            return Fore.RED
        elif self.__colour == "yellow":
            return Fore.YELLOW
    
    def calculate_average_turn_value(self, turn_array):
        if not turn_array:
            return 0
        
        total_value = sum(turn_array)
        average_value = total_value / len(turn_array)
        print(f"{average_value} = {total_value} / {len(turn_array)}")

        average_value = round(average_value, 2)
        return average_value
    
    def add_turn_time(self, time):
        #time = decimal.Decimal(time)  
        
        # rounding off  
        #time = time.quantize(decimal.Decimal('0.00'))  

        time = round(time, 4)
        self.__turn_times.append(time)

    def add_turn_nodes(self, node_count):
        self.__turn_nodes.append(node_count)
    
    def get_name(self):
        return self.__name

    def get_number(self):
        return self.__number
    
    def get_colour(self):
        return self.__colour
    
    def get_text_colour(self):
        return self.__text_colour
    
    def get_turn_times(self):
        return self.__turn_times
    
    def get_turn_nodes(self):
        return self.__turn_nodes

    def get_depth(self):
        return self.__depth
