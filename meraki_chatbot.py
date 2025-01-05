import os
from flask import Flask, request, jsonify
from webexteamssdk import WebexTeamsAPI
from meraki import DashboardAPI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize Webex API
webex_api = WebexTeamsAPI(access_token=os.getenv("WEBEX_BOT_TOKEN"))

# Initialize Meraki Dashboard API
meraki_api = DashboardAPI(api_key=os.getenv("MERAKI_API_KEY"))

# Webhook Endpoint
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if "data" in data:
        room_id = data["data"]["roomId"]
        message_id = data["data"]["id"]

        # Fetch the message sent to the bot
        message = webex_api.messages.get(message_id)
        user_message = message.text.lower()

        # Ignore messages sent by the bot itself
        if message.personEmail == os.getenv("WEBEX_BOT_EMAIL"):
            return jsonify({"success": True})

        # Process the user message
        response = handle_command(user_message)
        webex_api.messages.create(roomId=room_id, text=response)

    return jsonify({"success": True})


def handle_command(command):
    """
    Process user commands and interact with the Meraki Dashboard API.
    """
    if "help" in command:
        return (
            "I can assist you with the following commands:\n"
            "- `list networks`: List all networks in your organization.\n"
            "- `get devices <network_id>`: List devices in a specific network.\n"
            "- `reboot device <serial>`: Reboot a device by serial number.\n"
            "- `list clients <network_id>`: List clients connected to a network."
        )

    elif "list networks" in command:
        try:
            # Fetch networks using the organization ID
            networks = meraki_api.organizations.getOrganizationNetworks("1215707")
            if not networks:
                return "No networks found in the organization."
            return "\n".join([f"{n['name']} (ID: {n['id']})" for n in networks])
        except Exception as e:
            return f"Error fetching networks: {e}"

    elif "get devices" in command:
        try:
            # Parse the network ID from the command
            _, network_id = command.split("get devices", 1)
            network_id = network_id.strip()  # Keep the ID as-is (case-sensitive)

            # Fetch devices for the specified network ID
            devices = meraki_api.networks.getNetworkDevices(network_id)
            if not devices:
                return f"No devices found in the network with ID: {network_id}."
            return "\n".join([f"{d['name']} (Serial: {d['serial']})" for d in devices])
        except Exception as e:
            if "404" in str(e):
                return f"Network with ID {network_id} not found. Please verify the network ID."
            return f"Error fetching devices: {e}"

    elif "reboot device" in command:
        try:
            _, serial = command.split("reboot device", 1)
            serial = serial.strip()
            meraki_api.devices.rebootDevice(serial)
            return f"Device {serial} rebooted successfully."
        except Exception as e:
            return f"Error rebooting device: {e}"

    elif "list clients" in command:
        try:
            _, network_id = command.split("list clients", 1)
            network_id = network_id.strip()  # Keep the ID as-is (case-sensitive)
            clients = meraki_api.networks.getNetworkClients(network_id, total_pages=1)
            if not clients:
                return f"No clients found in the network with ID: {network_id}."
            return "\n".join([f"{c['description']} - {c['mac']}" for c in clients])
        except Exception as e:
            return f"Error fetching clients: {e}"

    return "Unknown command. Type `help` for available commands."



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
