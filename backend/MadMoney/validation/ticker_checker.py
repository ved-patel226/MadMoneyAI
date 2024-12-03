import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import yfinance as yf
from MadMoney.loadData import load_json_results

from MadMoney.essentials import MongoDBClient
import time
from bson import ObjectId
from collections import Counter


def is_valid_ticker(ticker):
    info = yf.Ticker(ticker).history(period="1d", interval="1d")
    return len(info) > 0


def check_json_ticker() -> None:
    data = load_json_results()
    data2 = data.copy()

    data = {k: v for k, v in data.items() if "_id" not in k and "date" not in k}
    data = {k: v for k, v in data.items() if is_valid_ticker(k)}

    result = {}

    for ticker, (recommendations, _) in data.items():
        recommendation_count = Counter(recommendations)
        most_common = recommendation_count.most_common(1)[0][0]
        result[ticker] = [most_common, data2[ticker][1]]

    result["_id"] = data2["_id"]
    result["date"] = data2["date"]

    mongo = MongoDBClient()
    mongo.delete_one("results", {"_id": data2["_id"]})
    mongo.insert_one("results", result)
    mongo.close()


def main() -> None:
    data = check_json_ticker()
    print(data)


if __name__ == "__main__":
    main()
