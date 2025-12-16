# Quick Fix for MongoDB Atlas Connection

## The Problem
You're seeing: `SSL handshake failed` or `TLSV1_ALERT_INTERNAL_ERROR`

This means **your IP address is not whitelisted** in MongoDB Atlas.

## Solution (Takes 2 minutes)

### Step 1: Open MongoDB Atlas
1. Go to: **https://cloud.mongodb.com/**
2. Log in with your MongoDB Atlas account

### Step 2: Whitelist Your IP
1. Click **"Network Access"** in the left sidebar
2. Click the green **"Add IP Address"** button
3. You have two options:

   **Option A (Quick - Development Only):**
   - Click **"Allow Access from Anywhere"**
   - This adds `0.0.0.0/0` (allows all IPs)
   - ⚠️ **Only use for development/testing!**

   **Option B (Secure - Recommended):**
   - Click **"Add Current IP Address"**
   - This adds only your current IP
   - More secure, but you'll need to update if your IP changes

4. Click **"Confirm"**

### Step 3: Wait
- MongoDB Atlas takes **1-2 minutes** to apply network changes
- You'll see a yellow "Pending" status that changes to "Active"

### Step 4: Verify Database User
1. Click **"Database Access"** in the left sidebar
2. Check if user `Research` exists
3. If not, create it:
   - Click **"Add New Database User"**
   - Authentication Method: **Password**
   - Username: `Research`
   - Password: `ilpg1234`
   - Database User Privileges: **Read and write to any database**
   - Click **"Add User"**

### Step 5: Check Cluster Status
1. Click **"Clusters"** in the left sidebar
2. Make sure your cluster shows **"Running"** (green)
3. If it says **"Paused"**, click **"Resume"** and wait for it to start

### Step 6: Restart Backend
After whitelisting, restart your backend server:
```powershell
# Stop current server (CTRL+C)
cd backend
python main.py
```

You should now see: **"✓ Successfully connected to MongoDB Atlas"**

### Step 7: Initialize Database
Once connected, run:
```powershell
cd backend
python init_db.py
```

This creates sample students, pathways, and quizzes.

## Still Not Working?

1. **Double-check the connection string:**
   ```
   mongodb+srv://Research:ilpg1234@students.jb1nyzd.mongodb.net/ilpg_db?retryWrites=true&w=majority
   ```

2. **Check if credentials are correct:**
   - Username: `Research`
   - Password: `ilpg1234`
   - Cluster: `students.jb1nyzd.mongodb.net`

3. **Try from MongoDB Atlas:**
   - Go to **Clusters** → Click **"Connect"**
   - Choose **"Connect your application"**
   - Copy the connection string and compare

4. **Check firewall/antivirus:**
   - Temporarily disable to test
   - Add MongoDB to firewall exceptions

## Visual Guide

```
MongoDB Atlas Dashboard
├── Network Access ← Click here first!
│   └── Add IP Address → 0.0.0.0/0 (or your IP)
├── Database Access ← Check user exists
│   └── Research / ilpg1234
└── Clusters ← Make sure it's Running
    └── students (jb1nyzd)
```

## Need Help?

If you're still having issues:
1. Share a screenshot of your Network Access page
2. Verify the cluster is running
3. Check if you can access MongoDB Atlas dashboard

The most common issue is simply forgetting to whitelist the IP address!







