import json
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
    trailing_stop = 20
    conditional_stop = 20
    sleep = True

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
        if self.sleep:
            sleep(6)
        resp = urllib2.urlopen(req)
        return resp.read()

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


    def start_market(self):
        open = self.open_market()
        take_profit  = self.update_take_profit()
        stop_loss = self.update_stop_loss()
        # self.update_trailing_stop()
        #self.update_conditional_stop()
        return open, take_profit, stop_loss

    def start_pending(self):
        open = self.open_pending()
        take_profit  = self.update_take_profit()
        stop_loss = self.update_stop_loss()
        # self.update_trailing_stop()
        #self.update_conditional_stop()
        return open, take_profit, stop_loss


    def update_trailing_stop(self):
        params = {
            "currencyName": self.currency,
            "buy": self.buy,
            "uniqueId":self.trade_id,
            "trailingStopValue":self.trailing_stop,
        }
        url = "/update/stop/trailing/?%s" % (urllib.urlencode(params))
        return_value = self.bind_auth(url)
        return return_value


    def update_conditional_stop(self):
        params = {
            "currencyName": self.currency,
            "buy": self.buy,
            "uniqueId":self.trade_id,
            "trailingStopValue":self.trailing_stop,
            "trailingStopConditionPipsValue":self.conditional_stop,
        }
        url = "/update/stop/trailingCondition/?%s" % (urllib.urlencode(params))
        return_value = self.bind_auth(url)
        return return_value


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
        return return_value


    def open_pending(self):
        params = {
            "currencyName": self.currency,
            "lots": self.lots,
            "buy": self.buy,
            "requestedPrice":self.requested_price,
            "uniqueId": "%s" % self.trade_id
        }
        url = "/open/pending/?%s" % (urllib.urlencode(params))
        return_value = self.bind_auth(url)
        return return_value


    def stop_market(self):
        params = {
            "currencyName": self.currency,
            "lots": self.lots,
            "buy": self.buy,
            "requestedPrice":self.requested_price,
            "uniqueId": self.trade_id,
        }
        url = "/close/market/?%s" % (urllib.urlencode(params))
        res = self.bind_auth(url)
        return res

    def stop_market_provider(self):
        params = {
            "currencyName": self.currency,
            "lots": self.lots,
            "buy": self.buy,
            "requestedPrice":self.requested_price,
            "providerTicket": self.trade_id,
        }
        url = "/close/market/?%s" % (urllib.urlencode(params))
        res = self.bind_auth(url)
        return res

    def stop_pending(self):
        params = {
            "currencyName": self.currency,
            "lots": self.lots,
            "buy": self.buy,
            "requestedPrice": self.requested_price,
            "uniqueId": "%s" % self.trade_id
        }
        url = "/close/pending/?%s" % (urllib.urlencode(params))
        res = self.bind_auth(url)
        return res

    def get_trades(self):
        url = "/getOpen"
        res = self.bind_auth(url)
        return json.loads(res)

    def get_instruments(self):
        url = "/getInstruments"
        res = self.bind_auth(url)
        return json.loads(res)

    def get_stream(self):
        url = "/stream"
        res = self.bind_auth(url)
        return json.loads(res)

    def get_provider_statistics(self):
        url = "/getProviderStatistics"
        res = self.bind_auth(url)
        return json.loads(res)

    def get_trading_configuration(self):
        url = "/getTradingConfiguration"
        res = self.bind_auth(url)
        return json.loads(res)
