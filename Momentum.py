from pyalgotrade import strategy
from pyalgotrade.barfeed.csvfeed import GenericBarFeed
from pyalgotrade.bar import Frequency
from pyalgotrade.technical import rsi, ma, macd

class MomentumStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instruments, smaPeriod):
        super(MomentumStrategy, self).__init__(feed)
        self.__instruments = instruments
        self.__feed = feed
        self.__prices = {}
        self.__rsi = {}
        self.__ma = {}
        self.__macd = {}

        for instrument in feed.getRegisteredInstruments():
            self.__prices[instrument] = feed[instrument].getPriceDataSeries()
            self.__rsi[instrument] = rsi.RSI(self.__prices[instrument], 14)
            self.__ma[instrument] = ma.SMA(self.__prices[instrument], smaPeriod)
            self.__macd[instrument] = macd.MACD(self.__prices[instrument], 12, 26, 9).getHistogram() # Buy when historgram is > 0. Sell when histogram is < 0

    def onBars(self, bars):

        # Loop through list of stocks
        for instrument in self.__instruments:

            if self.__rsi[instrument][-1] is None and self.__ma[instrument][-1] is not None:
                return

            
            bar = bars[instrument]
            self.info(f"{instrument}: {bar.getClose()} RSI: {self.__rsi[instrument][-1]}, SMA: {self.__ma[instrument][-1]}, MACD: {self.__macd[instrument][-1]}")


def main (instruments):
    feed = GenericBarFeed(Frequency.DAY)

    # building feed with multiple instruments
    for instrument in instruments:
        feed.addBarsFromCSV(instrument, f"data/{instrument}.csv")

    momentumStrategy = MomentumStrategy(feed, instruments, 200)
    momentumStrategy.run()
   

main(['AAPL', 'TSLA', 'SPY'])


