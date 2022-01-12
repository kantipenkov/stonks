from fractions import Fraction
import json
import numpy as np
from pathlib import Path
from pprint import pprint
import re
from datetime import datetime
from collections import namedtuple

import logging
logger = logging.getLogger('root')

PricePointBase = namedtuple('PricePointBase', ['timestamp', 'open', 'high', 'low', 'close', 'volume'])

SplitPoint = namedtuple('SplitPoint', ['timestamp', 'split_ratio'])


class PricePointTuple(PricePointBase):

    @property
    def date(self):
        return datetime.fromtimestamp(self.timestamp).strftime("%Y-%m-%d")

    def __repr__(self) -> str:
        return f"PricePointTuple(date={self.date}, open={self.open}, high={self.high}, low={self.low}, close={self.close}, volume={self.volume})"

    def to_dict(self):
        return {
            'date': self.date,
            'open': self.open,
            'high': self.high,
            'low':  self.low,
            'close': self.close,
            'volume': self.volume
        }


def apply_split(num, split_ratio: Fraction):
    return num / split_ratio.numerator * split_ratio.denominator

def process_prices(json_data):
    # data_file = Path('series_test.json')
    # with data_file.open('r') as fh:
    #     json_data = json.load(fh)
    # import pdb;pdb.set_trace()
    prices = list()
    for date, values in json_data["Time Series (Daily)"].items():
        timestamp = datetime.strptime(date, '%Y-%m-%d').timestamp()
        candle = {re.sub('\d+\.\s+', '', key): float(value) for key, value in values.items()}
        prices.append(PricePointTuple(timestamp, **candle))

    prices = np.array(prices)[::-1]

    closes = prices[:-1, 4:5]
    opens = prices[1:, 1:2]
    diff = closes - opens 
    ratio = np.divide(diff, opens)

    cond2 = np.where(abs(ratio) > 0.45)
    indices = np.unique(cond2[0])
    if len(indices) > 0:
        timestamps = prices[1:, :1][indices]
        timestamps = np.stack(np.vectorize(datetime.fromtimestamp)(timestamps))
        dates = np.stack(np.vectorize(datetime.strftime)(timestamps, "%Y-%m-%d"))
        # add calculation of split ratio
        days_around_ind = np.hstack((indices, indices + 1))
        days_around_ind.sort()
        # get prices
        splits = list()
        for before_split, after_split in prices[days_around_ind].reshape(indices.shape[0], -1, 6):
            bs_pp = PricePointTuple(*before_split)
            as_pp = PricePointTuple(*after_split)
            print("############")
            print(bs_pp)
            print(as_pp)
            print("############")
            if bs_pp.volume > 0 and as_pp.volume > 0:
                print("EEEEE")
                # print(bs_pp)
                # print(as_pp)
                rf = Fraction(bs_pp.close / as_pp.open)
                split_ratio = rf.limit_denominator(2)

                for i in range(3,100):
                    if split_ratio.numerator > 0 and abs((bs_pp.close / as_pp.open) - split_ratio.numerator / split_ratio.denominator) / (bs_pp.close / as_pp.open) < (9 - i) / 90:
                        break
                    split_ratio = rf.limit_denominator(i)
                logger.info(f"Potential split date {as_pp.date} " \
                    f"ratio {split_ratio.numerator}:{split_ratio.denominator}")
                splits.append(SplitPoint(as_pp.timestamp, split_ratio))
        import pdb;pdb.set_trace()
        for split_point in splits[::-1]:
            inds = np.where(prices[:,0] < split_point.timestamp)[0]
            prices[inds,1:] = np.stack(np.vectorize(apply_split)(prices[inds,1:], split_point.split_ratio))
    else:
        splits = list()
    
    return prices, np.array(splits)

# import pdb;pdb.set_trace()

# calculate splits ratios using fractions module
#  


# real splits:
# 07.20.2021 4-1
# 09.11.2007 1.5-1
# 04.07.2006 2-1
# 09.17.2001 2-1
# 06.27.2000 2-1

# ARWR real splits are 2011-11-17 1:10 and 2004-01-15 1:65
if __name__ == "__main__":
    data_file = Path('series_test.json')
    with data_file.open('r') as fh:
        json_data = json.load(fh)
    process_prices(json_data)