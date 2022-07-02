from fractions  import Fraction
from typing import Union, Dict, List
import numpy as np
from pathlib import Path
from pprint import pprint
from datetime import datetime
from collections import namedtuple
from dataclasses import dataclass, field


import logging
logger = logging.getLogger('root')

# PricePointBase = namedtuple('PricePointBase', ['timestamp', 'open', 'high', 'low', 'close', 'volume'])

SplitPoint = namedtuple('SplitPoint', ['timestamp', 'split_ratio'])

@dataclass(order=True)
class PricePoint:
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    date: str = field(init=False, repr=True)
    sort_index: float = field(init=False, repr=False)

    def __post_init__(self):
        self.date = datetime.fromtimestamp(self.timestamp).strftime("%Y-%m-%d")
        self.sort_index = self.timestamp

    def __repr__(self) -> str:
        return f"PricePoint(date={self.date}, open={self.open}, high={self.high}, low={self.low}, close={self.close}, volume={self.volume})"

    def to_dict(self):
        return {
            'timestamp': self.timestamp,
            'open': self.open,
            'high': self.high,
            'low':  self.low,
            'close': self.close,
            'volume': self.volume
        }


def detect_splits(points: Union[List[PricePoint], List[Dict]]):
    
    if isinstance(points[0], PricePoint):
        logger.debug("Tuple provided")
        prices = np.array(list(map(lambda x: list(x.to_dict().values()), points)))
        # print(points)
    elif isinstance(points[0], dict):
        logger.debug("dict provided")
        prices = np.array(list(map(lambda x: list(x.values()), points)))
        # print(initial_data)
    else:
        raise Exception(f"Unsupported element type! Provided {type(points[0])} but only PricePointTuple and Dict with corresponding names are supported.")

    
    closes = prices[:-1, 4:5]
    opens = prices[1:, 1:2]
    diff = closes - opens 
    ratio = np.divide(diff, opens)

    cond2 = np.where(abs(ratio) > 0.45)
    indices = np.unique(cond2[0])
    if len(indices) > 0:
        timestamps = prices[1:, :1][indices]
        timestamps = np.stack(np.vectorize(datetime.fromtimestamp)(timestamps))
        # dates = np.stack(np.vectorize(datetime.strftime)(timestamps, "%Y-%m-%d"))
        # add calculation of split ratio
        days_around_ind = np.hstack((indices, indices + 1))
        days_around_ind.sort()
        # get prices
        splits = list()
        for before_split, after_split in prices[days_around_ind].reshape(indices.shape[0], -1, 6):
            bs_pp = PricePoint(*before_split)
            as_pp = PricePoint(*after_split)
            if bs_pp.volume > 0 and as_pp.volume > 0:
                rf = Fraction(bs_pp.close / as_pp.open)
                split_ratio = rf.limit_denominator(2)
                for i in range(3,100):
                    if split_ratio.numerator > 0 and abs((bs_pp.close / as_pp.open) - split_ratio.numerator / split_ratio.denominator) / (bs_pp.close / as_pp.open) < 0.1:
                        break
                    split_ratio = rf.limit_denominator(i)
                logger.info(f"Potential split date {as_pp.date} " \
                    f"ratio {split_ratio.numerator}:{split_ratio.denominator}")
                splits.append(SplitPoint(as_pp.timestamp, split_ratio))
        # import pdb;pdb.set_trace()
        # for split_point in splits[::-1]:
        #     inds = np.where(prices[:,0] < split_point.timestamp)[0]
        #     prices[inds,1:] = np.stack(np.vectorize(apply_split)(prices[inds,1:], split_point.split_ratio))
    else:
        splits = list()
    return splits

def process_csv_data(data: str, as_dict: bool=False):
    """Returns either list of dicts for each price point or list of PricePointTuple elements for each point"""
    lines = list(map(lambda x: x.split(','), data.strip().split('\n')))
    # points_count = len(lines) - 1
    headers = lines[0]
    # just check that names are the same
    required_headers = ("timestamp","open","high","low","close","volume",)
    if not all([x in headers for x in required_headers]):
        logger.warning("some fields are missing. Pleaseupdate the parser")
    inds = dict(zip(required_headers, map(lambda x: headers.index(x), required_headers)))
    points = [{key: pp[inds[key]] for key in inds.keys()} for pp in lines[1:]]
    
    for elem in points:
        for key in elem.keys():
            if key == "timestamp":
                elem[key] = datetime.strptime(elem[key], '%Y-%m-%d').timestamp()
            else:
                elem[key] = float(elem[key])
    return points if as_dict else list(map(lambda x: PricePoint(**x), points))



if __name__ == "__main__":
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

    data_path = Path(__file__).parent / '..' / 'daily_NVDA.csv'
    # data_path = Path('../daily_adjusted_IBM.csv')

    with data_path.open('r') as fh:
        data = fh.read()
    # parse data
    series = process_csv_data(data, True)
    # series[0].items()
    # print(series)
    # get splits from yahoo and apply them
    # detect_splits(series)
    # apply split
    # apply series of splits

    # unapply split/ series of splits

    # detect splits
    # import pdb;pdb.set_trace()
