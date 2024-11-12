from pydub import AudioSegment
import os


def trim_audio(short=False) -> None:
    if os.path.exists("segments"):
        for file in os.listdir("segments"):
            file_path = os.path.join("segments", file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
    else:
        os.makedirs("segments", exist_ok=True)

    segment_duration = 100000
    audio = AudioSegment.from_wav("audio.wav")

    audio_length_ms = len(audio)
    audio_length_ms = (audio_length_ms // segment_duration) * segment_duration

    print(f"Audio duration: {audio_length_ms/1000} seconds")

    amt_itr = audio_length_ms / segment_duration
    amt_itr = int(amt_itr)
    print(f"Splitting audio into {audio_length_ms/segment_duration} segments...")

    if short:
        amt_itr = 1

    for i in range(amt_itr):
        start_time = i * segment_duration
        end_time = start_time + segment_duration
        segment = audio[start_time:end_time]
        segment.export(f"segments/audio_segment_{i+1}.wav", format="wav")

    print("Audio has been split into segments and saved in 'segments' folder")


def main() -> None:
    trim_audio()


if __name__ == "__main__":
    main()
