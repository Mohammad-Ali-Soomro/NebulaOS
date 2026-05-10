from nebula_brain import get_scaling_decision

print("=" * 55)
print(" NebulaOS Load Simulation")
print("=" * 55)

# Scenario 1: single instance under high memory load
print("\nScenario 1: High memory load --> expect SCALE OUT")
stats_high = {
    'timestamp': '2024-01-01 12:00:00',
    'total_instances': 1,
    'running_instances': 1,
    'auto_scaled_instances': 0,
    'instance_details': [{
        'name': 'baseline-vm',
        'status': 'Running',
        'memory_mb': 480.0,
        'cpu_usage_ns': 12000000000,
    }],
}
d = get_scaling_decision(stats_high)
print(f" Action: {d['action']}")
print(f" Reason: {d['reason']}")
print(f" Confidence: {d['confidence']}")

# Scenario 2: three instances all idle
print("\nScenario 2: Low load, many instances --> expect SCALE IN")
stats_low = {
    'timestamp': '2024-01-01 13:00:00',
    'total_instances': 3,
    'running_instances': 3,
    'auto_scaled_instances': 2,
    'instance_details': [
        {
            'name': 'baseline-vm', 
            'status': 'Running',
            'memory_mb': 45.0, 
            'cpu_usage_ns': 100000
        },
        {
            'name': 'nebula-auto-1', 
            'status': 'Running',
            'memory_mb': 42.0, 
            'cpu_usage_ns': 80000
        },
        {
            'name': 'nebula-auto-2', 
            'status': 'Running',
            'memory_mb': 40.0, 
            'cpu_usage_ns': 70000
        },
    ],
}
d = get_scaling_decision(stats_low)
print(f" Action: {d['action']}")
print(f" Reason: {d['reason']}")
print(f" Confidence: {d['confidence']}")

# Scenario 3: two instances, moderate load
print("\nScenario 3: Stable moderate load --> expect HOLD")
stats_stable = {
    'timestamp': '2024-01-01 14:00:00',
    'total_instances': 2,
    'running_instances': 2,
    'auto_scaled_instances': 1,
    'instance_details': [
        {
            'name': 'baseline-vm', 
            'status': 'Running',
            'memory_mb': 180.0, 
            'cpu_usage_ns': 3000000000
        },
        {
            'name': 'nebula-auto-1', 
            'status': 'Running',
            'memory_mb': 160.0, 
            'cpu_usage_ns': 2500000000
        },
    ],
}
d = get_scaling_decision(stats_stable)
print(f" Action: {d['action']}")
print(f" Reason: {d['reason']}")
print(f" Confidence: {d['confidence']}")

print("\nSimulation complete.")