from webexteamssdk import WebexTeamsAPI
import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Replace with your valid Personal Access Token
Personal_Access_Token = os.getenv("PersonalAccessToken")

# Initialize the Webex Teams API with the access token
api = WebexTeamsAPI(access_token=Personal_Access_Token)

####List all the rooms###
rooms = api.rooms.list()
for room in rooms:
    print(room)
    
    
#####Send message to room "Support"

for room in rooms:
    if room.title == "Support":
        roomId = room.id
        
api.messages.create(roomId, text="Hello message using SDK")

#####Sending message with conditions###

if 2 == 2:
    api.messages.create(roomId, text="Testing conditional messaging")
    
