"""
Test Next Fit via API
"""

import requests

BASE_URL = "http://localhost:5001"
session = requests.Session()

print("=" * 60)
print("Testing Next Fit Algorithm via API")
print("=" * 60)

# Test Next Fit with demo data
print("\n1. Testing Next Fit with Demo Data")
response = session.post(f"{BASE_URL}/api/start", json={'algorithm': 'nf'})
result = response.json()
print(f"Status: {response.status_code}")
print(f"Algorithm: {result['algorithm']}")

# Run all steps
step_count = 0
while True:
    response = session.post(f"{BASE_URL}/api/step")
    result = response.json()

    if result['is_complete']:
        break

    step_count += 1
    step = result['step_result']
    new_bin_indicator = " (NEW)" if step['is_new_bin'] else ""
    print(f"  Step {step_count}: Item {step['item']} → Bin #{step['bin_index'] + 1}{new_bin_indicator}")

# Get final stats
response = session.get(f"{BASE_URL}/api/statistics")
stats = response.json()

print(f"\nNext Fit Results:")
print(f"  Bins used: {stats['bins_used']}")
print(f"  Efficiency: {stats['efficiency']}%")

# Test custom worst case
print("\n2. Testing Worst Case: [6, 4, 6, 4, 6, 4]")
session = requests.Session()  # New session

response = session.post(f"{BASE_URL}/api/start", json={
    'algorithm': 'nf',
    'capacity': 10,
    'items': [6, 4, 6, 4, 6, 4]
})

step_count = 0
while True:
    response = session.post(f"{BASE_URL}/api/step")
    result = response.json()

    if result['is_complete']:
        break

    step_count += 1

response = session.get(f"{BASE_URL}/api/statistics")
stats = response.json()

print(f"  Bins used: {stats['bins_used']}")
print(f"  Bin details:")
for bin_detail in stats['bin_details']:
    print(f"    Bin #{bin_detail['bin_number']}: {bin_detail['items']}")

# Compare all three algorithms
print("\n3. Comparing All Algorithms")
print("-" * 60)

algorithms = [
    ('nf', 'Next Fit'),
    ('ff', 'First Fit'),
    ('bf', 'Best Fit')
]

for algo_code, algo_name in algorithms:
    session = requests.Session()

    response = session.post(f"{BASE_URL}/api/start", json={
        'algorithm': algo_code,
        'capacity': 10,
        'items': [4, 4, 5, 5, 5, 4, 4, 6, 6, 2, 2, 3, 3, 7, 7, 2, 2, 5, 5, 8, 8, 4, 4, 5]
    })

    while True:
        response = session.post(f"{BASE_URL}/api/step")
        result = response.json()
        if result['is_complete']:
            break

    response = session.get(f"{BASE_URL}/api/statistics")
    stats = response.json()

    complexity = "O(N)" if algo_code == 'nf' else "O(N²)"
    print(f"{algo_name:12} - {stats['bins_used']} bins ({stats['efficiency']}%) - {complexity}")

print("\n" + "=" * 60)
print("Next Fit API tests completed!")
print("=" * 60)
