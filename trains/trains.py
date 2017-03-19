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


def dijsktra(graph, initial):
    """dijsktra implementation, returns two dictionaries: visited nodes and path"""
    visited = {initial: 0}
    path = {}

    nodes = set(graph.nodes)

    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node

        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        for edge in graph.edges[min_node]:
            weight = current_weight + graph.distances[(min_node, edge)]
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = min_node

    return visited, path


def mysplit(s, delim=None):
    """Special split that does not return empty strings"""
    return [x for x in s.split(delim) if x]


def simple_route(_route, _graph):
    """If the route is valid it returns the total distance to travel"""

    if type(_route) is not list:
        _route = _route.split("-")

    _nodes = len(_route)
    _dist = 0

    for node in range(0, _nodes):
        if node+1 < _nodes:
            destiny = node+1

        else:
            break

        visited, path = dijsktra(_graph, _route[node])

        if (_route[destiny] in path) and (path[_route[destiny]] == _route[node]):
            _dist += visited[_route[destiny]]

        else:
            _dist = 0
            output = "NO SUCH ROUTE"
            break

    if _dist:
        output = str(_dist)

    return output


"""
  # C->C
  # Route starting at C and ending at C
  # L<30
  # lenght less than 30

  >>> route_verification("C->C, L<30", g)
  7
"""


def dist(_graph, pathway):
    pathway = pathway.replace(" ", "")
    edges = [(pathway[i], pathway[i + 1]) for i in range(len(pathway)) if i < len(pathway) - 1]
    return sum([_graph.distances[edge] for edge in edges])


def run_route_len3(_graph, start_node, end_node, max_dist=30, pathway=""):
    pathway = pathway + start_node + " "
    visited, path = dijsktra(_graph, start_node)
    count = 0
    # print("From", start_node, "to", end_node, "::", pathway)

    for k in path.keys():
        try:
            pathway_dist = dist(_graph, pathway + k)
        except:
            pathway_dist = None

        print(pathway + k + "?", str(pathway_dist), visited)

        if path[k] == start_node:
            if pathway_dist and pathway_dist >= max_dist:
                # print("breaking here", pathway_dist)
                # print("=---------------=")
                break

            # pathway = pathway + k

            if k == end_node:
                print(" ")
                print("!!!" + pathway + k + "!!!", pathway_dist)
                count += 1
                # print("=---------------=")
                # print("breaking here because found the ending")
                # break

            # print(start_node, "->", k, "-", pathway)
            count += run_route_len3(_graph=_graph, start_node=k, end_node=end_node, max_dist=max_dist, pathway=pathway)
            # print(output, pathway)
    return count


def run_route_len(_graph, start_node,  end_node, operator="<", _dist=0, min_dist=-1, pathway=""):
    pathway = pathway + start_node + " "
    visited, path = dijsktra(_graph, start_node)
    print("From", start_node, "to", end_node, "::")
    print(path)

    if end_node in visited and visited[end_node] is not 0:
        _dist += visited[end_node]
        print(_dist)
        return _dist

    for k in path.keys():
        if path[k] == start_node:
            if operator == "<":
                _dist += visited[k]
                pathway = pathway + k
                if _dist+visited[k] >= min_dist and min_dist > 0:
                    break

            print(start_node, "->", k, "-", pathway)
            dist = run_route_len(_graph=_graph, start_node=k, end_node=end_node, operator=operator, _dist=_dist,
                                 min_dist=min_dist, pathway=pathway)
            if min_dist == -1 or dist < max_dist:
                min_dist = dist
                _dist = dist

    return _dist


def run_route(_graph, start_node, max_stops, end_node, operator="<=", stops=-1, pathway=""):
    pathway = pathway + start_node + " "
    visited, path = dijsktra(_graph, start_node)
    output = 0
    print("From", start_node, "to", end_node, "::")
    print(path)

    stops += 1

    for k in path.keys():
        if path[k] == start_node:
            if stops > max_stops:
                pathway = pathway + end_node
                # print("Too far away, stops", stops, pathway)
                break

            if k == end_node:
                if operator == "<=":
                    pathway = pathway + end_node
                    # print("Found the end of the way!", pathway)
                    output = 1
                    break
                elif stops == max_stops:
                    pathway = pathway + end_node
                    # print("Found the end of the way!", pathway)
                    output = 1
                    break

            print(start_node, "->", k, stops, "-", pathway)
            output += run_route(_graph=_graph, start_node=k, max_stops=max_stops, end_node=end_node, operator=operator,
                                stops=stops, pathway=pathway)  # noqa

    return output


def complex_route(_route, _graph):
    """If the route is valid it returns the total distance to travel"""
    output = 0

    if type(_route) is not list:
        _route = _route.replace(" ", "").split(",")

    start_node, end_node = _route[0].split("->")[0], _route[0].split("->")[1]
    print(start_node, end_node)

    process = {"val": list(), "operator": ""}

    if "==" in _route[1]:
        process["operator"] = "=="

    elif "<=" in _route[1]:
        process["operator"] = "<="

    elif "<" in _route[1]:
        process["operator"] = "<"

    process["val"] = mysplit(_route[1], process["operator"])

    if process["val"][0].upper() == "S":
        # return number of routes with a defined number of stops betwen start and end
        if process["operator"] == "==":
            # which are equal to process["val"][1]
            max_stops = int(process["val"][1])
            print("start_node", start_node, "end node", end_node)
            output = run_route(_graph=_graph, start_node=start_node, max_stops=int(process["val"][1]),
                               end_node=end_node, operator=process["operator"])

        elif process["operator"] == "<=":
            # which are equal or less to process["val"][1]
            max_stops = int(process["val"][1])
            print("start_node", start_node, "end node", end_node)
            output = run_route(_graph=_graph, start_node=start_node, max_stops=max_stops, end_node=end_node,
                               operator=process["operator"])

    elif process["val"][0].upper() == "L":
        # return routes based on length
        if process["operator"] == "<":
            if len(process["val"]) == 2:
                # The number of different routes from start to end with a distance of less than process["val"][1].
                pass
            else:
                # The length of the shortest route from start_node to end_node
                output = run_route_len(_graph, start_node=start_node, end_node=end_node, operator=process["operator"])

    if not output:
        output = "NO SUCH ROUTE"

    return output


def route_verification(_route, _graph):
    if "->" in _route:
        output = complex_route(_route, _graph)

    elif "-" in _route:
        output = simple_route(_route, _graph)

    else:
        if type(_route) is not list:
            _route = _route.split("-")

        output = simple_route(_route, _graph)

    return output


if __name__ == '__main__':
    # g = create_graph(input("Enter Graph: "))
    g = Graph("AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7")
    # print(route_verification(input("enter route: "), g)) #A-B-C
    print("A-B-C:", route_verification("A-B-C", g))
    print("A-D:", route_verification("A-D", g))
    print("A-D-C:", route_verification("A-D-C", g))
    print("A-E-B-C-D:", route_verification("A-E-B-C-D", g))
    print("A-E-D:", route_verification("A-E-D", g))
    print(dijsktra(g, "C"))

    # TODO

    print("C->C, S <= 3", route_verification("C->C, S <= 3", g))
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
