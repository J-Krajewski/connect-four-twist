from colorama import Fore, Style
import networkx as nx
import matplotlib.pyplot as plt
from Token import Token

class Player():

    def __init__(self, colour, number):
        self.__colour = colour
        self.__number = number
        self.__graph = nx.DiGraph()
        self.__text_colour = self.init_text_colour()
        self.__placed_tokens = []

    def init_text_colour(self):
        if self.__colour == "red":
            return Fore.RED
        elif self.__colour == "yellow":
            return Fore.YELLOW


    def update_graphs(self, token):
        print(token)

    def add_token(self, token):
        self.__graph.add_node(token)
        self.__placed_tokens.append(token)
        
    def add_horizontal_connection(self, left_token, right_token):
        self.__graph.add_edge(left_token, right_token, labels="horizontal")
        
    def add_vertical_connection(self, lower_token, upper_token):
        self.__graph.add_edge(lower_token, upper_token, labels="vertical")

    def add_diagonal_lru_connection(self, lower_token, upper_token):
        self.__graph.add_edge(lower_token, upper_token, labels="diagonal lru")

    def add_diagonal_lrd_connection(self, lower_token, upper_token):
        self.__graph.add_edge(lower_token, upper_token, labels="diagonal lrd")



    def longest_path_with_label(self, label):
        longest_paths = []
        max_length = 0

        for node in self.__graph.nodes:
            target_nodes = set(self.__graph.nodes) - {node}  # Exclude the starting node
            for target in target_nodes:
                for path in nx.all_simple_paths(self.__graph, source=node, target=target):
                    if all(self.__graph.edges[path[i], path[i+1]]['labels'] == label for i in range(len(path)-1)):
                        path_length = len(path)
                        if path_length > max_length:
                            max_length = path_length
                            longest_paths = [path]
                        elif path_length == max_length:
                            longest_paths.append(path)


        #print(f"{label}: {longest_paths}")
        return longest_paths

    
    def check_win(self):
        labels = ["horizontal", "vertical", "diagonal lru", "diagonal lrd"]
        paths_dict = {}

        for label in labels:
            paths = self.longest_path_with_label(label)
            paths_dict[label] = paths

        for label, paths in paths_dict.items():
            for path in paths:
                if len(path) >= 4:
                    print("GAME WON")
                    return True, label, path, self
    


        print(paths_dict)

        return False, None, None, None

        

    def draw_graph(self, ax):
        #nx.draw(self.__graph, with_labels=True, node_color = self.__colour)
        #plt.show()

        #pos = nx.spring_layout(self.__graph)  # Layout for better visualization
        #nx.draw(self.__graph, pos, with_labels=True, node_color=self.__colour)
        #edge_labels = nx.get_edge_attributes(self.__graph, 'labels')
        #nx.draw_networkx_edge_labels(self.__graph, pos, edge_labels=edge_labels)

        #plt.show()

        #pos = nx.spring_layout(self.__graph)  # Layout for better visualization
        #nx.draw(self.__graph, pos, with_labels=True, node_color=self.__colour)
        #edge_labels = nx.get_edge_attributes(self.__graph, 'labels')
        #nx.draw_networkx_edge_labels(self.__graph, pos, edge_labels=edge_labels)

        pos = nx.spring_layout(self.__graph)  # Layout for better visualization
        nx.draw(self.__graph, pos, with_labels=True, node_color=self.__colour, ax=ax)
        edge_labels = nx.get_edge_attributes(self.__graph, 'labels')
        nx.draw_networkx_edge_labels(self.__graph, pos, edge_labels=edge_labels, ax=ax)
        ax.set_title('Graph')  # Add a title to the graph

    def get_graph(self):
        return self.__graph
    
    def get_number(self):
        return self.__number
    
    def get_colour(self):
        return self.__colour
    
    def get_text_colour(self):
        return self.__text_colour


def test_graphs():
    player1 = Player("red", 1)
    player2 = Player("yellow", 2)

    player1.init_graph()
    player2.init_graph()
    player1.add_horizontal_connection(left_token="A", right_token="B")
    player1.add_horizontal_connection(left_token="B", right_token="C")

    player2.add_horizontal_connection(left_token="A", right_token="B")
    player2.add_horizontal_connection(left_token="B", right_token="C")

    player1.draw_graph()
    player2.draw_graph()

