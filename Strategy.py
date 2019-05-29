from pyalgotrade import strategy
from pyalgotrade.barfeed.csvfeed import GenericBarFeed
from pyalgotrade.bar import Frequency

class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        super(MyStrategy, self).__init__(feed)
        self.__instrument = instrument

    def onBars(self, bars):
        bar = bars[self.__instrument]
        self.info(bar.getClose())

# Load the bar feed from the CSV file
feed = GenericBarFeed(Frequency.DAY)
feed.addBarsFromCSV("aapl", "data/AAPL.csv")

# Evaluate the strategy with the feed's bars.
myStrategy = MyStrategy(feed, "aapl")
myStrategy.run()