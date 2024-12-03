import sys
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from MadMoney.essentials import MongoDBClient
from datetime import datetime
from tqdm import tqdm
import whisper


def convert_to_json() -> None:
    model = whisper.load_model("medium")

    segments_dir = "segments"

    try:
        files = os.listdir(segments_dir)
        print(f"{len(files)} segments detected")
    except:
        raise FileNotFoundError("No segments detected")

    full_transcription = []

    for file in tqdm(files, desc="Converting voice to text (Please wait)"):
        with open("segments/" + file, "rb") as f:
            print(f"Converting {file} to text")

            transcription = model.transcribe(segments_dir + "/" + file)

            full_transcription.append(transcription["text"])

    mongo = MongoDBClient()
    mongo.insert_one(
        "transcriptions", {"date": datetime.now(), "transcriptions": full_transcription}
    )
    mongo.close()


def main() -> None:
    convert_to_json()


if __name__ == "__main__":
    main()
