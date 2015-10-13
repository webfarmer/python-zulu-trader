import random
from time import sleep
import urllib2
import urllib
import base64

class ZTrade(object):
    url = "http://tradingserver.zulutrade.com"
    req = False
    zulu_username = ""
    zulu_password = ""
    currency = "EUR/USD"
    buy = True
    lots = 0.01
    take_profit = 1.5
    trade_id = 0
    stop_loss = 0.5
    requested_price= 1.13980

    def __init__(self):
        self.get_trade_id()
        super(ZTrade, self).__init__()

    def set_trade_id(self, trade_id):
        self.trade_id = trade_id
        return self.trade_id

    def get_trade_id(self):
        self.trade_id = random.randint(100000, 999999)*87
        return self.trade_id

    def bind_auth(self, url_ammend):
        new_url = "%s%s" % (self.url, url_ammend)
        req = urllib2.Request(new_url)
        req.add_header('Authorization', 'Basic %s' % base64.b64encode(bytes("%s:%s" % (self.zulu_username, self.zulu_password)), 'utf-16be'))
        resp = urllib2.urlopen(req)
        return resp.read()

    def open_market(self):
        params = {
            "currencyName": self.currency,
            "lots": self.lots,
            "buy": self.buy,
            "requestedPrice":self.requested_price,
            "uniqueId": "%s" % self.trade_id
        }
        url = "/open/market/?%s" % (urllib.urlencode(params))
        return_value = self.bind_auth(url)
        sleep(5)
        return return_value

    #take profit
    def update_take_profit(self):
        params = {
            "currencyName": self.currency,
            "limitValue": self.take_profit,
            "buy": self.buy,
            "uniqueId": "%s" % self.trade_id
        }
        url = "/update/limit/?%s" % (urllib.urlencode(params))
        res = self.bind_auth(url)
        return res

    #stop loss
    def update_stop_loss(self):
        params = {
            "currencyName": self.currency,
            "stopValue": self.stop_loss,
            "buy": self.buy,
            "uniqueId": "%s" % self.trade_id
        }
        url = "/update/stop/?%s" % (urllib.urlencode(params))
        res = self.bind_auth(url)
        return res

    def start(self):
        open = self.open_market()
        take_profit  = self.update_take_profit()
        stop_loss = self.update_stop_loss()
        return open, take_profit, stop_loss

    def stop(self):
        params = {
            "currencyName": self.currency,
            "lots": self.lots,
            "buy": self.buy,
            "requestedPrice": self.requested_price,
            "uniqueId": "%s" % self.trade_id
        }
        url = "/close/market/?%s" % (urllib.urlencode(params))
        res = self.bind_auth(url)
        return res
