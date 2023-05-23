import pandas as pd
import pandas_datareader.data as pdr
import yfinance as yfin
from tradings.strategies import *
import matplotlib.pyplot as plt

yfin.pdr_override()
plt.style.use('Solarize_Light2')


def get_data(stocks, start, end) -> pd.DataFrame:
    ydata = pdr.get_data_yahoo(stocks, start, end)
    return ydata


def run_bh(data, cash_amount, start, end):
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.addstrategy(BuyAndHold)
    broker_args = dict(coc=True)
    cerebro.broker = bt.brokers.BackBroker(**broker_args)
    comminfo = FixedCommisionScheme()
    cerebro.broker.addcommissioninfo(comminfo)
    cerebro.broker.set_cash(cash_amount)

    cerebro.run()
    cerebro.plot(iplot=False, style='candlestick', figsize=(12, 8))


def run_bm(data, cash_amount):
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.addstrategy(BuyMore)
    broker_args = dict(coc=True)
    cerebro.broker = bt.brokers.BackBroker(**broker_args)
    comminfo = FixedCommisionScheme()
    cerebro.broker.addcommissioninfo(comminfo)
    cerebro.broker.set_cash(cash_amount)
    cerebro.run()
    cerebro.plot(iplot=False, style='candlestick')