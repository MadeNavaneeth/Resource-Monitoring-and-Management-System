import tkinter as tk
from tkinter import ttk, messagebox
import threading
import sys
import os
import time
import math
import multiprocessing
import requests
import ctypes
import logging
import socket
from dotenv import load_dotenv, set_key

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load vars
load_dotenv()

# Configuration (Target for setup_lab.py automation)
SERVER_URL = os.getenv("SERVER_URL", "http://127.0.0.1:8000/api/v1")

class RoundedButton(tk.Canvas):
    def __init__(self, parent, width, height, corner_radius, padding=0, color="#ff6600", fg="#000000", command=None, text="", state="normal"):
        tk.Canvas.__init__(self, parent, borderwidth=0, 
            relief="flat", highlightthickness=0, bg="#0a0a0a", width=width+padding, height=height+padding)
        self.command = command
        self.width = width
        self.height = height
        self.corner_radius = corner_radius
        self.color = color
        self.fg = fg
        self.base_color = color
        self.text_content = text
        self.state = state

        if color == "#ff6600": # Start Byte
            self.hover_color = "#ff8533"
            self.click_color = "#cc5200"
        else: # Stop/Disabled
            self.hover_color = "#333333"
            self.click_color = "#000000"

        # Events
        if self.state == "normal":
            self.bind("<ButtonPress-1>", self._on_press)
            self.bind("<ButtonRelease-1>", self._on_release)
            self.bind("<Enter>", self._on_hover)
            self.bind("<Leave>", self._on_leave)

        self._draw()

    def _draw(self):
        self.delete("all")
        if self.state == "disabled":
            draw_color = "#1a1a1a"
            text_color = "#444444"
        else:
            draw_color = self.color
            text_color = self.fg

        # Draw Pill Shape (Robust Composition)
        h = self.height
        w = self.width
        r = h / 2  # Full rounded ends (Pill)

        # Left Circle
        self.create_oval(0, 0, h, h, fill=draw_color, outline=draw_color)
        # Right Circle
        self.create_oval(w-h, 0, w, h, fill=draw_color, outline=draw_color)
        # Middle Rect
        self.create_rectangle(r, 0, w-r, h, fill=draw_color, outline=draw_color)
        
        self.create_text(w/2, h/2, text=self.text_content, fill=text_color, font=("Segoe UI", 10, "bold"))

    def _on_press(self, event):
        if self.state != "normal": return
        self.color = self.click_color
        self._draw()

    def _on_release(self, event):
        if self.state != "normal": return
        self.color = self.hover_color
        self._draw()
        if self.command:
            self.command()

    def _on_hover(self, event):
        if self.state != "normal": return
        self.color = self.hover_color
        self._draw()

    def _on_leave(self, event):
        if self.state != "normal": return
        self.color = self.base_color
        self._draw()

    def set_state(self, state, color="#1a1a1a", fg="#666666"):
        self.state = state
        if state == "normal":
            self.base_color = color
            self.color = color
            self.fg = fg
            self.bind("<ButtonPress-1>", self._on_press)
            self.bind("<ButtonRelease-1>", self._on_release)
            self.bind("<Enter>", self._on_hover)
            self.bind("<Leave>", self._on_leave)
        else:
            self.unbind("<ButtonPress-1>")
            self.unbind("<ButtonRelease-1>")
            self.unbind("<Enter>")
            self.unbind("<Leave>")
        
        self._draw()

class ModernEntry(tk.Entry):
    """Styled Entry widget matching TE design."""
    def __init__(self, parent, width=30, textvariable=None, **kwargs):
        super().__init__(
            parent,
            width=width,
            textvariable=textvariable,
            font=("Segoe UI", 11),
            bg="#111111", # Dark Info Card bg
            fg="#ffffff", # White Text
            insertbackground="#ffffff", # White Cursor
            relief="flat",
            highlightthickness=1,
            highlightbackground="#333333",
            highlightcolor="#ff6600",
            **kwargs
        )

class TicketDialog(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.title("Raise Issue")
        self.geometry("400x400") # Increased height
        self.configure(bg="#0a0a0a")
        self.resizable(False, False)
        
        # Center dialog
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 200
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 200
        self.geometry(f"+{x}+{y}")

        # Header
        lbl = tk.Label(self, text="DESCRIBE THE ISSUE", font=("Segoe UI", 12, "bold"), fg="#aaaaaa", bg="#0a0a0a")
        lbl.pack(pady=15)

        # Text Area
        self.text_area = tk.Text(self, height=6, width=40, font=("Segoe UI", 10), 
                               bg="#111111", fg="#ffffff", insertbackground="#ffffff",
                               relief="flat", highlightthickness=1, highlightbackground="#333333")
        self.text_area.pack(pady=5, padx=20)
        self.text_area.focus_set()

        # Buttons
        btn_frame = tk.Frame(self, bg="#0a0a0a")
        btn_frame.pack(pady=20)
        
        submit_btn = RoundedButton(btn_frame, 100, 35, 17, color="#ff6600", fg="#000000", text="SEND", command=self.submit)
        submit_btn.pack(side="left", padx=10)
        
        cancel_btn = RoundedButton(btn_frame, 100, 35, 17, color="#1a1a1a", fg="#aaaaaa", text="CANCEL", command=self.destroy)
        cancel_btn.pack(side="left", padx=10)

    def submit(self):
        msg = self.text_area.get("1.0", tk.END).strip()
        if msg:
            self.callback(msg)
            self.destroy()

class ModernAgentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SysMonitor Agent")
        
        # Start Maximized (Zoomed)
        try:
            self.root.state('zoomed')
        except Exception:
            self.root.geometry("1024x768") # Fallback to big window

        self.root.configure(bg="#0a0a0a")
        self.root.resizable(True, True)

        # Variables
        self.is_running = False
        self.thread = None
        self.stop_event = threading.Event()
        self.angle = 0
        
        # Styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Main Container (Centered in the middle of the screen)
        # We use place() to ensure it is always in the visual center
        self.main_container = tk.Frame(root, bg="#0a0a0a")
        self.main_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Header
        self.header_frame = tk.Frame(self.main_container, bg="#0a0a0a")
        self.header_frame.pack(pady=(10, 20))
        
        self.title_label = tk.Label(self.header_frame, text="SYSMONITOR", font=("Segoe UI", 32, "bold"), fg="#ff6600", bg="#0a0a0a")
        self.title_label.pack()
        
        self.subtitle_label = tk.Label(self.header_frame, text="AGENT CONTROLLER", font=("Segoe UI", 12, "bold"), fg="#aaaaaa", bg="#0a0a0a")
        self.subtitle_label.pack(pady=5)
        
        # Version
        self.version_label = tk.Label(self.header_frame, text="v1.0.0", font=("Segoe UI", 9), fg="#aaaaaa", bg="#0a0a0a")
        self.version_label.pack()

        # Input Group
        self.input_frame = tk.Frame(self.main_container, bg="#0a0a0a")
        self.input_frame.pack(pady=10)

        # Server URL Input
        self.url_label = tk.Label(self.input_frame, text="SERVER URL", font=("Segoe UI", 10, "bold"), fg="#aaaaaa", bg="#0a0a0a")
        self.url_label.pack(anchor="w")
        
        # Default to injected URL if env is empty
        env_url = SERVER_URL
        if not env_url:
             env_url = ""
             
        self.url_entry = ModernEntry(self.input_frame, width=35)
        self.url_entry.pack(pady=(5, 15))
        self.url_entry.insert(0, env_url)
        
        # Device Label Input
        self.name_label = tk.Label(self.input_frame, text="DEVICE NAME", font=("Segoe UI", 10, "bold"), fg="#aaaaaa", bg="#0a0a0a")
        self.name_label.pack(anchor="w")
        
        # Default to hostname if not set
        default_label = os.getenv("USER_LABEL", socket.gethostname())
        self.label_var = tk.StringVar(value=default_label)
        self.name_entry = ModernEntry(self.input_frame, width=35, textvariable=self.label_var)
        self.name_entry.pack(pady=(5, 10))

        # Dial
        self.canvas = tk.Canvas(self.main_container, width=260, height=260, bg="#0a0a0a", highlightthickness=0)
        self.canvas.pack(pady=20)
        self.draw_dial(False)

        # Status
        self.status_label = tk.Label(self.main_container, text="OFFLINE", font=("Segoe UI", 18, "bold"), fg="#aaaaaa", bg="#0a0a0a")
        self.status_label.pack(pady=10)
        
        # Auto-Scan Status
        self.scan_label = tk.Label(self.main_container, text="", font=("Segoe UI", 10), fg="#ff6600", bg="#0a0a0a")
        self.scan_label.pack()
        
        # Metrics Counter
        self.metrics_count = 0
        self.metrics_label = tk.Label(self.main_container, text="", font=("Segoe UI", 9), fg="#aaaaaa", bg="#0a0a0a")
        self.metrics_label.pack(pady=5)

        # Buttons
        self.btn_frame = tk.Frame(self.main_container, bg="#0a0a0a")
        self.btn_frame.pack(pady=20, fill="x")
        
        self.btn_frame.grid_columnconfigure(0, weight=1)
        self.btn_frame.grid_columnconfigure(1, weight=1)

        self.start_btn = RoundedButton(self.btn_frame, 160, 50, 25, color="#ff6600", fg="#000000", text="START", command=self.start_agent)
        self.start_btn.grid(row=0, column=0, padx=15)

        self.stop_btn = RoundedButton(self.btn_frame, 160, 50, 25, color="#1a1a1a", fg="#666666", text="STOP", command=self.stop_agent, state="disabled")
        self.stop_btn.grid(row=0, column=1, padx=15)

        # Raise Issue Button
        self.ticket_btn = RoundedButton(self.main_container, 200, 35, 17, color="#1a1a1a", fg="#aaaaaa", text="RAISE ISSUE", command=self.open_ticket_dialog)
        self.ticket_btn.pack(pady=(0, 20))

        self.animate_dial()
        
        # Auto-Scan if no URL
        if not env_url:
            self.start_scan()

    def start_scan(self):
        self.url_entry.config(state=tk.DISABLED)
        self.start_btn.set_state("disabled", "#1a1a1a", "#444444")
        self.scan_label.config(text="Scanning for Server...")
        
        threading.Thread(target=self.run_scan, daemon=True).start()

    def run_scan(self):
        from discovery import find_server
        url = find_server()
        if url:
            self.root.after(0, lambda: self.on_scan_success(url))
        else:
            self.root.after(0, self.on_scan_fail)

    def on_scan_success(self, url):
        self.url_entry.config(state=tk.NORMAL)
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, url)
        self.start_btn.set_state("normal", "#ff6600", "#000000")
        self.scan_label.config(text="Server Found!", fg="#00ff00")
        # Optional: Auto-start
        # self.start_agent() 

    def on_scan_fail(self):
        self.url_entry.config(state=tk.NORMAL)
        self.start_btn.set_state("normal", "#ff6600", "#000000")
        self.scan_label.config(text="Server not found. Enter manually.", fg="#ff0000")

    def draw_dial(self, active):
        self.canvas.delete("all")
        cx, cy, r = 130, 130, 100 # Slightly larger dial
        
        self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r, outline="#1a1a1a", width=6)
        
        if active:
            start = self.angle
            extent = 90
            self.canvas.create_arc(cx-r, cy-r, cx+r, cy+r, start=start, extent=extent, outline="#ff6600", width=6, style=tk.ARC)
            self.canvas.create_arc(cx-r, cy-r, cx+r, cy+r, start=start+180, extent=extent, outline="#ff6600", width=6, style=tk.ARC)
            
            pulse = (math.sin(math.radians(self.angle * 4)) + 1) / 2
            beat_r = 10 + (pulse * 5)
            
            self.canvas.create_oval(cx-beat_r-4, cy-beat_r-4, cx+beat_r+4, cy+beat_r+4, fill="#331100", outline="")
            self.canvas.create_oval(cx-beat_r, cy-beat_r, cx+beat_r, cy+beat_r, fill="#ff6600", outline="")
        else:
            self.canvas.create_oval(cx-6, cy-6, cx+6, cy+6, fill="#333333", outline="")

    def animate_dial(self):
        if self.is_running:
            self.angle = (self.angle + 3) % 360
            self.draw_dial(True)
        else:
            self.draw_dial(False)
        self.root.after(30, self.animate_dial)

    def start_agent(self):
        user_label = self.label_var.get().strip()
        server_url = self.url_entry.get().strip()
        
        if not user_label:
            messagebox.showwarning("Input Required", "Please enter a Device Name")
            return
        if not server_url:
            messagebox.showwarning("Input Required", "Please enter a Server URL")
            return

        try:
            with open(".env", "a") as f: pass
            set_key(".env", "USER_LABEL", user_label)
            set_key(".env", "SERVER_URL", server_url)
        except Exception: pass

        self.is_running = True
        self.stop_event.clear()
        
        self.start_btn.set_state("disabled", "#1a1a1a", "#444444")
        self.stop_btn.set_state("normal", "#ff6600", "#000000")
        
        self.name_entry.config(state=tk.DISABLED)
        self.url_entry.config(state=tk.DISABLED)
        self.status_label.config(text="ONLINE", fg="#ff6600")

        from main import register_agent
        self.thread = threading.Thread(target=self.run_agent_loop, args=(user_label, server_url))
        self.thread.daemon = True
        self.thread.start()

    def stop_agent(self):
        self.is_running = False
        self.stop_event.set()
        
        self.start_btn.set_state("normal", "#ff6600", "#000000")
        self.stop_btn.set_state("disabled", "#1a1a1a", "#666666")
        
        self.name_entry.config(state=tk.NORMAL)
        self.url_entry.config(state=tk.NORMAL)
        self.status_label.config(text="OFFLINE", fg="#444444")
        
        # Reset metrics counter
        self.metrics_count = 0
        self.metrics_label.config(text="")

    def run_agent_loop(self, user_label, server_url):
        # Ensure base URL doesn't end with slash and add API prefix
        base_url = server_url.rstrip('/')
        if not base_url.endswith('/api/v1'):
            base_url = f"{base_url}/api/v1"
        
        API_KEY = os.getenv("AGENT_API_KEY", "secret-agent-key")

        POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "1"))

        from collector import SystemCollector
        collector = SystemCollector()
        session = requests.Session()
        session.headers.update({"X-API-Key": API_KEY})
        # ... logic continues ...

        try:
            # Register logic (Simplified for space, but including re-register)
            sys_info = collector.get_system_info()
            sys_info['user_label'] = user_label
            
            reg_resp = session.post(f"{base_url}/systems/register", json=sys_info)
            if reg_resp.status_code != 200:
                 self.root.after(0, lambda: messagebox.showerror("Error", "Registration Failed"))
                 self.root.after(0, self.stop_agent)
                 return
            
            system_id = reg_resp.json()['id']
            self.system_id = system_id # Cache for UI usage

            while not self.stop_event.is_set():
                metrics = collector.get_metrics()
                metrics["system_id"] = system_id
                
                try:
                    resp = session.post(f"{base_url}/metrics", json=metrics)
                    if resp.status_code == 200:
                        self.metrics_count += 1
                        cpu = metrics.get('cpu_usage', 0)
                        mem = metrics.get('memory_percent', 0)
                        self.root.after(0, lambda c=self.metrics_count, cp=cpu, mp=mem: 
                            self.metrics_label.config(text=f"CPU: {cp:.0f}% | RAM: {mp:.0f}% | Sent: {c}"))
                    elif resp.status_code == 404:
                         logger.warning("404 Auto-Recovery")
                         sys_info = collector.get_system_info()
                         sys_info['user_label'] = user_label
                         reg_2 = session.post(f"{base_url}/systems/register", json=sys_info)
                         if reg_2.status_code == 200:
                             system_id = reg_2.json()['id']
                except Exception as e:
                    logger.error(f"Metrics send error: {e}")

                time.sleep(POLL_INTERVAL)

        except Exception as e:
            logger.error(f"Agent loop error: {e}")
            self.root.after(0, self.stop_agent)

    def on_closing(self):
        self.stop_agent()
        self.root.destroy()
        sys.exit(0)

    def open_ticket_dialog(self):
        TicketDialog(self.root, self.send_ticket)

    def send_ticket(self, message):
         if not self.is_running:
             messagebox.showerror("Error", "Agent must be running (Online) to send tickets.")
             return

         server_url = self.url_entry.get().strip()
         base_url = server_url.rstrip('/')
         if not base_url.endswith('/api/v1'):
            base_url = f"{base_url}/api/v1"
            
         # Use cached system_id if available
         if hasattr(self, 'system_id') and self.system_id:
             threading.Thread(target=self._post_ticket, args=(base_url, message, self.system_id)).start()
         else:
             # Fallback to current slow method if ID not found yet (race condition on startup)
             threading.Thread(target=self._post_ticket_slow, args=(base_url, message)).start()
         
    def _post_ticket(self, base_url, message, system_id):
        try:
            API_KEY = os.getenv("AGENT_API_KEY", "secret-agent-key")

            session = requests.Session()
            session.headers.update({"X-API-Key": API_KEY})
            
            payload = {
                "system_id": system_id,
                "message": message
            }
            resp = session.post(f"{base_url}/tickets", json=payload)
            if resp.status_code == 200:
                self.root.after(0, lambda: messagebox.showinfo("Success", "Ticket Sent Successfully!"))
            else:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to send ticket: {resp.status_code}"))
                
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Network Error: {e}"))

    def _post_ticket_slow(self, base_url, message):
        # ... logic as backup ...
        try:
            # Quick register/check to get ID
            API_KEY = os.getenv("AGENT_API_KEY", "secret-agent-key")

            user_label = self.label_var.get().strip()
            
            from collector import SystemCollector
            collector = SystemCollector()
            sys_info = collector.get_system_info()
            sys_info['user_label'] = user_label
            
            session = requests.Session()
            session.headers.update({"X-API-Key": API_KEY})
            
            reg_resp = session.post(f"{base_url}/systems/register", json=sys_info)
            if reg_resp.status_code == 200:
                system_id = reg_resp.json()['id']
                # Cache it now
                self.system_id = system_id
                self._post_ticket(base_url, message, system_id)
            else:
                 self.root.after(0, lambda: messagebox.showerror("Error", "Could not verify system ID"))

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Network Error: {e}"))
        try:
            # Quick register/check to get ID
            API_KEY = os.getenv("AGENT_API_KEY", "secret-agent-key")
            user_label = self.label_var.get().strip()
            
            from collector import SystemCollector
            collector = SystemCollector()
            sys_info = collector.get_system_info()
            sys_info['user_label'] = user_label
            
            session = requests.Session()
            session.headers.update({"X-API-Key": API_KEY})
            
            reg_resp = session.post(f"{base_url}/systems/register", json=sys_info)
            if reg_resp.status_code == 200:
                system_id = reg_resp.json()['id']
                
                payload = {
                    "system_id": system_id,
                    "message": message
                }
                resp = session.post(f"{base_url}/tickets", json=payload)
                if resp.status_code == 200:
                    self.root.after(0, lambda: messagebox.showinfo("Success", "Ticket Sent Successfully!"))
                else:
                    self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to send ticket: {resp.status_code}"))
            else:
                 self.root.after(0, lambda: messagebox.showerror("Error", "Could not verify system ID"))

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Network Error: {e}"))

if __name__ == "__main__":
    multiprocessing.freeze_support()
    
    try:
        # Enable High DPI Awareness
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass
            
        root = tk.Tk()
        app = ModernAgentGUI(root)
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        root.mainloop()
        
    except KeyboardInterrupt:
        pass
    except Exception:
        import traceback
        traceback.print_exc()
        print("\n❌ CRITICAL GUI ERROR: The agent crashed.")
        input("Press Enter to close this window...")
