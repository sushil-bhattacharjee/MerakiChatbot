from nornir import InitNornir

nr = InitNornir(config_file="config.yaml")

def test_connection(task):
    print(f"Connecting to {task.host.hostname}")

results = nr.run(task=test_connection)
