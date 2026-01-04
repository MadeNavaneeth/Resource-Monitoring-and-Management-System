
import sqlite3
from fpdf import FPDF
import os

# Configuration
DB_PATH = 'backend/resource_monitor.db'
OUTPUT_FILE = 'user_creds_report.pdf'

def fetch_users():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        return []
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Check if table exists
    try:
        cursor.execute("SELECT id, email, hashed_password, is_active FROM users")
        users = cursor.fetchall()
        return users
    except sqlite3.OperationalError as e:
        print(f"Error querying database: {e}")
        return []
    finally:
        conn.close()

class PDFreport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'User Credentials Report', 0, 1, 'C')
        self.ln(10)

    def chapter_body(self, users):
        self.set_font('Arial', 'B', 12)
        # Header
        self.cell(10, 10, 'ID', 1)
        self.cell(60, 10, 'Email/Username', 1)
        self.cell(90, 10, 'Hashed Password', 1)
        self.cell(20, 10, 'Active', 1)
        self.ln()
        
        # Data
        self.set_font('Arial', '', 10)
        for user in users:
            uid, email, pwd, active = user
            # Truncate pwd for display if too long
            display_pwd = pwd[:20] + "..." if len(pwd) > 20 else pwd
            
            self.cell(10, 10, str(uid), 1)
            self.cell(60, 10, str(email), 1)
            self.cell(90, 10, str(pwd), 1) # Full hash might overflow, let's see. Multi-cell might be better but let's try single line first.
            self.cell(20, 10, str(bool(active)), 1)
            self.ln()

def generate_pdf():
    users = fetch_users()
    if not users:
        print("No users found or database unreachable.")
        return

    pdf = PDFreport()
    pdf.add_page()
    
    # Custom layout for the table
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(10, 10, 'ID', 1)
    pdf.cell(50, 10, 'Email', 1)
    pdf.cell(20, 10, 'Status', 1)
    pdf.cell(110, 10, 'Hashed Password', 1)
    pdf.ln()
    
    pdf.set_font('Arial', '', 8)
    
    # Column widths
    w_id = 10
    w_email = 50
    w_status = 20
    w_pass = 110
    
    for user in users:
        uid, email, pwd, active = user
        status = "Active" if active else "Inactive"
        
        # Standard height
        h = 8
        
        pdf.set_font('Arial', '', 8)
        pdf.cell(w_id, h, str(uid), 1)
        pdf.cell(w_email, h, str(email), 1)
        pdf.cell(w_status, h, status, 1)
        
        # Switch to Courier (Monospace) 7pt for Hash to ensure fit
        pdf.set_font('Courier', '', 7)
        
        # Ensure it doesn't overflow the cell
        if pdf.get_string_width(pwd) > w_pass:
             # Truncate blindly if too long to prevent layout break
             pdf.cell(w_pass, h, pwd, 1)
        else:
            pdf.cell(w_pass, h, pwd, 1)
            
        pdf.ln()
        
    pdf.output(OUTPUT_FILE, 'F')
    print(f"PDF generated successfully: {os.path.abspath(OUTPUT_FILE)}")

if __name__ == "__main__":
    generate_pdf()
