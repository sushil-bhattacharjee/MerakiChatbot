from rich import print
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
import requests
import os
from nornir_utils.plugins.functions import print_result
from webexteamssdk import WebexTeamsAPI


#https://developer.webex.com/my-apps/merakichatbot
# Initialize the Webex Teams API with the access token
api = WebexTeamsAPI()


# Initialize Nornir with the configuration file
nr = InitNornir(config_file="config.yaml")


#################Testing Connection##############
def test_connection(task):
    print(f"Connecting to {task.host.hostname}")

results = nr.run(task=test_connection)

##################################

def ospf_test(task):
    """
    Test OSPF neighbors on a device.
    """
    dev_name = task.host

    try:
        # Run the "show ip ospf neighbor" command
        result = task.run(netmiko_send_command, command_string="show ip ospf neighbor")
        raw_output = result.result
        print(f"[bold blue]{dev_name} OSPF Neighbor Output:[/bold blue]\n{raw_output}")

        # Basic validation: Check for the presence of "Neighbor ID" in the output
        if "Neighbor ID" in raw_output:
            # Count the number of FULL states in the output
            num_neighbors = raw_output.count("FULL")
            if num_neighbors == 2:
                print(f"{dev_name}: [green]PASSED[/green] - {num_neighbors} neighbors found")
            else:
                print(f"{dev_name}: [red]FAILED[/red] - {num_neighbors} neighbors found")
                fail_report(dev_name)
        else:
            print(f"{dev_name}: [red]FAILED[/red] - No OSPF neighbors found")

    except Exception as e:
        print(f"{dev_name}: [red]ERROR[/red] - {str(e)}")
        
def fail_report(dev_name):
    rooms = api.rooms.list()
    for room in rooms:
        if room.title == "MerakiChatroom":
            target_room = room.id 
    api.messages.create(target_room, text=f"ALERT: {dev_name} OSPF NEIGHBOR FAILURE")

# Run the OSPF test on all devices
results = nr.run(task=ospf_test)

# Print the summary of results
print("\n[bold]OSPF Neighbor Test Completed[/bold]")