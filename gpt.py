import time
from datetime import datetime

import openai
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = API_KEY



message_log = [
    {"role": "system", "content": "You are a helpful assistant."}
]


def get_openAi_message(message_log):
    timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    #logging.info(f"Operation at {timestamp}:1 API message_log=''")


    # Use OpenAI's ChatCompletion API to get the chatbot's response
    response = openai.ChatCompletion.create(
        model="gpt-4",  # The name of the OpenAI chatbot model to use
        messages=message_log,  # The conversation history up to this point, as a list of dictionaries
        # max_tokens=4097-len(str(message_log).split(' ')),        # The maximum number of tokens (words or subwords) in the generated response
        stop=None,  # The stopping sequence for the generated response, if any (not used here)
        temperature=0,  # The "creativity" of the generated response (higher temperature = more creative)
    )

    # Find the first response from the chatbot that has text in it (some responses may not have text)
    timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    #logging.info(f"Operation at {timestamp}:----------->after API  response='{ response}'<--------------------")
    print(response)
    for choice in response.choices:
        if "text" in choice:
            return choice.text

    # If no response with text is found, return the first response's content (which may be empty)
    return response.choices[0].message.content

def make_sumarry():
    global message_log
    if len(str(message_log)) > 3800:
        so = message_log.copy()
        so.append({"role": "user", "content": 'Please briefly summarize this entire conversation and make sure to include the last example in more detail in the summary'})
        sommary = get_openAi_message(so)
        message_log = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": sommary}
        ]
        timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        #logging.info(f"Operation at {timestamp}: message_log='{message_log}'")
def build_a_response(user_input):
    # Since GPT does not remember a previous conversation, it is necessary for every contact to send the entire content of the conversation.
    # On the other hand, due to limitations on the length of the message, when the conversation is long, a summary must be created from it and only the summary sent
    # Therefore, it is necessary to update the global message_log variable throughout the run
    timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    ##logging.info(f"Operation at {timestamp}: user_input='{user_input}'")
    global message_log
    timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    #logging.info(f"Operation at {timestamp}: message_log='{message_log}'")

    # make_sumarry()
    message_log.append({"role": "user", "content": user_input})
    timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    #logging.info(f"Operation at {timestamp}:  message_log='{message_log}'")
    # make_sumarry()
    response = get_openAi_message(message_log)
    timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    #logging.info(f"Operation at {timestamp}: response  ='{response}'")

    message_log.append({"role": "assistant", "content": response})
    timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    #logging.info(f"Operation at {timestamp}: message_log='{message_log}'")

    return f"AI assistant: {response}"
