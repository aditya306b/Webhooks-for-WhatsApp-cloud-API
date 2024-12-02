import json
from database.connect import connect_db
from services.prompts import DETECT_TASK_PROMPT, EXTRACT_ID_PROMPT, EXTRACT_TASK_PROMPT
from utils.llm import llm_call
from utils.parsers import ResponseParser, TaskDiffrentiateParser, TaskParser


def task_diffrentiate(msg, usr, role=None):
    #parse the task and time from the msg
    intent = False
    if role:
        res = llm_call(DETECT_TASK_PROMPT, TaskDiffrentiateParser, msg=msg, layout=TaskDiffrentiateParser.get_json())
        intent = res.intent

    if intent == "add_task":
        res = llm_call(EXTRACT_TASK_PROMPT, TaskParser, msg=msg, layout=TaskParser.get_json())
        task = res.task

        conn = connect_db()
        """Insert a user into the users table."""
        insert_sql = """
        INSERT INTO tasks (user, status, task)
        VALUES (?, ?, ?);
        """
        try:
            cursor = conn.cursor()
            cursor.execute(insert_sql, [usr, "pending", task])
            conn.commit()
            print(f"Task added successfully.")
            cursor.close()
            conn.close()

        except Exception as e:
            print(f"Error inserting user: {e}")

        return "Task added"
    
    elif intent == "delete_task":
        res = llm_call(EXTRACT_ID_PROMPT, ResponseParser, msg=msg, layout=ResponseParser.get_json())
        task = ""
        task_id = None
        try:
            task = res.response
            task_id = int(task)
        except:
            return task

        conn = connect_db()
        delete_sql = "DELETE FROM tasks WHERE user=? AND id=?;"
        try:
            cursor = conn.cursor()
            cursor.execute(delete_sql, [usr, task_id])
            conn.commit()
            print(f"Task deleted successfully.")
            cursor.close()
            conn.close()
            return "Task deleted"
        except Exception as e:
            print(f"Error deleting task: {e}")
            return "Task not found"
        
        

    elif intent == "modify_task":
        print("Modify task")

    elif intent == "get_task":
        conn = connect_db()
        fetch_sql = "SELECT * FROM tasks WHERE user=?;"
        try:
            cursor = conn.cursor()
            cursor.execute(fetch_sql, [usr])
            rows = cursor.fetchall()
            text = "*Tasks Lists*\n\n"
            for row in rows: # 1st column is id, 2nd user 3rd is status 4th is task 
                text += f"*Task* {row[0]}: "
                text += f"{row[3]}" if row[2] == "pending" else f"~{row[3]}~"
                text += f"\n*Status* : {row[2]}\n\n"
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

def diffrentiate_user_input(msg, usr, intent=None):
    #generic check toc ehck wats user wants then sub divide it want to do

    # for now going with tasks only
    return task_diffrentiate(msg, usr, intent)
