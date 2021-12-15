
from typing import List
from dataclasses import dataclass
from collections import defaultdict

MAX = 9

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
        return Colours.wrap(color, f"{x:1}")
    else:
        return f"{x:1}"


def BFS_SP(grid, graph, start, goal):
    explored = []
    # Queue for traversing the
    # graph in the BFS
    queue = [[start]]
    # If the desired node is
    # reached
    if start == goal:
        print("Same Node")
        return
    # Loop to traverse the graph
    # with the help of the queue
    all_paths = []
    while queue:
        path = queue.pop(0)
        node = path[-1]
        # Condition to check if the
        # current node is not visited
        if node not in explored:
            neighbours = graph[node]
            # Loop to iterate over the
            # neighbours of the node
            if node == (0, 0):
                print("neighbours", neighbours)
            weights = [
                (grid.rows[neighbour[0]][neighbour[1]], neighbour)
                for neighbour in neighbours
            ]

            #if node[0] == 0:
            print("w", weights)
            weights.sort(reverse=False, key=lambda x: x[0])
            print("WEIGHTS ", weights)

            weights = list(filter(lambda x: x[1] not in path, weights))
            #print("Filtered WEIGHTS ", node, weights)
            
            #for prev in path:
            #    if weights[0][1] == prev:
            #        weights.remove()

            print(node)

            #if node == (1, 3):
            #    return path

            #if node == (0, 0):
            
            print("weights", weights)
            print("-- Weights", weights)
            lowest = weights[0][0]
            print(" -- lowest", lowest)
            lowest_weights = list(reversed(list(filter(lambda x: x[0] == lowest, weights))))
            print(" -- low weights", lowest_weights)

            for neighbour in neighbours:
                #if node == (0,0):
                print(" -- checking", node, "->", neighbour)
                if neighbour in path:
                    #if node == (0, 1):
                    #    print("Skipping ", neighbour, "in path", path)
                    continue
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                # Condition to check if the
                # neighbour node is the goal
                if neighbour == goal:
                    print("Shortest path = ", *new_path)
                    all_paths.append([*new_path])
            explored.append(node)

    # Condition when the nodes
    # are not connected
    for path in all_paths:
        print("Path", path)
    print("So sorry, but a connecting path doesn't exist :(", path)
    return all_paths


@dataclass
class Grid:
    rows: List[List[int]]

    def __str__(self):
        output = f"BOARD\n"
        output += "- "
        output += " ".join([
            format(x, color=Colours.blue)
            for x in range(len(self.rows[0]))]
        ) + "\n"
        for i, row in enumerate(self.rows):
            output += format(i, color=Colours.blue) + " "
            output += " ".join(format(x) for x in row) + "\n"
        return output

    def with_path(self, paths):
        output = f"BOARD\n"
        output += "- "
        output += " ".join([
            format(x, color=Colours.blue)
            for x in range(len(self.rows[0]))]
        ) + "\n"
        for i, row in enumerate(self.rows):
            output += format(i, color=Colours.blue) + " "
            output += " ".join(self.format_in_path(x, i, j, paths) for j, x in enumerate(row)) + "\n"
        return output

    def format_in_path(self, val, i, j, paths):
        if (i, j) in paths:
            return Colours.wrap(Colours.red, f"{val:1}")
        else:
            return f"{val:1}"

    def add_points(self, p1, p2):
        return (p1[0] + p2[0], p1[1] + p2[1])

    def get_neighbours(self, i, j, ignored):
        points_around = [
            self.add_points((i, j), p) for p in [
                (0, 1),
                (1, 0),
                (0, -1),
                (-1, 0),
                #(1, 1),
                #(-1, -1),
                #(-1, 1),
                #(1, -1),
            ]
        ]

        if ignored and ignored in points_around:
            points_around.remove(ignored)

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
                weight = self.rows[i][j]
                neighbours = self.get_neighbours(i, j, None)
                for neighbour in neighbours: 
                    routes[(i ,j)].append(neighbour)
        return routes

    def traverse(self, i=0, j=0, ignored=None):

        neighbours = self.get_neighbours(i, j, ignored=ignored)

        val_here = self.rows[i][j]

        print(f"We are at i={i} j={j} {val_here}")

        routes = []

        for other in neighbours:
            other_sum = self.rows[other[0]][other[1]]
            
            print(f"Neighbour   {other}", other_sum)

            routes.append(
                [val_here] + self.traverse(other[0], other[1], ignored=(i, j))
            )

        return routes
        


def process(test_data):
    grid = Grid(test_data)

    print(grid)

    graph = grid.graph()
    #for k, v in nodes.items():
    #    print(k, v)

    graph = {
        'G': ['C'], 
        'F': ['C'], 
        'E': ['A', 'B', 'D'], 
        'A': ['B', 'E', 'C'], 
        'B': ['A', 'D', 'E'], 
        'D': ['B', 'E'], 
        'C': ['A', 'F', 'G']
    }

    visitedList = [[]]

    def depthFirst(graph, currentVertex, targetVertex, visited):
        visited.append(currentVertex)
        for vertex in graph[currentVertex]:
            if vertex not in visited:
                depthFirst(graph, vertex, targetVertex, visited.copy())
        visitedList.append(visited)

    depthFirst(graph, 'F', (2, 2), [])

    print(visitedList[0])

    #all_paths = BFS_SP(grid, nodes, (0, 0), (9, 9))
#
    #if not all_paths:
    #    raise Exception("No paths found")
#
    #for path in all_paths:
    #    print(grid.with_path(path))

    return -1


def process_instructions(test_data):

    test_data = [td for td in test_data.split("\n") if td]

    test_data = [[int(t) for t in td] for td in test_data if td]

    return process(test_data)


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
    result = process_instructions(test_instructions)
    assert result == 99999


def test_day_real_input():
    test_instructions = open("day3_input").read()
    result = process_instructions(test_instructions)
    assert result == 99999

if __name__ == "__main__":
    test_day_short_input()
    #test_day_real_input()