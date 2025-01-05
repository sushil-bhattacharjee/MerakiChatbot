from webexteamssdk import WebexTeamsAPI
import os

# Replace with your Bot Access Token
WEBEX_BOT_TOKEN = "NzRjY2Q5OTQtOWNiMC00YmRiLTgzYzctYTg5NzhhMzIyNDdjZmY1YzEyODUtMjRl_P0A1_024cf1cc-0fff-4459-9d22-2bf3b7018d17"

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
