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
logger.setLevel(logging.INFO)
# add ch to logger
logger.addHandler(handler)

import os 
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stonks.settings')
import django
django.setup()

from utils.alpha_vantage import AlphaVantage, DailyReuestsAmountExceded
from utils.ticker_data import TickerData, TickerNotFound, update_earnings_dates

def log_failed_ticker(msg):
    with open("failed_tickers.json", "a") as fh:
        fh.write(msg + "\n")

if __name__ == '__main__':
    api_key = "VLFPX8TAR2XREWC2"
    AlphaVantage.api_key = api_key
    tickers = ('NVDA', 'AMD', 'INTC', 'ILMN', 'MDMG')
    if len(sys.argv) > 1:
        tickers_file = sys.argv[1]
        if os.path.exists(tickers_file):
            with open(tickers_file, 'r') as fh:
                tickers = json.load(fh)
    logger.debug('ap')
    try:
        for ticker in tickers:
            ticker_data = TickerData(ticker)
            try:
                ticker_data.update_db_fundamentals()
            except (TickerNotFound, Exception) as e:
                logger.warning(f"Cant get data for {ticker}")
                log_failed_ticker(f"{ticker}: {str(e)}")
                # raise
    except DailyReuestsAmountExceded as e:
        logger.warning("Daily limit of requests exceded")
    update_earnings_dates(6)
