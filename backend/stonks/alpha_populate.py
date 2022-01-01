from pprint import pprint

import logging
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
# create formatter

# add formatter to ch
handler.setFormatter(formatter)

logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)
# add ch to logger
logger.addHandler(handler)

import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stonks.settings')
import django
django.setup()

from utils.alpha_vantage import AlphaVantage
from utils.ticker_data import TickerData, update_earnings_dates


if __name__ == '__main__':
    api_key = "VLFPX8TAR2XREWC2"
    api = AlphaVantage.api_key = api_key
    ticker = "INTC"
    logger.debug('ap')
    # import pdb;pdb.set_trace()
    for ticker in ('NVDA', 'AMD', 'INTC', 'ILMN'):
        ticker_data = TickerData(ticker)
        ticker_data.update_db_fundamentals()
    # import pdb;pdb.set_trace()
    update_earnings_dates(6)
    # data = AlphaVantage.get_earnings_calendar(100, 'AMD') 
    # import numpy as np
    # arr = np.array(','.join(data.split('\r\n')).split(',')[:-1]).reshape(-1, 6)
