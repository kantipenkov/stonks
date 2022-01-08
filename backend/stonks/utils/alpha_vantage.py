from datetime import datetime
from pprint import pprint
# import pdb

import json
from enum import Enum
import os
import requests
import time

import logging
logger = logging.getLogger('root')


class AlphaVantageApiException(Exception):
    """incorrect API arguments"""


class NoApiKey(AlphaVantageApiException):
    "Please set api key to pull some data from api"


class DailyReuestsAmountExceded(AlphaVantageApiException):
    """No more API requests available this day"""

class API_FUNCTIONS(Enum):
    INCOME = "INCOME_STATEMENT"
    BALANCE = "BALANCE_SHEET"
    CASH_FLOW = "CASH_FLOW"
    EARNINGS = "EARNINGS"
    OVERVIEW = "OVERVIEW"
    TIME_SERIES_DAILY = "TIME_SERIES_DAILY"
    EARNINGS_CALENDAR = "EARNINGS_CALENDAR"


class ApiTimeoutManager():
    
    _config_file = "alpha_vantage_config.txt"
    _time_str_format = "%Y-%m-%d %H:%M:%S"
    _max_requests_per_minute = 5
    _max_requests_per_day = 350
    _current_operations_per_day = 0
    _current_operations_per_minute = 0
    _first_operation_timestamp = None
    _first_of_five_operations_timestamp = None

    @classmethod
    def _set_requests_limiters(cls, minute: int, day: int):
        cls._max_requests_per_minute = minute
        cls._max_requests_per_day = day

    @classmethod
    def reset_minute_counter(cls):
        cls._first_of_five_operations_timestamp = time.time()
        cls._current_operations_per_minute = 1

    @classmethod
    def reset_day_counter(cls):
        cls._current_operations_per_day = 1
        cls._first_operation_timestamp = time.time()

    @classmethod
    def check_api_timeout(cls):
        if not cls._first_operation_timestamp:
            if os.path.exists(cls._config_file):
                with open(cls._config_file, 'r') as fh:
                    config = json.load(fh)
                cls._max_requests_per_minute = config["_max_requests_per_minute"]
                cls._max_requests_per_day = config["_max_requests_per_day"]
                cls._current_operations_per_day = config["_current_operations_per_day"]
                cls._current_operations_per_minute = config["_current_operations_per_minute"]
                cls._first_operation_timestamp = datetime.strptime(config["_first_operation_timestamp"], cls._time_str_format).timestamp()
                cls._first_of_five_operations_timestamp = datetime.strptime(config["_first_of_five_operations_timestamp"], cls._time_str_format).timestamp()
            else:
                cls._first_operation_timestamp = time.time()
                cls._first_of_five_operations_timestamp = cls._first_operation_timestamp
        log_data = {
                    "_max_requests_per_minute" : cls._max_requests_per_minute,
                    "_max_requests_per_day" : cls._max_requests_per_day,
                    "_current_operations_per_day" : cls._current_operations_per_day,
                    "_current_operations_per_minute" : cls._current_operations_per_minute,
                    "_first_operation_timestamp" : datetime.fromtimestamp(cls._first_operation_timestamp).strftime(cls._time_str_format),
                    "_first_of_five_operations_timestamp" : datetime.fromtimestamp(cls._first_of_five_operations_timestamp).strftime(cls._time_str_format),
                    # "limit_exceeded_at": datetime.now().strftime(cls._time_str_format)
                }
        cls._current_operations_per_day += 1
        cls._current_operations_per_minute += 1
        with open(cls._config_file, "w") as fh:
            json.dump(log_data, fh, indent=4)
        if cls._current_operations_per_minute > cls._max_requests_per_minute:
            diff = time.time() - cls._first_of_five_operations_timestamp
            minute_in_seconds = 60
            if diff < minute_in_seconds:
                break_time = minute_in_seconds - diff + 2 # to be sure
                logger.info(f"Exceed max amount of requests per minute wait for {break_time} seconds")
                time.sleep(break_time)
                cls.reset_minute_counter()
            else:
                cls.reset_minute_counter()
        
        if cls._current_operations_per_day > cls._max_requests_per_day:
            diff =  time.time() - cls._first_operation_timestamp
            day_in_seconds = 24 * 60 * 60
            if diff < day_in_seconds:
                break_time = day_in_seconds - diff + 60 # just to be sure
                logger.info(f"Exceed maximum requests per day. Will wait for {time.strftime('%H hours %M minutes and %S seconds', time.gmtime(break_time))} seconds")
                raise DailyReuestsAmountExceded("No more API requests available this day")
            else:
                cls.reset_day_counter()
                # time.str


class AlphaVantage():
    api_key = None

    # implement time tracked our only 5 calls a minute and 500 calls a day are available
    # when request received we should wait if we exeeded available amount of calls

    @classmethod
    def check_api_timeout(cls):
        ApiTimeoutManager.check_api_timeout()

    @classmethod
    def compose_url(cls, api_key, function, ticker=None, **kwargs):
        base_url = f"https://www.alphavantage.co/query?function={function}&apikey={api_key}"
        if ticker:
            base_url += f"&symbol={ticker}"
        if kwargs:
            for key, value in kwargs.items():
                base_url += f"&{key}={value}"
        return base_url

    @classmethod
    def get_income(cls, ticker):        
        logger.info(f"getting income statements for {ticker}")
        return cls.request_data(API_FUNCTIONS.INCOME.value, ticker)

    @classmethod
    def get_balance(cls, ticker):
        logger.info(f"getting balances for {ticker}")
        return cls.request_data(API_FUNCTIONS.BALANCE.value, ticker)

    @classmethod
    def get_cash_flows(cls, ticker):
        logger.info(f"getting cash flows for {ticker}")
        return cls.request_data(API_FUNCTIONS.CASH_FLOW.value, ticker)

    @classmethod
    def get_earnings(cls, ticker):
        logger.info(f"getting earnings for {ticker}")
        return cls.request_data(API_FUNCTIONS.EARNINGS.value, ticker)

    @classmethod
    def get_overview(cls, ticker):
        logger.info(f"getting overview for {ticker}")
        return cls.request_data(API_FUNCTIONS.OVERVIEW.value, ticker)

    @classmethod
    def request_data(cls, function, ticker, output_format='json', **kwargs):
        """performs api call with given parameters"""
        cls.check_api_timeout()
        alowed_outputs = ('json', 'csv')
        if output_format not in alowed_outputs:
            raise AlphaVantageApiException("Improper output format provided {output_format}. Alowed only json and csv")
        logger.info(f"request data for {ticker} function {function}")
        if not cls.api_key:
            raise NoApiKey("please set api key before pulling data from api" )
        url = cls.compose_url(cls.api_key, function, ticker, **kwargs)
        # import pdb;pdb.set_trace()
        logger.debug(f"request to {url}")
        if output_format == "json":
            r = requests.get(url)
            # import pdb;pdb.set_trace()
            return r.json()
        else:
            with requests.Session() as s:
                download = s.get(url)
                decoded_content = download.content.decode('utf-8')
            return decoded_content
            # import pdb;pdb.set_trace()
                # cr = csv.reader(decoded_content.splitlines(), delimiter=',')
                # my_list = list(cr)
            return None
    
    @classmethod
    def get_price_series(cls, ticker):
        logger.info(f"getting price series for {ticker}")
        return cls.request_data(function=API_FUNCTIONS.TIME_SERIES_DAILY.value, ticker=ticker, outputsize="full")

    @classmethod
    def get_earnings_calendar(cls, months_num=3, ticker=None):
        """
            return estimated earnings dates for all provided ticker or for all available tickers on the period of next months_num months
            number of months can be 3,6,12 if different number was provided than func rounds it to closest of available
        """
        alowed_nums = (3, 6, 12)
        if months_num not in alowed_nums:
            cur_val = None
            cur_diff = 1000
            for i in alowed_nums:
                diff = abs(months_num - i)
                if diff < cur_diff:
                    cur_diff = diff
                    cur_val = i
            months_num = cur_val
        msg = "getting earnings calendar for next {month_num}"
        if ticker:
            msg += f" for {ticker}"
        logger.info(msg)
        return cls.request_data(API_FUNCTIONS.EARNINGS_CALENDAR.value, ticker=ticker, output_format="csv", horizon=f"{months_num}month")





def api_timeout_manager_test():
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

    ApiTimeoutManager._set_requests_limiters(5, 12)
    start_time = time.time()
    
    for i in range(1,15):
        logger.info(f"attempt {i}, time from start {time.time() - start_time} seconds")
        ApiTimeoutManager.check_api_timeout()
        time.sleep(1)

if __name__ == "__main__":
    api_timeout_manager_test()