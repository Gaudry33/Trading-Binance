from binance.client import Client
from binance.exceptions import BinanceAPIException
import time
import math
import pandas as pd
from ta import trend
from binance.helpers import round_step_size

API_KEY = "Clé API"
API_SECRET = "Clé API secrète"

CRYPTO = "BTC"
STABLE = "USDC"
PAIR = CRYPTO + STABLE
TRUNC = 4  

class Bot:
    def __init__(self):
        self.client = Client(API_KEY, API_SECRET)

    def trunc(self, value, n):
        power = 10 ** n
        return math.floor(value * power) / power

    def get_data(self):
        now = time.time()
        past = now - 30 * 86400

        klines = self.client.get_historical_klines(
            symbol=PAIR,
            interval=self.client.KLINE_INTERVAL_3MINUTE,
            start_str=str(float(past)),
            end_str=str(float(now))
        )

        df = pd.DataFrame(klines, columns=[
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "qav", "n_trades", "tbav", "tqav", "ignore"
        ])

        df["close"] = df["close"].astype(float)
        df = df[["close"]]
        df["SMA7"] = trend.sma_indicator(df["close"], window=7)
        df["SMA25"] = trend.sma_indicator(df["close"], window=25)
        return df

    def get_balance(self, asset):
        account = self.client.get_account()
        balances = pd.DataFrame(account["balances"])
        balances.set_index("asset", inplace=True)
        if asset in balances.index:
            return float(balances.loc[asset]["free"])
        else:
            return 0.0

    def run(self):
        data = self.get_data()
        price = data["close"].iloc[-1]
        sma7 = data["SMA7"].iloc[-2]
        sma25 = data["SMA25"].iloc[-2]

        stable_balance = self.get_balance(STABLE)
        crypto_balance = self.get_balance(CRYPTO)

        print("Prix :", price)
        print("USDC :", stable_balance)
        print("BTC :", crypto_balance)

        tick_size = '0.01'  

        if sma7 < sma25:
            qty = self.trunc(stable_balance / price, TRUNC)
            if qty > 0.0001:
                buy_price = round_step_size(price * 0.997, tick_size)
                print("Achat limite à", buy_price)
                self.client.create_order(
                    symbol=PAIR,
                    side=self.client.SIDE_BUY,
                    type=self.client.ORDER_TYPE_LIMIT,
                    timeInForce=self.client.TIME_IN_FORCE_GTC,
                    quantity=qty,
                    price=buy_price
                )
            else:
                print("Pas assez d'argents pour acheter")
        elif sma7 > sma25:
            qty = self.trunc(crypto_balance, TRUNC)
            if qty > 0.0001:
                sell_price = round_step_size(price * 1.003, tick_size)
                print("Vente limite à", sell_price)
                self.client.create_order(
                    symbol=PAIR,
                    side=self.client.SIDE_SELL,
                    type=self.client.ORDER_TYPE_LIMIT,
                    timeInForce=self.client.TIME_IN_FORCE_GTC,
                    quantity=qty,
                    price=sell_price
                )
            else:
                print("Pas assez de cryptos pour vendre")
        else:
            print("Pas de signal detecter.")

if __name__ == "__main__":
    bot = Bot()
    try:
        bot.run()
    except BinanceAPIException as e:
        print("Erreur API:", e)
