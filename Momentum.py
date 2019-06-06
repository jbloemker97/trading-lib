from pyalgotrade import strategy
from pyalgotrade.barfeed.csvfeed import GenericBarFeed
from pyalgotrade.bar import Frequency
from pyalgotrade.technical import rsi

class MomentumStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        super(MomentumStrategy, self).__init__(feed)
        self.__instrument = instrument
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__rsi = rsi.RSI(self.__prices, 14)

    def getRSI(self):
        return self.__rsi

    def onBars(self, bars):
        # Wait for bars to load
        if self.__rsi[-1] is None:
            return

        bar = bars[self.__instrument]

        if self.enterLongSignal(bar):
            self.info(f"Entering Long: {bar.getPrice()}")


    def enterLongSignal(self, bar):
        return self.__rsi[-1] < 50 # Threshold

feed = GenericBarFeed(Frequency.DAY)
feed.addBarsFromCSV("AAPL", "data/AAPL.csv")

momentumStrategy = MomentumStrategy(feed, "AAPL")
momentumStrategy.run()