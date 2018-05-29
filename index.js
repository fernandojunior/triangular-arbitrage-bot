const Graph = require('./graph')
const { findRoutePath } = require('./utils')
const { binance } = require('./exchangeApis')

binance.getTwoWayTickers().then((tickers) => {
  const pairCosts = new Graph()
  Object.keys(tickers).forEach((tickerName) => {
    const { baseSymbol, quotaSymbol, bidPrice } = tickers[tickerName]
    pairCosts.addEdge(baseSymbol, quotaSymbol, bidPrice)
  })

  // TODO change cost function for findRoutePath function to calculate profit
  console.log(findRoutePath(pairCosts, 'BTC', 'BTC', false))
})
