"""Problem one: Trains"""
from collections import defaultdict


class Graph:
    """ An unidireccional edge graph. This is a very simple implementation, it may only add nodes and edges"""

    def __init__(self, distances_str=None):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}

        if distances_str:
            self.add_edges(distances_str.replace(" ", "").split(","))

    def distance(self, from_node, to_node):
        return self.distances[(from_node, to_node)]

    def add_edges(self, node_pair_distances):
        for node_pair_distance in node_pair_distances:
            self.add_edge(node_pair_distance[0], node_pair_distance[1], int(node_pair_distance[2]))

    def add_node(self, node):
        self.nodes.add(node)

    def add_edge(self, from_node, to_node, distance):
        self.add_node(from_node)
        self.add_node(to_node)
        self.edges[from_node].append(to_node)
        self.distances[(from_node, to_node)] = distance


def mysplit(s, delim=None):
    """ Special split that does not return empty strings """
    return [x for x in s.split(delim) if x]


def route_distance(route, graph):
    """ Return the total route distance given a distance graph """
    route = route.replace("-", "")
    edges = [(route[i], route[i + 1]) for i in range(len(route)) if i < len(route) - 1]
    try:
        return str(sum([graph.distances[edge] for edge in edges]))
    except:
        return "NO SUCH ROUTE"


def shortest_route(graph, start_node, end_node):
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


def count_routes(graph, start_node, end_node, stops, operator="<=", route="", routes_=[]):
    """
    Count routes recursively between a start node and an end node
    """
    print("asdsada", routes_)
    route = route + start_node
    route_counts = 0
    current_stops = len(route) - 1

    for neighbor in graph.edges[start_node]:
        if current_stops > stops:
            break

        if neighbor == end_node:
            route = route + end_node
            if(eval(str(current_stops) + operator + str(stops))):
                routes_.append(route)
                route_counts = 1
                break

        route_counts += count_routes(graph, neighbor, end_node, stops, operator=operator, route=route, routes_=routes_)

    print(routes_)

    return route_counts


# def complex_route(route, graph, criteria_type=None, criteria=None):
#     """If the route is valid it returns the total distance to travel"""
#     output = 0
#
#     route, criteria = route.replace(" ", "").split(",")
#     start_node, end_node = route.split("->")
#
#     process = {"val": list(), "operator": ""}
#
#     if "==" in criteria:
#         process["operator"] = "=="
#
#     elif "<=" in criteria:
#         process["operator"] = "<="
#
#     elif "<" in criteria:
#         process["operator"] = "<"
#
#     process["val"] = mysplit(criteria, process["operator"])
#
#     if process["val"][0].upper() == "S":
#         # return number of routes with a defined number of stops betwen start and end
#         if process["operator"] == "==":
#             # which are equal to process["val"][1]
#             stops = int(process["val"][1])
#             output = count_routes(graph, start_node, end_node, stops=int(process["val"][1]),
#                                   operator=process["operator"])
#
#         elif process["operator"] == "<=":
#             # which are equal or less to process["val"][1]
#             stops = int(process["val"][1])
#             output = count_routes(graph, start_node, end_node, stops=stops, operator=process["operator"])
#
#     elif process["val"][0].upper() == "L":
#         # return routes based on length
#         if process["operator"] == "<":
#             if len(process["val"]) == 2:
#                 # The number of different routes from start to end with a distance of less than process["val"][1].
#                 pass
#             else:
#                 # The length of the shortest route from start_node to end_node
#                 output = run_route_len(graph, start_node=start_node, end_node=end_node, operator=process["operator"])
#
#     if not output:
#         output = "NO SUCH ROUTE"
#
#     return output


def route_verification(_route, graph):
    # if "->" in _route:
    #     output = complex_route(_route, graph)
    if "-" in _route:
        output = route_distance(_route, graph)

    else:
        if type(_route) is not list:
            _route = _route.split("-")

        output = route_distance(_route, graph)

    return output


if __name__ == '__main__':
    g = Graph("AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7")
    print(g.distances)
    print(g.edges)
    #
    # print(g.edges['A'])
    # print("C->C, S <= 3")
    # print(count_routes(g, 'C', 'C', 3, operator="<="))
    #
    # print("################")
    # print("A->C, S == 4")
    # print(count_routes(g, 'A', 'C', 4, operator="=="))
    # print("!!!!!!!!!!!!!!!!!!!!")
    print(shortest_route(g, 'B', 'B'))
    # print(shortest_route(g, 'C', 'C', max_dist=30))

    # assert route_verification("A->C, L<", g) == 9
    # assert route_verification("B->B, L<", g) == 9

    # print("########################")
    # print(route_verification("C->C, S <= 3", g)) # A-B-C
    # print("########################")
    # print("A-B-C:", route_verification("A-B-C", g))
    # print("A-D:", route_verification("A-D", g))
    # print("A-D-C:", route_verification("A-D-C", g))
    # print("A-E-B-C-D:", route_verification("A-E-B-C-D", g))
    # print("A-E-D:", route_verification("A-E-D", g))


def tmp():
    # TODO

    """
    # C->C
    # Route starting at C and ending at C
    # S <= 3
    # with less or equal to 3 stops

    >>> route_verification("C->C, S <= 3", g)
    2

    C-D-C (2 stops)
    C-E-B-C (3 stops)
    """

    print("A->C, S == 4", route_verification("A->C, S == 4", g))
    """
    # A->C
    # Route starting at A and ending at C
    # S == 4
    # equal to 4 stops

    >>> route_verification("A->C, S == 4", g)
    3

    A-B-C-D-C (4 stops)
    A-D-C-D-C (4 stops)
    A-D-E-B-C (4 stops)
    """

    print("A->C, L<", route_verification("A->C, L<", g))
    """
    # A->C
    # Route starting at A and ending at C
    # L<
    # lenght of the shortest route

    >>> route_verification("A->C, L<", g)
    9

    The length of the shortest route (in terms of distance to travel) from A to C.
    """

    print("B->B, L<", route_verification("B->B, L<", g))
    """
    # B->B
    # Route starting at B and ending at B
    # L<
    # lenght of the shortest route

    >>> route_verification("B->B, L<", g)
    9

    The length of the shortest route (in terms of distance to travel) from B to B.
    """

    print("C->C, L<30", route_verification("C->C, L<30", g))
    """
    # C->C
    # Route starting at C and ending at C
    # L<30
    # lenght less than 30

    >>> route_verification("C->C, L<30", g)
    7

    The number of different routes from C to C with a distance of less than 30.  In the sample data, the trips are:
    CDC,
    CEBC,
    CEBCDC,
    CDCEBC,
    CDEBC,
    CEBCEBC,
    CEBCEBCEBC.
    """
