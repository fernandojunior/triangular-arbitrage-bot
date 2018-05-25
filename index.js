const Graph = require('./graph')

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
