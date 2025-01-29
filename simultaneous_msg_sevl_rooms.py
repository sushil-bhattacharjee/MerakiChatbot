import sys
import requests
import json
import urllib3
import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Disable SSL warnings (for development use only; not recommended in production)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Your Webex Bot Access Token
Bot_Access_token = os.getenv("WEBEX_BOT_TOKEN")

# Webex API URL for fetching rooms
rooms_url = "https://webexapis.com/v1/rooms"

# Authorization header for Webex API
headers = {"Authorization": f"Bearer {Bot_Access_token}"}

# Fetch all rooms
response = requests.get(rooms_url, headers=headers)
response.raise_for_status()
rooms_data = response.json()

# List of target room titles
target_rooms = ["Support", "Development", "MerakiChatroom"]

# Read the message from the command-line argument
if len(sys.argv) < 2:
    print("Usage: python3 simultaneous_msg_sevl_rooms.py '<message>'")
    sys.exit(1)

message = sys.argv[1]

def send_message(room_id, room_title):
    """
    Sends a message to the given Webex room.
    """
    message_url = "https://webexapis.com/v1/messages"
    message_headers = {"Authorization": f"Bearer {Bot_Access_token}", "Content-Type": "application/json"}
    message_body = {"roomId": room_id, "text": message}
    
    response = requests.post(message_url, headers=message_headers, data=json.dumps(message_body), verify=False)
    
    if response.status_code == 200:
        print(f"[SUCCESS] Message sent to room: {room_title} (ID: {room_id})")
    else:
        print(f"[FAILED] Could not send message to room: {room_title} (ID: {room_id}). Response: {response.text}")

# Iterate over rooms and send the message to target rooms
for room in rooms_data["items"]:
    room_title = room["title"]
    room_id = room["id"]
    
    # Debug: Print room titles to confirm matching
    print(f"Checking room: {room_title}")
    
    if room_title in target_rooms:
        print(f"Sending message to room: {room_title}")
        send_message(room_id, room_title)

print("Finished sending messages to all matching rooms.")



##################send from CLI as given below
"""
(.VmChatbot) sushil@sushil:~/Merakichatbot$ python3 postmessage.py "Message testing from MerakichatBot to multiple rooms"python3 postmessage.py "

"""