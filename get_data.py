from yahoo_fin import stock_info
from datetime import datetime
from pprint import pprint
ticker = 'NVDA'
cash_flows = stock_info.get_cash_flow(ticker)
# cash_flows = stock_info.get_cash_flow(ticker).to_dict()

# cash_flows = {k.strftime('%Y-%b-%d'):v for k,v in cash_flows.items()}
# get net income
operating_cash = cash_flows[cash_flows.columns[0]]['totalCashFromOperatingActivities']
print(operating_cash)
stock_stats = stock_info.get_stats(ticker)
shares_outstanding_str = stock_stats[stock_stats.Attribute.str.match('Shares Outstanding')].Value.values[0] 
if shares_outstanding_str[-1:] == 'M':
    shares_outstanding = float(shares_outstanding_str[:-1]) * 10 ** 6
print(shares_outstanding)
print(operating_cash/shares_outstanding)
print(stock_info.get_earnings(ticker))
# import pdb;pdb.set_trace()