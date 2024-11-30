from utils.audio import get_transcribed_audio


def diffrentiate_msg_type(data: dict):
    
    if data.get("type") == "text":
       return data.get("text").get("body")
    
    elif data.get("type") == "audio":
        return get_transcribed_audio(data.get("audio").get("id"), data.get("audio").get("mime_type").split("/")[1][:3])

    elif data.get("type") == "image":
        return "Sorry, I can't process images at the moment"

    elif data.get("type") == "video":
        return "Sorry, I can't process videos at the moment"

    elif data.get("type") == "document":
        #Need to check mimetype to differentiate between pdf, docx, etc
        return "Sorry, I can't process documents at the moment"
    
    elif data.get("type") == "location":
        return "Sorry, I can't process location at the moment"
    
    elif data.get("type") == "contacts":
        return "Sorry, I can't process contacts at the moment"
    
    elif data.get("type") == "sticker":
        return "Sorry, I can't process stickers at the moment"

    elif data.get("type") == "unsupported":
        return data.get("errors")[0].get("error_data").get("details")
    
       



def get_msg_and_type(data: dict):
    if data.get("object"):
        entry = data.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})

        sender_details = value.get("contacts", [])[0]

        messages = value.get("messages", [{}])[0]
        # timestamp = messages.get("timestamp",0)
        # msg_type = messages.get("type")
        return sender_details, messages
    else:
        raise Exception("Invalid data recieved")

def process_msg(data: dict):
    sender_details, messages = get_msg_and_type(data)
    msg_body = diffrentiate_msg_type(messages)
    return sender_details, msg_body