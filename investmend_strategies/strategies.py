import math
import backtrader as bt
import datetime


class BuyAndHold(bt.Strategy):
    def __init__(self):
        self.end_date = datetime.datetime.now()                             # Change here if needed
        self.start_date = datetime.datetime(2015, 1, 2)                     # Change here if needed
        self.val_start = None
        self.roi = None

    def start(self):
        self.val_start = self.broker.get_cash()

    def nextstart(self):
        size = math.floor((self.broker.get_cash() - 10) / self.data[0])     # -10 for commission
        self.buy(size=size)

    def stop(self):
        self.roi = (self.broker.get_value() / self.val_start) - 1
        print('-'*50)
        print('BUY & HOLD')
        print(f'Starting Value:  ${self.val_start}')
        print(f'ROI:              {self.roi * 100.0}%')
        print(f'Annualised:       {100*((1+self.roi)**(365/(self.end_date-self.start_date).days) -1)}%')
        print(f'Gross Return:    ${self.broker.get_value() - self.val_start}')


class FixedCommisionScheme(bt.CommInfoBase):
    params = {
        'commission': 10,
        'stocklike': True,
        'commtype': bt.CommInfoBase.COMM_FIXED
    }

    def _getcommission(self, size, price, pseudoexec):
        return self.p.commission


class BuyMore(bt.Strategy):
    params = dict(
        monthly_cash=1000,
        monthly_range=[5, 20]
    )
    def __init__(self):
        self.end_date = datetime.datetime.now()
        self.start_date = datetime.datetime(2015, 1, 2)

        self.roi = None
        self.val_start = None
        self.cash_start = None
        self.froi = None
        self.order = None
        self.totalcost = 0
        self.cost_wo_bro = 0
        self.units = 0                      # N of shares
        self.times = 0

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def start(self):
        self.broker.set_fundmode(fundmode=True, fundstartval=100.0)

        self.cash_start = self.broker.get_cash()
        self.val_start = 100.0

        # ADD A TIMER
        self.add_timer(
            when=bt.timer.SESSION_START,
            monthdays=[i for i in self.p.monthly_range],
            monthcarry=True
            # timername='buytimer',
        )

    def notify_timer(self, timer, when, *args):
        self.broker.add_cash(self.p.monthly_cash)

        target_value = self.broker.get_value() + self.p.monthly_cash - 10
        self.order_target_value(target=target_value)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price %.2f, Cost %.2f, Comm %.2f, Size %.0f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm,
                     order.executed.size)
                )

                self.units += order.executed.size
                self.totalcost += order.executed.value + order.executed.comm
                self.cost_wo_bro += order.executed.value
                self.times += 1

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
            print(order.status, [order.Canceled, order.Margin, order.Rejected])

        self.order = None

    def stop(self):
        # calculate actual returns
        self.roi = (self.broker.get_value() / self.cash_start) - 1
        self.froi = (self.broker.get_fundvalue() - self.val_start)
        value = self.datas[0].close * self.units + self.broker.get_cash()
        print('-' * 50)
        print('BUY & BUY MORE')
        print(f'Time in Market: {(self.end_date - self.start_date).days / 365} years')
        print(f'#Times:         {self.times}')
        print(f'Value:         ${value}')
        print(f'Cost:          ${self.totalcost}')
        print(f'Gross Return:  ${value - self.totalcost}')
        print(f'Gross %:        {(value / self.totalcost - 1) * 100}%')
        print(f'ROI:            {100.0 * self.roi}%')
        print(f'Fund Value:     {self.froi}%')
        print(f'Annualised:     {100 * ((1 + self.froi / 100) ** (365 / (self.end_date - self.start_date).days) - 1)}%')
        print('-' * 50)

