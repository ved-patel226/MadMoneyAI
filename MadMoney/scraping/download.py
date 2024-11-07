from pytubefix import YouTube
from pydub import AudioSegment
import os


video_url = "https://www.youtube.com/watch?v=345GD1iE4I8&list=PLVbP054jv0KoZTJ1dUe3igU7K-wUcQsCI&index=1&pp=iAQB"


def download_audio_as_wav(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()

        print("Downloading audio...")
        audio_file = stream.download(filename="audio.mp4")

        print("Converting to wav...")
        audio = AudioSegment.from_file(audio_file)
        wav_file = audio_file.replace(".mp4", ".wav")
        audio.export(wav_file, format="wav")

        os.remove(audio_file)

        print(f"Download and conversion complete: {wav_file}")
        return wav_file

    except Exception as e:
        print(f"An error occurred: {e}")


def main() -> None:
    wav_file = download_audio_as_wav(video_url)


if __name__ == "__main__":
    main()
