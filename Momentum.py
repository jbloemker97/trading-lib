from pyalgotrade import strategy
from pyalgotrade.barfeed.csvfeed import GenericBarFeed
from pyalgotrade.bar import Frequency
from pyalgotrade.technical import rsi

class MomentumStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instruments):
        super(MomentumStrategy, self).__init__(feed)
        self.__instruments = instruments
        self.__rsi = None
        # self.__prices = feed[instrument].getPriceDataSeries()
        # self.__rsi = rsi.RSI(self.__prices, 14)

    def getRSI(self):
        if self.__rsi is not None: return self.__rsi

    def setValues(self, prices, rsi):
        self.__prices = prices
        self.__rsi = rsi

    def onBars(self, bars):

        for instrument in self.__instruments:
            bar = bars[instrument]
            self.info(f"{instrument}: {bar.getClose()}")


    def enterLongSignal(self, bar):
        return self.__rsi[-1] < 50 # Threshold


def main (instruments):
    feed = GenericBarFeed(Frequency.DAY)

    # building feed with multiple instruments
    for instrument in instruments:
        feed.addBarsFromCSV(instrument, f"data/{instrument}.csv")

    momentumStrategy = MomentumStrategy(feed, instruments)
    momentumStrategy.run()
   

main(['AAPL', 'TSLA', 'SPY'])


