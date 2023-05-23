import warnings
from tradings.utils import *
warnings.filterwarnings('ignore')

stockList = ['VGK']
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=1800)
cash_amount = 100000
cash_amount2 = 10000


stock_data = get_data(stockList[0], start_date, end_date)
data = bt.feeds.PandasData(dataname=stock_data)
run_bh(data=data, cash_amount=cash_amount, start=start_date, end=end_date)
run_bm(data=data, cash_amount=cash_amount2)

