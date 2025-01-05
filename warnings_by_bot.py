import os
from rich import print
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command

nr = InitNornir(config_file="config.yaml")

clear_command = "clear"
os.system(clear_command)

def ospftest(task):
    dev_name = task.host
    my_list = []
    result = task.run(netmiko_send_command, command_string="show ip ospf neighbor", use_genie=True)
    task.host["facts"] = result.result
    interfaces = task.host["facts"]["interfaces"]
    for interface in interfaces:
        neighbor = interfaces[interface]["neighbors"]
        for adjacency in neighbor:
            my_list.append(adjacency)
    num_neighbors = len(my_list)
    if num_neighbors == 2:
        print(f"{dev_name}: [green]PASSED[/green]")
    else:
        print(f"{dev_name}: [red]FAILED[/red]")
        
results = nr.run(task=ospftest)