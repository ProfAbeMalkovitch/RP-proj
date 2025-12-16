# Quick Setup Guide

Follow these steps to get the ILPG system up and running:

## Step 1: Install MongoDB

### Option A: Local MongoDB
1. Download and install MongoDB from https://www.mongodb.com/try/download/community
2. Start MongoDB service:
   - Windows: MongoDB should start automatically as a service
   - Mac/Linux: `sudo systemctl start mongod` or `brew services start mongodb-community`

### Option B: MongoDB Atlas (Cloud)
1. Create a free account at https://www.mongodb.com/cloud/atlas
2. Create a cluster and get your connection string
3. Update `MONGODB_URI` in `backend/.env`

## Step 2: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
# Copy .env.example to .env and update if needed
# The default is already configured for MongoDB Atlas
# MongoDB Atlas connection: mongodb+srv://Research:ilpg1234@students.jb1nyzd.mongodb.net/ilpg_db

# Initialize database with sample data
python init_db.py

# Start the server
python main.py
# Or: uvicorn main:app --reload
```

Backend will run on: http://localhost:8000
API docs available at: http://localhost:8000/docs

## Step 3: Frontend Setup

Open a new terminal:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will run on: http://localhost:3000

## Step 4: Test the Application

1. Open http://localhost:3000 in your browser
2. Login with demo credentials:
   - Email: `john@example.com`
   - Password: `password123`
3. Explore the three pathways
4. Take quizzes and see your scores update

## Troubleshooting

### MongoDB Connection Error
- Ensure MongoDB is running
- Check `MONGODB_URI` in `backend/.env`
- For MongoDB Atlas, ensure your IP is whitelisted

### Port Already in Use
- Backend: Change port in `main.py` (default: 8000)
- Frontend: React will prompt to use a different port

### Module Not Found Errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again
- For frontend: Delete `node_modules` and run `npm install` again

### CORS Errors
- Ensure backend is running
- Check CORS settings in `backend/main.py`
- Verify frontend URL matches allowed origins

## Next Steps

- Customize pathways and quizzes in `backend/init_db.py`
- Add more students or modify existing data
- Extend the API with new endpoints
- Enhance the UI with additional features

