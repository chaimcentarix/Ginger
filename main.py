import os
import time
from dotenv import load_dotenv
from slack_sdk.web import WebClient
import openai

load_dotenv()  # Load environment variables from .env file

SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
CHANNEL = os.environ.get("SLACK_CHANNEL")
SLACK_BOT_USER_ID = os.environ.get("SLACK_BOT_USER_ID")
API_KEY = os.environ.get("OPENAI_API_KEY")

openai.api_key = API_KEY


def generate_response(input_text):
    model_engine = "davinci"
    prompt = f"User: {input_text}\nBot:"
    response_ = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=40,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response_.choices[0].text.strip()


client = WebClient(token=SLACK_TOKEN)
current_time = time.time()

while True:
    try:
        conversation_history = client.conversations_history(channel=CHANNEL, limit=1)
        if conversation_history["messages"]:
            message = conversation_history["messages"][0]
            message_time = float(message["ts"])
            if message_time != current_time and message.get("user") != SLACK_BOT_USER_ID:
                current_time = message_time
                response = generate_response(message["text"])
                result = client.chat_postMessage(
                    channel=CHANNEL,
                    text=response
                )
        time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")
