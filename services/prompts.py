DETECT_TASK_PROMPT = """
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
    Response in the following JSON format: {layout}

    USER MESSAGE:
    ### 
    {msg}
    ###

    """

EXTRACT_TASK_PROMPT = """
    You are an assistant that extracts the task from a user's message.
    Donot add any prefix or suffix to the task. (eg. Task on or Add task on) only identify the main task. or in other words extract main task from the user message.
    Response in the following JSON format: {layout}

    USER MESSAGE:
    ###
    {msg}
    ###
    """

EXTRACT_ID_PROMPT = """
    You are an assistant who understand things carwfully.
    Your role is to understand the user msg and extract the task id from the user message. it could in words or numbers.
    Response in the following JSON format: {layout}
    If there are multiple numbers in the message, or no number, return an error message in the response key-value

    USER MESSAGE:
    ###
    {msg}
    ###
    """