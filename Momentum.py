from pyalgotrade import strategy
from pyalgotrade.barfeed.csvfeed import GenericBarFeed
from pyalgotrade.bar import Frequency
from pyalgotrade.technical import rsi

class MomentumStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instruments):
        super(MomentumStrategy, self).__init__(feed)
        self.__instruments = instruments
        self.__feed = feed
        self.__prices = {}
        self.__rsi = {}

        for instrument in feed.getRegisteredInstruments():
            self.__prices[instrument] = feed[instrument].getPriceDataSeries()
            self.__rsi[instrument] = rsi.RSI(self.__prices[instrument], 14)

        # self.__prices = feed[instrument].getPriceDataSeries()
        # self.__rsi = rsi.RSI(self.__prices, 14)

    def onBars(self, bars):

        # Loop through list of stocks
        for instrument in self.__instruments:

            if self.__rsi[instrument][-1] is None:
                return

            
            bar = bars[instrument]
            self.info(f"{instrument}: {bar.getClose()} RSI: {self.__rsi[instrument][-1]}")


def main (instruments):
    feed = GenericBarFeed(Frequency.DAY)

    # building feed with multiple instruments
    for instrument in instruments:
        feed.addBarsFromCSV(instrument, f"data/{instrument}.csv")

    momentumStrategy = MomentumStrategy(feed, instruments)
    momentumStrategy.run()
   

main(['AAPL', 'TSLA', 'SPY'])


