import datetime
import time
from database.connect import connect_task_db
from services.prompts import DETECT_TASK_PROMPT, EXTRACT_ID_PROMPT, EXTRACT_MAIL_PROMPT, EXTRACT_TASK_PROMPT
from services.reminder import send_msg
from utils.llm import llm_call
from utils.mail import send_mail
from utils.parsers import MailParser, ResponseDeleteTaskParser, ResponseParser, TaskDiffrentiateParser, TaskParser

def task_diffrentiate(msg, usr, role=None):
    #parse the task and time from the msg
    intent = False
    if role:
        res = llm_call(DETECT_TASK_PROMPT, TaskDiffrentiateParser, msg=msg, layout=TaskDiffrentiateParser.get_json())
        intent = res.intent

    if intent == "add_task":
        res = llm_call(EXTRACT_TASK_PROMPT, TaskParser, msg=msg, layout=TaskParser.get_json(), date=str(datetime.datetime.now()))
        task = res.task
        timestamp = res.timestamp.split(",")
        timestamp = [int(i) for i in timestamp]
        
        timestamp = datetime.datetime(*timestamp)
        print(f"Task: {task} | Timestamp: {timestamp}")

        conn = connect_task_db()
        """Insert a user into the users table."""
        insert_sql = """
        INSERT INTO tasks (user, status, task, time)
        VALUES (?, ?, ?, ?);
        """
        try:
            cursor = conn.cursor()
            cursor.execute(insert_sql, [usr, False, task, str(timestamp)])
            conn.commit()
            print(f"Task added successfully.")
            cursor.close()
            conn.close()

        except Exception as e:
            print(f"Error inserting user: {e}")

        return "Task added"
    
    elif intent == "delete_task":
        res = llm_call(EXTRACT_ID_PROMPT, ResponseDeleteTaskParser, msg=msg, layout=ResponseDeleteTaskParser.get_json())
        task = "Error in deleting task"
        task_id = None
        try:
            task = res.task_id
            task_id = [int(i) for i in task]
        except:
            return task

        conn = connect_task_db()
        delete_sql = f"DELETE FROM tasks WHERE user=? AND id IN ({','.join(['?']*len(task))});"
        try:
            cursor = conn.cursor()
            cursor.execute(delete_sql, [usr, *task_id])
            conn.commit()
            print(f"Task deleted successfully.")
            cursor.close()
            conn.close()
            return "Task deleted"
        except Exception as e:
            print(f"Error deleting task: {e}")
            return "Task ID not found to delete" 
        

    elif intent == "modify_task":
        print("Modify task")

    elif intent == "get_task":
        conn = connect_task_db()
        fetch_sql = "SELECT * FROM tasks WHERE user=?;"
        try:
            cursor = conn.cursor()
            cursor.execute(fetch_sql, [usr])
            rows = cursor.fetchall()
            text = "*Tasks Lists*\n"
            text += f"_Total Tasks_ : {len(rows)}\n\n"
            for row in rows: # 1st column is id, 2nd user 3rd is status 4th is task 
                text += f"*Task* {row[0]}: "
                text += f"{row[3]}" if not row[2] else f"~{row[3]}~"
                text += f"\n*Status* : {row[2]}\n"
                text += f"*Time* : {row[4]}\n\n"
            print(text)
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error fetching users: {e}")
                
        return text
    

    elif not intent:
        return msg

    else:
        response = llm_call("Response for the Query: {msg} Respone in JSON following format: {layout}", ResponseParser, msg=msg, layout=ResponseParser.get_json())
        return response.response
    


def mail_initiate(msg, usr):
    res = llm_call(EXTRACT_MAIL_PROMPT, MailParser, msg=msg, layout=MailParser.get_json(), name=usr.get("profile").get("name"))

    if not res.mail_id:
        return "No mail ID found, please provide the mail ID"
    msg = send_mail(res.mail_id, res.subject, res.body)
    return msg
