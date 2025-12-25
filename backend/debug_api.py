import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_api():
    print(f"Testing API at {BASE_URL}...")
    
    # 0. Health Check
    try:
        print("\n[0] Checking /health...")
        health_resp = requests.get("http://localhost:8000/health")
        print(f" -> URL: {health_resp.url}")
        print(f" -> Status: {health_resp.status_code}")
        print(f" -> Body: {health_resp.text}")
    except Exception as e:
        print(f"Health check failed: {e}")

    # 1. List Systems
    try:
        print("\n[1] Fetching Systems List...")
        url = f"{BASE_URL}/systems"
        print(f" -> Requesting: {url}")
        response = requests.get(url)
        print(f" -> Status: {response.status_code}")
        
        if response.status_code == 200:
            systems = response.json()
            print(f"SUCCESS: Found {len(systems)} systems.")
            if systems:
                test_system_id = systems[0]['id']
                print(f" -> Will test details for System ID: {test_system_id}")
                
                # 2. Get System Details
                print(f"\n[2] Fetching Details for System {test_system_id}...")
                details_resp = requests.get(f"{BASE_URL}/systems/{test_system_id}")
                print(f" -> Status: {details_resp.status_code}")
                if details_resp.status_code == 200:
                     print("SUCCESS: System details fetched.")
                else:
                    print(f"FAILED: {details_resp.text}")

                # 3. Get Metrics
                print(f"\n[3] Fetching Metrics for System {test_system_id}...")
                metrics_resp = requests.get(f"{BASE_URL}/systems/{test_system_id}/metrics")
                print(f" -> Status: {metrics_resp.status_code}")
                if metrics_resp.status_code == 200:
                    print("SUCCESS: Metrics fetched.")
                else:
                    print(f"FAILED: {metrics_resp.text}")
            else:
                print("WARNING: No systems found to test details.")
        else:
            print(f"FAILED to list systems: {response.text}")
            
    except Exception as e:
        print(f"ERROR: Could not connect to backend. {e}")

if __name__ == "__main__":
    test_api()
