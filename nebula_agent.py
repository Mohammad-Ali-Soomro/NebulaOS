import sys
import time
import os
from datetime import datetime

sys.path.insert(0, os.path.expanduser('~/nebulaos'))

from nebula_monitor import get_cluster_stats
from nebula_brain import get_scaling_decision
from nebula_action import execute_action

CHECK_INTERVAL = 60
LOG_FILE = os.path.expanduser('~/nebulaos/nebula_agent.log')

def log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = f"[{timestamp}] {message}"
    print(entry)
    with open(LOG_FILE, 'a') as f:
        f.write(entry + '\n')

def run_agent():
    log("=" * 55)
    log(" NebulaOS AI Auto-Scaling Agent Starting")
    log("=" * 55)
    log(f"Check interval: {CHECK_INTERVAL} seconds")
    log("")

    cycle = 0
    while True:
        cycle += 1
        log(f"--- Cycle {cycle} ---")
        try:
            log("Collecting cluster statistics...")
            stats = get_cluster_stats()
            log(f"Instances: {stats['running_instances']} running "
                f"({stats['auto_scaled_instances']} auto-scaled)")

            log("Asking Minimax AI for a decision...")
            decision = get_scaling_decision(stats)

            log(f"AI Action: {decision['action'].upper()}")
            log(f"AI Reason: {decision['reason']}")
            log(f"Confidence: {decision['confidence']}")

            log("Executing action...")
            result = execute_action(decision['action'])
            log(f"Result: {result}")

        except Exception as error:
            log(f"ERROR: {error}")

        log(f"Sleeping {CHECK_INTERVAL} seconds...")
        log("")
        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    run_agent()
