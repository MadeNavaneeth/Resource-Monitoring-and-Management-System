import socket
import json
import logging

logger = logging.getLogger(__name__)

BROADCAST_PORT = 54321

def find_server(timeout=10):
    """Listens for UDP beacon to find server URL."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', BROADCAST_PORT))
        s.settimeout(timeout)
        
        logger.info(f"Scanning for server on port {BROADCAST_PORT}...")
        data, addr = s.recvfrom(1024)
        logger.info(f"Beacon received from {addr}")
        
        msg = json.loads(data.decode('utf-8'))
        s.close()
        return msg.get("server_url")
        
    except socket.timeout:
        logger.warning("Discovery timed out.")
        return None
    except Exception as e:
        logger.error(f"Discovery error: {e}")
        return None
