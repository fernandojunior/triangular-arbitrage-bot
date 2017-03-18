"""Problem one: Trains


The local commuter railroad services a number of towns in Kiwiland.  Because of monetary concerns, all of the tracks are 'one-way.'  That is, a route from Kaitaia to Invercargill does not imply the existence of a route from Invercargill to Kaitaia.  In fact, even if both of these routes do happen to exist, they are distinct and are not necessarily the same distance!

The purpose of this problem is to help the railroad provide its customers with information about the routes.  In particular, you will compute the distance along a certain route, the number of different routes between two towns, and the shortest route between two towns.

Input:  A directed graph where a node represents a town and an edge represents a route between two towns.  The weighting of the edge represents the distance between the two towns.  A given route will never appear more than once, and for a given route, the starting and ending town will not be the same town.

Output: For test input 1 through 5, if no such route exists, output 'NO SUCH ROUTE'.  Otherwise, follow the route as given; do not make any extra stops!  For example, the first problem means to start at city A, then travel directly to city B (a distance of 5), then directly to city C (a distance of 4).
The distance of the route A-B-C.
The distance of the route A-D.
The distance of the route A-D-C.
The distance of the route A-E-B-C-D.
The distance of the route A-E-D.

The number of trips starting at C and ending at C with a maximum of 3 stops.  In the sample data below, there are two such trips: C-D-C (2 stops). and C-E-B-C (3 stops).
The number of trips starting at A and ending at C with exactly 4 stops.  In the sample data below, there are three such trips: A to C (via B,C,D); A to C (via D,C,D); and A to C (via D,E,B).
The length of the shortest route (in terms of distance to travel) from A to C.
The length of the shortest route (in terms of distance to travel) from B to B.
The number of different routes from C to C with a distance of less than 30.  In the sample data, the trips are: CDC, CEBC, CEBCDC, CDCEBC, CDEBC, CEBCEBC, CEBCEBCEBC.

Test Input:
For the test input, the towns are named using the first few letters of the alphabet from A to E.  A route between two towns (A to B) with a distance of 5 is represented as AB5.
Graph: AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7
Expected Output:
Output #1: 9
Output #2: 5
Output #3: 13
Output #4: 22
Output #5: NO SUCH ROUTE
Output #6: 2
Output #7: 3
Output #8: 9
Output #9: 9
Output #10: 7"""

from collections import defaultdict

class Graph:
  """Creates the graph for use with dijsktra
  This is a very simple implementation, it may only add nodes and edges"""
  def __init__(self, directed = False):
    self.nodes = set()
    self.edges = defaultdict(list)
    self.distances = {}
    self.directed = directed

  def add_node(self, value):
    self.nodes.add(value)

  def add_edge(self, from_node, to_node, distance):
    self.edges[from_node].append(to_node)
    if self.directed:
      self.edges[to_node].append(from_node)
    self.distances[(from_node, to_node)] = distance

def dijsktra(graph, initial):
  """dijsktra implementation, returns two dictionaries, visited nodes and path"""
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


def create_graph (graph):
  if type(graph) is not list:
    graph = graph.replace(" ", "").split(",")

  nodes = set()
  edges = list()

  for chars in graph:
    nodes.add(chars[0])
    nodes.add(chars[1])
    edges.append([chars[0],chars[1], int(chars[2])])

  g = Graph()

  for node in nodes:
    g.add_node(node)

  for edge in edges:
    g.add_edge(edge[0], edge[1], edge[2])

  return g


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

    visited , path = dijsktra(_graph, _route[node])

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

def run_route_len3( _graph, start_node, end_node, max_dist = 30, pathway = ""):
  pathway = pathway + start_node + " "
  visited , path = dijsktra(_graph, start_node)
  count = 0
  #print("From", start_node, "to", end_node, "::", pathway)

  for k in path.keys():
    try:
        pathway_dist = dist(_graph, pathway + k)
    except:
        pathway_dist = None

    print(pathway + k + "?", str(pathway_dist), visited)

    if path[k] == start_node:

      if pathway_dist and pathway_dist >= max_dist:
        print("breaking here", pathway_dist)
        print("=---------------=")
        break

      #pathway = pathway + k

      if k == end_node:
        print(" ")
        print("!!!" + pathway + k + "!!!", pathway_dist)
        count += 1
        print("=---------------=")
        #print("breaking here because found the ending")
        #break

      #print(start_node, "->", k, "-", pathway)
      count += run_route_len3( _graph = _graph, start_node=k, end_node=end_node, max_dist=max_dist, pathway=pathway)
      #print(output, pathway)
  return count

def run_route_len2( _graph, start_node,  end_node, operator="<", _dist = 0, min_dist = -1, pathway = ""):
  pathway = pathway + start_node + " "
  visited , path = dijsktra(_graph, start_node)
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
      output += run_route_len( _graph = _graph, start_node=k, end_node=end_node, operator=operator, _dist=_dist, min_dist=min_dist, pathway=pathway)

  return output

def run_route_len( _graph, start_node,  end_node, operator="<", _dist = 0, min_dist = -1, pathway = ""):
  pathway = pathway + start_node + " "
  visited , path = dijsktra(_graph, start_node)
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
      dist = run_route_len( _graph = _graph, start_node=k, end_node=end_node, operator=operator, _dist=_dist, min_dist=min_dist, pathway=pathway)
      if min_dist == -1 or dist < max_dist:
        min_dist = dist
        _dist = dist

  return _dist

def run_route( _graph, start_node, max_stops, end_node, operator="<=", stops = -1, pathway = ""):
  pathway = pathway + start_node + " "
  visited , path = dijsktra(_graph, start_node)
  output = 0
  print("From", start_node, "to", end_node, "::")
  print(path)

  stops += 1

  for k in path.keys():
    if path[k] == start_node:

      if stops > max_stops:
        pathway = pathway + end_node
        #print("Too far away, stops", stops, pathway)
        break

      if k == end_node:
        if operator == "<=":
          pathway = pathway + end_node
          #print("Found the end of the way!", pathway)
          output = 1
          break
        elif stops == max_stops:
          pathway = pathway + end_node
          #print("Found the end of the way!", pathway)
          output = 1
          break
        #else:
        #  pass

      print(start_node, "->", k, stops, "-", pathway)
      output += run_route( _graph = _graph, start_node=k, max_stops=max_stops, end_node=end_node, operator=operator, stops=stops, pathway=pathway)

  return output

def complex_route(_route, _graph):
  """If the route is valid it returns the total distance to travel"""

  output = 0

  if type(_route) is not list:
    _route = _route.replace(" ", "").split(",")

  start_node, end_node = _route[0].split("->")[0], _route[0].split("->")[1]
  print(start_node, end_node)

  process = {"val" : list(), "operator": ""}

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
      output = run_route( _graph = _graph, start_node = start_node,
                          max_stops = int(process["val"][1]), end_node = end_node, operator=process["operator"])

    elif process["operator"] == "<=":
      # which are equal or less to process["val"][1]
      max_stops = int(process["val"][1])
      print("start_node", start_node, "end node", end_node)
      output = run_route( _graph = _graph, start_node = start_node,
                          max_stops = int(process["val"][1]), end_node = end_node, operator=process["operator"])

  elif process["val"][0].upper() == "L":
    # return routes based on length
    if process["operator"] == "<":
      if len(process["val"]) == 2:
        # The number of different routes from start to end with a distance of less than process["val"][1].
        pass

      else:
        # The length of the shortest route from start_node to end_node
        output = run_route_len( _graph, start_node = start_node, end_node=end_node, operator=process["operator"])

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
  #g = create_graph(input("Enter Graph: "))
  g = create_graph("AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7")
  #print(route_verification(input("enter route: "), g)) #A-B-C
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
