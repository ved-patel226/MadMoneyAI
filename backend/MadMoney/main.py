import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from MadMoney.scraping import (
    download_audio_as_wav,
    get_latest_video,
    trim_audio,
    convert_to_json,
)

from MadMoney.loadData.prompt import prompt_result_mongo
from MadMoney.essentials import MongoDBClient
from MadMoney.validation import check_json_ticker

from datetime import datetime


def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


# download_audio_as_wav(get_latest_video())
# trim_audio()
# convert_to_json()

# clear_screen()

prompt_result_mongo()

check_json_ticker()

clear_screen()

print("Data has been successfully added to the database.")
