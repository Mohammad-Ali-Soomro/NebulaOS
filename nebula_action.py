import subprocess
import json
import time

MIN_INSTANCES = 1
MAX_INSTANCES = 3
BASE_IMAGE = 'ubuntu:22.04'

def get_all_instances():
    result = subprocess.run(
        ['lxc', 'list', '--format', 'json'],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

def launch_instance():
    instances = get_all_instances()
    if len(instances) >= MAX_INSTANCES:
        return f"Already at maximum capacity ({MAX_INSTANCES} instances). Scale-out skipped."

    name = f"nebula-auto-{int(time.time())}"
    result = subprocess.run(
        ['lxc', 'launch', BASE_IMAGE, name],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return f"Successfully launched instance: {name}"
    else:
        return f"Failed to launch instance. Error: {result.stderr.strip()}"

def terminate_instance():
    instances = get_all_instances()
    running = [i for i in instances if i['status'] == 'Running']
    if len(running) <= MIN_INSTANCES:
        return f"Already at minimum capacity ({MIN_INSTANCES} instances). Scale-in skipped."

    auto_instances = [i for i in running if i['name'].startswith('nebula-auto-')]
    if not auto_instances:
        return "No auto-scaled instances available to terminate."

    target = sorted(auto_instances, key=lambda x: x['name'])[-1]
    result = subprocess.run(
        ['lxc', 'delete', target['name'], '--force'],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return f"Successfully terminated instance: {target['name']}"
    else:
        return f"Failed to terminate. Error: {result.stderr.strip()}"

def execute_action(action):
    if action == 'scale_out':
        return launch_instance()
    elif action == 'scale_in':
        return terminate_instance()
    elif action == 'hold':
        return "Action: hold. No changes made to the cluster."
    else:
        return f"Unrecognised action {action}. No changes made."

if __name__ == '__main__':
    print("Action module loaded.")
    print(f"Min instances: {MIN_INSTANCES} | Max instances: {MAX_INSTANCES} | Image: {BASE_IMAGE}")