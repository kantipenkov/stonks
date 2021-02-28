""" implementation based on yahoofinancials"""
from datetime import datetime
from yahoofinancials import YahooFinancials

import pandas as pd


from interfaces import IStockFundamentals


class YahooStockData(IStockFundamentals):
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
    # _roic = None
    # _wacc = None
    _div_yield = None
    _div_payout_ratio = None
    # _div_growth = None
    _ocf_per_share = None
    _debt_to_equity = None
    _debt_to_ebidta = None

    _short_interest = None
    _beta = None
    _avg_volume = None
    _volume = None


    _desired_pe = None
    _desired_price = None

    _financials = None


    def __init__(self, ticker):
        self._ticker = ticker
        self.yahoo_obj = YahooFinancials(self.ticker)
        self._financials = StockFinansials(self.ticker, self.yahoo_obj)
        self.get_data()
        # read saved target
        # not implemented
        # read saved data from database and add new from object of there is some
        # it may be useful to know next earnings report date in order to reduce amount of requests and execution acceleration
        # not implemented
        # get current price and recalculate multiplicators or get them from yahoo

    def get_data(self):
        summary = self.yahoo_obj.get_summary_data()[self.ticker]
        self._market_cap = summary['marketCap']
        self._pe = summary['trailingPE']
        self._forward_pe = summary['forwardPE']
        self._ps = summary['priceToSalesTrailing12Months']
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
        self._eps = key_stats['trailingEps']
        self._forward_eps = key_stats['forwardEps']

        # calculate by self

        # self._roic
        # self._wacc
        # self._div_growth

    @property
    def ticker(self):
        return self._ticker

    @property
    def pe(self):
        if not self._pe:
            self._pe = self.yahoo_obj.get_current_price() * self.yahoo_obj.get_num_shares_outstanding() / self._financials.earnings_ttm
        return self._pe
    
    @property
    def forward_pe(self):
        if not self._forward_pe:
            self.get_data()
        return self._forward_pe

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
    def forward_eps(self):
        if not self._forward_eps:
            self.get_data()
        return self._forward_eps
    
    @property
    def net_margin(self):
        if not self._net_margin:
            self.get_data()
        return self._net_margin * 100

    @property
    def div_yield(self):
        if not self._div_yield:
            self._div_yield = self.yahoo_obj.get_dividend_yield()
        return self._div_yield * 100

    @property
    def div_payout_ratio(self):
        if not self._div_payout_ratio:
            self._div_payout_ratio = self.yahoo_obj.get_payout_ratio()
        return self._div_payout_ratio
    
    @property
    def roe(self):
        if not self._roe:
            self._roe = self._financials.earnings_ttm / self._financials.stockholders_equity_avg
        return self._roe * 100
    
    @property
    def roa(self):
        if not self._roa:
            self._roa = self._financials.earnings_ttm / self._financials.total_assets_avg
        return self._roa * 100
    
    @property
    def interest_coverage(self):
        if not self._interest_coverage:
            self._interest_coverage = -1 * self.yahoo_obj.get_operating_income() / self.yahoo_obj.get_interest_expense()
        return self._interest_coverage

    @property
    def current_ratio(self):
        if not self._current_ratio:
            self._current_ratio = self._financials.current_assets / self._financials.current_liabilities
        return self._current_ratio

    @property
    def ocf_per_share(self):
        if not self._ocf_per_share:
            self._ocf_per_share = self._financials.ttm_operating_cash_flow / self.yahoo_obj.get_num_shares_outstanding()
        return self._ocf_per_share

    @property
    def short_interest(self):
        if not self._short_interest:
            self.get_data()
        return self._short_interest * 100

    @property
    def beta(self):
        if not self._beta:
            self.get_data()
        return self._beta




class StockFinansials:
    earnings_quarterly = None
    erarnings_yearly = None

    def __init__(self, ticker, yahoo_obj):
        self.ticker = ticker
        self.yahoo_obj = yahoo_obj
        earnings_data = self.yahoo_obj.get_stock_earnings_data()
        self.earnings_quarterly = pd.DataFrame(earnings_data[self.ticker]['financialsData']['quarterly'])
        self.erarnings_yearly = pd.DataFrame(earnings_data[self.ticker]['financialsData']['yearly'])
        # self.balances = pd.DataFrame({datetime.strptime(list(x.keys())[0], '%Y-%m-%d'): x[list(x.keys())[0]] for x in self.yahoo_obj.get_financial_stmts('annual', 'balance')['balanceSheetHistory'][self.ticker]}) 
        # self.balances = self.balances[self.balances.columns.sort_values()]
        self.balances_y = self._get_financial_data_frame('annual', 'balance')
        self.income_y = self._get_financial_data_frame('annual', 'income')
        self.cash_y = self._get_financial_data_frame('annual', 'cash')
        self.cash_q = self._get_financial_data_frame('quarterly', 'cash')

    def _get_financial_data_frame(self, frequency, statement_type):
        mapping = {
            "balance": "balanceSheetHistory",
            "income": "incomeStatementHistory",
            "cash": "cashflowStatementHistory",
        }
        key = mapping[statement_type]
        if frequency == 'quarterly':
            key = key + 'Quarterly'
        data = self.yahoo_obj.get_financial_stmts(frequency, statement_type)
        df = pd.DataFrame({datetime.strptime(list(x.keys())[0], '%Y-%m-%d'): x[list(x.keys())[0]] for x in data[key][self.ticker]})
        df = df[df.columns.sort_values()]
        return df


    @property
    def earnings_ttm(self):
        return self.earnings_quarterly.loc[:,  "earnings"].sum()

    @property
    def stockholders_equity_avg(self, num_of_periods: int=2):
        return self.balances_y.loc['totalStockholderEquity', :].tail(num_of_periods).sum() / num_of_periods

    @property
    def total_assets_avg(self, num_of_periods: int=2):
        return self.balances_y.loc['totalAssets', :].tail(num_of_periods).sum() / num_of_periods
    
    @property
    def current_assets(self):
        return self.balances_y.loc['totalCurrentAssets', self.balances_y.columns[-1]]
    
    @property
    def current_liabilities(self):
        return self.balances_y.loc['totalCurrentLiabilities', self.balances_y.columns[-1]]

    @property
    def ttm_operating_cash_flow(self):
        return self.cash_q.loc['totalCashFromOperatingActivities', :].sum()
