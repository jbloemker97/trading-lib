from pyalgotrade import strategy
from pyalgotrade.barfeed.csvfeed import GenericBarFeed
from pyalgotrade.bar import Frequency
from pyalgotrade.technical import rsi

class MomentumStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        super(MomentumStrategy, self).__init__(feed)
        self.__instrument = instrument
        self.setUseAdjustedValues(True)
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__rsi = rsi.RSI(feed, 14)

    def getRSI(self):
        return self.__rsi

    def onBars(self, bars):
        pass