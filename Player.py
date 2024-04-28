from colorama import Fore, Style
import networkx as nx
import matplotlib.pyplot as plt
from Token import Token

TWO_NODES_CONNECTED_SCORE = 20
THREE_NODES_CONNECTED_SCORE = 80
FOUR_NODES_CONNECTED_SCORE = 1000


SCORE_PER_CONNECTED_NODE = 5
LABELS = ["horizontal", "vertical", "diagonal lru", "diagonal lrd"]

class Player():

    def __init__(self, colour, number):
        self.__colour = colour
        self.__number = number
        self.__graph = nx.DiGraph()
        self.__text_colour = self.init_text_colour()
        self.__placed_tokens = []
        self.__paths = None
        self.__paths_scored = None
        self.__score_total = 0

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

    def print_path_info(self):
        
        print(f"Player {self.__number} Paths: ")
        for label in LABELS:
            print(f"{label}: {self.__paths[label]}  - SCORE {self.__paths_scored[label]}")
            #print(f"{label}: {self.__paths_scored[label]}")

        #print(f"Player {self.__number} Path Scores:")
        #for label in LABELS:
        #    print(f"{label}: {self.__paths_scored[label]}")

        print(f"Total Path Score: {self.__score_total}")


    def clear(self):
        self.nodes.clear()
        self.edges.clear()

    
    def all_paths_with_label(self, label):
        all_paths = []

        for node in self.__graph.nodes:
            target_nodes = set(self.__graph.nodes) - {node}  # Exclude the starting node
            for target in target_nodes:
                for path in nx.all_simple_paths(self.__graph, source=node, target=target):
                    if all(self.__graph.edges[path[i], path[i+1]]['labels'] == label for i in range(len(path) - 1)):
                        # Convert the path to a set and add it to all_paths
                        path_set = set(path)
                        all_paths.append(path_set)

        all_paths2 = all_paths[:]

        for m in all_paths:
            for n in all_paths:
                if set(m).issubset(set(n)) and m != n:
                    all_paths2.remove(m)
                    break


        return all_paths2

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
    

    
    def calculate_path_scores(self):
        # Reset path scores and the total
        score = 0
        self.__paths_scored = {}
        self.__score_total = 0

        # Calculate scores for each path label
        for label in ["horizontal", "vertical", "diagonal lru", "diagonal lrd"]:
            #paths = self.longest_path_with_label(label)
            paths = self.all_paths_with_label(label)

            #print(paths)
            #score = sum(len(path) * SCORE_PER_CONNECTED_NODE for path in paths)
            # Exponential Scoring 
            #score = sum(len(path) ** 3 * SCORE_PER_CONNECTED_NODE for path in paths)

            if any(len(path) == 2 for path in paths):
                score += TWO_NODES_CONNECTED_SCORE

            if any(len(path) == 3 for path in paths):
                score += THREE_NODES_CONNECTED_SCORE

            # Assign very high score for a win
            if any(len(path) == 4 for path in paths):
                score += FOUR_NODES_CONNECTED_SCORE

            self.__paths_scored[label] = score
            self.__score_total += score
            score = 0

        return self.__score_total


    def check_win(self, print_game_stats):
        labels = ["horizontal", "vertical", "diagonal lru", "diagonal lrd"]
        paths_dict = {}
        
        for label in labels:
            paths = self.all_paths_with_label(label)
            paths_dict[label] = paths
            #paths_scored.append(len(paths) * SCORE_PER_CONNECTED_NODE)

        for label, paths in paths_dict.items():
            for path in paths:
                if len(path) >= 4:
                    if print_game_stats:
                        print("GAME WON")
                    # Returning: If the game is won, how the game is won, the nodes that won and the player object
                    
                    return True, label, path, self
    

        self.calculate_path_scores()
        self.__paths = paths_dict

        if print_game_stats:
            self.print_path_info()
        

        return False, None, None, None

    def draw_graph(self, ax):
        
        pos = nx.spring_layout(self.__graph)  # Layout for better visualization
        nx.draw(self.__graph, pos, with_labels=True, node_color=self.__colour, ax=ax)
        edge_labels = nx.get_edge_attributes(self.__graph, 'labels')
        nx.draw_networkx_edge_labels(self.__graph, pos, edge_labels=edge_labels, ax=ax)
        ax.set_title(f'Player {self.__number} Graph')  # Add a title to the graph

    def get_graph(self):
        return self.__graph
    
    def get_number(self):
        return self.__number
    
    def get_colour(self):
        return self.__colour
    
    def get_text_colour(self):
        return self.__text_colour
    
    def get_path_scored(self):
        return self.__paths_scored
    
    def get_score_total(self):
        return self.__score_total
    

    def reset_graph(self):
        self.__graph = nx.DiGraph()


    def remove_token(self, token):
         if token in self.__graph.nodes:
            # Iterate over the edges in the graph
            for edge in list(self.__graph.edges):
                # Check if the edge is associated with the token
                if token in edge:
                    # Remove the edge from the graph
                    self.__graph.remove_edge(*edge)

            # Remove the token from the graph
            self.__graph.remove_node(token)

    def get_all_elements(self):
        # Get all nodes (tokens) in the graph
        nodes = list(self.__graph.nodes)
        
        # Get all edges (connections) in the graph
        edges = list(self.__graph.edges)
        
        return nodes, edges

