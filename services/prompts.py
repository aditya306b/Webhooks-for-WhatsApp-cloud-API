BIFERGATE_PROMPT = """
    You are an assistant that classifies user requests into one of the following intents:

    - task: The user wants to add, update, delete or modify or want to do something with tasks.
    - mail: The user wants to send an email.

    Given a user's input, identify and output the intent category it belongs to.
    Response in the following JSON format: {layout}

    USER MESSAGE:
    ### 
    {msg}
    ###
"""

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

    # Donot add any prefix or suffix to the task. (eg. Task on or Add task on) only identify the main task. or in other words extract main task from the user message.
EXTRACT_TASK_PROMPT = """
    You are an assistant that extracts the task from a user's message.

    Extract a structured task with its associated reminder time from user input.

    Input Processing Requirements:
    - Identify the task description
    - User Provide Data and time covner tit in timestamp
    - Avoid Prefix the task
    - Handle various time formats and natural language expressions

    Input Parsing Rules:
    - Avoid prefixes like "Create task on or add task on" and extract the main task from the user message.

    Time can be in multiple formats like the following :
    - Relative times (e.g., "in 2 hours", "tomorrow at 3 PM")
    - Absolute times (e.g., "2024-06-15 14:30", "June 15th at 2:30 PM")
    - Natural language expressions (e.g., "next week", "in 3 days")

    You'll be provided with date and time and your task will be to convert it in following desired output - "YYYY,MM,DD,HR,MIN"
    - If you are provided with date , year and month considre time 0:0
    - If you are provided with date and month considre year 2024
    - If you are given tommorow or day after tommorow then then think step by step and calculate the time by current time and date
    - If you are given time only consider today's date (only when time is not passed in given time if passed return 0)
    # Current time - {date}

    If you dont get time in user message you can send it 0.
    
    Response in the following JSON format: {layout}    

    USER MESSAGE:
    ###
    {msg}
    ###
    """

EXTRACT_ID_PROMPT = """
    You are an assistant who understand things carwfully.
    Your role is to understand the user msg and extract the list task id from the user message. 
    -   It could in words or numbers.
    -   If there are multiple numbers in the message extract in list.
    -   If there only one number still return in list.
    -   If there are no numbers return an error message.
    Response in the following JSON format: {layout}

    USER MESSAGE:
    ###
    {msg}
    ###
    """