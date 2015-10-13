from django.core.management.base import NoArgsCommand
from zulutrade_api import ZTrade
import time

class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        jpy = ZTrade()
        jpy.currency = "EUR/JPY"
        jpy.take_profit = 135.92
        jpy.stop_loss = 137.12
        jpy.buy = False
        jpy.start()

        time.sleep(5)

        cad = ZTrade()
        cad.currency = "USD/CAD"
        cad.take_profit = 1.32001
        cad.stop_loss = 1.2918
        cad.buy = True
        cad.start()

        time.sleep(5)

        cad.stop()