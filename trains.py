"""
ThoughtWorks Trains Solution.

author: Fernando Felix do Nascimento Junior
year: 2017
"""
from collections import defaultdict
import operator


class Graph:
    """ An unidireccional distance graph. This is a very simple implementation, it may only add nodes and edges"""

    def __init__(self, distances_str=None):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}

    def distance(self, from_node, to_node):
        """ Return a distance between two nodes """
        return self.distances[(from_node, to_node)]

    def get_neighbor_distances(self, from_node):
        """ Return the node neighboor distances """
        return {to_node: self.distance(from_node, to_node) for to_node in self.edges[from_node]}

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


def sort_neighbor_distances(graph, node, reverse=False):
    ''' Return the sorted neighbor distances of a node '''
    neighbor_distances = graph.get_neighbor_distances(node).items()
    sorted_neighbor_distances = sorted(neighbor_distances, key=operator.itemgetter(1), reverse=reverse)

    return sorted_neighbor_distances

def find_route_path(graph, start_node, end_node, current_node=None, route="", total_distance=0, max_stops=3, shortest=True):
    """
    Giving a distance graph, return the shortest or largest route distance between a starting and ending routes without repetition.
    It's based on nearest neighbour algorithm. https://en.wikipedia.org/wiki/Nearest_neighbour_algorithm
    """
    current_node = current_node or start_node
    route = route + current_node

    sorted_neighbor_distances = sort_neighbor_distances(graph, current_node, reverse=not shortest)

    if len(route) > 2 and current_node in [start_node, end_node]:
        return { 'route': route, 'distance': total_distance }

    for neighbor, distance in sorted_neighbor_distances:
        if (len(route) > max_stops):
            continue

        if (neighbor not in [start_node, end_node] and neighbor in route):
            continue

        current_node = neighbor

        result = find_route_path(
            graph,
            start_node,
            end_node,
            current_node=current_node,
            route=route,
            total_distance=total_distance + distance,
            shortest=shortest
        )

        if (result):
            return result

    return None


if __name__ == '__main__':
    pairCosts = Graph()

    # fake crypto pairs and its profits
    pairCosts.add_edge('A', 'Z', 1)
    pairCosts.add_edge('Z', 'X', 2)
    pairCosts.add_edge('X', 'A', 1)
    pairCosts.add_edge('A', 'B', 5)
    pairCosts.add_edge('B', 'C', 4)
    pairCosts.add_edge('C', 'D', 8)
    pairCosts.add_edge('D', 'C', 8)
    pairCosts.add_edge('D', 'E', 6)
    pairCosts.add_edge('A', 'D', 6)
    pairCosts.add_edge('C', 'E', 6)
    pairCosts.add_edge('E', 'B', 6)
    pairCosts.add_edge('A', 'E', 6)
    pairCosts.add_edge('B', 'A', 6)

    print(find_route_path(pairCosts, 'A', 'A', shortest=True))
    print(find_route_path(pairCosts, 'A', 'A', shortest=False))
