# sandbox_token = r"t.M2YY9WI1qpyj08Gtyz3K1tKIJKrlv-GOovaEbuPaxM1NUoqS9DGViZzoYE62KTefdO_UdFkPkwsveq6LMyNNuA"
import json
from pprint import pprint

import tinvest
token = r"t.EfCp4TofWCVKSaX03bmK7ub22251uoulrZipEcjMqV3ilGH9tmNpj0mgbto-_9pwkC-kkgpFh3P0bnkcbGa_sQ"
client = tinvest.SyncClient(token)
# client.register_sandbox_account(SandboxRegisterRequest())
client.get_market_stocks()
stocks_list = client.get_market_stocks().dict()['payload']['instruments']
tickers = [x["ticker"] for x in stocks_list]

with open("tickers.json", "w") as fh:
    json.dump(ticker, fh, indent=4)
import pdb;pdb.set_trace()
