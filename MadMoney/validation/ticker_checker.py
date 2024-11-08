import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import yfinance as yf
from MadMoney.loadData import load_json_results

from MadMoney.essentials import MongoDBClient


def is_valid_ticker(ticker):
    info = yf.Ticker(ticker).history(period="1d", interval="1d")
    return len(info) > 0


def check_json_ticker() -> None:
    data = load_json_results()
    data2 = data.copy()

    print("Checking for valid tickers in the JSON data...")
    data = {
        key: value
        for key, value in data.items()
        if key == "_id" or key == "date" or is_valid_ticker(key)
    }

    print("Number of valid tickers: ", len(data) - 2)
    print(data)

    if len(data2) == len(data):
        print("All tickers are valid!")
    else:
        print("Invalid tickers: ")
        for key, value in data2.items():
            if key not in data:
                print(key, value)

        mongo = MongoDBClient()
        mongo.update_one("results", data2, data)
        mongo.close()

        print("Invalid tickers have been removed from the JSON data.")


def main() -> None:
    data = check_json_ticker()
    # print(is_valid_ticker("BROADCOM"))


if __name__ == "__main__":
    main()
