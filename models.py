import json
from django.db import models
from zulutrade_api import ZTrade
from django.conf import settings

class Trade(models.Model):
    TRADE_CHOICES = (
        ("cancelled", "Cancelled"),
        ("filled", "Filled"),
        ("trading", "Trading"),
    )
    status = models.CharField(max_length=75, choices = TRADE_CHOICES)
    currency = models.CharField(max_length=10)
    lots = models.FloatField(default=0.01)
    trade_id = models.CharField(max_length=75, blank=True, null=True)
    is_buy = models.BooleanField(default=False)
    take_profit = models.FloatField(null=True, blank=True)
    stop_loss = models.FloatField(null=True, blank=True)
    requested_price = models.FloatField(null=True, blank=True)

    trailing_stop = models.IntegerField(default=20)
    conditional_stop = models.IntegerField(default=20)

    created_at = models.DateTimeField(auto_now = True)
    modified_at = models.DateTimeField(auto_now_add = True)

    trade_list = []
    pending_list = []

    def set_trades(self, trade_res):
        trade_res = trade_res
        self.trade_list =  trade_res["openPositions"]
        self.pending_list =  trade_res["openOrders"]
        return self.trade_list, self.pending_list

    def get_trade_obj(self):
        return_value = None
        hit_trade = False
        for item in self.trade_list:
            if ("%s" % item["currencyName"]).strip() == ("%s" % self.currency).strip():
                return_value = item
                self.trade_id = item["uniqueId"]
                self.save()
                hit_trade = True

        if not hit_trade:
            for item in self.pending_list:
                if ("%s" % item["currencyName"]).strip() == ("%s" % self.currency).strip():
                    return_value = item
                    self.trade_id = item["uniqueId"]
                    self.save()
        return return_value


    def start_pending(self):
        trade = ZTrade()
        trade.currency = self.currency
        trade.take_profit = self.take_profit
        trade.stop_loss = self.stop_loss
        trade.requested_price = self.requested_price
        trade.trailing_stop = self.trailing_stop
        trade.conditional_stop = self.conditional_stop
        if self.lots:
            trade.lots = self.lots
        else:
            trade.lots = settings.TRADE_LOTS
        trade.buy = self.is_buy
        trade.start_pending()
        self.status = "trading"
        self.trade_id = trade.trade_id
        self.save()


    def stop_pending(self):
        trade = ZTrade()
        trade.trade_id = self.trade_id
        trade.currency = self.currency
        if self.lots:
            trade.lots = self.lots
        else:
            trade.lots = settings.TRADE_LOTS
        trade.take_profit = self.take_profit
        trade.stop_loss = self.stop_loss
        trade.trailing_stop = self.trailing_stop
        trade.conditional_stop = self.conditional_stop
        trade.buy = self.is_buy
        self.status = "filled"
        trade.stop_pending()
        self.trade_id = None
        self.save()


    def start_market(self):
        trade = ZTrade()
        trade.currency = self.currency
        trade.take_profit = self.take_profit
        trade.stop_loss = self.stop_loss
        trade.trailing_stop = self.trailing_stop
        trade.conditional_stop = self.conditional_stop
        if self.lots:
            trade.lots = self.lots
        else:
            trade.lots = settings.TRADE_LOTS
        trade.buy = self.is_buy
        trade.start_market()
        self.status = "trading"
        self.trade_id = trade.trade_id
        self.save()


    def stop_market(self):
        trade = ZTrade()
        trade.trade_id = self.trade_id
        trade.currency = self.currency
        if self.lots:
            trade.lots = self.lots
        else:
            trade.lots = settings.TRADE_LOTS
        trade.take_profit = self.take_profit
        trade.stop_loss = self.stop_loss
        trade.trailing_stop = self.trailing_stop
        trade.conditional_stop = self.conditional_stop
        trade.buy = self.is_buy
        self.status = "filled"
        trade.stop_market()
        self.trade_id = None
        self.save()

    def stop_market_provider(self):
        trade = ZTrade()
        trade.trade_id = self.trade_id
        trade.currency = self.currency
        if self.lots:
            trade.lots = self.lots
        else:
            trade.lots = settings.TRADE_LOTS
        trade.take_profit = self.take_profit
        trade.stop_loss = self.stop_loss
        trade.trailing_stop = self.trailing_stop
        trade.conditional_stop = self.conditional_stop
        trade.buy = self.is_buy
        self.status = "filled"
        trade.stop_market_provider()
        self.trade_id = None
        self.save()

    def get_instruments(self):
        trade = ZTrade()
        trade.sleep = False
        return trade.get_instruments()

    def get_stream(self):
        trade = ZTrade()
        trade.sleep = False
        return trade.get_stream()
