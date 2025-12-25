import socket
import os
import re
import subprocess
import sys

def get_ip_addresses():
    """Get all non-loopback IPv4 addresses."""
    ips = []
    try:
        # Get all interfaces
        hostname = socket.gethostname()
        for ip in socket.gethostbyname_ex(hostname)[2]:
            if not ip.startswith("127."):
                ips.append(ip)
    except Exception:
        pass
    
    # Fallback/Additional method using socket connection (doesn't actually connect)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        if ip not in ips and not ip.startswith("127."):
            ips.append(ip)
        s.close()
    except Exception:
        pass
        
    return list(set(ips))

def update_agent_url(ip):
    """Updates the API_URL in agent/main.py."""
    file_path = os.path.join("agent", "main.py")
    new_url = f"http://{ip}:8000/api/v1"
    
    print(f"Reading {file_path}...")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Regex replace SERVER_URL default value
        # Matches: SERVER_URL = os.getenv("SERVER_URL", "...")
        pattern = r'SERVER_URL\s*=\s*os\.getenv\("SERVER_URL",\s*["\'].*?["\']\)'
        replacement = f'SERVER_URL = os.getenv("SERVER_URL", "{new_url}")'
        
        if re.search(pattern, content):
            new_content = re.sub(pattern, replacement, content)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"✅ Updated Agent Code: SERVER_URL set to {new_url}")
            return True
        else:
            print("❌ Error: Could not find SERVER_URL definition in agent/main.py")
            return False
    except FileNotFoundError:
        print(f"❌ Error: File not found: {file_path}")
        return False

def update_frontend_url(ip):
    """Updates the API_URL in dashboard/src/services/api.js."""
    file_path = os.path.join("dashboard", "src", "services", "api.js")
    new_url = f"http://{ip}:8000/api/v1"
    
    print(f"Reading {file_path}...")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Regex replace const API_URL = '...'
        pattern = r"const API_URL\s*=\s*['\"].*?['\"];"
        replacement = f"const API_URL = '{new_url}';"
        
        if re.search(pattern, content):
            new_content = re.sub(pattern, replacement, content)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"✅ Updated Frontend Config: API_URL set to {new_url}")
            return True
        else:
            print("❌ Error: Could not find API_URL definition in dashboard/src/services/api.js")
            return False
    except FileNotFoundError:
        print(f"❌ Error: File not found: {file_path}")
        return False

def build_agent():
    """Runs PyInstaller to build the agent."""
    print("\n🔨 Building Agent.exe (This may take a minute)...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--name", "agent",
            # "--noconsole",  <-- Keep disabled for debugging
            "--clean",
            os.path.join("agent", "gui.py")
        ])
        print("\n✅ Build Complete!")
        print(f"📂 Output: {os.path.abspath('dist/agent.exe')}")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build Failed: {e}")

def main():
    print("="*50)
    print("   🤖 LAB CONNECTION AUTO-SETUP 🤖")
    print("="*50)
    
    ips = get_ip_addresses()
    
    if not ips:
        print("❌ Error: No network connection found.")
        print("   Please connect to WiFi or LAN and try again.")
        input("Press Enter to exit...")
        return

    selected_ip = None
    if len(ips) == 1:
        selected_ip = ips[0]
        print(f"\n📡 Detected Network IP: {selected_ip}")
    else:
        print("\n📡 Multiple IPs found. Which one is your Lab Network?")
        for i, ip in enumerate(ips):
            print(f"   [{i+1}] {ip}")
        
        while True:
            try:
                choice = int(input("\nSelect IP (enter number): ")) - 1
                if 0 <= choice < len(ips):
                    selected_ip = ips[choice]
                    break
            except ValueError:
                pass
            print("Invalid choice.")

    print(f"\n🎯 Target Server: {selected_ip}")
    confirm = input("\nUpdate Agent to connect to this IP? [Y/n]: ").lower()
    if confirm == 'n':
        print("Cancelled.")
        return

    # Update Code
    agent_updated = update_agent_url(selected_ip)
    frontend_updated = update_frontend_url(selected_ip)
    
    if agent_updated:
        # Build
        build_agent()
        
        print("\n" + "="*50)
        print("🚀 READY FOR LAB DEPLOYMENT!")
        print("="*50)
        
        if frontend_updated:
            print("✅ Frontend configured to use Lab IP.")
            print("   (You may need to restart the Dashboard: `npm run dev`)")
        
        print(f"\n1. Copy 'dist/agent.exe' to your Pen Drive.")
        print(f"2. Plug into the 20 Lab Systems.")
        print(f"3. Run it.")
        print(f"4. They will auto-connect to: {selected_ip}")
        print("\nNOTE: Ensure your Firewall allows port 8000!")
    
    input("\nPress Enter to close...")

if __name__ == "__main__":
    main()
