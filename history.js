const binance = require('node-binance-api')
const request = require('request-promise')
const { promisify } = require('es6-promisify')

const mock = require('./mock')
const Graph = require('./graph')
const { findRoutePath } = require('./utils')

const exchangeApis = {
  bittrex: {
    async getTicker (currencyPairStr) {
      const url = `https://bittrex.com/api/v1.1/public/getticker?market=${currencyPairStr}`
      return JSON.parse(await request(url)).result
    }
  },
  binance: {
    getTicker (currencyPairStr) {
      return promisify(binance.bookTickers)(currencyPairStr)
    },

    async getTickers () {
      const tickerList = (await promisify(binance.bookTickers)())

      return tickerList.reduce((acc, { symbol, bidPrice, askPrice }) => {
        acc[symbol] = { bidPrice: parseFloat(bidPrice), askPrice: parseFloat(askPrice) }
        return acc
      }, {})
    },

    getBalances () {
      return Promise.resolve(mock.binanceBalances)
    },

    async getSymbols () {
      return Object.keys(await this.getBalances())
    },

    async getSymbolPairMetas () {
      const symbols = (await this.getSymbols())
      const pairs = {}

      symbols.forEach(baseSymbol => symbols.forEach(quotaSymbol => {
        if (baseSymbol !== quotaSymbol) {
          pairs[baseSymbol + quotaSymbol] = { baseSymbol, quotaSymbol, reversePair: quotaSymbol + baseSymbol }
        }
      }))

      return pairs
    }

  }
}

exchangeApis.binance.getTickers().then(async (tickers) => {
  const twoWayTickers = {}

  const allSymbolPairMetas = await exchangeApis.binance.getSymbolPairMetas()

  const tickerSymbolPairs = Object.keys(tickers)

  tickerSymbolPairs.forEach(tickerSymbolPair => {
    const pairMeta = allSymbolPairMetas[tickerSymbolPair]

    if (pairMeta && !Object.keys(twoWayTickers).includes(pairMeta.reversePair)) {
      // main way to trade
      const ticker = tickers[tickerSymbolPair]
      ticker.isReversePair = false
      ticker.baseSymbol = pairMeta.baseSymbol
      ticker.quotaSymbol = pairMeta.quotaSymbol
      twoWayTickers[tickerSymbolPair] = ticker

      // reverse way to trade
      twoWayTickers[pairMeta.reversePair] = {
        bidPrice: 1 / ticker.askPrice,
        askPrice: 1 / ticker.bidPrice,
        isReversePair: true,
        baseSymbol: ticker.quotaSymbol,
        quotaSymbol: ticker.baseSymbol
      }
    }
  })

  const pairCosts = new Graph()
  Object.keys(twoWayTickers).forEach((tickerName) => {
    const ticker = twoWayTickers[tickerName]
    pairCosts.addEdge(ticker.baseSymbol, ticker.quotaSymbol, ticker.bidPrice)
  })

  // TODO change cost function for findRoutePath function
  console.log(findRoutePath(pairCosts, 'BTC', 'BTC', false))
})
