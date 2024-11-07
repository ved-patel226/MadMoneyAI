from .download import download_audio_as_wav
from .latestVideo import get_latest_video
from .trim import trim_audio
from .wavToString import convert_to_json

download_audio_as_wav(get_latest_video())
trim_audio()
convert_to_json()
