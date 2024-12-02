import json
from langchain_openai import ChatOpenAI
from openai import OpenAI
from langchain_core.prompts import PromptTemplate


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

def llm_call(prompt, parser, **format):
    try:
        llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o-mini")
        res=llm.with_structured_output(parser ,method="json_mode", include_raw=True)
        refined_prompt = PromptTemplate.from_template(prompt).format(**format)
        response = res.invoke(refined_prompt)
        response = response["raw"].content
        response = json.loads(response)
        response = parser(**response)
        return response
    except Exception as e:
        print("Error")
        print(e)
        raise e
