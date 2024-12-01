import json
from db.connect import db_init
from services.prompts import detect_task_prompt, extract_task_promtp
from utils.llm import llm_call
from utils.parsers import TaskDiffrentiateParser, TaskParser


def task_diffrentiate(msg, usr):
    #parse the task and time from the msg
    res = llm_call(None, detect_task_prompt(msg, TaskDiffrentiateParser.get_json()))
    res = eval(res)
    intent = res["intent"]

    if intent == "add_task":
        res = llm_call(None, extract_task_promtp(msg, TaskParser.get_json()))
        res = eval(res)
        task = res["task"]
        data = ""
        with open("tasks.json", "r") as f:
            data = f.read()
            data = eval(data)
        
        with open("tasks.json", "w") as f:
            data.append({"user": usr, "task": task, "status": "pending"})
            f.write(json.dumps(data))

        # conn = db_init()
        # cursor = conn.cursor()
        # cursor.execute("INSERT INTO tasks (user, task, status) VALUES (?, ?, ?)", (usr, task, "pending"))
        # conn.commit()
        # conn.close()
        # cursor.close()
        return "Task added"
    elif intent == "delete_task":
        print("Delete task")
    elif intent == "modify_task":
        print("Modify task")
    elif intent == "get_task":
        data = ""
        with open("tasks.json", "r") as f:
            data = f.read()
            data = eval(data)
        all_tasks = []
        for i in data:
            if i["user"] == usr:
                all_tasks.append(i["task"])
                
        return "\n".join(all_tasks)
    else:
        response = llm_call("Response for the Query", msg)
        return response

def diffrentiate_user_input(msg, usr):
    #generic check toc ehck wats user wants then sub divide it want to do

    # for now going with tasks only
    return task_diffrentiate(msg, usr)
