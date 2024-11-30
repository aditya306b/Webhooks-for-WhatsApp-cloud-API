from openai import OpenAI

from constants import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def trascribe_audio(audio_path):
    audio_file = open(audio_path, "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file, 
    response_format="text"
    )
    return transcription