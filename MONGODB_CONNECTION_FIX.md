# MongoDB Connection Fix - 503 Service Unavailable Error

## Problem
You're getting a **503 Service Unavailable** error when trying to log in. This happens because the MongoDB database connection is failing.

## Root Cause
The error `The DNS query name does not exist: _mongodb._tcp.students.jb1nyzd.mongodb.net` indicates:
- The MongoDB Atlas cluster cannot be found
- The cluster may be **paused**, **deleted**, or the connection string is **incorrect**
- Network/DNS issues preventing connection

## Solutions

### Option 1: Fix MongoDB Atlas Connection (Recommended)

1. **Check if cluster exists:**
   - Go to https://cloud.mongodb.com/
   - Log in to your MongoDB Atlas account
   - Navigate to **Clusters** (left sidebar)
   - Check if cluster `students.jb1nyzd.mongodb.net` exists

2. **If cluster is paused:**
   - Click **"Resume"** button
   - Wait 2-3 minutes for cluster to start

3. **If cluster doesn't exist:**
   - Create a new cluster (Free tier M0 is fine)
   - Copy the new connection string
   - Update `backend/.env` file (see below)

4. **Whitelist your IP:**
   - Go to **Network Access** (left sidebar)
   - Click **"Add IP Address"**
   - Click **"Allow Access from Anywhere"** (for development)
   - Click **"Confirm"**

5. **Verify database user:**
   - Go to **Database Access** (left sidebar)
   - Check if user `Research` exists
   - If not, create user:
     - Username: `Research`
     - Password: `ilpg1234`
     - Permissions: **Read and write to any database**

6. **Update connection string:**
   - Get your connection string from MongoDB Atlas:
     - Click **"Connect"** on your cluster
     - Choose **"Connect your application"**
     - Copy the connection string
   - Create/update `backend/.env`:
     ```
     MONGODB_URI=mongodb+srv://Research:ilpg1234@YOUR-CLUSTER.mongodb.net/ilpg_db?retryWrites=true&w=majority
     DATABASE_NAME=ilpg_db
     ```

7. **Restart backend server:**
   ```powershell
   cd backend
   python main.py
   ```

### Option 2: Use Local MongoDB (If you have it installed)

1. **Update `backend/.env`:**
   ```
   MONGODB_URI=mongodb://localhost:27017/
   DATABASE_NAME=ilpg_db
   ```

2. **Ensure MongoDB is running:**
   ```powershell
   # Check MongoDB service
   Get-Service MongoDB
   
   # If not running, start it
   Start-Service MongoDB
   ```

3. **Restart backend server**

### Option 3: Verify Connection String Format

The connection string should look like:
```
mongodb+srv://USERNAME:PASSWORD@CLUSTER.mongodb.net/DATABASE?retryWrites=true&w=majority
```

**Important:**
- Replace `USERNAME` with your MongoDB Atlas username
- Replace `PASSWORD` with your MongoDB Atlas password
- Replace `CLUSTER` with your actual cluster name
- Replace `DATABASE` with your database name (usually `ilpg_db`)

## Quick Test

Test your connection string with this Python script:

```python
from pymongo import MongoClient
import sys

# Replace with your connection string
MONGODB_URI = "mongodb+srv://Research:ilpg1234@students.jb1nyzd.mongodb.net/ilpg_db?retryWrites=true&w=majority"

try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("✓ Connection successful!")
    sys.exit(0)
except Exception as e:
    print(f"✗ Connection failed: {e}")
    sys.exit(1)
```

Save as `test_connection.py` and run:
```powershell
cd backend
python test_connection.py
```

## After Fixing Connection

Once connected, initialize the database:
```powershell
cd backend
python init_db.py
```

Then restart your backend server:
```powershell
python main.py
```

You should see: `[SUCCESS] Successfully connected to MongoDB Atlas`

## Still Having Issues?

1. Check your internet connection
2. Try a different network (mobile hotspot)
3. Check if your firewall is blocking the connection
4. Verify MongoDB Atlas account is active and not suspended
5. Contact MongoDB Atlas support if cluster is missing

