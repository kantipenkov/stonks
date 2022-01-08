from pprint import pprint

import json

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
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stonks.settings')
import django
django.setup()

from utils.alpha_vantage import AlphaVantage, DailyReuestsAmountExceded
from utils.ticker_data import TickerData, TickerNotFound, update_earnings_dates


if __name__ == '__main__':
    tickers = ('NVDA', 'AMD', 'INTC', 'ILMN')
    if len(sys.argv) > 1:
        tickers_file = sys.argv[1]
        if os.path.exists(tickers_file):
            with open(tickers_file, 'r') as fh:
                tickers = json.load(fh)
    # import pdb;pdb.set_trace()
    api_key = "VLFPX8TAR2XREWC2"
    api = AlphaVantage.api_key = api_key
    # ticker = "INTC"
    logger.debug('ap')
    # import pdb;pdb.set_trace()
    failed_tickers = list()
    try:
        for ticker in tickers:
            ticker_data = TickerData(ticker)
            try:
                ticker_data.update_db_fundamentals()
            except TickerNotFound as e:
                failed_tickers.append(f"{ticker}: {str(e)}")
    except DailyReuestsAmountExceded as e:
        logger.warning("Daily limit of requests exceded")
    with open("failed_tickers.json", "w") as fh:
        fh.writelines(failed_tickers)
    update_earnings_dates(6)
    # data = AlphaVantage.get_earnings_calendar(100, 'AMD') 
    # import numpy as np
    # arr = np.array(','.join(data.split('\r\n')).split(',')[:-1]).reshape(-1, 6)
