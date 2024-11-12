import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from MadMoney.essentials import MongoDBClient
from datetime import datetime


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

    return most_recent


def main() -> None:
    print(get_recent())


if __name__ == "__main__":
    main()
