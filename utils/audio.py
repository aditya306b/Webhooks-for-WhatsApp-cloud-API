import os
import tempfile
from constants import URL
from utils.fetch import fetch_data
from utils.llm import trascribe_audio
import random
import string


def generate_random_text(length=5):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def get_transcribed_audio(msg_id, format):
    # This function will transcribe the audio and return the text
    text = ""
    res = fetch_data(fetch_data(f"{URL}/{msg_id}").json().get("url"))  # Fetching the audio file
    temp_audio_path = f"{generate_random_text()}.{format}"
    with open(temp_audio_path, "wb") as temp_audio_file:
        temp_audio_file.write(res.content)
    text = trascribe_audio(temp_audio_path)
    print("Text: ", text)
    os.remove(temp_audio_path)
    return text