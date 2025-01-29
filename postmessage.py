import sys
import requests
import json
import urllib3
import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()


#Disable notifications
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

Bot_Access_token = os.getenv("WEBEX_BOT_TOKEN") # update the token from the webex developer portal

####https://developer.webex.com/my-apps/merakichatbot

url = "https://webexapis.com/v1/rooms"

headers = {"Authorization": f"Bearer {Bot_Access_token}"}

get_response = requests.get(url, headers=headers).json()

items = get_response["items"]
for item in items:
    title = item["title"]
    #if title == "MerakiChatroom":
    if title in ["MerakiChatroom"]:
        roomId = item["id"]
        
message = sys.argv[1]

def send_message():
    header = {"Authorization": f"Bearer {Bot_Access_token}", "Content-Type": "application/json"}
    data = {"roomId": f"{roomId}", "text": message}
    message_url = "https://webexapis.com/v1/messages"
    return requests.post(message_url, headers=header, data=json.dumps(data), verify=False)


send_message()

#####in your CLI run the following line
"""
(.VmChatbot) sushil@sushil:~/Merakichatbot$ python3 postmessage.py "Message testing From MerakichatBot to the room"
"""