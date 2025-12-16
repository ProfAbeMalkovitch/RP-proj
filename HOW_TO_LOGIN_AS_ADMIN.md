# How to Login as Admin

## Quick Steps

1. **Open your browser** and navigate to: `http://localhost:3000/admin/login`
   - Or if your frontend runs on a different port, use: `http://localhost:[PORT]/admin/login`

2. **Use these credentials**:
   - **Email**: `admin@ilpg.com`
   - **Password**: `admin123`

3. **Click "Login as Admin"**

4. You'll be redirected to the **Admin Dashboard** at `/admin/dashboard`

## Available Admin Accounts

Your database has **2 admin accounts**:

### Admin Account 1 (Primary)
- **Email**: `admin@ilpg.com`
- **Password**: `admin123`
- **Name**: Admin User

### Admin Account 2 (Secondary)
- **Email**: `donaldgarcia@example.net`
- **Password**: `admin123`
- **Name**: Allison Hill

Both accounts use the same password: **`admin123`**

## Step-by-Step Instructions

### Method 1: Using the Frontend (Easiest)

1. **Start your frontend server** (if not already running):
   ```bash
   cd frontend
   npm start
   ```

2. **Start your backend server** (if not already running):
   ```bash
   cd backend
   python main.py
   ```

3. **Open your browser** and go to:
   ```
   http://localhost:3000/admin/login
   ```

4. **Enter credentials**:
   - Email: `admin@ilpg.com`
   - Password: `admin123`

5. **Click "Login as Admin"**

6. You'll be redirected to the Admin Dashboard!

### Method 2: Using the API Directly (For Testing)

You can test the admin login using curl or Postman:

**Endpoint**: `POST http://localhost:8000/api/auth/admin/login`

**Request Body**:
```json
{
  "email": "admin@ilpg.com",
  "password": "admin123"
}
```

**Response**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "user_id": "admin_001",
    "name": "Admin User",
    "email": "admin@ilpg.com",
    "role": "admin"
  },
  "role": "admin"
}
```

## Troubleshooting

### "Invalid email or password" Error

1. **Check if admin account exists**:
   ```bash
   cd backend
   python -c "from database import admins_collection; admins = list(admins_collection.find({}, {'email': 1})); print(admins)"
   ```

2. **If no admin accounts exist, create them**:
   ```bash
   cd backend
   python seeders/seed_admins.py
   ```

### Can't Access `/admin/login` Page

1. **Make sure frontend is running**:
   - Check if `http://localhost:3000` is accessible
   - Look for React app running message in terminal

2. **Check the route**:
   - The route should be `/admin/login` (with a forward slash)
   - Not `/admin/login/` (no trailing slash)

3. **Check browser console** for errors

### Backend Connection Error

1. **Make sure backend is running**:
   - Check if `http://localhost:8000` is accessible
   - Look for "Uvicorn running on..." message

2. **Check MongoDB connection**:
   - Verify your database connection in backend logs
   - Look for "Successfully connected to MongoDB" message

3. **Check CORS settings**:
   - Make sure frontend URL is allowed in backend CORS settings

## Admin Dashboard Features

Once logged in, you'll have access to:

- **System Statistics**: View overall system metrics
- **User Management**: Manage students and teachers
- **System Settings**: Configure system-wide settings
- **Analytics**: View system-wide analytics and reports

## Creating New Admin Accounts

If you need to create more admin accounts:

### Option 1: Use the Seeder Script
```bash
cd backend
python seeders/seed_admins.py
```

### Option 2: Create via Database
```python
from database import admins_collection
from utils.password import hash_password

new_admin = {
    "admin_id": "admin_003",
    "name": "New Admin Name",
    "email": "newadmin@ilpg.com",
    "password": hash_password("your_password_here")
}

admins_collection.insert_one(new_admin)
```

### Option 3: Use API (if admin creation endpoint exists)
Check your API documentation at `http://localhost:8000/docs`

## Security Notes

⚠️ **Important**: These are default demo credentials. For production:

1. **Change default passwords** immediately
2. **Use strong passwords** (minimum 12 characters, mixed case, numbers, symbols)
3. **Enable two-factor authentication** (if implemented)
4. **Limit admin account access** to authorized personnel only
5. **Monitor admin account activity** regularly

## Quick Reference

| Item | Value |
|------|-------|
| Login URL | `http://localhost:3000/admin/login` |
| API Endpoint | `POST /api/auth/admin/login` |
| Default Email | `admin@ilpg.com` |
| Default Password | `admin123` |
| Dashboard URL | `http://localhost:3000/admin/dashboard` |

## Still Having Issues?

1. Check that both frontend and backend servers are running
2. Verify MongoDB connection is active
3. Check browser console for JavaScript errors
4. Check backend terminal for Python errors
5. Verify you're using the correct URL format

For more help, check:
- Backend logs in terminal
- Browser Developer Console (F12)
- Network tab in browser DevTools








## Quick Steps

1. **Open your browser** and navigate to: `http://localhost:3000/admin/login`
   - Or if your frontend runs on a different port, use: `http://localhost:[PORT]/admin/login`

2. **Use these credentials**:
   - **Email**: `admin@ilpg.com`
   - **Password**: `admin123`

3. **Click "Login as Admin"**

4. You'll be redirected to the **Admin Dashboard** at `/admin/dashboard`

## Available Admin Accounts

Your database has **2 admin accounts**:

### Admin Account 1 (Primary)
- **Email**: `admin@ilpg.com`
- **Password**: `admin123`
- **Name**: Admin User

### Admin Account 2 (Secondary)
- **Email**: `donaldgarcia@example.net`
- **Password**: `admin123`
- **Name**: Allison Hill

Both accounts use the same password: **`admin123`**

## Step-by-Step Instructions

### Method 1: Using the Frontend (Easiest)

1. **Start your frontend server** (if not already running):
   ```bash
   cd frontend
   npm start
   ```

2. **Start your backend server** (if not already running):
   ```bash
   cd backend
   python main.py
   ```

3. **Open your browser** and go to:
   ```
   http://localhost:3000/admin/login
   ```

4. **Enter credentials**:
   - Email: `admin@ilpg.com`
   - Password: `admin123`

5. **Click "Login as Admin"**

6. You'll be redirected to the Admin Dashboard!

### Method 2: Using the API Directly (For Testing)

You can test the admin login using curl or Postman:

**Endpoint**: `POST http://localhost:8000/api/auth/admin/login`

**Request Body**:
```json
{
  "email": "admin@ilpg.com",
  "password": "admin123"
}
```

**Response**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "user_id": "admin_001",
    "name": "Admin User",
    "email": "admin@ilpg.com",
    "role": "admin"
  },
  "role": "admin"
}
```

## Troubleshooting

### "Invalid email or password" Error

1. **Check if admin account exists**:
   ```bash
   cd backend
   python -c "from database import admins_collection; admins = list(admins_collection.find({}, {'email': 1})); print(admins)"
   ```

2. **If no admin accounts exist, create them**:
   ```bash
   cd backend
   python seeders/seed_admins.py
   ```

### Can't Access `/admin/login` Page

1. **Make sure frontend is running**:
   - Check if `http://localhost:3000` is accessible
   - Look for React app running message in terminal

2. **Check the route**:
   - The route should be `/admin/login` (with a forward slash)
   - Not `/admin/login/` (no trailing slash)

3. **Check browser console** for errors

### Backend Connection Error

1. **Make sure backend is running**:
   - Check if `http://localhost:8000` is accessible
   - Look for "Uvicorn running on..." message

2. **Check MongoDB connection**:
   - Verify your database connection in backend logs
   - Look for "Successfully connected to MongoDB" message

3. **Check CORS settings**:
   - Make sure frontend URL is allowed in backend CORS settings

## Admin Dashboard Features

Once logged in, you'll have access to:

- **System Statistics**: View overall system metrics
- **User Management**: Manage students and teachers
- **System Settings**: Configure system-wide settings
- **Analytics**: View system-wide analytics and reports

## Creating New Admin Accounts

If you need to create more admin accounts:

### Option 1: Use the Seeder Script
```bash
cd backend
python seeders/seed_admins.py
```

### Option 2: Create via Database
```python
from database import admins_collection
from utils.password import hash_password

new_admin = {
    "admin_id": "admin_003",
    "name": "New Admin Name",
    "email": "newadmin@ilpg.com",
    "password": hash_password("your_password_here")
}

admins_collection.insert_one(new_admin)
```

### Option 3: Use API (if admin creation endpoint exists)
Check your API documentation at `http://localhost:8000/docs`

## Security Notes

⚠️ **Important**: These are default demo credentials. For production:

1. **Change default passwords** immediately
2. **Use strong passwords** (minimum 12 characters, mixed case, numbers, symbols)
3. **Enable two-factor authentication** (if implemented)
4. **Limit admin account access** to authorized personnel only
5. **Monitor admin account activity** regularly

## Quick Reference

| Item | Value |
|------|-------|
| Login URL | `http://localhost:3000/admin/login` |
| API Endpoint | `POST /api/auth/admin/login` |
| Default Email | `admin@ilpg.com` |
| Default Password | `admin123` |
| Dashboard URL | `http://localhost:3000/admin/dashboard` |

## Still Having Issues?

1. Check that both frontend and backend servers are running
2. Verify MongoDB connection is active
3. Check browser console for JavaScript errors
4. Check backend terminal for Python errors
5. Verify you're using the correct URL format

For more help, check:
- Backend logs in terminal
- Browser Developer Console (F12)
- Network tab in browser DevTools







































