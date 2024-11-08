import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from MadMoney.scraping import (
    download_audio_as_wav,
    get_latest_video,
    trim_audio,
    convert_to_json,
)

from MadMoney.loadData.prompt import prompt_result
from MadMoney.essentials import MongoDBClient

from datetime import datetime


def run() -> None:
    # download_audio_as_wav(get_latest_video())
    # trim_audio()
    # convert_to_json()

    result = prompt_result()
    result["date"] = datetime.now()

    mongo = MongoDBClient()
    mongo.insert_one("results", result)
    mongo.close()


def main() -> None:
    run()


if __name__ == "__main__":
    main()
