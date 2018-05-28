function findRoutePath (graph, startNode, endNode, shortest = true, currentNode = null, route = '', totalDistance = 0, maxStops = 3) {
  currentNode = currentNode || startNode
  route = route + currentNode

  const sortedNeighborDistances = graph.getSortedNeighborDistances(currentNode, !shortest)

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

    const result = findRoutePath(
      graph,
      startNode,
      endNode,
      shortest,
      currentNode,
      route,
      totalDistance + distance,
      maxStops
    )

    if (result) {
      return result
    }
  }

  return null
}

module.exports = {
  findRoutePath
}
