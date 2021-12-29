import numpy as np
import json
from pathlib import Path
from pprint import pprint
import re
from datetime import datetime
from collections import namedtuple
PricePoint = namedtuple('PricePoint', ['date', 'open', 'high', 'low', 'close', 'volume'])
# c = np.array([[[  0,  1,  2],  # a 3D array (two stacked 2D arrays)
#                 [ 10, 12, 13]],
#                [[100, 101, 102],
#                 [110, 112, 113]]])

# print(c.shape)
# print(c[1, ...])
# print(c[..., 1])
data_file = Path('series_test.json')
with data_file.open('r') as fh:
    json_data = json.load(fh)
# json.loads(Path('series_test.json').open('r').as)
# {date: values for date, values in json_data.items()}
prices = list()
for date, values in json_data["Time Series (Daily)"].items():
    # print(date, values)
    # import pdb;pdb.set_trace()
    # pprint({re.sub('\d+\.\s+', '', key): value for key, value in values.items()})
    timestamp = datetime.strptime(date, '%Y-%m-%d').timestamp()
    candle = {re.sub('\d+\.\s+', '', key): float(value) for key, value in values.items()}
    prices.append(PricePoint(timestamp, **candle))
    # updated_dict[datetime.strptime(date, '%Y-%m-%d').timestamp()] = {re.sub('\d+\.\s+', '', key): float(value) for key, value in values.items()}
prices = np.array(prices)[::-1]
# pprint(prices)
# split indicators:
# big diff bigger than 20% between close and open or in all four values
#  
closes = prices[:-1, 4:5]
opens = prices[1:, 1:2]
diff = closes - opens 
ratio = np.divide(diff, opens)
# diff = np.diff(prices[:,1:-1], axis=0)
# ratio = np.divide(diff, prices[1:, 1:-1])
# cond = abs(ratio) > 0.3
cond2 = np.where(abs(ratio) > 0.45)
indices = np.unique(cond2[0])
timestamps = prices[1:, :1][indices]
timestamps = np.stack(np.vectorize(datetime.fromtimestamp)(timestamps))
dates = np.stack(np.vectorize(datetime.strftime)(timestamps, "%Y-%m-%d"))
print(timestamps)
pprint(np.hstack((dates, ratio[:,0:1][indices])))
# add calculation of split ratio
import pdb;pdb.set_trace()

# real splits:
# 07.20.2021 4-1
# 09.11.2007 1.5-1
# 04.07.2006 2-1
# 09.17.2001 2-1
# 06.27.2000 2-1