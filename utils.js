function findRoutePath (graph, startNode, endNode, shortest = true, currentNode = null, route = [], totalDistance = 0, maxStops = 3) {
  currentNode = currentNode || startNode
  route.push(currentNode)

  const sortedNeighborDistances = graph.getSortedNeighborDistances(currentNode, !shortest)

  if (route.length > 2 && route[0] === startNode && route[route.length - 1] === endNode) {
    return { route, totalDistance }
  }

  for (const neighbor of Object.keys(sortedNeighborDistances)) {
    const distance = sortedNeighborDistances[neighbor]
    const expetedEdgeNumber = [...route, neighbor].length - 1

    if (![startNode, endNode].includes(neighbor) && (route.includes(neighbor) || expetedEdgeNumber === maxStops)) {
      continue
    }

    currentNode = neighbor

    const result = findRoutePath(graph, startNode, endNode, shortest, currentNode, route, totalDistance + distance, maxStops)

    if (result) {
      return result
    }
  }

  return null
}

module.exports = {
  findRoutePath
}
