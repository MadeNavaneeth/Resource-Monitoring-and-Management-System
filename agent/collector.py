import psutil
import platform
import socket
import subprocess
import re
from datetime import datetime, timezone

class SystemCollector:
    def get_system_info(self):
        """Collects detailed static system information."""
        try:
            ip = socket.gethostbyname(socket.gethostname())
        except Exception:
            ip = "127.0.0.1"
        
        # Get MAC address
        mac_address = None
        try:
            for interface, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    if addr.family == psutil.AF_LINK:
                        if addr.address and addr.address != "00:00:00:00:00:00":
                            mac_address = addr.address
                            break
                if mac_address:
                    break
        except Exception:
            pass
        
        # CPU Info
        cpu_name = platform.processor() or 'Unknown CPU'
        
        # Better OS Detection
        os_name = platform.system()
        os_release = platform.release()
        os_build = platform.version()
        
        if os_name == "Windows":
            try:
                version_parts = os_build.split('.')
                if len(version_parts) >= 3 and int(version_parts[2]) >= 22000:
                    os_release = "11"
            except Exception:
                pass
        
        os_info = f"{os_name} {os_release}"
        
        # GPU Info (Windows) - using PowerShell, prioritize discrete GPUs
        gpu_name = None
        if os_name == "Windows":
            try:
                output = subprocess.check_output(
                    ["powershell", "-Command", "(Get-CimInstance Win32_VideoController).Name"],
                    stderr=subprocess.DEVNULL, timeout=10
                ).decode().strip()
                if output:
                    gpus = [g.strip() for g in output.split('\n') if g.strip()]
                    # Priority: NVIDIA > AMD > Others (skip Virtual/Intel)
                    nvidia_gpu = next((g for g in gpus if 'NVIDIA' in g.upper()), None)
                    amd_gpu = next((g for g in gpus if 'AMD' in g.upper() or 'RADEON' in g.upper()), None)
                    # Pick best GPU, fallback to first non-virtual
                    if nvidia_gpu:
                        gpu_name = nvidia_gpu
                    elif amd_gpu:
                        gpu_name = amd_gpu
                    else:
                        # Skip virtual monitors and pick first real one
                        real_gpu = next((g for g in gpus if 'VIRTUAL' not in g.upper() and 'META' not in g.upper()), None)
                        gpu_name = real_gpu or gpus[0]
            except Exception:
                pass
        
        # Machine Manufacturer/Model (Windows)
        manufacturer = None
        model = None
        if os_name == "Windows":
            try:
                output = subprocess.check_output(
                    ["powershell", "-Command", "(Get-CimInstance Win32_ComputerSystem).Manufacturer"],
                    stderr=subprocess.DEVNULL, timeout=10
                ).decode().strip()
                if output:
                    manufacturer = output
            except Exception:
                pass
            try:
                output = subprocess.check_output(
                    ["powershell", "-Command", "(Get-CimInstance Win32_ComputerSystem).Model"],
                    stderr=subprocess.DEVNULL, timeout=10
                ).decode().strip()
                if output:
                    model = output
            except Exception:
                pass
        
        # Total disk space
        disk_path = "C:\\" if os_name == "Windows" else "/"
        try:
            disk = psutil.disk_usage(disk_path)
            total_disk_gb = round(disk.total / (1024**3), 1)
        except Exception:
            total_disk_gb = None
        
        # Username and Domain
        username = None
        domain = None
        try:
            import getpass
            username = getpass.getuser()
            if os_name == "Windows":
                domain = os.environ.get('USERDOMAIN', None)
        except Exception:
            pass
        
        # Timezone
        timezone_name = None
        try:
            import time
            timezone_name = time.tzname[0]
        except Exception:
            pass
        
        # Battery (for laptops)
        battery_percent = None
        is_plugged_in = None
        try:
            battery = psutil.sensors_battery()
            if battery:
                battery_percent = battery.percent
                is_plugged_in = battery.power_plugged
        except Exception:
            pass
        
        # BIOS Version and Serial Number (Windows)
        bios_version = None
        serial_number = None
        if os_name == "Windows":
            try:
                output = subprocess.check_output(
                    ["powershell", "-Command", "(Get-CimInstance Win32_BIOS).SMBIOSBIOSVersion"],
                    stderr=subprocess.DEVNULL, timeout=10
                ).decode().strip()
                if output:
                    bios_version = output
            except Exception:
                pass
            
            try:
                output = subprocess.check_output(
                    ["powershell", "-Command", "(Get-CimInstance Win32_BIOS).SerialNumber"],
                    stderr=subprocess.DEVNULL, timeout=10
                ).decode().strip()
                if output:
                    serial_number = output
            except Exception:
                pass
        
        # Windows Edition
        windows_edition = None
        if os_name == "Windows":
            try:
                output = subprocess.check_output(
                    ["powershell", "-Command", "(Get-CimInstance Win32_OperatingSystem).Caption"],
                    stderr=subprocess.DEVNULL, timeout=10
                ).decode().strip()
                if output:
                    windows_edition = output
            except Exception:
                pass
        
        # Disk Model (Windows)
        disk_model = None
        if os_name == "Windows":
            try:
                # Get the model of the first disk drive (usually the boot drive 0)
                output = subprocess.check_output(
                    ["powershell", "-Command", "Get-CimInstance Win32_DiskDrive | Select-Object -First 1 -ExpandProperty Model"],
                    stderr=subprocess.DEVNULL, timeout=10
                ).decode().strip()
                if output:
                    disk_model = output
            except Exception:
                pass

        # Network Adapter Name
        network_adapter = None
        try:
            stats = psutil.net_if_stats()
            for name, stat in stats.items():
                if stat.isup and name not in ['Loopback Pseudo-Interface 1', 'lo']:
                    network_adapter = name
                    break
        except Exception:
            pass

        # Driver Inventory (Windows)
        drivers = []
        if os_name == "Windows":
            try:
                # Fetch signed drivers with key details
                cmd = [
                    "powershell", "-Command",
                    "Get-CimInstance Win32_PnPSignedDriver | Select-Object DeviceName, DeviceClass, DriverVersion, @{N='DriverDate';E={$_.DriverDate.ToString('yyyy-MM-dd')}} | ConvertTo-Json -Compress"
                ]
                output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, timeout=15).decode().strip()
                if output:
                    import json
                    # PowerShell might return a single object or list; handle both
                    driver_data = json.loads(output)
                    if isinstance(driver_data, dict):
                        drivers = [driver_data]
                    elif isinstance(driver_data, list):
                        drivers = driver_data
            except Exception:
                pass

        return {
            "hostname": platform.node(),
            "ip_address": ip,
            "mac_address": mac_address,
            "os_info": os_info,
            "os_build": os_build,
            "windows_edition": windows_edition,
            "agent_version": "1.0.0",
            "cpu_name": cpu_name,
            "cpu_cores": psutil.cpu_count(logical=False) or 1,
            "cpu_threads": psutil.cpu_count(logical=True) or 1,
            "architecture": platform.machine(),
            "total_memory_gb": round(psutil.virtual_memory().total / (1024**3), 1),
            "total_disk_gb": total_disk_gb,
            "disk_model": disk_model,
            "gpu_name": gpu_name,
            "manufacturer": manufacturer,
            "model": model,
            "serial_number": serial_number,
            "bios_version": bios_version,
            "username": username,
            "domain": domain,
            "timezone": timezone_name,
            "network_adapter": network_adapter,
            "battery_percent": battery_percent,
            "is_plugged_in": is_plugged_in,
            "python_version": platform.python_version(),
            "drivers": drivers
        }

    def get_metrics(self):
        """Collects detailed dynamic system metrics."""
        disk_path = "C:\\" if platform.system() == "Windows" else "/"
        
        # Per-CPU usage (Non-blocking: returns usage since last call)
        cpu_per_core = psutil.cpu_percent(interval=None, percpu=True)
        
        # Memory details
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        # Disk details
        disk = psutil.disk_usage(disk_path)
        
        # Network
        net = psutil.net_io_counters()
        
        # Disk I/O - Manual Aggregation for robustness
        disk_io_dict = psutil.disk_io_counters(perdisk=True)
        read_total = 0
        write_total = 0
        if disk_io_dict:
            for metrics in disk_io_dict.values():
                read_total += metrics.read_bytes
                write_total += metrics.write_bytes
        
        # print(f"DEBUG IO: {read_total}, {write_total}")
        
        # Process count
        process_count = len(psutil.pids())
        
        # Boot time and uptime
        boot_timestamp = psutil.boot_time()
        boot_time = datetime.fromtimestamp(boot_timestamp).isoformat()
        uptime_seconds = int(datetime.now().timestamp() - boot_timestamp)
        
        # Human-readable uptime
        days, remainder = divmod(uptime_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, _ = divmod(remainder, 60)
        if days > 0:
            uptime_human = f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            uptime_human = f"{hours}h {minutes}m"
        else:
            uptime_human = f"{minutes}m"
        
        # Top 5 processes by CPU
        top_processes = []
        try:
            procs = []
            for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    pinfo = p.info
                    if pinfo['cpu_percent'] is not None:
                        procs.append(pinfo)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            # Sort by CPU, take top 5
            procs.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
            top_processes = procs[:5]
        except Exception:
            pass
        
        return {
            "cpu_usage": psutil.cpu_percent(interval=None),
            "cpu_per_core": cpu_per_core,
            "memory_total": mem.total,
            "memory_used": mem.used,
            "memory_available": mem.available,
            "memory_percent": mem.percent,
            "swap_total": swap.total,
            "swap_used": swap.used,
            "swap_percent": swap.percent,
            "disk_total": disk.total,
            "disk_used": disk.used,
            "disk_free": disk.free,
            "disk_usage": disk.percent,
            "disk_read_bytes": read_total,
            "disk_write_bytes": write_total,
            "network_sent": net.bytes_sent,
            "network_recv": net.bytes_recv,
            "network_packets_sent": net.packets_sent,
            "network_packets_recv": net.packets_recv,
            "process_count": process_count,
            "boot_time": boot_time,
            "uptime_seconds": uptime_seconds,
            "uptime_human": uptime_human,
            "top_processes": top_processes,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
