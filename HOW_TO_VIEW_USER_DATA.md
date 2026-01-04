# 📖 How to View User Data in Your Software

## 🎯 Location of User Data

**Database File Location:**
```
C:\Users\HP\.gemini\antigravity\scratch\Resource-Monitoring-and-Management-System\backend\resource_monitor.db
```

**Table Name:** `users`

**Columns:**
- `id` - Unique user identifier (INTEGER)
- `email` - User email address (VARCHAR)
- `hashed_password` - Encrypted password (VARCHAR)
- `is_active` - Account status (BOOLEAN)
- `created_at` - Account creation timestamp (DATETIME)

---

## 🖥️ Method 1: Using DB Browser for SQLite (Visual Interface)

### Step 1: Install DB Browser (if not already installed)
You have the installer in your project directory:
```
db_browser_sqlite_installer.msi
```

Double-click it to install if you haven't already.

### Step 2: Open the Database
1. Launch **DB Browser for SQLite**
2. Click **"Open Database"** (or File > Open Database)
3. Navigate to and select:
   ```
   backend\resource_monitor.db
   ```

### Step 3: View User Data
1. Click on the **"Browse Data"** tab at the top
2. In the "Table:" dropdown, select **`users`**
3. You'll see all user records with their details

### Step 4: View Database Structure
1. Click on the **"Database Structure"** tab
2. Expand the **"Tables"** section
3. Expand the **"users"** table to see all columns

---

## 🐍 Method 2: Using Python Scripts

### Quick View (Current Users)
```bash
python inspect_db.py
```

### Detailed View (Full Information)
```bash
python view_all_user_data.py
```

### Custom Query
```python
import sqlite3
conn = sqlite3.connect('backend/resource_monitor.db')
cursor = conn.cursor()

# Example: Get all active users
cursor.execute("SELECT id, email, created_at FROM users WHERE is_active = 1")
for row in cursor.fetchall():
    print(row)

conn.close()
```

---

## 🌐 Method 3: Via Web Dashboard (When Server is Running)

### Step 1: Start the Backend Server
```bash
# From project root
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 2: Access the API
The user data is accessible through the authentication endpoints:

#### Login Endpoint
```
POST http://localhost:8000/api/auth/login
```

#### Register Endpoint
```
POST http://localhost:8000/api/auth/register
```

### Step 3: View in Dashboard
1. Start the frontend dashboard
2. Login with credentials
3. User information will be displayed after authentication

---

## 🔧 Method 4: Direct SQL Query

### Using SQLite Command Line
```bash
sqlite3 backend/resource_monitor.db
```

Then run:
```sql
-- View all users
SELECT * FROM users;

-- View specific user
SELECT * FROM users WHERE email = 'nthy2355@gmail.com';

-- Count total users
SELECT COUNT(*) FROM users;

-- View only active users
SELECT id, email, created_at FROM users WHERE is_active = 1;
```

Exit with: `.quit`

---

## 📊 Current Users in Your Database

Based on the latest data:

| ID | Email | Status | Created At |
|----|-------|--------|------------|
| 1 | nthy2355@gmail.com | ✅ Active | 2025-12-25 13:16:06 |
| 2 | Admin1@gmail.com | ✅ Active | 2025-12-27 08:39:59 |

---

## 💡 Quick Reference

### File Locations
- **Database:** `backend/resource_monitor.db`
- **User Model:** `backend/app/models/models.py` (lines 6-13)
- **Auth API:** `backend/app/api/auth.py`
- **User Schema:** `backend/app/schemas/schemas.py`

### Quick Scripts
```bash
# View users
python inspect_db.py

# View detailed user data
python view_all_user_data.py

# Check all tables
python inspect_s_admins.py
```

---

## 🔐 Security Note

The passwords are stored as **PBKDF2-SHA256 hashes**, which means:
- ✅ Passwords are securely encrypted
- ✅ Original passwords cannot be retrieved
- ✅ Only password verification is possible
- ❌ You cannot see plain-text passwords

If you need to reset a password, you must create a new hash using the registration endpoint or directly in the database.

---

## 📝 Code References

### Where User Data is Used

1. **User Registration:** `backend/app/api/auth.py` (line 11-22)
2. **User Login:** `backend/app/api/auth.py` (line 24-31)
3. **Database Model:** `backend/app/models/models.py` (line 6-13)
4. **Password Security:** `backend/app/core/security.py`

---

**Last Updated:** 2025-12-27
