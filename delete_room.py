import requests
import json
from rich import print
import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()
Personal_Access_Token = os.getenv("PersonalAccessToken") # update the token from the webex developer portal

rooms_url = "https://webexapis.com/v1/rooms"

headers = {"Authorization": f"Bearer {Personal_Access_Token}"}

get_response = requests.get(rooms_url, headers=headers).json()

items = get_response["items"]

for item in items:
    title = item["title"]
    #if title == "Support" or title == "Development":
    if title in ["CBT-test3", "Sales"]:
        roomId = item["id"]
        roomId_url = f"https://webexapis.com/v1/rooms/{roomId}"
        headers = {"Authorization": f"Bearer {Personal_Access_Token}"}

        del_response = requests.delete(roomId_url, headers=headers)
        
                # Log response for debugging
        print(f"DELETE Response Status Code: {del_response.status_code}")
        print(f"DELETE Response Body: {del_response.text}\n")
        
        del_response.raise_for_status()
        if del_response.status_code == 204:
            print(f"\n[green]SUCCESS![/green] Room {title} : [red]DELETED[/red]\n")