# python-zulu-trader

This is a Pythonic API wrapper for the ZuluTrade platform. 
http://zulutrade.com

It follows these docs: https://www.zulutrade.com/restapi-reference

I wanted to use this to automate and track other signal-providers and ultimately become a signal-provider myself.

To use this script, you will need to modify the zulutrade_api.py file to hold your signal provider's account username and password. Go look at Line 10 and 11.

'''
zulu_username = ""
zulu_password = ""
'''

Once that's done, simply import the code and setup your trades, then start the trade:

'''
from zulutrade_api import ZTrade

jpy = ZTrade()

jpy.currency = "EUR/JPY"
jpy.take_profit = 135.92
jpy.stop_loss = 137.12
jpy.buy = False
jpy.start()

time.sleep(5)
'''

Note that I make the script sleep for 5 seconds. 

I do this if I am trying to create multiple trades one after the next as the Zulutrade platform does not allow immediate trades to be executed in succession.

Once you start the trade, it will return a generated ID for you to log.

'''
print jpy.trade_id
'''

You can also stop the trade.
'''
jpy.stop()
'''

Lets say you log the trade_id in your database and want to stop the trade, you can also simply set the trade_id and stop it.

'''
jpy = ZTrade()
jpy.trade_id = "111222333"
jpy.stop()
'''

Cool, that's that.

Let me know if you ammend the script to open "pending" trades. I'll attach it to the code base.


Do test this script :)

Happy trading! 