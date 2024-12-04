from pydantic import BaseModel  

class TaskParser(BaseModel):
    task: str
    timestamp: str

    @staticmethod
    def get_json():
        return {
            "task": "",
            "timestamp": "YYYY,MM,DD,HR,MIN"
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

class ResponseDeleteTaskParser(BaseModel):
    task_id: list[int]

    @staticmethod
    def get_json():
        return {
            "task_id": []
        }