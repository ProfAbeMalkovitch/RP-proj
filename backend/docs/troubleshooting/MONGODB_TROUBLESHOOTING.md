# MongoDB Atlas Connection Troubleshooting

## Current Error
SSL handshake failed when connecting to MongoDB Atlas.

## Solutions

### 1. Check Network Access in MongoDB Atlas

1. Go to [MongoDB Atlas Dashboard](https://cloud.mongodb.com/)
2. Navigate to **Network Access** (left sidebar)
3. Click **Add IP Address**
4. For development, you can temporarily add:
   - `0.0.0.0/0` (allows all IPs - **use only for development**)
   - Or add your specific IP address

### 2. Verify Database User

1. Go to **Database Access** in MongoDB Atlas
2. Ensure user `Research` exists with password `ilpg1234`
3. User should have **Read and write to any database** permissions

### 3. Check Cluster Status

1. Go to **Clusters** in MongoDB Atlas
2. Ensure your cluster is **Running** (not paused)
3. If paused, click **Resume** to start it

### 4. Test Connection String

Your connection string format:
```
mongodb+srv://Research:ilpg1234@students.jb1nyzd.mongodb.net/ilpg_db?retryWrites=true&w=majority
```

### 5. Alternative: Use Local MongoDB (for testing)

If you have MongoDB installed locally:

1. Update `backend/database.py` or create `.env` file:
   ```
   MONGODB_URI=mongodb://localhost:27017/
   DATABASE_NAME=ilpg_db
   ```

2. Make sure MongoDB service is running:
   ```powershell
   # Check if MongoDB is running
   Get-Service MongoDB
   ```

### 6. Firewall/Antivirus

- Temporarily disable firewall/antivirus to test
- Add MongoDB Atlas IPs to firewall exceptions

### 7. Test Connection Manually

Run this Python script to test:
```python
from pymongo import MongoClient

try:
    client = MongoClient(
        "mongodb+srv://Research:ilpg1234@students.jb1nyzd.mongodb.net/ilpg_db?retryWrites=true&w=majority",
        serverSelectionTimeoutMS=5000
    )
    client.admin.command('ping')
    print("✓ Connection successful!")
except Exception as e:
    print(f"✗ Connection failed: {e}")
```

## Quick Fix for Development

If you need to get started quickly:

1. **MongoDB Atlas Network Access:**
   - Add `0.0.0.0/0` to allow all IPs (development only)
   - Click **Confirm**

2. **Restart backend:**
   ```powershell
   cd backend
   python main.py
   ```

3. **Initialize database:**
   ```powershell
   python init_db.py
   ```

## Security Note

⚠️ **Important:** Using `0.0.0.0/0` allows access from anywhere. For production:
- Use specific IP addresses
- Use MongoDB Atlas VPC peering
- Use IP access lists with specific ranges







