const dateFormat = require('dateformat')
const binance = require('node-binance-api')
const request = require('request-promise')
const { promisify } = require('es6-promisify')

const exchangeApis = {
  bittrex: {
    getTicker: async (currencyPairStr) => {
      const url = `https://bittrex.com/api/v1.1/public/getticker?market=${currencyPairStr}`
      return JSON.parse(await request(url)).result
    }
  },
  binance: {
    getTicker: (...args) => {
      return promisify(binance.bookTickers)(...args)
    }
  }
}

const tickerHistory = []
const delayTime = 1000
const maxRequests = 4
let requestCounter = 0

// Bitcoin prices vary depending on the exchange you're buying it on
// https://www.cnbc.com/2017/12/12/why-bitcoin-prices-are-different-on-each-exchange.html
const exchangeRequestInterval = setInterval(() => {
  if (requestCounter === maxRequests) {
    clearInterval(exchangeRequestInterval)
  }

  exchangeApis.binance.getTicker('LTCBTC').then((ticker) => {
    tickerHistory.push({ time: dateFormat(new Date(), 'UTC:HH:MM:ss.l'), Bid: ticker.askPrice, Ask: ticker.bidPrice, exchange: 'binance' })
  })

  exchangeApis.bittrex.getTicker('BTC-LTC').then((ticker) => {
    tickerHistory.push({ time: dateFormat(new Date(), 'UTC:HH:MM:ss.l'), Bid: ticker.Bid, Ask: ticker.Ask, exchange: 'bittrex' })
  })

  requestCounter++
}, delayTime)

setTimeout(() => console.log(tickerHistory), delayTime * maxRequests + 1000)
