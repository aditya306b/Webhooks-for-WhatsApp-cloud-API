from pydantic import BaseModel  

class TaskParser(BaseModel):
    task: str

    @staticmethod
    def get_json():
        return {
            "task": ""
        }

class ResponseParser(BaseModel):
    response: str

class TaskDiffrentiateParser(BaseModel):
    intent: str

    @staticmethod
    def get_json():
        return {
            "intent": "str"
        }
