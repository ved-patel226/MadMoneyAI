import json


def load_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


if __name__ == "__main__":
    data = load_json("transcription.json")
    print(data)
