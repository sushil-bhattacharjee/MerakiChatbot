from webexteamssdk import WebexTeamsAPI

# Replace with your valid Personal Access Token
Personal_Access_Token = "NmZmOGU5MjMtYzgzYi00ZmE4LWJmZGQtN2Q3ZWM2ZjdmODA1NjAwOGM1MDctYTYz_P0A1_024cf1cc-0fff-4459-9d22-2bf3b7018d17"

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
    
