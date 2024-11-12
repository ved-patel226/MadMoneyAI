import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from MadMoney.loadData.ai import get_chat_completion
from MadMoney.loadData.loadJson import load_json_transcripts
from MadMoney.essentials import MongoDBClient
from tqdm import tqdm


def summarize():
    datas = load_json_transcripts()

    data = datas["transcriptions"]

    prompt = "Make a summary of stocks and add info about if you should buy/sell/hold them. If there is no information about buying/selling/holding stocks... Just give a brief summary of the text. Do not begin with anything and just give the information. Here is the data: "

    chats = []

    for d in tqdm(data, desc="Summarizing transcriptions"):
        chat = get_chat_completion(prompt + d)
        chats.append(chat)

    mongo = MongoDBClient()
    mongo.update_one(
        "transcriptions",
        {"date": datas["date"]},
        {"transcriptions": chats},
    )
    mongo.close()


def main() -> None:
    summarize()


if __name__ == "__main__":
    main()
