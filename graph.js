class Graph {
  constructor () {
    this.nodes = new Set()
    this.edges = {}
    this.distances = {}
  }

  getNeighbors (fromNode) {
    return this.edges[fromNode]
  }

  getNeighborDistances (fromNode) {
    const neighbors = this.getNeighbors(fromNode)
    return neighbors.reduce((neighborDistances, neighbor) => {
      return {
        ...neighborDistances,
        [neighbor]: this.getDistance(fromNode, neighbor)
      }
    }, {})
  }

  getSortedNeighborDistances (fromNode, reverse = false) {
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

  addDistance (fromNode, toNode, distance) {
    this.distances[String([fromNode, toNode])] = distance
  }

  getDistance (fromNode, toNode) {
    return this.distances[String([fromNode, toNode])]
  }

  addNode (node) {
    this.nodes.add(node)
  }

  addEdge (fromNode, toNode, distance) {
    this.addNode(fromNode)
    this.addNode(toNode)
    this.addDistance(fromNode, toNode, distance)

    this.edges[fromNode] = this.edges[fromNode] || []
    this.edges[fromNode].push(toNode)
  }
}

module.exports = Graph
