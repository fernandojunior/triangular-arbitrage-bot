const request = require('request-promise')
const { promisify } = require('es6-promisify')
const binanceOfficialApi = require('node-binance-api')
const { getSymbolPairMeta } = require('./symbols')

const bittrex = {
  async getTicker (currencyPairStr) {
    const url = `https://bittrex.com/api/v1.1/public/getticker?market=${currencyPairStr}`
    return JSON.parse(await request(url)).result
  }
}

const binance = {
  /**
   * @param {string} Ex: 'BTCADX'
   * @example
   * { bidPrice: 0.00055916, askPrice: 0.00056655 }
   */
  getTicker (currencyPairStr) {
    return promisify(binanceOfficialApi.bookTickers)(currencyPairStr)
  },

  /**
   * @example
   * {
   *   'BTCADX': { bidPrice: 0.00055916, askPrice: 0.00056655 },
   *   'BTCADA': { bidPrice: 0.00195621, askPrice: 0.00196695 },
   *   ...
   * }
   */
  async getTickers () {
    const tickerList = (await promisify(binanceOfficialApi.bookTickers)())

    return tickerList.reduce((acc, { symbol, bidPrice, askPrice }) => {
      acc[symbol] = { bidPrice: parseFloat(bidPrice), askPrice: parseFloat(askPrice) }
      return acc
    }, {})
  },

  /**
   * @example
   * {
   *   'BTCADX': { bidPrice: 0.00055916, askPrice: 0.00056655, isReversePair: false },
   *   'ADXBTC': { bidPrice: 1/0.00056655, askPrice: 1/0.00055916, isReversePair: true },
   *   'BTCADA': { bidPrice: 0.00195621, askPrice: 0.00196695, isReversePair: false },
   *   'ADABTC': { bidPrice: 1/0.00196695, askPrice: 1/0.00195621, isReversePair: true },
   *   ...
   * }
   */
  async getTwoWayTickers () {
    const tickers = await this.getTickers()
    const tickerSymbolPairs = Object.keys(tickers)
    const twoWayTickers = {}

    tickerSymbolPairs.forEach(symbolPair => {
      const symbolPairMeta = getSymbolPairMeta(symbolPair)

      if (symbolPairMeta) {
        const ticker = tickers[symbolPair]
        const { baseSymbol, quotaSymbol, reversePair } = symbolPairMeta

        // main way info to trade
        twoWayTickers[symbolPair] = {
          bidPrice: ticker.bidPrice,
          askPrice: ticker.askPrice,
          isReversePair: false,
          baseSymbol,
          quotaSymbol
        }

        // reverse way info to trade
        twoWayTickers[reversePair] = {
          bidPrice: 1 / ticker.askPrice,
          askPrice: 1 / ticker.bidPrice,
          isReversePair: true,
          baseSymbol: quotaSymbol,
          quotaSymbol: baseSymbol
        }
      }
    })

    return twoWayTickers
  }
}

module.exports = {
  bittrex,
  binance
}
