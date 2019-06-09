from pyalgotrade import strategy, plotter
from pyalgotrade.barfeed.csvfeed import GenericBarFeed
from pyalgotrade.bar import Frequency
from pyalgotrade.technical import rsi, ma, macd
from pyalgotrade.stratanalyzer import sharpe

class MomentumStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instruments, smaPeriod, overBoughtThreshold):
        super(MomentumStrategy, self).__init__(feed)
        self.__instruments = instruments
        self.__overBoughtThreshold = overBoughtThreshold
        self.__feed = feed
        self.__prices = {}
        self.__rsi = {}
        self.__ma = {}
        self.__macd = {}
        self.__longPos = None

        for instrument in feed.getRegisteredInstruments():
            self.__prices[instrument] = feed[instrument].getPriceDataSeries()
            self.__rsi[instrument] = rsi.RSI(self.__prices[instrument], 14)
            self.__ma[instrument] = ma.SMA(self.__prices[instrument], smaPeriod)
            self.__macd[instrument] = macd.MACD(self.__prices[instrument], 12, 26, 9).getHistogram() # Buy when historgram is > 0. Sell when histogram is < 0

    def onBars(self, bars):

        # Loop through list of stocks
        for instrument in self.__instruments:

            if self.__rsi[instrument][-1] is None or self.__ma[instrument][-1] is None or self.__macd[instrument][-1] is None:
                return
            
            bar = bars[instrument]

            if self.__longPos is not None:
                if self.exitSignal(bar, instrument):
                    self.__longPos.exitMarket()
            else:
                if self.entrySignal(bar, instrument):
                    shares = int(self.getBroker().getCash() * 0.9 / bar.getPrice())
                    self.__longPos = self.enterLong(instrument, shares, True)

    def entrySignal(self, bar, instrument):
        return bar.getClose() > self.__ma[instrument][-1] and self.__macd[instrument][-1] >= 0
    
    def exitSignal(self, bar, instrument):
        return self.__rsi[instrument][-1] > self.__overBoughtThreshold or self.__macd[instrument][-1] < 0

def main (instruments, plot=False):
    smaPeriod = 200
    overBoughtThreshold = 70
    feed = GenericBarFeed(Frequency.DAY)

    # building feed with multiple instruments
    for instrument in instruments:
        feed.addBarsFromCSV(instrument, f"data/{instrument}.csv")

    strat = MomentumStrategy(feed, instruments, smaPeriod, overBoughtThreshold)
    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    strat.attachAnalyzer(sharpeRatioAnalyzer)

    strat.run()
    print("Sharpe ratio: %.2f" % sharpeRatioAnalyzer.getSharpeRatio(0.05))

    if plot:
        plt.plot()
   

main(['AAPL', 'TSLA', 'SPY'])


