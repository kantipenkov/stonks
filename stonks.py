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
    _forward_pe = None
    _pb = None
    _ps = None
    _eps = None
    _forward_eps = None
    _net_margin = None
    _roe = None
    _roa = None
    _interest_coverage = None
    _current_ratio = None
    _roic = None
    _wacc = None
    _div_yield = None
    _div_payout_ratio = None
    _div_growth = None
    _ocf_per_share = None
    _debt_to_equity = None
    _debt_to_ebidta = None

    _short_interest = None
    _beta = None
    _avg_volume = None
    _volume = None


    _desired_pe = None
    _desired_proce = None

    _financials = None


    def __init__(self, ticker):
        self.ticker = ticker
        self.yahoo_obj = YahooFinancials(self.ticker)
        self._financials = StockFinansials(self.ticker, self.yahoo_obj)
        self._get_data()
        # read saved target
        # not implemented
        # read saved data from database and add new from object of there is some
        # it may be useful to know next earnings report date in order to reduce amount of requests and execution acceleration
        # not implemented
        # get current price and recalculate multiplicators or get them from yahoo

    def _get_data(self):
        summary = self.yahoo_obj.get_summary_data()[self.ticker]
        self._market_cap = summary['marketCap']
        self._pe = summary['trailingPE']
        self._forward_pe = summary['forwardPE']
        self._ps = summary['priceToSalesTrailing12Months']
        self._eps = summary['trailingEps']
        self._forward_eps = summary['forwardEps']
        self._div_yield = summary['dividendYield'] * 100
        self._div_payout_ratio = summary['payoutRatio']
        self._beta = summary['beta']
        self._avg_volume = summary['averageVolume']
        self._volume = summary['volume']

        # key statistics
        key_stats = self.yahoo_obj.get_key_statistics_data()[self.ticker]
        self._net_margin = key_stats['profitMargins']
        self._short_interest = key_stats['shortPercentOfFloat']
        self._pb = key_stats['priceToBook']

        # calculate by self
        self._roe
        self._roa
        self._current_ratio
        self._interest_coverage
        self._roic
        self._wacc
        self._div_growth




    def to_dataframe(self):
        pass

    @property
    def pe(self):
        if not self._pe:
            self._pe = self.yahoo_obj.get_current_price() * self.yahoo_obj.get_num_shares_outstanding() / self._financials.earnings_ttm
        return self._pe

    @property
    def market_cap(self):
        if not self._market_cap:
            self._market_cap = self.yahoo_obj.get_market_cap()
        return self._market_cap
    
    @property
    def pb(self):
        if not self._pb:
            if self._market_cap:
                self._pb = self._market_cap /  self.yahoo_obj.get_book_value()
            else:
                self._pb = self.yahoo_obj.get_market_cap /  self.yahoo_obj.get_book_value()
        return self._pb
    
    @property
    def ps(self):
        if not self._ps:
            self.yahoo_obj.get_price_to_sales()
        return self._ps

    @property
    def eps(self):
        if not self._eps:
            self._eps = self.yahoo_obj.get_earnings_per_share()
        return self._eps
    
    @property
    def net_margin(self):
        if not self._net_margin:
            self._get_data()
        return self._net_margin

    @property
    def div_yield(self):
        if not self._div_yield:
            self._div_yield = self.yahoo_obj.get_dividend_yield()
        return self._div_yield

    @property
    def div_payout_ratio(self):
        if not self._div_payout_ratio:
            self._div_payout_ratio = self.yahoo_obj.get_payout_ratio()
        return self._div_payout_ratio
    
    @property
    def roe(self):
        if not self._roe:
            # update stock finansial to get required data
            # get formula from gurufocus
            self._roe = self._financials
        return self._roe


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