import subprocess
import json
import time

def get_cluster_stats():
    result = subprocess.run(
        ['lxc', 'list', '--format', 'json'],
        capture_output=True,
        text=True
    )
    instances = json.loads(result.stdout)
    running = [i for i in instances if i['status'] == 'Running']
    auto_instances = [i for i in running if i['name'].startswith('nebula-auto-')]

    instance_details = []
    for inst in running:
        mem_bytes = 0
        cpu_ns = 0
        state = inst.get('state') or {}
        memory = state.get('memory') or {}
        cpu = state.get('cpu') or {}
        mem_bytes = memory.get('usage', 0)
        cpu_ns = cpu.get('usage', 0)

        instance_details.append({
            'name': inst['name'],
            'status': inst['status'],
            'memory_mb': round(mem_bytes / 1024 / 1024, 1),
            'cpu_usage_ns': cpu_ns,
        })

    return {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'total_instances': len(instances),
        'running_instances': len(running),
        'auto_scaled_instances': len(auto_instances),
        'instance_details': instance_details,
    }

if __name__ == '__main__':
    stats = get_cluster_stats()
    print("Cluster Stats:")
    print(f"  Total: {stats['total_instances']}")
    print(f"  Running: {stats['running_instances']}")
    print(f"  Auto-scaled: {stats['auto_scaled_instances']}")
    for inst in stats['instance_details']:
        print(f"  - {inst['name']} | RAM: {inst['memory_mb']} MB | CPU ns: {inst['cpu_usage_ns']}")