from tinkoff.invest import Client
from tinkoff.invest import BondsResponse, CurrenciesResponse, Currency, CandleInterval, InstrumentStatus, SecurityTradingStatus
from pathlib import Path
from datetime import timedelta
from tinkoff.invest.utils import now
from pprint import pprint

TOKEN = 't.6tuRwI5OJHWofEK4M5ZjwmTQWMn2aHZGkcmqxjNy_OROTfzSwfmZkCDWyxYpxMGZxSJaQkjhuI7f5cXqdRiT3g'

with Client(TOKEN) as client:
    ass = client.instruments.get_assets()
    ass_wi = list(filter(lambda x: len(x.instruments) > 0, ass.assets))
    names = list(map(lambda x: x.name, ass_wi))
    gold = next(filter(lambda x: x.name == 'Золото', ass_wi))

    # client.instruments.get_asset_by(id="b6a73950-20a8-46c7-8b49-9dfbc14fe0ba")
    # print(set(map(lambda x: x.instruments[0].instrument_type, ass.assets)))
    cr = client.instruments.currencies()
    # fp_gold = client.market_data.get_last_prices(figi=["BBG000VJ5YR4", "BBG0013HGFT4"])
    cp_gold = client.market_data.get_candles(figi="BBG000VJ5YR4", from_=now() - timedelta(hours=5), to=now(), interval=CandleInterval.CANDLE_INTERVAL_1_MIN)
    close = client.market_data.get_last_prices(figi=["BBG000VJ5YR4", "BBG0013HGFT4"])
    cp_usd = client.market_data.get_candles(figi="BBG0013HGFT4", from_=now() - timedelta(hours=5), to=now(), interval=CandleInterval.CANDLE_INTERVAL_1_MIN)
    etfs = client.instruments.etfs(instrument_status=InstrumentStatus.INSTRUMENT_STATUS_ALL)
    # client.instruments.find_instrument(query='BBG000VJ5YR4')
    # print(len(cr.instruments))
    # print(list(map(lambda x: x.ticker, cr.instruments)))
    breakpoint()
out = Path('res.txt')
with out.open('w', encoding='utf8') as fh:
    fh.write("\r\n".join(names))