import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import json
from collections import defaultdict
from MadMoney.loadData import *


def prompt_result() -> dict:
    summarize()

    datas = load_json_transcripts()

    data = datas["transcriptions"]

    json_format = "{ 'stock symbol': 'buy/sell'}"

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
                print(f"Failed to decode JSON, retrying... Attempt {attempt + 1}")

                if len(prompt.split("\n")) > 1:
                    prompt = "\n".join(prompt.split("\n")[:-1])
                else:
                    print("No more data to remove, exiting...")
                    raise ValueError(
                        "Failed to decode JSON after 10 attempts, exiting..."
                    )

    try_again()

    if len(jsons) == 0:
        raise ValueError("Failed to decode JSON 10 times, exiting...")
    elif len(jsons) <= 3:
        print("Only 1-3 JSONs detected, continuing...")
        try_again()

    merged = defaultdict(list)

    for json_result in jsons:
        for stock, recommendation in json_result.items():
            merged[stock].append(recommendation)

    merged_dict = dict(merged)

    keys_to_delete = [
        stock
        for stock, recommendations in merged_dict.items()
        if len(set(recommendations)) != 1
    ]

    for key in keys_to_delete:
        print("Deleting because of conflicts: ", key)
        del merged_dict[key]

    merged_dict["date"] = datas["date"]

    print("Merged dict: ", merged_dict)

    return merged_dict


def main() -> None:
    prompt_result()


if __name__ == "__main__":
    main()
