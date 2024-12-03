import whisper

model = whisper.load_model("medium")

result = model.transcribe("backend/MadMoney/loadData/audio_segment_1.wav")
print(result["text"])
