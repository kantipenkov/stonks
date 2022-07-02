from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from enum import Enum

from datetime import datetime
import argparse
from pathlib import Path
from time import sleep
import json
import shutil
from pprint import pprint


class ScrapMethods(Enum):
    SEEKING_ALPHA = "SEEKING_ALPHA"
    YAHOO_FINANCE = "YAHOO_FINANCE"

def alpha_splits(driver, url):
    # import pdb;pdb.set_trace()
    # driver.
    driver.get(url)

    # elem = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, "info")))
    elem = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test-id='table-header']")))

    rows = elem.find_elements(By.TAG_NAME, "tr")
    if rows:
        print("found splits")
        for row in rows:
            print(row.text)
    else:
        data = elem.find_element(By.CLASS_NAME, "no-data")
        if data:
            print(data.text)
    sleep(10)
    
    driver.quit()
    sleep(5)

class FinanceException(Exception):
    "Failed to get data for ticker"

def finance_splits(driver, url):
    driver.get(url)
    try:
        elem = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Download')))
        elem.click()
        sleep(10)
    except TimeoutException as e:
        raise FinanceException(f"failed get data for f{url}")

def download_splits_data(method:ScrapMethods, tickers=(), out_folder="tmp"):
    options = webdriver.ChromeOptions()
    downloads = Path(out_folder).resolve()
    if downloads.exists():
        shutil.rmtree(str(downloads))
    downloads.mkdir()
    prefs = {"download.default_directory": str(downloads.resolve())}
    options.add_experimental_option("prefs", prefs)
    # options.add_argument("--headless")
    
    alpha_template = r'https://seekingalpha.com/symbol/{ticker}/splits'
    yahoo_url_template = r'https://finance.yahoo.com/quote/{ticker}/history?period1={start}&period2={end}&interval=div%7Csplit&filter=split&frequency=1d'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    failed_tickers_path = Path("f_tickers.json")
    failed_tickers = []
    try:
        for ticker in tickers:
            if method == ScrapMethods.SEEKING_ALPHA.value:
                url = alpha_template.format(ticker=ticker)
            elif method == ScrapMethods.YAHOO_FINANCE.value:
                url = yahoo_url_template.format(
                                                ticker=ticker,
                                                start=int(datetime(1999, 12, 1, 3, 0).timestamp()),
                                                end=int(datetime.now().timestamp())
                                                )
            else:
                raise Exception("Unknown resource to scrap")
            try:
                finance_splits(driver, url)
            except FinanceException:
                failed_tickers.append(ticker)

    except Exception as e:
        raise
    finally:
        driver.quit()
        with failed_tickers_path.open("w") as fh:
            json.dump(failed_tickers, fh)

def parse_splits(path):
    results = dict()
    for f in Path(path).glob("*.csv"):
        # print(f.stem)
        with f.open('r') as fh:
            data = fh.readlines()
        splits = list()
        if len(data) > 1:
            for i in range(1, len(data)):
                (date, ratio) = data[i].strip().split(',')
                (denominator, numerator) = ratio.split(":")
                # print(date)
                # print(ratio)
                # print(int(numerator) / int(denominator))
                splits.append((datetime.strptime(date, '%Y-%m-%d'),
                                int(numerator) / int(denominator)
                                ))
        results[f.stem] = splits
    return results

if __name__ == "__main__":
    # add mode options
    # make it available to run separate operations
    # use argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--get_splits", action="store_true", help="get splis for tickers")
    parser.add_argument("-t", "--tickers_file", help="path to json with tickers")
    parser.add_argument("--ticker", help="a single ticker to get splits")
    parser.add_argument("-p", "--process", action="store_true", help="process gathered data")
    parser.add_argument("-o", "--out_folder", default="tmp", help="folder to store downloaded files")
    args = parser.parse_args()
    print(args)
    if args.get_splits:
        if not any((args.tickers_file, args.ticker)):
            raise Exception("no tickers provided to get data for")
        if args.tickers_file:
            tickers_file = Path(args.tickers_file).resolve()
            print(tickers_file)
            if tickers_file.exists():
                with tickers_file.open('r') as fh:
                    tickers = json.load(fh)
            else:
                raise Exception(f"can't find {str(tickers_file)}")
        elif args.ticker:
            tickers = list()
            tickers.append(args.ticker)
        download_splits_data(method=ScrapMethods.YAHOO_FINANCE.value, tickers=tickers, out_folder=args.out_folder)
    if args.process:
        splits = parse_splits(path=args.out_folder)
        pprint(splits)
        # print("process downloaded files")
        
        # read all files and get splits
