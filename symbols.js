/**
 * @type {string[]}
 */
const symbols = JSON.parse(`["ADA","ADX","AE","AION","AMB","APPC","ARK","ARN","AST","BAT","BCC","BCD","BCN","BCPT","BLZ","BNB","BNC","BNT","BQX","BRD","BTC","BTG","BTM","BTS","CDT","CHAT","CLOAK","CMT","CND","CTR","CVC","DASH","DGD","DLT","DNT","EDO","ELC","ELF","ENG","ENJ","EOS","ETC","ETH","EVX","FID","FUEL","FUN","GAS","GNT","GRS","GTO","GVT","GXS","HCC","HSR","ICN","ICO","ICX","INS","IOST","IOTA","KMD","KNC","LEND","LINK","LLT","LOOM","LRC","LRX","LSK","LTC","LUN","MANA","MCO","MDA","MOD","MTH","MTL","NANO","NAV","NCASH","NEBL","NEO","NULS","OAX","OMG","ONT","OST","PAY","PIVX","POA","POE","POWR","PPT","QLC","QSP","QTUM","RCN","RDN","REP","REQ","RLC","RPX","SALT","SKY","SNGLS","SNM","SNT","STEEM","STORJ","STORM","STRAT","SUB","SYS","TNB","TNT","TRIG","TRX","TUSD","USDT","VEN","VIA","VIB","VIBE","WABI","WAN","WAVES","WINGS","WPR","WTC","XEM","XLM","XMR","XRP","XVG","XZC","YOYO","ZEC","ZEN","ZIL","ZRX"]`)

/**
 * @type {Object}
 * @example
 *   {
 *     'BTCADA': { baseSymbol: 'BTC', quotaSymbol: 'ADA', reversePair: 'ADABTC' },
 *     'BTCADX': { baseSymbol: 'BTC', quotaSymbol: 'ADX', reversePair: 'ADXBTC' },
 *     ...
 *   }
 */
const symbolPairMetas = (() => {
  const pairs = {}

  symbols.forEach(baseSymbol => symbols.forEach(quotaSymbol => {
    if (baseSymbol !== quotaSymbol) {
      pairs[baseSymbol + quotaSymbol] = { baseSymbol, quotaSymbol, reversePair: quotaSymbol + baseSymbol }
    }
  }))

  return pairs
})()

/**
 * @param {string} Ex: 'BTCADA'
 * @returns {Object}
 * @example
 *   { baseSymbol: 'BTC', quotaSymbol: 'ADA', reversePair: 'ADABTC' },
 */
function getSymbolPairMeta (symbolPair) {
  return symbolPairMetas[symbolPair]
}

module.exports = {
  symbols,
  symbolPairMetas,
  getSymbolPairMeta
}
