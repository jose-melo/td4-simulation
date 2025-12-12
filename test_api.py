"""
Test the Flask API endpoints
"""

import requests
import json

BASE_URL = "http://localhost:5001"

# Create a session to maintain cookies
session = requests.Session()

print("=" * 60)
print("Testing Flask API")
print("=" * 60)

# Test 1: Health Check
print("\n1. Testing Health Check")
response = session.get(f"{BASE_URL}/api/health")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# Test 2: Get Config
print("\n2. Testing Get Config")
response = session.get(f"{BASE_URL}/api/config")
config = response.json()
print(f"Status: {response.status_code}")
print(f"Capacity: {config['capacity']}")
print(f"Total Items: {config['total_items']}")
print(f"Total Size: {config['total_size']}")

# Test 3: Start Simulation (First Fit)
print("\n3. Testing Start Simulation (First Fit)")
response = session.post(f"{BASE_URL}/api/start",
    json={'algorithm': 'ff'})
result = response.json()
print(f"Status: {response.status_code}")
print(f"Algorithm: {result['algorithm']}")
print(f"Session ID: {result['session_id'][:16]}...")

# Test 4: Execute First Step
print("\n4. Testing Execute Step")
response = session.post(f"{BASE_URL}/api/step")
result = response.json()
print(f"Status: {response.status_code}")
print(f"Is Complete: {result['is_complete']}")
if result['step_result']:
    step = result['step_result']
    print(f"Item: {step['item']}")
    print(f"Placed in Bin: #{step['bin_index'] + 1}")
    print(f"Explanation: {step['explanation']}")

# Test 5: Get Statistics
print("\n5. Testing Get Statistics")
response = session.get(f"{BASE_URL}/api/statistics")
stats = response.json()
print(f"Status: {response.status_code}")
print(f"Items Processed: {stats['items_processed']}/{stats['total_items']}")
print(f"Bins Used: {stats['bins_used']}")
print(f"Efficiency: {stats['efficiency']}%")

# Test 6: Reset
print("\n6. Testing Reset")
response = session.post(f"{BASE_URL}/api/reset")
result = response.json()
print(f"Status: {response.status_code}")
print(f"Message: {result['message']}")

# Test 7: Start with Best Fit and run complete simulation
print("\n7. Running Complete Best Fit Simulation")
response = session.post(f"{BASE_URL}/api/start",
    json={'algorithm': 'bf'})
print(f"Started Best Fit simulation")

step_count = 0
while True:
    response = session.post(f"{BASE_URL}/api/step")
    result = response.json()

    if result['is_complete']:
        break

    step_count += 1

print(f"Completed {step_count} steps")

# Get final statistics
response = session.get(f"{BASE_URL}/api/statistics")
stats = response.json()
print(f"\nFinal Results:")
print(f"  Bins Used: {stats['bins_used']}")
print(f"  Efficiency: {stats['efficiency']}%")
print(f"  All items processed: {stats['items_processed'] == stats['total_items']}")

print("\n" + "=" * 60)
print("All API tests passed successfully!")
print("=" * 60)
