import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from MadMoney.essentials import MongoDBClient
from datetime import datetime
from yfinance import Ticker


def get_30_day_price_history(ticker_symbol: str):
    ticker = Ticker(ticker_symbol)
    history = ticker.history(period="1mo")

    return history


def get_recent():

    mongo = MongoDBClient()
    ttl = mongo.find_many("results", {})

    most_recent = None
    for item in ttl:
        if most_recent is None:
            most_recent = item
        else:
            if item["date"] > most_recent["date"]:
                most_recent = item

    most_recent.pop("_id", None)
    most_recent["date"] = most_recent["date"].strftime("%Y-%m-%d")

    itemsToChange = []
    prices = []

    itemsToLoop = [key for key in most_recent.keys() if key != "date"]

    for item in itemsToLoop:
        if item[0] == "^":
            itemsToChange.append(item)
            most_recent[item[1:]] = most_recent.pop(item)
            item = item[1:]

        history = get_30_day_price_history(item)

        prices.append([item, history["Close"].to_numpy().tolist()])

    most_recent["prices"] = prices

    return most_recent


def main() -> None:
    print(get_recent())


if __name__ == "__main__":
    main()
