# This is reminder system which will run everytime and will remind the user about the task.

import time
from constants import TWILIO_ID, TWILIO_TOKEN
from database.connect import connect_task_db
from twilio.rest import Client
import datetime


def send_msg(task, time):
    client = Client(TWILIO_ID, TWILIO_TOKEN)

    message = client.messages.create(
        body=f"\nYou have task '{task}' to do at {time}",
        from_="+17752627819",
        to="+919009713031",
    )
    print(message)

def notifcation():
    while True:
        time.sleep(10)
        conn = connect_task_db()
        fetch_sql = "SELECT * FROM tasks WHERE time != 0;"
        try:
            cursor = conn.cursor()
            cursor.execute(fetch_sql)
            rows = cursor.fetchall()
            print(f"Rows: {rows}")
            for row in rows:
                status = row[2]
                task = row[3]
                task_time = row[4]
                task_time = datetime.datetime.strptime(task_time, '%Y-%m-%d %H:%M:%S')
                current_time = datetime.datetime.now()
                if task_time <= current_time and status == 0:
                    send_msg(task, time)
                    update_sql = "UPDATE tasks SET status = 1 WHERE id = ?;"
                    cursor.execute(update_sql, [row[0]])
                    conn.commit()
        
            cursor.close()
            conn.close()
        
        except Exception as e:
            print(f"Error fetching tasks: {e}")
