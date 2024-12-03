import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import json
from collections import defaultdict
from MadMoney.loadData import *
from MadMoney.essentials import MongoDBClient
from datetime import datetime
from pprint import pprint


def prompt_result() -> dict:
    summarize()

    datas = load_json_transcripts()

    data = datas["transcriptions"]

    json_format = "{ 'stock symbol': ['buy/sell', 'reason why to buy/sell the stock'] }"

    prompt_lines = [
        f"You are an investment advisor. You will return JSON data in the form: {json_format} DO NOT PUT ANYTHING ELSE. JUST THE JSON DATA. You will use this data to figure out the stock data. DO NOT USE ANY OTHER KNOWLEDGE EXCEPT FOR THIS DATA:"
    ]

    for stock in data:
        prompt_lines.append(stock)

    prompt = "\n".join(prompt_lines)

    jsons = []

    for stock in data:
        prompt += f"\n{stock}"

    def try_again(prompt: str = prompt) -> None:
        for attempt in range(10):
            result = get_chat_completion(prompt)
            try:
                json_result = json.loads(result)
                jsons.append(json_result)

            except json.JSONDecodeError:
                print(
                    f"Failed to decode JSON, retrying... Attempt {attempt + 1}. Result: {result}"
                )

                if len(prompt.split("\n")) > 1:
                    prompt = "\n".join(prompt.split("\n")[:-1])
                else:
                    print("No more data to remove, exiting...")
                    raise ValueError(
                        "Failed to decode JSON after 10 attempts, exiting..."
                    )

    try_again()

    if len(jsons) <= 3:
        print("Only 1-3 JSONs detected, continuing...")
        try_again()

    return normalize_result(jsons)


def normalize_result(result=dict) -> dict:

    results = defaultdict(list)

    for r in result:
        for stock, data in r.items():
            results[stock].append(data)

    transformed_data = {}
    for key, values in results.items():
        actions = [item[0] for item in values]
        reasons = max([item[1] for item in values], key=len)
        transformed_data[key] = [actions, reasons]

    return transformed_data


def prompt_result_mongo() -> dict:
    result = prompt_result()
    result["date"] = datetime.now()

    pprint(result)

    mongo = MongoDBClient()
    mongo.insert_one("results", result)
    mongo.close()


def main() -> None:
    promptt = prompt_result_mongo()


if __name__ == "__main__":
    main()
