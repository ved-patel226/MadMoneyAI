import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from MadMoney.essentials import MongoDBClient
from datetime import datetime


def load_json_transcripts():
    mongo = MongoDBClient()
    transcripts = mongo.find_many("transcriptions", {})
    dates = []
    for transcript in transcripts:
        dates.append(transcript["date"])

    latest = max(dates)
    latest_transcript = mongo.find_one("transcriptions", {"date": latest})

    return latest_transcript


def load_json_results():
    mongo = MongoDBClient()

    results = mongo.find_many("results", {})
    dates = []
    for result in results:
        dates.append(result["date"])

    latest = max(dates)
    latest_result = mongo.find_one("results", {"date": latest})

    return latest_result


if __name__ == "__main__":
    data = load_json_transcripts()
    print(data)
