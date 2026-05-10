import subprocess
import json

result = subprocess.run(
    ['lxc', 'list', '--format', 'json'],
    capture_output=True,
    text=True
)

instances = json.loads(result.stdout)
print(f"LXD is reachable. Total instances: {len(instances)}")
for inst in instances:
    print(f" - {inst['name']} ({inst['status']})")
print("Python to LXD connection is working.")
