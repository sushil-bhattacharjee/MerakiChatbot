import requests
import json
from rich import print

Personal_Access_Token = "NmZmOGU5MjMtYzgzYi00ZmE4LWJmZGQtN2Q3ZWM2ZjdmODA1NjAwOGM1MDctYTYz_P0A1_024cf1cc-0fff-4459-9d22-2bf3b7018d17"

rooms_url = "https://webexapis.com/v1/rooms"

headers = {"Authorization": f"Bearer {Personal_Access_Token}"}

get_response = requests.get(rooms_url, headers=headers).json()

items = get_response["items"]

for item in items:
    title = item["title"]
    #if title == "Support" or title == "Development":
    if title in ["SDK room", "Marketing"]:
        roomId = item["id"]
        membership_url = "https://webexapis.com/v1/memberships"
        headers = {
            "Authorization": f"Bearer {Personal_Access_Token}",
            "Content-Type": "application/json",
        }
        body = {
            "roomId": f"{roomId}",
            "personEmail": "merakichatbot@webex.bot",
            "isModerator": False,
        }
        post_response = requests.post(membership_url, headers=headers, data=json.dumps(body)) #Convert Python dict to json
        
                # Log response for debugging
        print(f"POST Response Status Code: {post_response.status_code}")
        print(f"POST Response Body: {post_response.text}\n")
        
        post_response.raise_for_status()
        if post_response.status_code == 200:
            print(f"\n[green]SUCCESS![/green] user Merakichatbot@webex.bot added to {title}\n")

