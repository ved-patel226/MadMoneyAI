"""
* Expiremental code to remove background noise from audio files

! WARNING: THIS CODE HAS BEEN FOUND TO BE INEFFECTIVE***

"""

import noisereduce as nr
from pydub import AudioSegment
import numpy as np
import scipy.io.wavfile as wav


audio = AudioSegment.from_wav("audio.wav")


samples = np.array(audio.get_array_of_samples())


sample_rate = audio.frame_rate


reduced_noise_samples = nr.reduce_noise(y=samples, sr=sample_rate)


reduced_noise_audio = AudioSegment(
    reduced_noise_samples.tobytes(),
    frame_rate=sample_rate,
    sample_width=audio.sample_width,
    channels=audio.channels,
)


def main() -> None:
    reduced_noise_audio.export("audio.wav", format="wav")

    print("Background noise has been removed and saved as 'reduced_noise_audio.wav'")


if __name__ == "__main__":
    main()
