# python-zulu-trader

Hi all,

This is a Pythonic API wrapper for the ZuluTrade platform. http://zulutrade.com

It follows these docs: https://www.zulutrade.com/restapi-reference

I use this code to automate and track other signal-providers and ultimately feed it to my own zulu signal-provider account.

To use this script, you will need to modify the code in 'zulutrade_api.py' to hold your signal provider's account username and password.
Go look at Line 13 and 14.

```
zulu_username = ""
zulu_password = ""
```

Once that's done, simply import the code and setup your trades, then start the pending order:

```
from zulutrade_api import ZTrade

t = ZTrade()
t.currency = "EUR/JPY"
t.take_profit = 135.92
t.stop_loss = 137.12
t.buy = False
t.start_pending()

```

Once you start the pending order, it will return a generated trade_id for you to work with.

```
print t.trade_id
```

If you would like to enter the trade as an open position, rather use:

```
t.start_market()
```

You can also stop the trade if you provide ZTrade with it's Unique Id.

```
t.trade_id = "111222333"
t.stop_market()
t.stop_pending()
```

Using models.py, you are able to track your trade and start/stop the pending order or open positions.

```
from models import Trade
t = Trade()
t.currency = "EUR/JPY"
t.take_profit = 135.92
t.stop_loss = 137.12
t.buy = False
t.start_market()

t.stop_market()
```

Do test this script and let me know if you have any suggestions :)

I've also added a Django models.py file, so that you can quickly save and track your trades.

Happy trading!

Paul Hoft
