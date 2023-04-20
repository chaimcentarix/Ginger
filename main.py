import os
import time
from dotenv import load_dotenv
from slack_sdk.web import WebClient
import openai
import json

METADATA_FILENAME_PATH = "/home/user/Downloads/metadata_epi_v6_189k.jsonl"  # TODO move here: "data/metadata.nd_json"
metadata = {json.loads(l).get('_id',0):json.loads(l) for l in open(METADATA_FILENAME_PATH).readlines()}
load_dotenv()  # Load environment variables from .env file

SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
CHANNEL = os.environ.get("SLACK_CHANNEL")
SLACK_BOT_USER_ID = os.environ.get("SLACK_BOT_USER_ID")
API_KEY = os.environ.get("OPENAI_API_KEY")

openai.api_key = API_KEY
client = WebClient(token=SLACK_TOKEN)
current_time = time.time()


def extract_gsm(s):
    # To extract the GSM from the user's input
    l = s.find('GSM')
    if l > -1:
        # That means there is GSM there
        gsm = 'GSM'
        for u in range(min(len(s) - (l + 3), 20)):
            t = s[l + 3 + u]
            if t.isnumeric():
                gsm += t
        return gsm
    return None


message_log = [
    {"role": "system", "content": "You are a helpful assistant."}
]


def get_openAi_message(message_log):
    # Use OpenAI's ChatCompletion API to get the chatbot's response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # The name of the OpenAI chatbot model to use
        messages=message_log,  # The conversation history up to this point, as a list of dictionaries
        # max_tokens=4097-len(str(message_log).split(' ')),        # The maximum number of tokens (words or subwords) in the generated response
        stop=None,  # The stopping sequence for the generated response, if any (not used here)
        temperature=0.7,  # The "creativity" of the generated response (higher temperature = more creative)
    )

    # Find the first response from the chatbot that has text in it (some responses may not have text)
    for choice in response.choices:
        if "text" in choice:
            print('ct', choice.text)
            return choice.text

    # If no response with text is found, return the first response's content (which may be empty)
    return response.choices[0].message.content


def build_a_response(user_input):
    # Since GPT does not remember a previous conversation, it is necessary for every contact to send the entire content of the conversation.
    # On the other hand, due to limitations on the length of the message, when the conversation is long, a summary must be created from it and only the summary sent
    # Therefore, it is necessary to update the global message_log variable throughout the run
    global message_log
    if len(str(message_log)) > 3800:
        so = message_log.copy()
        so.append({"role": "user", "content": 'Please briefly summarize this entire conversation'})
        sommary = get_openAi_message(so)
        message_log = [
            {"role": "system", "content": sommary}
        ]
    message_log.append({"role": "user", "content": user_input})

    response = get_openAi_message(message_log)

    message_log.append({"role": "assistant", "content": response})

    return f"AI assistant: {response}"


print("Server started...")

while True:
    # In order to answer the applicant's last question, we turn to the Slack server in each iteration and request the message history and extract the last message from there
    # We check if the message is not a response of this code and also if it is new to know that it is new we save the beginning of the running time of the code and if we enter a new message from the beginning of the running of the code we save the time of the new message
    time.sleep(0.5)
    try:
        conversation_history = client.conversations_history(channel=CHANNEL, limit=1)
        if conversation_history["messages"]:
            message = conversation_history["messages"][0]
            message_time = float(message["ts"])
            if message_time != current_time and message.get("user") != SLACK_BOT_USER_ID:
                current_time = message_time

                question = message["text"]
                gsm = extract_gsm(question)
                response = ''
                gsm_metadata = str(metadata.get(gsm,0))
                if gsm_metadata !='0':
                    response = build_a_response(
                        f'Please take this data: {gsm_metadata} example and formulate an answer to the following question: {question} and give a description of this example: ' + gsm_metadata)
                else:
                    response = build_a_response(question)
                result = client.chat_postMessage(
                    channel=CHANNEL,
                    text=response
                )
    except Exception as e:
        print(f"Error: {e}")
