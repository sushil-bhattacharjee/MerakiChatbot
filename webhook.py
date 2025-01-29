from webexteamssdk import WebexTeamsAPI
import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Replace with your Bot Access Token
WEBEX_BOT_TOKEN = os.getenv("WEBEX_BOT_TOKEN")

# Replace with your ngrok forwarding URL
NGROK_URL = "https://9664-27-96-222-36.ngrok-free.app"

# Initialize Webex API
webex_api = WebexTeamsAPI(access_token=WEBEX_BOT_TOKEN)

# Create a webhook
webhook = webex_api.webhooks.create(
    name="MerakiChatbotWebhook",
    targetUrl=f"{NGROK_URL}/webhook",
    resource="messages",
    event="created"
)

print(f"Webhook created with ID: {webhook.id}")
