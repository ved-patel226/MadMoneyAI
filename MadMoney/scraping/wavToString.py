import os
from groq import Groq
import json
from MadMoney.essentials import env_to_var


def convert_to_json() -> str:
    segments_dir = "segments"
    files = os.listdir(segments_dir)
    print(f"{len(files)} segments detected")

    client = Groq(api_key=env_to_var("GROQ_KEY"))

    full_transcription = []

    for file in files:
        with open("segments/" + file, "rb") as f:
            transcription = client.audio.transcriptions.create(
                file=(file, f.read()),
                model="whisper-large-v3",
                response_format="verbose_json",
            )
            print(transcription.text)
            full_transcription.append(transcription.text)

    file_path = "transcription.json"

    with open(file_path, "w") as f:
        json.dump(full_transcription, f, indent=4)

    return file_path
