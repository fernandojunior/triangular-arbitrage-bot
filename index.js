class Graph {

  constructor() {
    this.nodes = new Set()
    this.edges = {}
    this.distances = {}
  }

  getNeighbors(fromNode) {
    return this.edges[fromNode]
  }

  getNeighborDistances(fromNode) {
    const neighbors = this.getNeighbors(fromNode)

    return neighbors.reduce((neighborDistances, neighbor) => {
      return {
        ...neighborDistances,
        [neighbor]: this.getDistance(fromNode, neighbor)
      }
    }, {})
  }

  getSortedNeighborDistances(fromNode, reverse=false) {
    const neighborDistances = this.getNeighborDistances(fromNode)

    let sortedKeys = Object
      .keys(neighborDistances)
      .sort((a, b) => neighborDistances[a] - neighborDistances[b])

    if (reverse) {
      sortedKeys.reverse()
    }

    return sortedKeys
      .reduce((sortedNeighborDistances, neighbor) => {
        return {
          ...sortedNeighborDistances,
          [neighbor]: neighborDistances[neighbor]
        }
      }, {})
  }

  addDistance(from_node, to_node, distance) {
    this.distances[String([from_node, to_node])] = distance
  }

  getDistance (from_node, to_node) {
    return this.distances[String([from_node, to_node])]
  }

  addNode(node) {
    this.nodes.add(node)
  }

  addEdge(fromNode, toNode, distance) {
    this.addNode(fromNode)
    this.addNode(toNode)
    this.addDistance(fromNode, toNode, distance)

    this.edges[fromNode] = this.edges[fromNode] || []
    this.edges[fromNode].push(toNode)
  }

}

function findRoutePath(graph, startNode, endNode, shortest=true, currentNode=null, route='', totalDistance=0, maxStops=3) {
  currentNode = currentNode ? currentNode : startNode
  route = route + currentNode

  sortedNeighborDistances = graph.getSortedNeighborDistances(currentNode, reverse=!shortest)

  if (route.length > 2 && [startNode, endNode].includes(currentNode)) {
    return { route, totalDistance }
  }

  for (const neighbor of Object.keys(sortedNeighborDistances)) {
    const distance = sortedNeighborDistances[neighbor]

    if (route.length > maxStops) {
      continue
    }

    if (![startNode, endNode].includes(neighbor) && route.includes(neighbor)) {
      continue
    }

    currentNode = neighbor

    result = findRoutePath(
        graph,
        startNode,
        endNode,
        shortest,
        currentNode,
        route,
        totalDistance=totalDistance + distance,
        maxStops
    )

    if (result) {
      return result
    }
  }

  return null
}

const pairCosts = new Graph()

pairCosts.addEdge('A', 'Z', 1)
pairCosts.addEdge('Z', 'X', 2)
pairCosts.addEdge('X', 'A', 1)
pairCosts.addEdge('A', 'B', 5)
pairCosts.addEdge('B', 'C', 4)
pairCosts.addEdge('C', 'D', 8)
pairCosts.addEdge('D', 'C', 8)
pairCosts.addEdge('D', 'E', 6)
pairCosts.addEdge('A', 'D', 5)
pairCosts.addEdge('C', 'E', 2)
pairCosts.addEdge('E', 'B', 3)
pairCosts.addEdge('A', 'E', 7)
pairCosts.addEdge('B', 'A', 4)

console.log(findRoutePath(pairCosts, 'A', 'A', true))
console.log(findRoutePath(pairCosts, 'A', 'A', false))
