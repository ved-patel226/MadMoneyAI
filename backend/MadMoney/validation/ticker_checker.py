import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import yfinance as yf
from MadMoney.loadData import load_json_results, get_chat_completion

from MadMoney.essentials import MongoDBClient
import time
from bson import ObjectId
from collections import Counter
from pprint import pprint


def is_valid_ticker(ticker):
    info = yf.Ticker(ticker).history(period="1d", interval="1d")
    return len(info) > 0


def valid_ticker(stock):
    if is_valid_ticker(stock):
        return stock

    def try_again(stock):
        prompt = f"What is the correct stock ticker for {stock}? ONLY OUTPUT THE TICKER"
        return get_chat_completion(prompt)

    for _ in range(5):
        stock = try_again(stock)
        if is_valid_ticker(stock):
            return stock

    return False


def check_json_ticker() -> None:
    data = load_json_results()
    data2 = data.copy()

    data = {k: v for k, v in data.items() if "_id" not in k and "date" not in k}
    data = {valid_ticker(k): v for k, v in data.items() if valid_ticker(k)}
    data = {
        k: [v[0].title(), v[1]]
        for k, v in data.items()
        if v[0].lower() in ["buy", "sell", "hold"]
    }

    data["_id"] = data2["_id"]
    data["date"] = data2["date"]

    pprint(data)

    mongo = MongoDBClient()
    mongo.delete_one("results", {"_id": data2["_id"]})
    mongo.insert_one("results", data)
    mongo.close()


def main() -> None:
    data = check_json_ticker()


if __name__ == "__main__":
    main()
