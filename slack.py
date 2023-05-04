import os
import time
from dotenv import load_dotenv
from slack_sdk.web import WebClient
import gsms

load_dotenv()  # Load environment variables from .env file

SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
CHANNEL = os.environ.get("SLACK_CHANNEL")
SLACK_BOT_USER_ID = os.environ.get("SLACK_BOT_USER_ID")
API_KEY = os.environ.get("OPENAI_API_KEY")


client = WebClient(token=SLACK_TOKEN)
current_time = time.time()

def get_slack_message(current_time):
    conversation_history = client.conversations_history(channel=CHANNEL, limit=1)
    if conversation_history["messages"]:
        message = conversation_history["messages"][0]
        message_time = float(message["ts"])
        if message_time != current_time and message.get("user") != SLACK_BOT_USER_ID:
            question = message["text"]
            gsm = gsms.extract_gsm(question)
            gsm_metadata = str(gsms.metadata.get(gsm, 0))
            return question,message_time,gsm_metadata
        return None
    return None

def post_slack(response):
            result = client.chat_postMessage(
                channel=CHANNEL,
                text=response
            )
            return result


            # timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            # logging.info(f"Operation at {timestamp}: question='{question}', response='{response}'")

