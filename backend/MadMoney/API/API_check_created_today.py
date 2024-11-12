import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from MadMoney.essentials import MongoDBClient
from datetime import datetime


def check_created_today() -> dict | bool:
    mongo = MongoDBClient()
    transcripts = mongo.find_many("results", {})
    dates = [transcript["date"] for transcript in transcripts]

    today = datetime.today().strftime("%Y-%m-%d")
<<<<<<< HEAD
    try:
        latest = max(dates)
    except:
        return False

=======
    latest = max(dates)
>>>>>>> 0a0662676ea2ca5ef2b8eac4b75e1ba2fcb82ee4
    latest_strftime = latest.strftime("%Y-%m-%d")

    if latest_strftime == today:
        latest_transcript = mongo.find_one("results", {"date": latest})

        keys_to_remove = [key for key in latest_transcript if key == "_id"]
        for key in keys_to_remove:
            latest_transcript.pop(key)

        return latest_transcript

    return False


def main() -> None:
    latest_transcript = check_created_today()


if __name__ == "__main__":
    main()