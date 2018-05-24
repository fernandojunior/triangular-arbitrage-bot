"""
ThoughtWorks Trains Solution.

author: Fernando Felix do Nascimento Junior
year: 2017
"""
from collections import defaultdict
import operator

ENDLESS_ROUTE_PATH_ERROR = 'ENDLESS_ROUTE_PATH_ERROR'


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


def route_distance(graph, route, exception_message="NO SUCH ROUTE"):
    """ Return the total route distance given a distance graph """
    route = route.replace("-", "")
    edges = [(route[i], route[i + 1]) for i in range(len(route)) if i < len(route) - 1]
    try:
        return str(sum([graph.distances[edge] for edge in edges]))
    except:
        return exception_message

def find_nearest_neighbor(graph, node):
    ''' Return the nearest neighbor of a node '''
    min_distance = float('Inf')
    nearest = None

    for neighbor in graph.edges[node]:
        distance = graph.distance(node, neighbor)
        if distance < min_distance:
            min_distance = distance
            nearest = neighbor

    return nearest, min_distance

def sort_neighbor_distances(graph, node, reverse=False):
    ''' Return the sorted neighbor distances of a node '''
    neighbor_distances = graph.get_neighbor_distances(node).items()
    sorted_neighbor_distances = sorted(neighbor_distances, key=operator.itemgetter(1), reverse=reverse)

    return sorted_neighbor_distances

def shortest_route_distance(graph, start_node, end_node, current_node=None, route="", total_distance=0, max_stops=3):
    """
    Giving a distance graph, return the shortest route distance between a starting and ending routes without repetition.
    It's based on nearest neighbour algorithm. https://en.wikipedia.org/wiki/Nearest_neighbour_algorithm
    """
    current_node = current_node or start_node
    route = route + current_node

    print('init', route, start_node, end_node, current_node)
    sorted_neighbor_distances = sort_neighbor_distances(graph, current_node, reverse=False)

    if len(route) > 2 and current_node in [start_node, end_node]:
        return { 'route': route, 'distance': total_distance }

    print(sorted_neighbor_distances)

    for neighbor, distance in sorted_neighbor_distances:
        if (len(route) > max_stops):
            continue

        if (neighbor not in [start_node, end_node] and neighbor in route):
            continue

        current_node = neighbor

        result = shortest_route_distance(
            graph,
            start_node,
            end_node,
            current_node=current_node,
            route=route,
            total_distance=total_distance + distance
        )

        if (result):
            return result

    return None


def count_routes_by_stops(graph, start_node, end_node, stops, operator="<=", _route=""):
    """
    Giving a distance graph, count routes recursively between a start node and an end node based on number of stops
    criterion (operator). For example, given a starting route at C and an ending at C, count and return the number of
    routes (or trips) with a maximum (operator=="<=") of stops=3.
    """
    _route = _route + start_node
    stop_counter = 0
    current_stops = len(_route) - 1  # similar to number of edges

    for neighbor in graph.edges[start_node]:
        if current_stops > stops:
            break

        if neighbor == end_node:
            _route = _route + end_node
            if(eval(str(current_stops) + operator + str(stops))):
                stop_counter += 1
                break

        stop_counter += count_routes_by_stops(graph, neighbor, end_node, stops, operator=operator, _route=_route)

    return stop_counter


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
    g = Graph("AZ1, ZX2, XA1, AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7, BA4")

    # calculate route distances
    # print(route_distance(g, "A-B-C"))
    # print(route_distance(g, "A-D"))
    # print(route_distance(g, "A-D-C"))
    # print(route_distance(g, "A-E-B-C-D"))
    # print(route_distance(g, "A-E-D"))

    # count routes recursively between a start node and an end node based on a number of stops
    # print(count_routes_by_stops(g, 'C', 'C', 3, operator="<="))  # a maximum of 3 stops
    # print(count_routes_by_stops(g, 'A', 'C', 4, operator="=="))  # exactly 4 stops
    # print(count_routes_by_stops(g, 'A', 'A', 3, operator="=="))  # exactly 4 stops

    # shortest route distance based on Nearest Neighbour Algorithm
    print(shortest_route_distance(g, 'A', 'A'))
    # print(shortest_route_distance(g, 'A', 'C'))
    # print(shortest_route_distance(g, 'B', 'B'))

    # count routes recursively between a start node and an end node based on a max distance
    # print(count_routes_by_max_distance(g, 'C', 'C', max_distance=30))
