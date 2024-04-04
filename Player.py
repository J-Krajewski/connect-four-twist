
import networkx as nx

class Player():

    def __init__(self, colour, number):
        
        self.__colour = colour
        self.__number = number
        self.__horizontal_lr_graph = nx.Graph()
        self.__tokens = ["A", "B", "C", "D", "E"]

    def update_graphs(self, token):
        print(token)
        
    def init_graph(self):
        self.__horizontal_lr_graph.add_nodes_from(self.__tokens)
        self.__horizontal_lr_graph.add_edge('A', 'B')
