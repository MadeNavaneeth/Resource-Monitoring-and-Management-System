import time
import requests
import os
import logging
from dotenv import load_dotenv
from collector import SystemCollector

load_dotenv()

# Configuration
SERVER_URL = os.getenv("SERVER_URL", "http://192.168.62.122:8000/api/v1")
API_KEY = os.getenv("AGENT_API_KEY", "secret-agent-key")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "5"))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def register_agent(collector, session, user_label=None):
    """Registers the agent with the backend."""
    sys_info = collector.get_system_info()
    if user_label:
        sys_info['user_label'] = user_label
    while True:
        try:
            logger.info(f"Attempting to register with {SERVER_URL}...")
            response = session.post(f"{SERVER_URL}/systems/register", json=sys_info)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Registered successfully. System ID: {data['id']}")
            return data['id']
        except requests.exceptions.RequestException as e:
            logger.error(f"Registration failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)

def main():
    collector = SystemCollector()
    session = requests.Session()
    session.headers.update({"X-API-Key": API_KEY})

    user_label = os.getenv("USER_LABEL", None)
    
    # Debug: Print collected info before registering
    print("--- DEBUG: Collecting System Info ---")
    sys_info = collector.get_system_info()
    print(f"Hostname: {sys_info.get('hostname')}")
    print(f"OS: {sys_info.get('os_info')}")
    print(f"GPU: {sys_info.get('gpu_name')}")
    print(f"Drivers Count: {len(sys_info.get('drivers', []) if sys_info.get('drivers') else [])}")
    print("-------------------------------------")

    # Re-use collected info for registration to save time? 
    # The register_agent function calls get_system_info() again. 
    # Let's just pass this sys_info to avoid double collection if we modify register_agent, 
    # but for safety I'll let it stay as is or modify register_agent to accept it.
    # Actually, register_agent calls it. Let's just trust the print.
    
    system_id = register_agent(collector, session, user_label)

    logger.info("Starting metric collection loop...")
    while True:
        try:
            metrics = collector.get_metrics()
            metrics["system_id"] = system_id
            
            response = session.post(f"{SERVER_URL}/metrics", json=metrics)
            if response.status_code == 201:
                logger.debug("Metrics sent successfully.")
            elif response.status_code == 404:
                logger.warning("System ID not found (404). Re-registering...")
                system_id = register_agent(collector, session, user_label)
            else:
                logger.warning(f"Failed to send metrics: {response.text}")
            
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
        
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Agent stopped by user.")
    except Exception:
        import traceback
        traceback.print_exc()
        print("\n❌ CRITICAL ERROR: The agent crashed.")
        input("Press Enter to close this window...")
