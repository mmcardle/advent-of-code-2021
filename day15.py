
from typing import List
from dataclasses import dataclass
from collections import defaultdict
from multiprocessing import Pool


class Colours:
    green = "\033[92m"
    red = "\033[91m"
    blue = "\033[0;34m"
    endc = "\033[0m"
    
    @classmethod
    def wrap(cls, color, text):
        return color + text + cls.endc


def format(x, color=None):
    if color:
        return Colours.wrap(color, f"{x:2}")
    else:
        return f"{x:2}"

def red(t):
    return Colours.wrap(Colours.red, t)


def green(t):
    return Colours.wrap(Colours.green, t)


@dataclass
class Grid:
    rows: List[List[int]]

    def __str__(self):
        output = f"BOARD\n"
        output += " - "
        output += "".join([
            format(x, color=Colours.blue)
            for x in range(len(self.rows[0]))]
        ) + "\n"
        for i, row in enumerate(self.rows):
            output += format(i, color=Colours.blue) + " "
            output += "".join(format(x) for x in row) + "\n"
        return output

    def with_path(self, paths):
        output = f"BOARD\n"
        output += " - "
        output += "".join([
            format(x, color=Colours.blue)
            for x in range(len(self.rows[0]))]
        ) + "\n"
        for i, row in enumerate(self.rows):
            output += format(i, color=Colours.blue) + " "
            output += "".join(self.format_in_path(x, i, j, paths) for j, x in enumerate(row)) + "\n"
        return output

    def format_in_path(self, val, i, j, paths):
        if (i, j) in paths:
            return Colours.wrap(Colours.red, f"{val:2}")
        else:
            return f"{val:2}"

    def add_points(self, p1, p2):
        return (p1[0] + p2[0], p1[1] + p2[1])

    def get_neighbours(self, i, j):
        points_around = [
            self.add_points((i, j), p) for p in [
                (0, 1),
                (1, 0),
                (0, -1),
                (-1, 0),
            ]
        ]

        all_points_in_range = [
            p
            for p in points_around
            if p[0] >= 0
            and p[1] >= 0
            and p[0] < len(self.rows)
            and p[1] < len(self.rows[i])
        ]
        return set(all_points_in_range)

    def graph(self):
        routes = defaultdict(list)
        for i, row in enumerate(self.rows):
            for j, val in enumerate(row):
                neighbours = self.get_neighbours(i, j)
                if neighbours:
                    for neighbour in neighbours:
                        neighbour_val = self.rows[neighbour[0]][neighbour[1]]
                        routes[(i ,j)].append((neighbour[0], neighbour[1], neighbour_val))
                else:
                    routes[(i, j)] = []
        return routes

    def graph_list(self):
        routes = []
        for i, row in enumerate(self.rows):
            for j, val in enumerate(row):
                neighbours = self.get_neighbours(i, j)
                if neighbours:
                    for neighbour in neighbours:
                        neighbour_val = self.rows[neighbour[0]][neighbour[1]]
                        routes.append(((i, j), (neighbour[0], neighbour[1]), neighbour_val))
                else:
                    routes.append(((i, j), None, None))
        return routes


import sys
 
class Graph(object):
    def __init__(self, nodes, init_graph):
        self.nodes = nodes
        self.graph = self.construct_graph(nodes, init_graph)
        
    def construct_graph(self, nodes, init_graph):
        '''
        This method makes sure that the graph is symmetrical. In other words, if there's a path from node A to B with a value V, there needs to be a path from node B to node A with a value V.
        '''
        graph = {}
        for node in nodes:
            graph[node] = {}
        
        graph.update(init_graph)
        
        for node, edges in graph.items():
            for adjacent_node, value in edges.items():
                if graph[adjacent_node].get(node, False) == False:
                    graph[adjacent_node][node] = value
                    
        return graph
    
    def get_nodes(self):
        "Returns the nodes of the graph."
        return self.nodes
    
    def get_outgoing_edges(self, node):
        "Returns the neighbors of a node."
        connections = []
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False) != False:
                connections.append(out_node)
        return connections
    
    def value(self, node1, node2):
        "Returns the value of an edge between two nodes."
        return self.graph[node1][node2]


def dijkstra_algorithm(graph, start_node):
    unvisited_nodes = list(graph.get_nodes())
 
    # We'll use this dict to save the cost of visiting each node and update it as we move along the graph   
    shortest_path = {}
 
    # We'll use this dict to save the shortest known path to a node found so far
    previous_nodes = {}
 
    # We'll use max_value to initialize the "infinity" value of the unvisited nodes   
    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    # However, we initialize the starting node's value with 0   
    shortest_path[start_node] = 0
    
    # The algorithm executes until we visit all nodes
    while unvisited_nodes:
        # The code block below finds the node with the lowest score
        current_min_node = None
        for node in unvisited_nodes: # Iterate over the nodes
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node
                
        # The code block below retrieves the current node's neighbors and updates their distances
        neighbors = graph.get_outgoing_edges(current_min_node)
        for neighbor in neighbors:
            tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                # We also update the best path to the current node
                previous_nodes[neighbor] = current_min_node
 
        # After visiting its neighbors, we mark the node as "visited"
        unvisited_nodes.remove(current_min_node)
    
    return previous_nodes, shortest_path


def get_shortest(previous_nodes, shortest_path, start_node, target_node):
    path = []
    node = target_node
    
    while node != start_node:
        path.append(node)
        node = previous_nodes[node]
 
    # Add the start node manually
    path.append(start_node)

    shortest = shortest_path[target_node]
    print("We found the following best path with a value of {}.".format(shortest))
    print(" -> ".join(str(x) for x in reversed(path)))

    return shortest, path

def tester():
    nodes = ["Reykjavik", "Oslo", "Moscow", "London", "Rome", "Berlin", "Belgrade", "Athens"]
 
    init_graph = {}
    for node in nodes:
        init_graph[node] = {}
        
    init_graph["Reykjavik"]["Oslo"] = 5
    init_graph["Reykjavik"]["London"] = 4
    init_graph["Oslo"]["Berlin"] = 1
    init_graph["Oslo"]["Moscow"] = 3
    init_graph["Moscow"]["Belgrade"] = 5
    init_graph["Moscow"]["Athens"] = 4
    init_graph["Athens"]["Belgrade"] = 1
    init_graph["Rome"]["Berlin"] = 2
    init_graph["Rome"]["Athens"] = 2

    graph = Graph(nodes, init_graph)
    previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node="Reykjavik")

    get_shortest(previous_nodes, shortest_path, start_node="Reykjavik", target_node="Belgrade")


def process(init_test_data, n = 1):

    print(Grid(init_test_data))
    extended_cols = []
    for row in init_test_data:
        print(row)
        long_row = []
        for i in range(n):
            long_row.extend([v + i for v in row])
        long_row = [v - 9 if v > 9 else v for v in long_row]
        extended_cols.append(long_row)

    test_data = []
    for i in range(n):
        for long_row in extended_cols:
            long_row = [v + i for v in long_row]
            long_row = [v-9 if v > 9 else v for v in long_row]
            test_data.append(long_row)

    grid = Grid(test_data)
    print(grid)
    graph = grid.graph()

    nodes = graph.keys()
 
    init_graph = {}
    for node in graph.keys():
        init_graph[node] = {}
        for neighbor in graph[node]:
            n1, n2, risk = neighbor
            init_graph[node][(n1, n2)] = risk
    
    graph = Graph(nodes, init_graph)
    start_node = (0, 0)
    end_node = (len(test_data) - 1, len(test_data[0]) - 1)
    print(start_node, end_node)
    previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node=start_node)

    shortest, path = get_shortest(previous_nodes, shortest_path, start_node=start_node, target_node=end_node)

    print(grid.with_path(path))
    risks = [grid.rows[i][j] for i,j in path if (i ,j) not in [start_node]]

    print(sum(risks))

    return sum(risks)

def process_instructions(test_data, n=1):
    test_data = [td for td in test_data.split("\n") if td]
    test_data = [[int(t) for t in td] for td in test_data if td]
    return process(test_data, n=n)


def test_day_short_input():
    test_instructions = """
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""
    result = process_instructions(test_instructions, n = 5)
    assert result == 315

def test_day_very_short_input():
    test_instructions = """
11634
13813
21367
36942
"""
    result = process_instructions(test_instructions, n = 5)
    assert result == 19

def test_day_real_input():
    test_instructions = open("day15_input").read()
    result = process_instructions(test_instructions)
    assert result == 621, result
    result = process_instructions(test_instructions, n = 5)
    assert result == 1025

if __name__ == "__main__":
    #test_day_very_short_input()
    #test_day_short_input()
    test_day_real_input()