import socket
import time
import threading
import json
import logging

logger = logging.getLogger(__name__)

BROADCAST_PORT = 54321
BEACON_INTERVAL = 5

class ServiceBeacon(threading.Thread):
    def __init__(self, port=8000):
        super().__init__()
        self.port = port
        self.stop_event = threading.Event()
        self.daemon = True

    def get_local_ip(self):
        try:
            # Connect to a public DNS server to determine the best local IP
            # (Doesn't actually send data)
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            return "127.0.0.1"

    def run(self):
        broadcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        logger.info("Starting UDP Discovery Beacon...")
        
        while not self.stop_event.is_set():
            try:
                local_ip = self.get_local_ip()
                message = {
                    "server_url": f"http://{local_ip}:{self.port}/api/v1",
                    "hostname": socket.gethostname()
                }
                data = json.dumps(message).encode('utf-8')
                
                # Broadcast to the specific port
                broadcast_sock.sendto(data, ('<broadcast>', BROADCAST_PORT))
                
            except Exception as e:
                logger.error(f"Error broadcasting beacon: {e}")
            
            time.sleep(BEACON_INTERVAL)

    def stop(self):
        self.stop_event.set()
