def detect_task_prompt(usr_msg, response_format):
    return f"""
    You are an assistant that classifies user requests related to task management into one of the following intents:

    1. **add_task**: The user wants to create a new task.
    - *Examples*: "Add a new task to call the client tomorrow.", "Remind me to buy groceries at 5 PM.", "Schedule a meeting with the team on Friday at 3 PM."

    2. **delete_task**: The user wants to remove an existing task.
    - *Examples*: "Delete the task 'submit the report'.", "Remove the meeting scheduled for Friday.", "Erase the reminder to water the plants."

    3. **modify_task**: The user wants to update the status of an existing task.
    - *Examples*: "Mark the 'call mom' task as completed.", "Change the deadline for the project task to next Monday.", "Update the meeting time to 4 PM instead of 3 PM."

    4. **get_task**: The user wants to view the list of tasks.
    - *Examples*: "Show me all my tasks.", "What tasks are scheduled for today?", "List all my pending tasks."

    5. **other**: The user's request does not fall into any of the above categories.

    Given a user's input, identify and output the intent category it belongs to.
    Response in the following JSON format: {response_format}

    USER MESSAGE:
    ### 
    {usr_msg}
    ###

    """

def extract_task_promtp(msg, format):
    return f"""
    You are an assistant that extracts the task from a user's message.
    Response in the following JSON format: {format}

    USER MESSAGE:
    ###
    {msg}
    ###
    """