from pydantic import BaseModel  

class TaskParser(BaseModel):
    task: str
    timestamp: float

    @staticmethod
    def get_json():
        return {
            "task": "",
            "timestamp": 0.0
        }

class ResponseParser(BaseModel):
    response: str

    @staticmethod
    def get_json():
        return {
            "response": ""
        }

class TaskDiffrentiateParser(BaseModel):
    intent: str

    @staticmethod
    def get_json():
        return {
            "intent": "str"
        }

