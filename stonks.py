# from datetime import datetime
# from yahoofinancials import YahooFinancials
from pprint import pprint
import pandas as pd
from interfaces import IStockFundamentals
from yahoo_stock import YahooStockData




class StockData:

    def __init__(self, data_provider_type, tickers):
        self.tickers = tickers
        self.tickers_data = dict()
        for ticker in set(tickers):
            self.tickers_data[ticker] = data_provider_type(ticker)
            

    def __getitem__(self, key):
        return self.tickers_data[key]

    def has_key(self, k):
        return k in self.tickers_data


    def keys(self):
        return self.tickers_data.keys()

    def values(self):
        return self.tickers_data.values()

    def items(self):
        return self.tickers_data.items()

    def __contains__(self, item):
        return item in self.tickers_data

    def __iter__(self):
        return iter(self.tickers_data)
        
    def to_dataframe(self):
        return pd.concat([x.to_dataframe() for x in self.tickers_data.values()])


if __name__ == '__main__':
    stocks = StockData(YahooStockData ,['NVDA'])
    # print(stock.pe)
    import pdb;pdb.set_trace()