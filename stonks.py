# from datetime import datetime
# from yahoofinancials import YahooFinancials
from pprint import pprint
import pandas as pd
from interfaces import IStockFundamentals
from yahoo_stock import YahooStockData




class StockData:

    def __init__(self, data_provider: IStockFundamentals, ticker):
        self._data_provider = data_provider
        self.ticker = ticker

    def __getattr__(self, name):
        return getattr(self._data_provider, name)

    def to_dataframe(self):
        return pd.DataFrame(
            {
                "Market Cap"                   : self.market_cap,
                "p/e"                          : self.pe,
                "Forward p/e"                  : self.forward_pe,
                "p/b"                          : self.pb,
                "p/s"                          : self.ps,
                "eps"                          : self.eps,
                "Forward eps"                  : self.forward_eps,
                "Net Margin"                   : self.net_margin,
                "ROE"                          : self.roe,
                "ROA"                          : self.roa,
                "Interest Coverage"            : self.interest_coverage,
                "Current Ratio"                : self.current_ratio,
                "Div %"                        : self.div_yield,
                "Payout Ratio"                 : self.div_payout_ratio,
                "Operating Cash Flow per Share": self.ocf_per_share,
                "Short interest"               : self.short_interest,
                "Beta"                         : self.beta,
                # add hystory of earnings, essetsd equity and calculated growth
            },
            index = [self.ticker]
        )

class A():
    def __getattr__(self, name):
        return name

if __name__ == '__main__':
    stock = StockData(YahooStockData('NVDA') ,'NVDA')
    print(stock.pe)
    import pdb;pdb.set_trace()