import base64
import os
from constants import URL
from utils.audio import generate_random_text
from utils.fetch import fetch_data
from utils.llm import img_call


def img_process(msg_id, format):
    
    res = fetch_data(fetch_data(f"{URL}/{msg_id}").json().get("url"))  # Fetching the img file
    # temp_video_path = f"{generate_random_text()}.{format}"
    # with open(temp_video_path, "wb") as temp_audio_file:
    #     temp_audio_file.write(res.content)
    text = img_call(f"data:{format};base64,{base64.b64encode(res.content).decode('utf-8')}", "Describe the image!")
    print("Text: ", text)
    return text
    # os.remove(temp_video_path)