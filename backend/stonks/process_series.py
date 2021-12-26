import json
import numpy as np
from pathlib import Path
from pprint import pprint


if __name__ =="__main__":
    data_file = Path("time_series.json")
    with data_file.open('r') as fh:
        data = json.load(fh)
    series_data = data["Time Series (Daily)"]
    names = ["date", "values"]
    import pdb;pdb.set_trace()