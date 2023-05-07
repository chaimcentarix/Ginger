import os
import time
import openai
import logging
from datetime import datetime
import gsms
import slack
import gpt

current_time = time.time()
print("Server started...")

def get_timestamp():
        return datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

while True:
    # In order to answer the applicant's last question, we turn to the Slack server in each iteration and request the message history and extract the last message from there
    # We check if the message is not a response of this code and also if it is new to know that it is new we save the beginning of the running time of the code and if we enter a new message from the beginning of the running of the code we save the time of the new message
    time.sleep(0.5)

    #logging.info(f"{get_timestamp()}: Waiting...")

    try:
            if slack.get_slack_message(current_time):
                question, message_time, gsm_metadata=slack.get_slack_message(current_time)
                current_time = message_time
                response = ''
                if gsm_metadata !='0':
                    response = gpt.build_a_response(
                        f'Please take this data: {gsm_metadata} example and formulate an answer to the following question: {question}')
                else:
                    response = gpt.build_a_response(question)

                result = slack.post_slack(response=response)
                gpt.make_sumarry()
    except Exception as e:
            timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            logging.error(f"Error at {timestamp}: {e}")
            print(f"Error at {timestamp}: {e}")

