from services.functions import mail_initiate, task_diffrentiate
from services.prompts import BIFERGATE_PROMPT
from utils.llm import llm_call
from utils.parsers import TaskDiffrentiateParser



def diffrentiate_user_input(msg, usr, intent=None):
    #generic check toc ehck wats user wants then sub divide it want to do

    # for now going with tasks only
    res = llm_call(BIFERGATE_PROMPT, TaskDiffrentiateParser, msg=msg, layout=TaskDiffrentiateParser.get_json())
    if res.intent == "task":
        return task_diffrentiate(msg, usr.get("wa_id"), intent)

    elif res.intent == "mail":
        return mail_initiate(msg, usr)
    
    else:
        return "I am new born and don't know what to do with this message."

