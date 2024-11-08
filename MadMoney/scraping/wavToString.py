import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from groq import Groq
from MadMoney.essentials import env_to_var, MongoDBClient
from datetime import datetime
from tqdm import tqdm


def convert_to_json() -> None:
    segments_dir = "segments"

    try:
        files = os.listdir(segments_dir)
        print(f"{len(files)} segments detected")
    except:
        raise FileNotFoundError("No segments detected")

    client = Groq(api_key=env_to_var("GROQ_KEY"))

    full_transcription = []

    for file in tqdm(files, desc="Converting voice to text (Please wait)"):
        with open("segments/" + file, "rb") as f:
            transcription = client.audio.transcriptions.create(
                file=(file, f.read()),
                model="whisper-large-v3",
                response_format="verbose_json",
            )
            full_transcription.append(transcription.text)

    mongo = MongoDBClient()
    mongo.insert_one(
        "transcriptions", {"date": datetime.now(), "transcriptions": full_transcription}
    )
    mongo.close()


def main() -> None:
    convert_to_json()


if __name__ == "__main__":
    main()
