from openai import OpenAI
import json

GROQ_API_KEY = 'your-groq-key-here'

def get_scaling_decision(cluster_stats):
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key="api-key"
    )

    prompt = f"""
    You are an intelligent auto-scaling agent managing a private LXD cloud.
    Analyse the cluster statistics below and decide what action to take.

    Cluster Statistics:
    {json.dumps(cluster_stats, indent=2)}

    Rules you must follow:
    - If running_instances is 0, always respond with scale_out.
    - If running_instances is 1 and memory_mb is above 300, respond with scale_out.
    - If running_instances is 3 or more and all memory_mb values are below 100, respond with scale_in.
    - If auto_scaled_instances is 0, never respond with scale_in.
    - Otherwise respond with hold.

    Reply ONLY with a JSON object in this exact format, no other text:
    {{
      "action": "scale_out",
      "reason": "one clear sentence explaining why",
      "confidence": 0.9
    }}
    The action field must be exactly one of scale_out, scale_in, hold.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )

    output_text = response.choices[0].message.content.strip()

    if '```' in output_text:
        parts = output_text.split('```')
        for part in parts:
            part = part.strip().strip('json').strip()
            if part.startswith('{'):
                output_text = part
                break

    return json.loads(output_text)

if __name__ == '__main__':
    print("Testing AI brain module...")
    test_stats = {
        'timestamp': '2024-01-01 12:00:00',
        'total_instances': 1,
        'running_instances': 1,
        'auto_scaled_instances': 0,
        'instance_details': [
            {
                'name': 'baseline-vm',
                'status': 'Running',
                'memory_mb': 420.5,
                'cpu_usage_ns': 9800000000,
            }
        ],
    }
    decision = get_scaling_decision(test_stats)
    print(f"Action: {decision['action']}")
    print(f"Reason: {decision['reason']}")
    print(f"Confidence: {decision['confidence']}")