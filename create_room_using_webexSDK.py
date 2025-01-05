from webexteamssdk import WebexTeamsAPI

# Replace with your valid Personal Access Token
Personal_Access_Token = "NmZmOGU5MjMtYzgzYi00ZmE4LWJmZGQtN2Q3ZWM2ZjdmODA1NjAwOGM1MDctYTYz_P0A1_024cf1cc-0fff-4459-9d22-2bf3b7018d17"

# Initialize the Webex Teams API with the access token
api = WebexTeamsAPI(access_token=Personal_Access_Token)

# Create a new room
try:
    new_room = api.rooms.create("Room_by_SDK")
    print(f"Room created: {new_room.title}, ID: {new_room.id}")

    # Send a message to the new room
    api.messages.create(new_room.id, text="Creating new room using WebexAPI SDK")
    print("Message sent successfully!")
except Exception as e:
    print(f"Error: {e}")
