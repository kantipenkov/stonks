from yahoofinancials import YahooFinancials
from pprint import pprint
import pandas as pd

# stock = YahooFinancials('NVDA')
# pprint(stock.get_summary_data())
# pprint(stock.get_stock_earnings_data())
# pprint(stock.get_financial_stmts('annual', ['cash', 'balance', 'income']))
# import pdb;pdb.set_trace()

class StockData:
    ticker = None
    yahoo_obj = None
    _market_cap = None
    _pe = None
    _pb = None
    _ps = None
    _net_margin = None
    _roe = None
    _roa = None
    _interest_coverage = None
    _current_ratio = None
    _roic = None
    _wacc = None
    _div_yeld = None
    _div_payout_ratio = None
    _div_grouth = None
    _ocf_per_share = None
    _debt_to_equity = None
    _debt_to_ebidta = None

    _desired_pe = None
    _desired_proce = None

    _financials = None


    def __init__(self, ticker):
        self.ticker = ticker
        self.yahoo_obj = YahooFinancials(self.ticker)
        self._financials = StockFinansials(self.ticker, self.yahoo_obj)
        # read saved target
        # not implemented
        # read saved data from database and add new from object of there is some
        # it may be useful to know next earnings report date in order to reduce amount of requests and execution acceleration
        # not implemented
        # get current price and recalculate multiplicators or get them from yahoo

    def _get_data(self):
        price_data = self.yahoo_obj.get_stock_price_data()
        # self.
        self.yahoo_obj.get_financial_stmts('annual', '')

    def to_dataframe(self):
        pass

    @property
    def pe(self):
        if not self._pe:
            self._pe = self.yahoo_obj.get_current_price() * self.yahoo_obj.get_num_shares_outstanding() / self._financials.earnings_ttm
        return self._pe

class StockFinansials:
    quarterly = None
    yearly = None

    def __init__(self, ticker, yahoo_obj):
        self.ticker = ticker
        self.yahoo_obj = yahoo_obj
        earnings_data = self.yahoo_obj.get_stock_earnings_data()
        self.quarterly = pd.DataFrame(earnings_data[self.ticker]['financialsData']['quarterly'])
        self.yearly = pd.DataFrame(earnings_data[self.ticker]['financialsData']['yearly'])

    @property
    def earnings_ttm(self):
        return self.quarterly.loc[:,  "earnings"].sum()


if __name__ == '__main__':
    stock = StockData('NVDA')
    import pdb;pdb.set_trace()