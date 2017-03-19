"""
ThoughtWorks Trains Solution

author: Fernando Felix do Nascimento Junior
year: 2017
"""
from collections import defaultdict


class Graph:
    """ An unidireccional distance graph. This is a very simple implementation, it may only add nodes and edges"""

    def __init__(self, distances_str=None):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}

        if distances_str:
            self.add_edges(distances_str.replace(" ", "").split(","))

    def distance(self, from_node, to_node):
        """ Return a distance between two nodes """
        return self.distances[(from_node, to_node)]

    def add_edges(self, node_pair_distance_arrs):
        """ Add edges from an array of node_pair_distances array: [from node, to_node, distance] """
        for node_pair_distance_arr in node_pair_distance_arrs:
            self.add_edge(node_pair_distance_arr[0], node_pair_distance_arr[1], int(node_pair_distance_arr[2]))

    def add_node(self, node):
        """ Add node into graph nodes """
        self.nodes.add(node)

    def add_edge(self, from_node, to_node, distance):
        """ Add a distance edge between from_node and to_node"""
        self.add_node(from_node)
        self.add_node(to_node)
        self.edges[from_node].append(to_node)
        self.distances[(from_node, to_node)] = distance


def route_distance(graph, route, exception_message="NO SUCH ROUTE"):
    """ Return the total route distance given a distance graph """
    route = route.replace("-", "")
    edges = [(route[i], route[i + 1]) for i in range(len(route)) if i < len(route) - 1]
    try:
        return str(sum([graph.distances[edge] for edge in edges]))
    except:
        return exception_message


def shortest_route_distance(graph, start_node, end_node):
    """
    Giving a distance graph, return the shortest route distance between a starting and ending routes without repetition.
    It's based on nearest neighbour algorithm. https://en.wikipedia.org/wiki/Nearest_neighbour_algorithm
    """
    route = ""
    total_distance = 0

    current_node = start_node
    route = route + current_node

    def nearest_neighbor(node):
        ''' Return the nearest neighbor of a node '''
        min_distance = float('Inf')
        nearest = None

        for neighbor in graph.edges[node]:
            distance = graph.distance(node, neighbor)
            if distance < min_distance:
                min_distance = distance
                nearest = neighbor

        return nearest, min_distance

    while True:
        nearest_node, nearest_distance = nearest_neighbor(current_node)
        route = route + nearest_node
        total_distance = total_distance + nearest_distance
        current_node = nearest_node
        if current_node is end_node:
            break

    return total_distance


def count_routes_by_stops(graph, start_node, end_node, stops, operator="<=", _route=""):
    """
    Giving a distance graph, count routes recursively between a start node and an end node based on number of stops
    criterion (operator). For example, given a starting route at C and an ending at C, count and return the number of
    routes (or trips) with a maximum (operator=="<=") of stops=3.
    """
    _route = _route + start_node
    count = 0
    current_stops = len(_route) - 1  # similar to number of edges

    for neighbor in graph.edges[start_node]:
        if current_stops > stops:
            break

        if neighbor == end_node:
            _route = _route + end_node
            if(eval(str(current_stops) + operator + str(stops))):
                count += 1
                break

        count += count_routes_by_stops(graph, neighbor, end_node, stops, operator=operator, _route=_route)

    return count


def count_routes_by_max_distance(graph, start_node, end_node, max_distance=30, _route=""):
    """
    Count routes recursively between a start node and an end node based on a maximum distance criterion. For example,
    given a starting route at C and an ending at C, count and return the number of different routes with a distance of
    less than 30, ie, maximum distance==30.
    """
    _route = _route + start_node
    count = 0

    for neighbor in graph.edges[start_node]:
        distance = int(route_distance(graph, _route + neighbor, exception_message=0))

        if distance and distance >= max_distance:
            break

        if neighbor == end_node:
            count += 1

        count += count_routes_by_max_distance(graph, neighbor, end_node, max_distance=max_distance, _route=_route)
    return count


if __name__ == '__main__':
    g = Graph("AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7")
    print(shortest_route_distance(g, 'B', 'B'))
    print(count_routes_by_max_distance(g, 'C', 'C', max_distance=30))
