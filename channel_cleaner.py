import os
from dotenv import load_dotenv
load_dotenv()

CHANNEL = os.environ.get("SLACK_CHANNEL")
from slack_sdk.web import WebClient
client = WebClient(token=os.environ.get("SLACK_USER_TOKEN"))
def clean(channel):
    try:
        result = client.conversations_history(channel=channel)

        # Delete each message returned by the conversations.history method
        for message in result["messages"]:
            print(message)
            try:
                # Call the chat.delete method using the WebClient
                client.chat_delete(channel=CHANNEL, ts=message["ts"])
            except (Exception) as e:
                print("Error deleting message: {}".format(e))
    except (Exception) as e:
        print("Error getting channel history: {}".format(e))
        print("cont2")

# clean(CHANNEL)