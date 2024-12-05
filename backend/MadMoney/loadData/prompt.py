import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import json
from collections import defaultdict
from MadMoney.loadData import summarize, load_json_transcripts, get_chat_completion
from MadMoney.essentials import MongoDBClient
from datetime import datetime
from pprint import pprint


def prompt_result() -> dict:
    # summarize()

    datas = load_json_transcripts()

    data = datas["transcriptions"]

    json_format = "{ 'stock ticker': ['buy/sell', 'reason why to buy/sell the stock'] }"

    prompt_lines = [
        f"You are an investment advisor. You will return JSON data in the form: {json_format}. the stock ticker is the STOCK TICKER. example: APPL for APPLE; DIS for DISNEY. DO NOT PUT ANYTHING ELSE. JUST THE JSON DATA. You will use this data to figure out the stock data. DO NOT USE ANY OTHER KNOWLEDGE EXCEPT FOR THIS DATA:"
    ]

    for stock in data:
        prompt_lines.append(stock)

    prompt = "\n".join(prompt_lines)

    jsons = []

    for stock in data:
        prompt += f"\n{stock}"

    def try_again(prompt: str = prompt) -> None:
        result = (
            get_chat_completion(prompt)
            .replace("\n", "")
            .replace("`", "")
            .replace("json", "")
            .replace("JSON", "")
        )

        try:
            json_result = json.loads(result)
            jsons.append(json_result)

        except json.JSONDecodeError:
            print(f"Failed to decode JSON, trying again... {result}")
            prompt_fix = "FIX THE JSON DATA. ONLY OUTPUT THE FIXED JSON DATA"
            prompt_fix += f"\n{prompt_fix}"

            result = get_chat_completion(prompt_fix)

            if len(prompt.split("\n")) > 1:
                prompt = "\n".join(prompt.split("\n")[:-1])
            else:
                print("No more data to remove, exiting...")
                raise ValueError("Failed to decode JSON after 10 attempts, exiting...")

    for i in range(5):
        try_again()

    return normalize_result(jsons)


def normalize_result(results: list) -> dict:
    transformed_data = {}

    for results in results:
        for stock, data in results.items():
            try:
                action, reason = data
                transformed_data[stock] = [action, reason]
            except:
                pass

    return transformed_data


def prompt_result_mongo() -> dict:
    result = prompt_result()
    result["date"] = datetime.now()

    pprint(result)

    mongo = MongoDBClient()
    mongo.insert_one("results", result)
    mongo.close()


def main() -> None:
    prompt_result_mongo()


if __name__ == "__main__":
    main()
