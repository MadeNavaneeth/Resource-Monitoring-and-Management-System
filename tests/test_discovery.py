
from agent.discovery import find_server
import time

print("--- Testing UDP Discovery ---")
print("Listening for Server Beacon...")
url = find_server(timeout=5)

if url:
    print(f"✅ SUCCESS: Server found at {url}")
else:
    print("❌ FAILURE: Discovery timed out")
