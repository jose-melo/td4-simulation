"""
Test custom input functionality via API
"""

import requests

BASE_URL = "http://localhost:5001"
session = requests.Session()

print("=" * 60)
print("Testing Custom Input Functionality")
print("=" * 60)

# Test 1: Start with custom capacity and items
print("\n1. Testing Custom Input (capacity=15, items=[5,5,10,7,8,3])")
response = session.post(f"{BASE_URL}/api/start", json={
    'algorithm': 'ff',
    'capacity': 15,
    'items': [5, 5, 10, 7, 8, 3]
})
result = response.json()
print(f"Status: {response.status_code}")
print(f"Session ID: {result['session_id'][:16]}...")

# Run simulation
step_count = 0
while True:
    response = session.post(f"{BASE_URL}/api/step")
    result = response.json()

    if result['is_complete']:
        break

    step = result['step_result']
    step_count += 1
    print(f"  Step {step_count}: Item {step['item']} → Bin #{step['bin_index'] + 1}")

# Get final statistics
response = session.get(f"{BASE_URL}/api/statistics")
stats = response.json()

print(f"\nResults:")
print(f"  Items processed: {stats['items_processed']}")
print(f"  Bins used: {stats['bins_used']}")
print(f"  Efficiency: {stats['efficiency']}%")

# Test 2: Validation - Item larger than capacity
print("\n2. Testing Validation (item > capacity)")
response = session.post(f"{BASE_URL}/api/start", json={
    'algorithm': 'bf',
    'capacity': 5,
    'items': [3, 4, 6]  # 6 > 5
})
print(f"Status: {response.status_code}")
if response.status_code == 400:
    error = response.json()
    print(f"Expected error: {error['error']}")

# Test 3: Small custom example
print("\n3. Testing Small Custom Example (capacity=10, items=[4,6,3,7])")
session = requests.Session()  # New session
response = session.post(f"{BASE_URL}/api/start", json={
    'algorithm': 'bf',
    'capacity': 10,
    'items': [4, 6, 3, 7]
})
result = response.json()
print(f"Status: {response.status_code}")

# Run all steps
bins_sequence = []
while True:
    response = session.post(f"{BASE_URL}/api/step")
    result = response.json()

    if result['is_complete']:
        break

    bins_sequence.append(result['step_result']['bins_state'])

# Get final statistics
response = session.get(f"{BASE_URL}/api/statistics")
stats = response.json()

print(f"\nFinal bin packing:")
for i, bin_detail in enumerate(stats['bin_details']):
    print(f"  Bin #{i + 1}: {bin_detail['items']} = {bin_detail['capacity']}/10 ({bin_detail['utilization']}%)")

print(f"\nTotal bins: {stats['bins_used']}")
print(f"Efficiency: {stats['efficiency']}%")

print("\n" + "=" * 60)
print("Custom input tests completed successfully!")
print("=" * 60)
