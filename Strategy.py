from pyalgotrade import strategy
from pyalgotrade.barfeed.csvfeed import GenericBarFeed
from pyalgotrade.bar import Frequency

class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        super(MyStrategy, self).__init__(feed)
        self.__instrument = instrument

    def onBars(self, bars):
            bar = bars[self.__instrument]
            self.info(f"{self.__instrument}: {bar.getClose()}")   



    


def run_strat(instrument):
    # Load the bar feed from the CSV file
    feed = GenericBarFeed(Frequency.DAY)
    feed.addBarsFromCSV(instrument, f"data/{instrument}.csv")

    myStrategy = MyStrategy(feed, instrument)
    myStrategy.run()

def main():
    # Evaluate the strategy with the feed's bars.
    stocks = ['TSLA', 'SPY', 'AAPL']

    for stock in stocks:
        run_strat(stock)

main()