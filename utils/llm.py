from openai import OpenAI

from constants import OPENAI_API_KEY
from utils.parsers import ResponseParser

client = OpenAI(api_key=OPENAI_API_KEY)

def trascribe_audio(audio_path):
    audio_file = open(audio_path, "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file, 
    response_format="text"
    )
    return transcription

def img_call(base_64, prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant which understands images perfectly."},
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": base_64}}
                ]}
            ])
    except Exception as e:
        print("Error")
        print(e)
        raise e
  
    return response.choices[0].message.content if response.choices else None

def llm_call(sys_prompt, usr_prompt, parser=ResponseParser):
    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": sys_prompt if sys_prompt else "You are a helpful assistant"},
                {"role": "user", "content": usr_prompt},
            ],
            response_format=parser,
        )
        return completion.choices[0].message.parsed.response
    except Exception as e:
        print("Error")
        print(e)
        raise e
